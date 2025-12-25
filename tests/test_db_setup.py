import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models import Property

def test_connection():
    db = SessionLocal()
    try:
        # Create a dummy house
        test_house = Property(address="123 Portfolio St", price=100.0)
        db.add(test_house)
        db.commit()
        print("🎉 Success! Data saved to database.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()