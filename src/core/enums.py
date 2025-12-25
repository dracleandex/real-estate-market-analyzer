from enum import Enum

class PropertyType(str, Enum):
    """Property type classifications."""
    HOUSE = "house"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    APARTMENT = "apartment"
    MULTI_FAMILY = "multi_family"
    LAND = "land"
    MANUFACTURED = "manufactured"
    OTHER = "other"

class ListingStatus(str, Enum):
    """Listing status classifications."""
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"
    OFF_MARKET = "off_market"
    COMING_SOON = "coming_soon"
    CONTINGENT = "contingent"

class DataSource(str, Enum):
    """Data source sites."""
    ZILLOW = "zillow"
    REALTOR = "realtor"
    REDFIN = "redfin"
    TRULIA = "trulia"
    MANUAL = "manual"
    OTHER = "other"