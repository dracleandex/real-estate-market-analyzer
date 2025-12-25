import requests
from abc import ABC, abstractmethod
from typing import Optional
from src.utils.rate_limiter import RateLimiter
from src.utils.retry import retry_request # <--- IMPORT THE NEW TOOL

class BaseScraper(ABC):
    """
    Abstract Base Class for all real estate scrapers.
    """
    
    def __init__(self, base_url: str, site_name: str):
        self.base_url = base_url
        self.site_name = site_name
        self.session = requests.Session()
        
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) RealEstateBot/1.0",
            "Accept-Language": "en-US,en;q=0.9",
        })

    @retry_request(max_attempts=3, delay=2) # <--- THIS IS THE SAFETY NET
    def fetch_page(self, url: str) -> Optional[str]:
        print(f"🌐 [{self.site_name}] Fetching: {url}")
        
        # --- SIMULATION MODE ---
        if "mock" in url:
            # We don't print "Simulation Mode" every time to keep logs clean
            return """<html><body><div class='mock'>Fake Data</div></body></html>"""
        # -----------------------

        RateLimiter.delay()
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    @abstractmethod
    def parse(self, html_content: str):
        pass
    
    @abstractmethod
    def run(self):
        pass