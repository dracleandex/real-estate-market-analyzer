import sys
import os
import random
from datetime import datetime, timedelta

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.core.models import Property
# FIX: Import Enums from their own file, not from models.py
from src.core.enums import PropertyType, ListingStatus, DataSource

def init_db():
    print("🚀 Starting Database Initialization...")
    
    # 1. Initialize Manager
    db = DatabaseManager()
    
    # 2. Create Tables
    print("🔨 Creating tables...")
    db.create_all_tables()
    
    # 3. Ask for Sample Data
    print("✅ Tables created successfully.")
    
    # Auto-generate 10 samples for testing
    print("🎲 Generating 10 sample properties...")
    with db.session_scope() as session:
        for i in range(10):
            prop = Property(
                address=f"{random.randint(100, 999)} Test Street",
                city="Test City",
                state="NY",
                zip_code="10001",
                price=float(random.randint(100000, 1000000)),
                square_feet=random.randint(500, 5000),
                # Now these work because we imported them correctly
                property_type=PropertyType.HOUSE.value,
                listing_status=ListingStatus.ACTIVE.value,
                source_site=DataSource.ZILLOW.value
            )
            session.add(prop)
    
    print("🎉 Success! Database is ready and populated.")

if __name__ == "__main__":
    init_db()