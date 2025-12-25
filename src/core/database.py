from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

# Import the Base and Models so SQLAlchemy knows what to build
from src.core.models import Base, Property, PriceHistory 

class DatabaseManager:
    def __init__(self, db_url=None):
        if db_url is None:
            # Ensure the data directory exists
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, 'data')
            os.makedirs(data_dir, exist_ok=True)
            db_url = f"sqlite:///{os.path.join(data_dir, 'real_estate.db')}"
            
        self.engine = create_engine(db_url)
        
        # --- 🏗️ CRITICAL FIX: BUILD TABLES AUTOMATICALLY ---
        # This creates the 'properties' and 'price_history' tables 
        # if they don't exist yet.
        Base.metadata.create_all(self.engine)
        # ----------------------------------------------------
        
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()