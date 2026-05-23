import os
import json
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
from data.database import engine, Base
from data.models import Driver, Location, Trip
from sqlalchemy.orm import Session

fake = Faker()

def generate_data(num_drivers=20, num_locations=100, num_trips=5000):
    print("Generating synthetic data...")
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    
    # 1. Generate Drivers
    drivers = []
    for _ in range(num_drivers):
        d = Driver(
            id=str(uuid.uuid4())[:8],
            name=fake.name(),
            vehicle_type=np.random.choice(["van", "truck", "car"]),
            preferred_region=np.random.choice(["north", "south", "east", "west", "central"])
        )
        drivers.append(d)
        session.add(d)
    
    # 2. Generate Locations (Clustered)
    # Let's say San Francisco bounds roughly
    base_lat = 37.7749
    base_lon = -122.4194
    
    locations = []
    for _ in range(num_locations):
        # Add random noise to create clusters
        cluster_center_lat = base_lat + np.random.normal(0, 0.05)
        cluster_center_lon = base_lon + np.random.normal(0, 0.05)
        
        loc_lat = cluster_center_lat + np.random.normal(0, 0.01)
        loc_lon = cluster_center_lon + np.random.normal(0, 0.01)
        
        loc = Location(
            id=str(uuid.uuid4())[:8],
            name=fake.company(),
            latitude=loc_lat,
            longitude=loc_lon,
            cluster_id=np.random.randint(0, 5),
            address=fake.address()
        )
        locations.append(loc)
        session.add(loc)
        
    session.commit()
    
    # 3. Generate Trips
    start_date = datetime.utcnow() - timedelta(days=365)
    
    for _ in range(num_trips):
        driver = np.random.choice(drivers)
        # Select 5 to 12 locations for a trip
        num_stops = np.random.randint(5, 13)
        stops = np.random.choice(locations, size=num_stops, replace=False)
        stop_ids = [s.id for s in stops]
        
        # Calculate rough duration and distance based on random heuristic + stops
        base_duration = num_stops * 15 # 15 mins per stop average
        traffic_factor = np.random.uniform(0.8, 1.5)
        duration = base_duration * traffic_factor
        distance = num_stops * np.random.uniform(2.0, 8.0) # km per segment
        
        trip_date = start_date + timedelta(days=np.random.randint(0, 365), hours=np.random.randint(7, 18))
        
        efficiency = np.clip(100 - (duration / (num_stops * 10)) * 20 + np.random.normal(0, 5), 40, 100)
        
        trip = Trip(
            id=str(uuid.uuid4()),
            driver_id=driver.id,
            date=trip_date,
            stop_sequence=stop_ids,
            actual_duration_minutes=round(duration, 2),
            actual_distance_km=round(distance, 2),
            efficiency_score=round(efficiency, 2)
        )
        session.add(trip)
        
        # Commit in batches
        if _ % 500 == 0:
            session.commit()
            print(f"Generated {_} trips...")
            
    session.commit()
    session.close()
    print(f"Data generation complete! {num_trips} trips stored in database.")

if __name__ == "__main__":
    generate_data()
