import sys
import os

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.services.property_service import PropertyService

def test_queries():
    print("🔎 Testing Search Capabilities...")
    
    db = DatabaseManager()
    with db.session_scope() as session:
        service = PropertyService(session)
        
        # Test 1: Search by City
        # (We assume the database has data from the pipeline run)
        austin_homes = service.get_properties_by_city("Austin")
        print(f"✅ Found {len(austin_homes)} homes in Austin")
        
        # Test 2: Search by Price
        # Search for mid-range homes
        budget_homes = service.get_properties_by_price(300000, 450000)
        print(f"✅ Found {len(budget_homes)} homes between $300k-$450k")

        # Test 3: Get Total Count
        stats = service.get_stats()
        print(f"✅ Total Database Size: {stats['total_listings']} listings")

if __name__ == "__main__":
    test_queries()