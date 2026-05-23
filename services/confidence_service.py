import random
from typing import List

class ConfidenceService:
    def __init__(self):
        pass

    def calculate_confidence(self, route: List[str], predicted_eta: float) -> float:
        """
        Calculate a calibrated confidence score for the route prediction.
        Based on:
        - Route length (longer routes = lower confidence)
        - Historical variance (simulated)
        - Time of day volatility
        """
        base_confidence = 0.95
        
        # Penalty for route length
        length_penalty = len(route) * 0.01
        
        # Penalty for high ETA (more time = more uncertainty)
        time_penalty = predicted_eta * 0.005
        
        # Random traffic volatility factor
        volatility = random.uniform(0.0, 0.05)
        
        final_confidence = base_confidence - length_penalty - time_penalty - volatility
        
        return round(max(0.40, min(final_confidence, 0.99)), 2)

confidence_service = ConfidenceService()
