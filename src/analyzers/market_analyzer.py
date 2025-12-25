import pandas as pd
from src.analyzers.price_analyzer import PriceAnalyzer

class MarketAnalyzer(PriceAnalyzer):
    """
    Analyzes broader market trends and inventory health.
    Inherits from PriceAnalyzer to share the data loading logic.
    """
    
    def get_market_health(self):
        """
        Returns high-level market metrics.
        """
        df = self.get_dataframe()
        
        # 1. Calculate Market Share (which city has most listings)
        city_counts = df['city'].value_counts()
        
        # 2. Price Volatility (Standard Deviation tells us if prices vary wildly)
        # High Std Dev = Mixed market (mansions next to shacks)
        # Low Std Dev = Uniform market (everything costs the same)
        volatility = df.groupby('city')['price'].std().round(0)
        
        # 3. Combine into a nice table
        market_summary = pd.DataFrame({
            'Inventory Count': city_counts,
            'Price Volatility': volatility
        }).fillna(0) # Fix NaNs if only 1 house exists
        
        return market_summary.sort_values('Inventory Count', ascending=False)