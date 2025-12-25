class PropertyCleaner:
    """
    Standardizes property details like City, State, and Beds/Baths.
    """
    
    @staticmethod
    def clean_city(city: str) -> str:
        if not city:
            return "Unknown"
        # " austin " -> "Austin"
        return city.strip().title()
        
    @staticmethod
    def clean_state(state: str) -> str:
        if not state:
            return "XX"
        return state.strip().upper()[:2] # Ensure it's 2 chars like "TX"
    
    @staticmethod
    def validate_beds_baths(value):
        """
        Ensures beds/baths are positive numbers.
        If we get "3 Beds", we extract 3.
        """
        if value is None:
            return 0
            
        if isinstance(value, (int, float)):
            return abs(value) # No negative bedrooms allowed!
            
        # Simple text handling (e.g. "3 bd")
        try:
            # Grab the first number found
            import re
            numbers = re.findall(r'\d+', str(value))
            if numbers:
                return int(numbers[0])
        except:
            pass
            
        return 0