import random
import time
from datetime import datetime
from src.core.models import Property

class RedfinScraper:
    """
    Simulates scraping data from Redfin.
    """
    def __init__(self, base_url="http://mock-redfin.com", site_name="Redfin"):
        self.base_url = base_url
        self.site_name = site_name

    def run(self, pages=1):
        print(f"🔴 [Redfin] Connecting to {self.base_url}...")
        results = []
        
        # Simulate processing pages
        for page in range(1, pages + 1):
            time.sleep(0.5) # Simulate network delay
            print(f"   📄 Parsing Redfin Page {page}...")
            
            # Generate 5 fake properties per page
            for _ in range(5):
                results.append(self._generate_mock_listing())
                
        print(f"✅ [Redfin] Finished. Found {len(results)} listings.")
        return results

    def _generate_mock_listing(self):
        """
        Creates a fake Redfin listing.
        """
        cities = ["Dallas", "Fort Worth", "Arlington"]
        street_names = ["Main St", "Cooper St", "Division St", "Abrams Rd"]
        
        return Property(
            address=f"{random.randint(100, 9999)} {random.choice(street_names)}",
            city=random.choice(cities),
            state="TX",
            zip_code=f"76{random.randint(100, 999)}",
            price=float(random.randint(250000, 650000)),
            bedrooms=random.randint(2, 5),
            bathrooms=float(random.randint(1, 4)),
            square_feet=random.randint(1200, 3500),
            property_type="Townhouse", # Redfin specializes in these for our mock
            source_site=self.site_name,
            url=f"http://redfin.com/listing/{random.randint(10000,99999)}",
            scraped_at=datetime.utcnow()
        )