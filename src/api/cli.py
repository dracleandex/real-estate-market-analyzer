import typer
import sys
import os
from enum import Enum
from tqdm import tqdm
from typing import Optional
from tabulate import tabulate

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.database import DatabaseManager
from src.scrapers.scraper_factory import ScraperFactory
from src.services.property_service import PropertyService
from src.services.cleaning_service import CleaningService
from src.geocoding.geocoder import Geocoder
from src.analyzers.price_analyzer import PriceAnalyzer
from src.analyzers.market_analyzer import MarketAnalyzer
from src.analyzers.neighborhood_analyzer import NeighborhoodAnalyzer
from src.analyzers.comparative_analyzer import ComparativeAnalyzer
from src.visualizers.statistical_visualizer import StatisticalVisualizer
from src.visualizers.map_visualizer import MapVisualizer
from src.services.export_service import ExportService
from src.services.duplicate_detector import DuplicateDetector

# 1. Define the Lenses as an Enum
class MarketLens(str, Enum):
    summary = "summary"
    health = "health"
    neighborhoods = "neighborhoods"
    deals = "deals"

app = typer.Typer(help="🏠 PropTech Commander CLI")

@app.command()
def scrape(
    site: str = typer.Option("all", help="zillow, redfin, realtor, or all"),
    pages: int = typer.Option(1, prompt="🔢 How many pages?", help="Pages per site")
):
    """🤖 Run scrapers to fetch housing data."""
    db_manager = DatabaseManager()
    geocoder = Geocoder()
    scrapers = ScraperFactory.get_all_scrapers() if site.lower() == "all" else [ScraperFactory.get_scraper(site)]

    with db_manager.session_scope() as session:
        service = PropertyService(session)
        dup_detector = DuplicateDetector(session)
        for scraper in scrapers:
            typer.secho(f"\n📡 Connecting to {scraper.site_name}...", fg=typer.colors.BLUE, bold=True)
            try:
                raw_properties = scraper.run(pages=pages) 
                for prop_obj in tqdm(raw_properties, desc=f"Processing {scraper.site_name}"):
                    raw_data = {"address": prop_obj.address, "city": prop_obj.city, "state": prop_obj.state, "price": prop_obj.price, "beds": prop_obj.bedrooms, "baths": prop_obj.bathrooms, "sqft": prop_obj.square_feet, "url": prop_obj.url}
                    clean_data = CleaningService.clean_listing(raw_data)
                    if dup_detector.find_potential_duplicate(clean_data['address'], clean_data['city']): continue 
                    full_address = f"{clean_data['address']}, {clean_data['city']}, {clean_data['state']}"
                    lat, lon = geocoder.geocode(full_address)
                    prop_obj.latitude, prop_obj.longitude = lat, lon
                    service.save_listing(prop_obj)
            except Exception as e:
                typer.secho(f"   ❌ Error: {e}", fg=typer.colors.RED)
    typer.secho("\n✅ Pipeline Finished!", fg=typer.colors.GREEN, bold=True)

@app.command()
def analyze(
    # Typer will now see 'MarketLens' and automatically offer the choices!
    lens: MarketLens = typer.Option(
        MarketLens.summary, 
        prompt="🧐 Which lens would you like to use for analysis?", 
        help="The perspective for analysis"
    ),
    city: Optional[str] = typer.Option(None, help="Filter by city")
):
    """📊 Advanced Market Intelligence Engine."""
    db = DatabaseManager()
    p_analyzer = PriceAnalyzer(db)
    m_analyzer = MarketAnalyzer(db)
    n_analyzer = NeighborhoodAnalyzer(db)
    c_analyzer = ComparativeAnalyzer(db)
    
    df = p_analyzer.get_dataframe()
    if df.empty:
        typer.secho("❌ Database is empty!", fg=typer.colors.RED)
        return

    # Filter by city if requested
    if city:
        df = df[df['city'].str.lower() == city.lower()]

    # Use 'lens.value' to get the string choice
    if lens == MarketLens.summary:
        typer.secho(f"\n📈 Market Summary ({city or 'All Cities'})", fg=typer.colors.CYAN, bold=True)
        stats = p_analyzer.get_summary_stats(group_by_city=True if not city else False)
        print(stats.to_string())

    elif lens == MarketLens.health:
        typer.secho("\n🏥 Market Health Check", fg=typer.colors.GREEN, bold=True)
        health = m_analyzer.get_market_health()
        print(health.to_string())

    elif lens == MarketLens.neighborhoods:
        typer.secho("\n🏘️ Neighborhood Ranking (by ZIP)", fg=typer.colors.MAGENTA, bold=True)
        n_stats = n_analyzer.compare_zip_codes()
        print(n_stats.to_string())

    elif lens == MarketLens.deals:
        typer.secho("\n💎 Deal Hunter: High Discount Opportunities", fg=typer.colors.YELLOW, bold=True)
        deals = c_analyzer.find_deals(discount_threshold=0.10)
        if deals.empty:
            print("No deals found matching the threshold.")
        else:
            print(tabulate(deals[['address', 'city', 'price', 'market_diff_pct']], headers='keys', tablefmt='psql'))

@app.command()
def visualize():
    """🎨 Generate maps and charts."""
    db = DatabaseManager()
    analyzer = PriceAnalyzer(db)
    df = analyzer.get_dataframe()
    if df.empty: return
    viz = StatisticalVisualizer(df)
    viz.plot_price_distribution()
    viz.plot_price_vs_sqft()
    map_viz = MapVisualizer(df)
    map_viz.generate_interactive_map()
    typer.secho("\n✅ Reports saved to output/", fg=typer.colors.GREEN)

@app.command()
def export(format: str = typer.Option("csv", help="csv, excel, json, or pdf")):
    """📄 Export data."""
    db = DatabaseManager()
    analyzer = PriceAnalyzer(db)
    df = analyzer.get_dataframe()
    if df.empty: return
    exporter = ExportService(df)
    path = exporter.to_csv() if format == "csv" else exporter.to_pdf() if format == "pdf" else exporter.to_json() if format == "json" else exporter.to_excel()
    typer.secho(f"✅ Exported to: {path}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()