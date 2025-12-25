import sys
import os
import pandas as pd
from sqlalchemy import create_engine

# Fix imports so Python can find 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models import Property
from src.core.database import DatabaseManager

def show_data():
    print("🔎 Inspecting Database...")
    
    # Connect to the database
    db = DatabaseManager()
    
    # We use a context manager to ensure the session closes
    with db.session_scope() as session:
        # Fetch all properties
        properties = session.query(Property).all()
        
        if not properties:
            print("❌ Database is empty. Run 'scripts/run_pipeline.py' first!")
            return

        print(f"✅ Found {len(properties)} listings.\n")
        
        # Build a list of dictionaries for the table
        data = []
        for p in properties:
            data.append({
                "ID": p.id,
                "Address": p.address,
                "City": p.city,
                "Price": f"${p.price:,.0f}",
                "Beds": p.bedrooms,
                "SqFt": p.square_feet,
                "Status": p.listing_status
            })
            
        # Create a DataFrame
        df = pd.DataFrame(data)
        
        # Print the table nicely
        print(df.to_string(index=False))

if __name__ == "__main__":
    show_data()