import random
import time
from datetime import datetime, timedelta
from src.scrapers.base_scraper import BaseScraper
from src.core.models import Property
from src.core.enums import PropertyType, ListingStatus, DataSource

class ZillowScraper(BaseScraper):
    """
    Advanced Simulation Scraper.
    Generates realistic real estate data for development and portfolio showing.
    """
    
    # Neighborhoods for our "City"
    LOCATIONS = [
        {"city": "Austin", "state": "TX", "zip": "78701", "base_price": 450000},
        {"city": "Dallas", "state": "TX", "zip": "75201", "base_price": 350000},
        {"city": "Houston", "state": "TX", "zip": "77002", "base_price": 300000},
        {"city": "San Antonio", "state": "TX", "zip": "78205", "base_price": 280000},
    ]

    STREET_NAMES = ["Oak", "Maple", "Pine", "Cedar", "Elm", "Main", "Washington", "Lake", "Hill"]
    TYPES = ["St", "Ave", "Blvd", "Ln", "Dr", "Ct"]

    def parse(self, html_content):
        """
        In this simulation, 'parse' actually generates the data.
        """
        results = []
        
        # We simulate finding 10-15 houses per "page"
        houses_on_page = random.randint(10, 15)
        
        print(f"   🧠 Parsing found {houses_on_page} listings on this page...")
        
        for i in range(houses_on_page):
            # Pick a random location
            loc = random.choice(self.LOCATIONS)
            
            # Generate realistic variation
            beds = random.randint(2, 5)
            baths = random.randint(1, 4) + (0.5 if random.random() > 0.5 else 0)
            sqft = random.randint(1200, 4500)
            
            # Price math: Base price + ($200 * sqft) + random variance
            price = loc["base_price"] + (sqft * 150) + random.randint(-50000, 50000)
            
            # Create Address
            num = random.randint(100, 9999)
            street = random.choice(self.STREET_NAMES)
            st_type = random.choice(self.TYPES)
            address = f"{num} {street} {st_type}"
            
            # Create the Property Object
            prop = Property(
                address=address,
                city=loc["city"],
                state=loc["state"],
                zip_code=loc["zip"],
                price=round(price, -3), # Round to nearest 1000
                bedrooms=beds,
                bathrooms=baths,
                square_feet=sqft,
                property_type=PropertyType.HOUSE.value,
                listing_status=ListingStatus.ACTIVE.value,
                source_site=DataSource.ZILLOW.value,
                url=f"https://zillow.com/homedetails/{num}-{street}-{st_type}",
                scraped_at=datetime.utcnow()
            )
            results.append(prop)
            
        return results

    def run(self, pages=3):
        """
        Runs the scraper for X number of pages.
        """
        print(f"🚀 Starting {self.site_name} Simulation (Target: {pages} pages)...")
        all_properties = []
        
        for page in range(1, pages + 1):
            url = f"{self.base_url}/homes/Austin-TX_rb/{page}_p/"
            print(f"\n📄 Processing Page {page}...")
            
            # 1. Fetch (This triggers our BaseScraper 'Simulation Mode')
            html = self.fetch_page(url + "?mock=true")
            
            if html:
                # 2. Parse (Generate data)
                page_results = self.parse(html)
                all_properties.extend(page_results)
                
                # 3. Random delay between pages (Simulation)
                time.sleep(random.uniform(0.5, 1.5))
            
        print(f"\n✅ Simulation Complete. Generated {len(all_properties)} total properties.")
        return all_properties