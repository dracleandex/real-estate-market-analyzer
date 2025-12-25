from sqlalchemy.orm import Session
from src.core.models import Property
from thefuzz import fuzz

class DuplicateDetector:
    """
    Uses fuzzy logic to find properties that look the same 
    but have slightly different spelling.
    """
    
    def __init__(self, session: Session):
        self.session = session

    def find_potential_duplicate(self, new_address, city, threshold=85):
        """
        Checks if a similar address already exists in the same city.
        Returns the existing Property object if found, else None.
        
        threshold=85 means "85% similar".
        """
        # 1. Filter by City first (Optimization to avoid checking every house in the world)
        # We perform a rough database search first
        candidates = self.session.query(Property).filter(
            Property.city == city
        ).all()
        
        if not candidates:
            return None

        # 2. Check Fuzzy Similarity on Address
        best_match = None
        highest_score = 0
        
        for candidate in candidates:
            # Calculate similarity score (0 to 100)
            score = fuzz.token_sort_ratio(new_address, candidate.address)
            
            if score > highest_score:
                highest_score = score
                best_match = candidate
        
        # 3. Decision
        if highest_score >= threshold:
            print(f"   ⚠️ Potential Duplicate Found (Score: {highest_score}%)")
            print(f"      New: {new_address}")
            print(f"      Old: {best_match.address}")
            return best_match
            
        return None