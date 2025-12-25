import sys
import os

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers.zillow_scraper import ZillowScraper

def test_zillow_parsing():
    print("🧪 Testing Zillow Parsing Logic...")
    
    # 1. Initialize the scraper
    # We use a fake URL because we won't actually download anything in this test
    scraper = ZillowScraper(base_url="http://mock-zillow.com", site_name="Zillow")
    
    # 2. Create FAKE HTML (The "Dummy")
    # This simulates what Zillow's website looks like
    dummy_html = """
    <html>
        <body>
            <h1>Zillow Listings</h1>
            <div class="property-card">
                <span class="price">$450,000</span>
                <span class="address">123 Scraped Lane, Austin, TX</span>
            </div>
        </body>
    </html>
    """
    
    # 3. Ask the scraper to parse our dummy HTML
    results = scraper.parse(dummy_html)
    
    # 4. Check the results
    if len(results) > 0:
        house = results[0]
        print(f"\n🎉 SUCCESS! Extracted Property:")
        print(f"   🏠 Address: {house.address}")
        print(f"   💰 Price: ${house.price:,.2f}")
        print(f"   🛏️  Beds: {house.bedrooms}")
    else:
        print("❌ Failed to parse any properties.")

if __name__ == "__main__":
    test_zillow_parsing()