# AI Route Prediction System

A fully deployment-ready AI-powered route intelligence and optimization platform for logistics and field-sales companies.

## Overview

This system provides a robust API for predicting and optimizing routes using a hybrid architecture. It combines heuristic optimization (OR-Tools, Beam Search) with Machine Learning (XGBoost) for route ranking, ETA prediction, and confidence scoring.

### Key Features
- **Daily & Weekly Routing:** Plan optimized routes for immediate execution or weekly workload balancing.
- **Dynamic Rerouting:** Intelligently update routes in real-time when traffic or conditions change.
- **ETA & Confidence:** Get highly accurate ML-based ETAs along with a calibrated confidence score.
- **Explainability:** SHAP integration to understand why a particular route was chosen.
- **Google Maps Integration:** Caches and utilizes Google APIs for accurate distances and geocoding.
- **Visualization:** Interactive Folium-based maps for easy route review.

## Architecture

1. **Input Request** -> Geospatial Preprocessing
2. **Traffic-Aware Graph Builder** -> Builds the weighted graph of locations
3. **Candidate Route Generation** -> OR-Tools & Beam Search create multiple path candidates
4. **Feature Extraction** -> Spatial, temporal, and historical features
5. **ML Route Ranking** -> XGBoost model scores all candidates
6. **ETA Prediction** -> Independent regression model for precise timing
7. **Confidence Calibration** -> Historical and variance-based scoring
8. **Final Route Selection** -> Outputs top route with explanations

## Setup

### Requirements
- Python 3.11+
- Docker & Docker Compose (Optional)

### Local Installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
make setup
```

### Environment
Copy `.env.example` to `.env` and fill in your keys (e.g., `GOOGLE_MAPS_API_KEY`). If the key is omitted, the system falls back to mock mode.

### Running the API
```bash
make run
```

### Docker Deployment
```bash
make docker-up
```

## Synthetic Data & Training

To simulate data and train the models locally:
```bash
make generate-data
make train
```

## API Endpoints

- `POST /predict/daily` - Predict optimal daily route.
- `POST /predict/weekly` - Optimize assignments across a week.
- `POST /reroute` - Recalculate route mid-trip.
- `POST /retrain` - Trigger model retraining.
- `GET /health` - System health check.
- `GET /metrics` - Prometheus metrics.
- `GET /visualize/{driver_id}` - Get an interactive map of the route.
- `GET /route/{route_id}` - Fetch route details from the database.

## Scalability
The system is built on FastAPI and AsyncIO. It uses SQLite by default for simplicity, but can be seamlessly switched to PostgreSQL via `.env` configuration. Redis is supported for high-performance caching of API requests and map data.
