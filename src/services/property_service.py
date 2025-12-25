from sqlalchemy.orm import Session
from src.core.models import Property, PriceHistory
from datetime import datetime

class PropertyService:
    def __init__(self, session: Session):
        self.session = session

    def save_listing(self, new_data: Property):
        """
        Saves a property. If it exists, checks for price changes.
        If price changed, records history before updating.
        """
        # 1. Check if property exists (by URL)
        existing_prop = self.session.query(Property).filter_by(url=new_data.url).first()

        if existing_prop:
            # --- UPDATE EXISTING ---
            print(f"   🔄 Updating: {existing_prop.address}")
            
            # Check for Price Change
            if existing_prop.price != new_data.price:
                print(f"   📉 PRICE CHANGE DETECTED: ${existing_prop.price:,.0f} -> ${new_data.price:,.0f}")
                
                # Create History Record (Save the OLD price)
                history = PriceHistory(
                    property_id=existing_prop.id,
                    price=existing_prop.price,
                    recorded_at=datetime.utcnow()
                )
                self.session.add(history)
                
                # Update main record
                existing_prop.price = new_data.price
                existing_prop.updated_at = datetime.utcnow()
                
            # Update other fields just in case they changed
            existing_prop.listing_status = new_data.listing_status
            
        else:
            # --- CREATE NEW ---
            print(f"   🆕 New Listing: {new_data.address}")
            self.session.add(new_data)
        
        # Commit the transaction
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"   ❌ Error saving property: {e}")

    def get_price_drops(self):
        """
        Finds all properties that are currently cheaper than their history.
        """
        results = []
        properties = self.session.query(Property).all()
        
        for prop in properties:
            # Get history sorted by date
            history = sorted(prop.price_history, key=lambda x: x.recorded_at, reverse=True)
            
            if history:
                old_price = history[0].price # The most recent old price
                if prop.price < old_price:
                    drop_amount = old_price - prop.price
                    results.append({
                        "address": prop.address,
                        "current_price": prop.price,
                        "old_price": old_price,
                        "drop_amount": drop_amount
                    })
        return results