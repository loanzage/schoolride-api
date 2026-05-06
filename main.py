from fastapi import FastAPI
import joblib
import requests

from supabase_client import (
    test_connection,
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI()

# Load ML model once at startup
model = joblib.load("model.pkl")


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
    input_data = [[
        data["distance_km"],
        data["traffic_level"],
        data["stops"],
        data["weather"],
        data["departure_hour"]
    ]]

    prediction = model.predict(input_data)

    return {
        "predicted_delay_minutes": float(prediction[0])
    }


# =========================
# CREATE TRIP ENDPOINT
# =========================
@app.post("/create-trip")
def create_trip(data: dict):

    payload = {
        "driver_id": data["driver_id"],
        "child_id": data["child_id"],
        "pickup_location": data["pickup_location"],
        "dropoff_location": data["dropoff_location"],
        "departure_time": data.get("departure_time"),
        "status": "scheduled"
    }

    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/trips",
            headers=headers,
            json=payload
        )

        return {
            "status_code": response.status_code,
            "response": response.text
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