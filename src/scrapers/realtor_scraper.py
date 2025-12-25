import random
import time
from datetime import datetime
from src.core.models import Property

class RealtorScraper:
    """
    Simulates scraping data from Realtor.com.
    """
    def __init__(self, base_url="http://mock-realtor.com", site_name="Realtor.com"):
        self.base_url = base_url
        self.site_name = site_name

    def run(self, pages=1):
        print(f"🔵 [Realtor] Connecting to {self.base_url}...")
        results = []
        
        for page in range(1, pages + 1):
            time.sleep(0.5)
            print(f"   📄 Parsing Realtor.com Page {page}...")
            
            for _ in range(5):
                results.append(self._generate_mock_listing())
                
        print(f"✅ [Realtor] Finished. Found {len(results)} listings.")
        return results

    def _generate_mock_listing(self):
        cities = ["Austin", "Round Rock", "Georgetown"]
        street_names = ["Congress Ave", "Lamar Blvd", "6th St", "Burnet Rd"]
        
        return Property(
            address=f"{random.randint(100, 9999)} {random.choice(street_names)}",
            city=random.choice(cities),
            state="TX",
            zip_code=f"78{random.randint(100, 999)}",
            price=float(random.randint(450000, 1200000)), # More expensive
            bedrooms=random.randint(3, 6),
            bathrooms=float(random.randint(2, 5)),
            square_feet=random.randint(2000, 5000),
            property_type="Single Family",
            source_site=self.site_name,
            url=f"http://realtor.com/realestateandhomes-detail/{random.randint(10000,99999)}",
            scraped_at=datetime.utcnow()
        )