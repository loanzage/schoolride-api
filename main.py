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
    return {"message": "🚀 SchoolRide API running"}

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
# CREATE TRIP
# =========================
@app.post("/create-trip")
def create_trip(data: dict):

    try:
        delay = predict_delay(
            data.get("distance_km", 0),
            data.get("traffic_level", 0),
            data.get("stops", 0),
            data.get("weather", 0),
            data.get("departure_hour", 0)
        )

        payload = {
            "driver_id": data["driver_id"],
            "child_id": data["child_id"],
            "pickup_location": data["pickup_location"],
            "dropoff_location": data["dropoff_location"],
            "departure_time": data.get("departure_time"),
            "status": "scheduled",
            "delay_minutes": delay
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/trips",
            headers=headers,
            json=payload
        )

        return {
            "success": True,
            "trip": payload,
            "supabase_status": response.status_code
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# =========================
# GET TRIPS
# =========================
@app.get("/trips")
def get_trips():

    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/trips?select=*",
            headers=headers
        )

        data = response.json()

        return {
            "success": True,
            "data": data,
            "count": len(data)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# =========================
# GPS UPDATE ENDPOINT (NEW)
# =========================
@app.post("/drivers/location/update")
def update_driver_location(data: dict):

    try:
        payload = {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "last_seen": "now()"
        }

        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/drivers?id=eq.{data['driver_id']}",
            headers=headers,
            json=payload
        )

        return {
            "success": True,
            "message": "Location updated",
            "status_code": response.status_code
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# =========================
# ANALYTICS DASHBOARD (NEW)
# =========================
@app.get("/analytics/dashboard")
def analytics_dashboard():

    try:
        # DRIVERS
        drivers = requests.get(
            f"{SUPABASE_URL}/rest/v1/drivers?select=status",
            headers=headers
        ).json()

        total_drivers = len(drivers)
        approved = len([d for d in drivers if d["status"] == "approved"])
        pending = len([d for d in drivers if d["status"] == "pending"])
        rejected = len([d for d in drivers if d["status"] == "rejected"])
        suspended = len([d for d in drivers if d["status"] == "suspended"])

        # TRIPS
        trips = requests.get(
            f"{SUPABASE_URL}/rest/v1/trips?select=*",
            headers=headers
        ).json()

        total_trips = len(trips)
        delayed_trips = len([
            t for t in trips
            if t.get("delay_minutes", 0) > 10
        ])

        return {
            "drivers": {
                "total": total_drivers,
                "approved": approved,
                "pending": pending,
                "rejected": rejected,
                "suspended": suspended
            },
            "trips": {
                "total": total_trips,
                "delayed": delayed_trips
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# =========================
# SUPABASE TEST
# =========================
@app.get("/test-db")
def test_db():
    status, response = test_connection()

    return {
        "status_code": status,
        "response": response
    }