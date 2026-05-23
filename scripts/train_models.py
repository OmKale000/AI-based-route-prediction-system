import os
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from data.database import engine
import joblib

MODEL_DIR = "./artifacts"

def trigger_retraining():
    print("Starting ML Model Retraining Pipeline...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # 1. Fetch data
    try:
        query = "SELECT * FROM trips"
        df = pd.read_sql(query, engine)
        if df.empty:
            print("No data available for training.")
            return
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print(f"Loaded {len(df)} records for training.")
    
    # 2. Feature Engineering (Simplified)
    # Target 1: Efficiency score (for ranking)
    # Target 2: Duration (for ETA)
    
    # Mocking features: stops count, hour, day
    df['num_stops'] = df['stop_sequence'].apply(lambda x: len(x) if isinstance(x, list) else 5)
    df['hour'] = pd.to_datetime(df['date']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
    
    X = df[['num_stops', 'hour', 'day_of_week']]
    y_duration = df['actual_duration_minutes']
    y_score = df['efficiency_score']
    
    # Train ETA Model
    print("Training ETA XGBoost Regressor...")
    X_train, X_test, y_train, y_test = train_test_split(X, y_duration, test_size=0.2, random_state=42)
    eta_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    eta_model.fit(X_train, y_train)
    preds = eta_model.predict(X_test)
    print(f"ETA Model MAE: {mean_absolute_error(y_test, preds):.2f} minutes")
    joblib.dump(eta_model, os.path.join(MODEL_DIR, "eta_model.pkl"))
    
    # Train Ranking Model
    print("Training Route Ranking Model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y_score, test_size=0.2, random_state=42)
    rank_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=4)
    rank_model.fit(X_train, y_train)
    preds = rank_model.predict(X_test)
    print(f"Ranking Model MSE: {mean_squared_error(y_test, preds):.2f}")
    joblib.dump(rank_model, os.path.join(MODEL_DIR, "rank_model.pkl"))
    
    print("Retraining completed successfully. Models saved to /artifacts.")

if __name__ == "__main__":
    trigger_retraining()
