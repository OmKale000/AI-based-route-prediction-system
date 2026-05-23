from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from api.schemas.requests import RerouteRequest
from api.schemas.responses import RerouteResponse, HealthResponse, RouteDetailsResponse
from data.database import get_db

from services.reroute_engine import calculate_reroute
from services.visualization_service import generate_route_map
# Mock retrain function
from scripts.train_models import trigger_retraining

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", version="1.0.0")

@router.post("/reroute", response_model=RerouteResponse)
async def reroute(request: RerouteRequest, db: Session = Depends(get_db)):
    """
    Dynamically recalculate route due to traffic or driver deviation.
    """
    try:
        response = await calculate_reroute(request, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrain")
def retrain_model():
    """
    Trigger the ML training pipeline.
    """
    try:
        trigger_retraining()
        return {"status": "retraining started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visualize/{driver_id}", response_class=HTMLResponse)
def visualize_route(driver_id: str, db: Session = Depends(get_db)):
    """
    Generate an interactive map for the driver's latest route.
    """
    try:
        map_html = generate_route_map(driver_id, db)
        return HTMLResponse(content=map_html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/route/{route_id}", response_model=RouteDetailsResponse)
def get_route(route_id: str, db: Session = Depends(get_db)):
    """
    Fetch a previously computed route by ID.
    """
    # For now, return a mock response
    return RouteDetailsResponse(
        id=route_id,
        driver_id="mock_driver",
        recommended_route=["A", "B", "C"],
        predicted_duration_minutes=45.0,
        confidence_score=0.92
    )
