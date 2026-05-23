from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

def test_predict_daily():
    payload = {
        "driver_id": "driver_1",
        "date": "2026-05-20",
        "locations": ["locA", "locB", "locC"]
    }
    response = client.post("/predict/daily", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_route" in data
    assert "confidence" in data
    assert "route_score" in data
    assert len(data["recommended_route"]) > 0

def test_reroute():
    payload = {
        "driver_id": "driver_1",
        "route_id": "route_42",
        "current_location": "locB",
        "remaining_locations": ["locC", "locD"]
    }
    response = client.post("/reroute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "rerouted_route" in data
    assert "time_saved_minutes" in data
