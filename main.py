from fastapi import FastAPI
from supabase_client import test_connection
import joblib

app = FastAPI()

model = joblib.load("model.pkl")


@app.get("/")
def home():
    return {"message": "UPDATED VERSION 🚀"}


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
    return {"predicted_delay_minutes": float(prediction[0])}


@app.get("/test-db")
def test_db():
    status, response = test_connection()
    return {
        "status_code": status,
        "response": response
    }