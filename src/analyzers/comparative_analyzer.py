from src.analyzers.price_analyzer import PriceAnalyzer

class ComparativeAnalyzer(PriceAnalyzer):
    """
    The 'Deal Hunter'. Compares individual properties against the market average.
    """
    
    def find_deals(self, discount_threshold=0.10):
        """
        Finds houses that are X% cheaper than the city average.
        """
        df = self.calculate_price_per_sqft()
        
        # 1. Calculate Average Price per City
        city_avgs = df.groupby('city')['price'].transform('mean')
        
        # 2. Calculate Difference (%)
        # Negative number = Cheaper than average
        df['market_diff_pct'] = (df['price'] - city_avgs) / city_avgs
        
        # 3. Filter for 'Deals' (e.g., 10% below average)
        deals = df[df['market_diff_pct'] < -discount_threshold].copy()
        
        # Format for display
        return deals[['address', 'city', 'price', 'market_diff_pct']].sort_values('market_diff_pct')