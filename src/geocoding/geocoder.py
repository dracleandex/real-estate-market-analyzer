from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

class Geocoder:
    """
    Converts text addresses into Latitude/Longitude coordinates.
    """
    
    def __init__(self):
        # We must provide a unique user_agent to be polite to the free API
        self.geolocator = Nominatim(user_agent="my_real_estate_project_v1")
        self.cache = {} # Simple memory cache to avoid repeat calls

    def geocode(self, address_str):
        """
        Returns (lat, lon) for a given address string.
        Returns (None, None) if not found.
        """
        # 1. Check Cache first
        if address_str in self.cache:
            return self.cache[address_str]
        
        try:
            # 2. Ask the API
            # We add a small delay to respect the free API's rules (1 request per second)
            time.sleep(1.1) 
            
            print(f"   🗺️ Geocoding: {address_str}...")
            location = self.geolocator.geocode(address_str, timeout=10)
            
            if location:
                coords = (location.latitude, location.longitude)
                self.cache[address_str] = coords
                return coords
            else:
                print("   ❌ Location not found.")
                return None, None
                
        except GeocoderTimedOut:
            print("   ⏳ Geocoding timed out.")
            return None, None
        except Exception as e:
            print(f"   ⚠️ Geocoding Error: {e}")
            return None, None