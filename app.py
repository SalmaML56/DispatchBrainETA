import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------
model_path = os.path.join(os.path.dirname(__file__), 'models', 'lightgbm_model.pkl')
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

model = joblib.load(model_path)

# --------------------------------------------------
# Load Feature Template for Column Alignment
# --------------------------------------------------
feature_path = os.path.join(os.path.dirname(__file__), 'data', 'features', 'X_features_dispatchbrain.csv')
if not os.path.exists(feature_path):
    raise FileNotFoundError(f"Feature template not found at: {feature_path}")

feature_template = pd.read_csv(feature_path)
expected_columns = feature_template.columns.tolist()

# --------------------------------------------------
# Define Input Schema for Request Validation
# --------------------------------------------------
class DispatchInput(BaseModel):
    hour: int
    day_of_week: int
    is_weekend: int
    distance_km: float
    log_distance: float
    weather_severity: float
    delivery_duration: float

# --------------------------------------------------
# Initialize FastAPI App
# --------------------------------------------------
app = FastAPI()

# --------------------------------------------------
# Define Prediction Endpoint
# --------------------------------------------------
@app.post("/predict_eta")
def predict_eta(data: DispatchInput):
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])

    # Ensure column alignment
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0.0

    input_df = input_df[expected_columns]

    try:
        prediction = model.predict(input_df)[0]
        return {"predicted_eta": round(float(prediction), 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
