from src.scrapers.zillow_scraper import ZillowScraper
from src.scrapers.redfin_scraper import RedfinScraper
from src.scrapers.realtor_scraper import RealtorScraper

class ScraperFactory:
    """
    The 'Manager' that hands out the correct scraper tool.
    """
    
    @staticmethod
    def get_scraper(site_name):
        site_name = site_name.lower()
        
        if "zillow" in site_name:
            return ZillowScraper(base_url="http://mock-zillow.com", site_name="Zillow")
        elif "redfin" in site_name:
            return RedfinScraper()
        elif "realtor" in site_name:
            return RealtorScraper()
        else:
            raise ValueError(f"Unknown scraper type: {site_name}")
            
    @staticmethod
    def get_all_scrapers():
        """Returns a list of all available scrapers."""
        return [
            # FIX: We now provide the required arguments here
            ZillowScraper(base_url="http://mock-zillow.com", site_name="Zillow"),
            RedfinScraper(),
            RealtorScraper()
        ]