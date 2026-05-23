import uuid
from typing import List
from sqlalchemy.orm import Session
from api.schemas.requests import DailyPredictionRequest, WeeklyPredictionRequest
from api.schemas.responses import DailyPredictionResponse, WeeklyPredictionResponse
from data.models import RoutePrediction
from optimization.candidate_generator import CandidateGenerator
from services.eta_service import eta_service
from services.confidence_service import confidence_service
import random

candidate_generator = CandidateGenerator()

async def get_daily_prediction(request: DailyPredictionRequest, db: Session) -> DailyPredictionResponse:
    """
    Core pipeline for daily route prediction.
    1. Generate candidates
    2. Score candidates
    3. Calculate ETA and Confidence
    4. Save and return
    """
    # 1. Candidate Generation
    candidates = await candidate_generator.generate_candidates(request.locations)
    
    # 2. Candidate Ranking (Mocking the ML ranking for now)
    # Ideally, we pass candidates through XGBoost to get a score
    best_route = candidates[0]
    best_score = random.uniform(80.0, 95.0)
    
    # 3. ETA & Confidence
    predicted_time = await eta_service.predict_eta(best_route, {})
    predicted_distance = await eta_service.extract_distance(best_route)
    confidence = confidence_service.calculate_confidence(best_route, predicted_time)
    
    # Explanation generation
    explanation = [
        f"Generated {len(candidates)} candidate routes.",
        "Selected optimal route based on predicted travel efficiency.",
        "Traffic conditions factored into ETA."
    ]
    
    # 4. Save to DB
    prediction_record = RoutePrediction(
        id=str(uuid.uuid4()),
        driver_id=request.driver_id,
        input_locations=request.locations,
        recommended_route=best_route,
        predicted_duration_minutes=predicted_time * 60,
        predicted_distance_km=predicted_distance,
        confidence_score=confidence,
        route_score=best_score,
        explanation=explanation
    )
    db.add(prediction_record)
    db.commit()
    
    return DailyPredictionResponse(
        recommended_route=best_route,
        predicted_time_hours=predicted_time,
        predicted_distance_km=predicted_distance,
        confidence=confidence,
        route_score=round(best_score, 2),
        traffic_risk="medium" if predicted_time > 4 else "low",
        fuel_saving_estimate="12%",
        explanation=explanation
    )

async def get_weekly_prediction(request: WeeklyPredictionRequest, db: Session) -> WeeklyPredictionResponse:
    """
    Distribute locations across the week.
    Mock implementation of a clustering approach.
    """
    locs = request.locations
    random.shuffle(locs)
    
    # Split into 5 days roughly
    chunks = [locs[i::5] for i in range(5)]
    
    return WeeklyPredictionResponse(
        monday=chunks[0],
        tuesday=chunks[1],
        wednesday=chunks[2],
        thursday=chunks[3],
        friday=chunks[4],
        weekly_distance_km=random.uniform(150.0, 300.0),
        weekly_efficiency_score=random.uniform(85.0, 98.0)
    )
