from pydantic import BaseModel, Field
from typing import List
from datetime import date as dt_date


class DailyPredictionRequest(BaseModel):
    driver_id: str = Field(..., description="ID of the driver")
    prediction_date: dt_date = Field(..., description="Date for the route")
    locations: List[str] = Field(
        ...,
        min_length=2,
        description="List of location IDs to visit"
    )


class WeeklyPredictionRequest(BaseModel):
    driver_id: str = Field(..., description="ID of the driver")
    week_id: str = Field(
        ...,
        description="Week identifier, e.g., '2026-W20'"
    )
    locations: List[str] = Field(
        ...,
        description="List of all locations to visit over the week"
    )


class RerouteRequest(BaseModel):
    driver_id: str = Field(..., description="ID of the driver")
    route_id: str = Field(..., description="Current route ID")
    current_location: str = Field(
        ...,
        description="Driver's current location ID"
    )
    remaining_locations: List[str] = Field(
        ...,
        description="Locations yet to be visited"
    )