import sys
import os
import requests
from unittest.mock import MagicMock

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers.base_scraper import BaseScraper
from src.utils.retry import retry_request

class BrokenScraper(BaseScraper):
    """A scraper designed to fail."""
    
    def parse(self, html):
        pass
    
    def run(self):
        pass
    
    # We override fetch_page to ALWAYS crash
    @retry_request(max_attempts=3, delay=1)
    def fetch_page(self, url):
        print(f"💥 Trying to connect to {url}...")
        raise requests.exceptions.ConnectionError("Fake Internet Outage")

def test_retry_logic():
    print("🧪 Testing Retry Mechanism...")
    
    scraper = BrokenScraper("http://bad-url.com", "BadSite")
    
    try:
        scraper.fetch_page("http://bad-url.com")
    except requests.exceptions.ConnectionError:
        print("\n✅ Test Passed: The scraper failed gracefully after retrying.")
    except Exception as e:
        print(f"❌ Test Failed: Unexpected error: {e}")

if __name__ == "__main__":
    test_retry_logic()