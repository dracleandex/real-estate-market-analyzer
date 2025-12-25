import pandas as pd
from src.core.models import PriceHistory
from src.core.database import DatabaseManager

class TimeSeriesAnalyzer:
    """
    Analyzes price changes over time.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_price_changes(self):
        """
        Fetches the history table to see trends.
        """
        with self.db.session_scope() as session:
            # Query history join with Property to get address
            # (Requires SQL knowledge, simplified here)
            query = session.query(PriceHistory)
            df = pd.read_sql(query.statement, session.bind)
            
            return df
            
    # NOTE: This analyzer becomes powerful after running the scheduler for a few days.