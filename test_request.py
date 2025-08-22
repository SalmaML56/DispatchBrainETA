import requests

url = "http://127.0.0.1:8000/predict_eta"
payload = {
    "hour": 14,
    "day_of_week": 2,
    "is_weekend": 0,
    "distance_km": 7.5,
    "log_distance": 2.14,
    "weather_severity": 3.2,
    "delivery_duration": 18.0,
    "pickup_lat": 31.5204,
    "pickup_lon": 74.3587,
    "drop_lat": 31.4504,
    "drop_lon": 73.1350
}

response = requests.post(url, json=payload)
print("Predicted ETA:", response.json())