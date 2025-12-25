from src.cleaners.price_cleaner import PriceCleaner
from src.cleaners.property_cleaner import PropertyCleaner
from src.core.models import Property

class CleaningService:
    """
    The Manager that hires specific janitors to clean parts of the house.
    """
    
    @staticmethod
    def clean_listing(raw_data: dict) -> dict:
        """
        Takes a raw dictionary (from a scraper) and cleans all fields.
        """
        cleaned = {}
        
        # 1. Clean Price
        cleaned['price'] = PriceCleaner.clean_price(raw_data.get('price'))
        
        # 2. Clean Location
        cleaned['city'] = PropertyCleaner.clean_city(raw_data.get('city'))
        cleaned['state'] = PropertyCleaner.clean_state(raw_data.get('state'))
        cleaned['address'] = raw_data.get('address', 'Unknown Address').strip()
        
        # 3. Clean Details
        cleaned['bedrooms'] = PropertyCleaner.validate_beds_baths(raw_data.get('beds'))
        cleaned['bathrooms'] = PropertyCleaner.validate_beds_baths(raw_data.get('baths'))
        cleaned['square_feet'] = PropertyCleaner.validate_beds_baths(raw_data.get('sqft')) # Same logic works for sqft integers
        
        # Keep other fields
        cleaned['url'] = raw_data.get('url')
        
        return cleaned