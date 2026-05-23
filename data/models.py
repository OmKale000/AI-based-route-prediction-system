from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from data.database import Base
from datetime import datetime

class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    vehicle_type = Column(String)
    preferred_region = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    trips = relationship("Trip", back_populates="driver")
    routes = relationship("RoutePrediction", back_populates="driver")

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    cluster_id = Column(Integer, nullable=True)
    address = Column(String, nullable=True)

class Trip(Base):
    """Historical trip records for training."""
    __tablename__ = "trips"
    
    id = Column(String, primary_key=True, index=True)
    driver_id = Column(String, ForeignKey("drivers.id"))
    date = Column(DateTime, default=datetime.utcnow)
    
    # Stores an ordered list of location IDs
    stop_sequence = Column(JSON)
    actual_duration_minutes = Column(Float)
    actual_distance_km = Column(Float)
    efficiency_score = Column(Float, nullable=True)
    
    driver = relationship("Driver", back_populates="trips")

class RoutePrediction(Base):
    """Stored route predictions."""
    __tablename__ = "route_predictions"
    
    id = Column(String, primary_key=True, index=True)
    driver_id = Column(String, ForeignKey("drivers.id"))
    date = Column(DateTime, default=datetime.utcnow)
    
    input_locations = Column(JSON)
    recommended_route = Column(JSON)
    predicted_duration_minutes = Column(Float)
    predicted_distance_km = Column(Float)
    confidence_score = Column(Float)
    route_score = Column(Float)
    explanation = Column(JSON)
    
    driver = relationship("Driver", back_populates="routes")
