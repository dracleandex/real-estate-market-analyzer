import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.analyzers.price_analyzer import PriceAnalyzer
from src.analyzers.market_analyzer import MarketAnalyzer
from src.analyzers.comparative_analyzer import ComparativeAnalyzer
from src.analyzers.neighborhood_analyzer import NeighborhoodAnalyzer

def test_full_analysis():
    print("📊 Running Full Analysis Suite...\n")
    db = DatabaseManager()
    
    # 1. Market Health
    print("--- 🌍 Market Health ---")
    m_analyzer = MarketAnalyzer(db)
    print(m_analyzer.get_market_health())
    print("\n")
    
    # 2. Neighborhoods
    print("--- 🏘️ Neighborhood Rankings ---")
    n_analyzer = NeighborhoodAnalyzer(db)
    print(n_analyzer.compare_zip_codes())
    print("\n")
    
    # 3. DEAL HUNTER
    print("--- 💰 Potential Deals (Undervalued) ---")
    c_analyzer = ComparativeAnalyzer(db)
    deals = c_analyzer.find_deals(discount_threshold=0.20) # Find houses 20% off
    
    if not deals.empty:
        print(deals.to_string())
    else:
        print("No deals found (Everything is expensive!).")

if __name__ == "__main__":
    test_full_analysis()