import pandas as pd
from sqlalchemy.orm import Session
from src.core.database import DatabaseManager
from src.core.models import Property

class PriceAnalyzer:
    """
    Performs statistical analysis on real estate data.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_dataframe(self):
        """
        Fetches all data and converts it to a Pandas DataFrame.
        """
        with self.db.session_scope() as session:
            # Query all properties
            query = session.query(Property)
            
            # Use Pandas to read SQL directly
            df = pd.read_sql(query.statement, session.bind)
            
            return df

    def calculate_price_per_sqft(self, df=None):
        """
        Adds a 'price_per_sqft' column to the dataframe.
        """
        if df is None:
            df = self.get_dataframe()
            
        # Avoid division by zero
        df = df[df['square_feet'] > 0].copy()
        
        # Calculate
        df['price_per_sqft'] = df['price'] / df['square_feet']
        
        # Round to 2 decimal places
        df['price_per_sqft'] = df['price_per_sqft'].round(2)
        
        return df

    def get_summary_stats(self, group_by_city=True):
        """
        Returns a table with Mean, Median, Min, and Max prices.
        """
        df = self.calculate_price_per_sqft()
        
        if group_by_city:
            # Group by City and calculate stats
            stats = df.groupby('city').agg({
                'price': ['count', 'mean', 'median', 'min', 'max'],
                'price_per_sqft': ['mean']
            })
            
            # Rename columns to look nice
            stats.columns = ['Count', 'Avg Price', 'Median Price', 'Min Price', 'Max Price', 'Avg Price/SqFt']
            
            # Round values
            return stats.round(0)
        else:
            # Global stats
            return df[['price', 'price_per_sqft']].describe().round(2)