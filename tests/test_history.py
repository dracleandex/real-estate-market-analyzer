import sys
import os
from datetime import datetime

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.services.property_service import PropertyService
from src.core.models import Property

def test_price_history():
    print("📉 Testing Historical Tracking...")
    
    db_manager = DatabaseManager()
    
    with db_manager.session_scope() as session:
        service = PropertyService(session)
        
        # 1. Create a Fake House
        url = "http://test-history.com/house1"
        house_v1 = Property(
            address="999 History Lane",
            city="Test City",
            price=500000.0,  # ORIGINAL PRICE
            bedrooms=3, bathrooms=2, square_feet=2000,
            url=url,
            scraped_at=datetime.utcnow()
        )
        service.save_listing(house_v1)
        
        # 2. Update the SAME house with a LOWER price
        print("\n⏳ Simulating time passing... Price drops!")
        house_v2 = Property(
            address="999 History Lane",
            city="Test City",
            price=450000.0,  # NEW LOWER PRICE
            bedrooms=3, bathrooms=2, square_feet=2000,
            url=url  # Same URL means same house
        )
        service.save_listing(house_v2)
        
        # 3. Verify History
        print("\n🔍 Checking Database Records...")
        prop = session.query(Property).filter_by(url=url).first()
        
        print(f"   Current Price in DB: ${prop.price:,.0f}")
        print(f"   History Count: {len(prop.price_history)}")
        
        if len(prop.price_history) > 0:
            old_price = prop.price_history[0].price
            print(f"   ✅ SUCCESS! Found historical record of: ${old_price:,.0f}")
        else:
            print("   ❌ FAILURE. No history found.")

if __name__ == "__main__":
    test_price_history()