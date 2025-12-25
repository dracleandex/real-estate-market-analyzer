import sys
import os
import webbrowser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.analyzers.price_analyzer import PriceAnalyzer
from src.visualizers.statistical_visualizer import StatisticalVisualizer
from src.visualizers.map_visualizer import MapVisualizer # <--- NEW IMPORT

def test_visuals():
    print("🎨 Generating All Reports...")
    
    # 1. Get Data
    db = DatabaseManager()
    analyzer = PriceAnalyzer(db)
    df = analyzer.get_dataframe()
    
    if df.empty:
        print("❌ No data found.")
        return

    # 2. Static Charts (Step 6)
    print("   Generating PNG charts...")
    viz = StatisticalVisualizer(df)
    viz.plot_price_distribution()
    viz.plot_price_vs_sqft()
    
    # 3. Interactive Map (Step 8)
    print("   Generating HTML Map...")
    map_viz = MapVisualizer(df)
    map_viz.generate_interactive_map("real_estate_heatmap.html")
    
    print("\n✅ Success! Check the 'output' folder.")
    
    # BONUS: Automatically open the map to show you
    output_path = os.path.abspath("output/real_estate_heatmap.html")
    webbrowser.open(f"file://{output_path}")

if __name__ == "__main__":
    test_visuals()