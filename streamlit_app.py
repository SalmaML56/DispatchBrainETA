import os
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import streamlit as st
import requests

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="DispatchBrain ETA Predictor", layout="centered")
st.title("Dispatch ETA Prediction")
st.write("Fill in the delivery details below to get an estimated arrival time.")

# -------------------------------
# Input Section
# -------------------------------
st.subheader("Delivery Information")

# Time and Date Inputs
hour = st.slider("Hour of Day", min_value=0, max_value=23, value=14)
day_of_week = st.selectbox("Day of Week", options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
is_weekend = st.radio("Is it Weekend?", options=["No", "Yes"])

# Distance and Duration Inputs
distance_km = st.number_input("Distance (km)", value=7.5)
log_distance = st.number_input("Log Distance", value=2.14)
delivery_duration = st.number_input("Expected Delivery Duration (minutes)", value=18.0)

# Weather Input
weather_severity = st.slider("Weather Severity (0 = Clear, 10 = Severe)", 0.0, 10.0, 3.2)

# Location Inputs
pickup_lat = st.number_input("Pickup Latitude", value=31.5204)
pickup_lon = st.number_input("Pickup Longitude", value=74.3587)
drop_lat = st.number_input("Drop Latitude", value=31.4504)
drop_lon = st.number_input("Drop Longitude", value=73.1350)

# -------------------------------
# Prepare Payload for API
# -------------------------------
# Convert day name to numeric format
day_map = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

# Create dictionary to send to FastAPI
payload = {
    "hour": hour,
    "day_of_week": day_map[day_of_week],
    "is_weekend": 1 if is_weekend == "Yes" else 0,
    "distance_km": distance_km,
    "log_distance": log_distance,
    "weather_severity": weather_severity,
    "delivery_duration": delivery_duration,
    "pickup_lat": pickup_lat,
    "pickup_lon": pickup_lon,
    "drop_lat": drop_lat,
    "drop_lon": drop_lon
}

# -------------------------------
# API Call and Prediction Display
# -------------------------------
if st.button("Predict ETA"):
    try:
        # Send POST request to FastAPI
        response = requests.post("http://127.0.0.1:8000/predict_eta", json=payload)
        result = response.json()

        # Show prediction result
        st.success(f"Estimated Arrival Time: {result['predicted_eta_minutes']} minutes")

    except Exception as e:
        # Show error if API call fails
        st.error("❌ Prediction failed. Please check if the FastAPI server is running.")
        st.code(str(e), language="bash")