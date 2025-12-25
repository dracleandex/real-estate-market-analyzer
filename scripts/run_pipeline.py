import sys
import os

# Fix imports to ensure Python finds your 'src' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.services.property_service import PropertyService
from src.services.cleaning_service import CleaningService
from src.geocoding.geocoder import Geocoder
from src.scrapers.scraper_factory import ScraperFactory
from src.services.duplicate_detector import DuplicateDetector # <--- NEW IMPORT

def run_full_pipeline():
    print("🏭 Starting Smart Data Pipeline...")
    
    db_manager = DatabaseManager()
    geocoder = Geocoder()
    
    # 1. Load All Robots (Zillow, Redfin, Realtor)
    scrapers = ScraperFactory.get_all_scrapers()
    print(f"📋 Loaded {len(scrapers)} scrapers: {[s.site_name for s in scrapers]}")
    
    with db_manager.session_scope() as session:
        service = PropertyService(session)
        dup_detector = DuplicateDetector(session) # <--- Initialize the Detective
        
        # 2. Cycle through each website
        for scraper in scrapers:
            print(f"\n🚀 Launching {scraper.site_name} Scraper...")
            
            try:
                # Run the scraper (Limit to 1 page for testing speed)
                raw_properties = scraper.run(pages=1)
                
                print(f"   Processing {len(raw_properties)} items from {scraper.site_name}...")
                
                # 3. Process each house found
                for prop_obj in raw_properties:
                    
                    # --- A. CLEANING ---
                    # Convert object to dict for the cleaner
                    raw_data = {
                        "address": prop_obj.address,
                        "city": prop_obj.city,
                        "state": prop_obj.state,
                        "price": prop_obj.price,
                        "beds": prop_obj.bedrooms,
                        "baths": prop_obj.bathrooms,
                        "sqft": prop_obj.square_feet,
                        "url": prop_obj.url
                    }
                    clean_data = CleaningService.clean_listing(raw_data)
                    
                    # --- B. DUPLICATE DETECTION (NEW) ---
                    # Check if a similar address already exists in the DB
                    existing_duplicate = dup_detector.find_potential_duplicate(
                        clean_data['address'], 
                        clean_data['city']
                    )
                    
                    if existing_duplicate:
                        print(f"   ⏭️ Skipping Fuzzy Duplicate: '{clean_data['address']}' (Matches: '{existing_duplicate.address}')")
                        continue # Skip to the next house, don't save this one!
                    
                    # --- C. GEOCODING ---
                    # If it's unique, let's find where it is on the map
                    full_address = f"{clean_data['address']}, {clean_data['city']}, {clean_data['state']}"
                    lat, lon = geocoder.geocode(full_address)
                    
                    # --- D. UPDATE OBJECT ---
                    prop_obj.address = clean_data["address"]
                    prop_obj.city = clean_data["city"]
                    prop_obj.state = clean_data["state"]
                    prop_obj.price = clean_data["price"]
                    prop_obj.bedrooms = clean_data["bedrooms"]
                    prop_obj.bathrooms = clean_data["bathrooms"]
                    prop_obj.square_feet = clean_data["square_feet"]
                    prop_obj.latitude = lat
                    prop_obj.longitude = lon
                    
                    # --- E. SAVE (History logic happens inside here) ---
                    service.save_listing(prop_obj)
                    
            except Exception as e:
                print(f"   ❌ Error running {scraper.site_name}: {e}")

    print("\n✅ Smart Pipeline Finished! Data is Cleaned, Deduped, and Geocoded.")

if __name__ == "__main__":
    run_full_pipeline()