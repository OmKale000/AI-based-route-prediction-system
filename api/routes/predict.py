from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from api.schemas.requests import DailyPredictionRequest, WeeklyPredictionRequest, RerouteRequest
from api.schemas.responses import DailyPredictionResponse, WeeklyPredictionResponse, RerouteResponse
from data.database import get_db

# Assuming services will be implemented
from services.prediction_service import get_daily_prediction, get_weekly_prediction
from services.reroute_engine import calculate_reroute

router = APIRouter()

@router.post("/daily", response_model=DailyPredictionResponse)
async def predict_daily(request: DailyPredictionRequest, db: Session = Depends(get_db)):
    """
    Predict the optimal route sequence and ETA for a driver's daily locations.
    """
    try:
        response = await get_daily_prediction(request, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/weekly", response_model=WeeklyPredictionResponse)
async def predict_weekly(request: WeeklyPredictionRequest, db: Session = Depends(get_db)):
    """
    Optimize and distribute visits across the week to balance workload.
    """
    try:
        response = await get_weekly_prediction(request, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
