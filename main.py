from fastapi import FastAPI
from ai_model import predict_delay
import requests

from supabase_client import (
    test_connection,
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI()

# =========================
# HEADERS (Supabase Auth)
# =========================
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


# =========================
# HOME ROUTE
# =========================
@app.get("/")
def home():
    return {"message": "UPDATED VERSION 🚀 SchoolRide API running"}


# =========================
# AI PREDICTION ENDPOINT
# =========================
@app.post("/predict")
def predict(data: dict):
    delay = predict_delay(
        data["distance_km"],
        data["traffic_level"],
        data["stops"],
        data["weather"],
        data["departure_hour"]
    )

    return {
        "predicted_delay_minutes": delay
    }


# =========================
# CREATE TRIP ENDPOINT
# =========================
@app.post("/create-trip")
def create_trip(data: dict):

    # 1. Run AI prediction
    delay = predict_delay(
        data.get("distance_km", 0),
        data.get("traffic_level", 0),
        data.get("stops", 0),
        data.get("weather", 0),
        data.get("departure_hour", 0)
    )

    # 2. Build payload (NOW includes delay)
    payload = {
        "driver_id": data["driver_id"],
        "child_id": data["child_id"],
        "pickup_location": data["pickup_location"],
        "dropoff_location": data["dropoff_location"],
        "departure_time": data.get("departure_time"),
        "status": "scheduled",
        "delay_minutes": delay
    }

    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/trips",
            headers=headers,
            json=payload
        )

        return {
            "status_code": response.status_code,
            "response": response.text,
            "predicted_delay": delay
        }

    except Exception as e:
        return {
            "status_code": 500,
            "error": str(e)
        }


# =========================
# SUPABASE TEST ROUTE
# =========================
@app.get("/test-db")
def test_db():
    status, response = test_connection()

    return {
        "status_code": status,
        "response": response
    }