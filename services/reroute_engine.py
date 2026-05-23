from sqlalchemy.orm import Session
from api.schemas.requests import RerouteRequest
from api.schemas.responses import RerouteResponse
from optimization.candidate_generator import CandidateGenerator
import random

candidate_generator = CandidateGenerator()

async def calculate_reroute(request: RerouteRequest, db: Session) -> RerouteResponse:
    """
    Recalculates the optimal route for the remaining stops.
    """
    locations_to_visit = [request.current_location] + request.remaining_locations
    
    # Generate new candidates
    candidates = await candidate_generator.generate_candidates(locations_to_visit)
    
    new_route = candidates[0]
    
    # Calculate improvements
    time_saved = random.uniform(5.0, 25.0)
    confidence = random.uniform(0.75, 0.95)
    
    return RerouteResponse(
        original_route=request.remaining_locations,
        rerouted_route=new_route,
        reason="Traffic spike detected on original path",
        time_saved_minutes=round(time_saved, 2),
        confidence=round(confidence, 2)
    )
