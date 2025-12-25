from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'
    
    id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    square_feet = Column(Integer)
    property_type = Column(String)
    listing_status = Column(String)
    source_site = Column(String)
    url = Column(String, unique=True)
    
    # --- NEW COLUMNS FOR STEP 7 ---
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # ------------------------------
    
    scraped_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    price_history = relationship("PriceHistory", back_populates="property")

class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    price = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    property = relationship("Property", back_populates="price_history")