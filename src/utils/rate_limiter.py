import time
import random

class RateLimiter:
    """
    Helps scrapers look like humans by waiting between requests.
    """
    
    @staticmethod
    def delay(min_seconds=2, max_seconds=5):
        """
        Pauses execution for a random amount of time.
        
        Args:
            min_seconds (int): Minimum wait time.
            max_seconds (int): Maximum wait time.
        """
        sleep_time = random.uniform(min_seconds, max_seconds)
        print(f"⏳ Waiting for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)