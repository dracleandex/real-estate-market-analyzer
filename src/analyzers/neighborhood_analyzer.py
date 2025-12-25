import pandas as pd
from src.analyzers.price_analyzer import PriceAnalyzer

class NeighborhoodAnalyzer(PriceAnalyzer):
    """
    Drills down into specific zip codes or streets.
    """
    
    def compare_zip_codes(self):
        """
        Ranking neighborhoods by expensiveness.
        """
        df = self.calculate_price_per_sqft()
        
        # Group by Zip Code
        stats = df.groupby('zip_code').agg({
            'price': ['count', 'mean', 'median'],
            'price_per_sqft': ['mean']
        })
        
        # Flatten columns for clean display
        stats.columns = ['Count', 'Avg Price', 'Median Price', '$/SqFt']
        
        # Sort by most expensive $/SqFt
        return stats.sort_values('$/SqFt', ascending=False).round(0)