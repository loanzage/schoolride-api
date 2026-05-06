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

    try:
        # 1. AI prediction
        delay = predict_delay(
            data.get("distance_km", 0),
            data.get("traffic_level", 0),
            data.get("stops", 0),
            data.get("weather", 0),
            data.get("departure_hour", 0)
        )

        # 2. Payload for Supabase
        payload = {
            "driver_id": data["driver_id"],
            "child_id": data["child_id"],
            "pickup_location": data["pickup_location"],
            "dropoff_location": data["dropoff_location"],
            "departure_time": data.get("departure_time"),
            "status": "scheduled",
            "delay_minutes": delay
        }

        # 3. Send to Supabase
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/trips",
            headers=headers,
            json=payload
        )

        return {
            "success": True,
            "trip": {
                "driver_id": data["driver_id"],
                "child_id": data["child_id"],
                "status": "scheduled",
                "delay_minutes": delay
            },
            "supabase_status": response.status_code
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# =========================
# GET TRIPS ENDPOINT
# =========================
@app.get("/trips")
def get_trips():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/trips?select=*",
            headers=headers
        )

        return {
            "success": True,
            "data": response.json(),
            "count": len(response.json()) if response.status_code == 200 else 0
        }

    except Exception as e:
        return {
            "success": False,
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