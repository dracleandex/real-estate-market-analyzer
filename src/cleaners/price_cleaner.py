import re

class PriceCleaner:
    """
    Cleans price strings into usable float values.
    Example: "$450,000" -> 450000.0
    """
    
    @staticmethod
    def clean_price(price_input):
        """
        Removes currency symbols, commas, and whitespace.
        Returns a float or None if invalid.
        """
        if not price_input:
            return None
            
        # If it's already a number, just return it
        if isinstance(price_input, (int, float)):
            return float(price_input)
            
        # Convert to string just in case
        price_str = str(price_input)
        
        # 1. Remove anything that ISN'T a digit or a decimal point
        # Regex explanation: [^\d.] means "Match anything that is NOT a number or dot"
        clean_str = re.sub(r'[^\d.]', '', price_str)
        
        try:
            return float(clean_str)
        except ValueError:
            print(f"⚠️ Could not convert price: {price_input}")
            return None