import os
import streamlit as st
import requests

# --------------------------------------------------
# Environment Config (Optional for Hugging Face)
# --------------------------------------------------
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_DATA_PATH"] = "/tmp"
os.environ["STREAMLIT_CONFIG_FILE"] = "/tmp/config.toml"

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(page_title="DispatchBrain ETA Predictor", layout="centered")

# --------------------------------------------------
# App Header
# --------------------------------------------------
st.title("Dispatch ETA Prediction")
st.write("Fill in the delivery details below to get an estimated arrival time.")

# --------------------------------------------------
# Input Section
# --------------------------------------------------
st.subheader("Delivery Information")

hour = st.slider("Hour of Day", min_value=0, max_value=23, value=14)
day_of_week = st.selectbox("Day of Week", options=[
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])
is_weekend = st.radio("Is it Weekend?", options=["No", "Yes"])
distance_km = st.number_input("Distance (km)", value=7.5)
log_distance = st.number_input("Log Distance", value=2.14)
delivery_duration = st.number_input("Expected Delivery Duration (minutes)", value=18.0)
weather_severity = st.slider("Weather Severity (0 = Clear, 10 = Severe)", 0.0, 10.0, 3.2)

# Optional fields for display only (not sent to backend)
pickup_lat = st.number_input("Pickup Latitude", value=31.5204)
pickup_lon = st.number_input("Pickup Longitude", value=74.3587)
drop_lat = st.number_input("Drop Latitude", value=31.4504)
drop_lon = st.number_input("Drop Longitude", value=73.1350)

# --------------------------------------------------
# Prepare Payload (Only Required Fields)
# --------------------------------------------------
day_map = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

payload = {
    "hour": hour,
    "day_of_week": day_map[day_of_week],
    "is_weekend": 1 if is_weekend == "Yes" else 0,
    "distance_km": distance_km,
    "log_distance": log_distance,
    "weather_severity": weather_severity,
    "delivery_duration": delivery_duration
}

# --------------------------------------------------
# API Call and Prediction Display
# --------------------------------------------------
API_URL = "https://salmaml56-dispacthbraineta.hf.space/predict_eta"

if st.button("Predict ETA"):
    st.info("Sending request to backend...")
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()
        st.success(f"Estimated Arrival Time: {result['predicted_eta']} minutes")

    except requests.exceptions.RequestException as req_err:
        st.error("Prediction failed due to a connection issue.")
        st.code(str(req_err), language="text")

    except Exception as e:
        st.error("An unexpected error occurred during prediction.")
        st.code(str(e), language="text")
