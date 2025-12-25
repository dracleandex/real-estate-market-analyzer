import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.core.models import Property
from src.services.duplicate_detector import DuplicateDetector

def test_fuzzy_logic():
    print("🔍 Testing Fuzzy Duplicate Detection...")
    
    db_manager = DatabaseManager()
    
    with db_manager.session_scope() as session:
        # 1. Clear old test data (optional, but cleaner)
        session.query(Property).filter(Property.city == "DuplicateCity").delete()
        
        # 2. Add an "Original" House
        original = Property(
            address="1234 Main Street", # Note: Spelled out "Street"
            city="DuplicateCity",
            price=100000,
            url="http://test.com/1"
        )
        session.add(original)
        session.commit()
        print("   ✅ Added: '1234 Main Street'")
        
        # 3. Try to match a "Messy" version
        detector = DuplicateDetector(session)
        messy_address = "1234 Main St." # Note: Abbreviation and dot
        
        print(f"   ❓ Checking: '{messy_address}'...")
        match = detector.find_potential_duplicate(messy_address, "DuplicateCity")
        
        if match:
            print(f"   ✅ SUCCESS! It matched '{messy_address}' to '{match.address}'")
        else:
            print("   ❌ FAILED. It thought they were different.")

if __name__ == "__main__":
    test_fuzzy_logic()