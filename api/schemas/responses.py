from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DailyPredictionResponse(BaseModel):
    recommended_route: List[str]
    predicted_time_hours: float
    predicted_distance_km: float
    confidence: float
    route_score: float
    traffic_risk: str
    fuel_saving_estimate: str
    explanation: List[str]

class WeeklyPredictionResponse(BaseModel):
    monday: List[str]
    tuesday: List[str]
    wednesday: List[str]
    thursday: List[str]
    friday: List[str]
    weekly_distance_km: float
    weekly_efficiency_score: float

class RerouteResponse(BaseModel):
    original_route: List[str]
    rerouted_route: List[str]
    reason: str
    time_saved_minutes: float
    confidence: float

class RouteDetailsResponse(BaseModel):
    id: str
    driver_id: str
    recommended_route: List[str]
    predicted_duration_minutes: float
    confidence_score: float

class HealthResponse(BaseModel):
    status: str
    version: str
