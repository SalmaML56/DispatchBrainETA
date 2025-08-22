import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 🔹 Load model
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'lightgbm_model.pkl')
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")
model = joblib.load(model_path)

# 🔹 Load feature template
feature_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'features', 'X_features_dispatchbrain.csv')
if not os.path.exists(feature_path):
    raise FileNotFoundError(f"Feature template not found at: {feature_path}")
feature_template = pd.read_csv(feature_path)
expected_columns = feature_template.columns.tolist()

# 🔹 Define input schema
class DispatchInput(BaseModel):
    hour: int
    day_of_week: int
    is_weekend: int
    distance_km: float
    log_distance: float
    weather_severity: float
    delivery_duration: float
    pickup_lat: float
    pickup_lon: float
    drop_lat: float
    drop_lon: float

# 🔹 Initialize FastAPI app
app = FastAPI(title="DispatchBrain ETA Predictor")

# 🔹 Prediction endpoint
@app.post("/predict_eta")
def predict_eta(data: DispatchInput):
    try:
        input_df = pd.DataFrame([data.dict()])

        # Add missing columns with default 0
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Reorder columns to match training
        input_df = input_df[expected_columns]

        prediction = model.predict(input_df)[0]
        return {"predicted_eta_minutes": round(prediction, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")