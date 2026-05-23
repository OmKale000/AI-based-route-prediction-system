import folium
from sqlalchemy.orm import Session
from data.models import RoutePrediction, Location

def generate_route_map(driver_id: str, db: Session) -> str:
    """
    Generates a Folium map HTML for the driver's latest route.
    """
    # Fetch latest route
    route_prediction = db.query(RoutePrediction).filter(
        RoutePrediction.driver_id == driver_id
    ).order_by(RoutePrediction.date.desc()).first()
    
    if not route_prediction:
        return "<h1>No route found for this driver</h1>"
        
    route_ids = route_prediction.recommended_route
    
    # In a real scenario, fetch lat/lon from Location table
    # For now, we mock San Francisco coordinates if not found
    
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)
    
    points = []
    base_lat = 37.7749
    base_lon = -122.4194
    
    for idx, loc_id in enumerate(route_ids):
        # Retrieve from DB if exists
        loc = db.query(Location).filter(Location.id == loc_id).first()
        
        if loc:
            lat = loc.latitude
            lon = loc.longitude
            name = loc.name
        else:
            lat = base_lat + (idx * 0.005)
            lon = base_lon + (idx * 0.005)
            name = f"Stop {idx+1} ({loc_id})"
            
        points.append((lat, lon))
        folium.Marker(
            [lat, lon],
            popup=name,
            tooltip=f"Stop {idx+1}"
        ).add_to(m)
        
    # Draw line connecting stops
    if len(points) > 1:
        folium.PolyLine(points, color="blue", weight=2.5, opacity=0.8).add_to(m)
        
    return m._repr_html_()
