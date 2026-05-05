from fastapi import FastAPI
from database import SessionLocal
from sqlalchemy import text
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
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database connected successfully 🚍"}
    except Exception as e:
        print("DB ERROR:", e)  # 👈 forces log output
        return {
            "error": str(e),
            "type": str(type(e))
        }
        finally:
        db.close()  # ✅ VERY IMPORTANT