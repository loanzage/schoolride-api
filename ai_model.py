import joblib

model = joblib.load("model.pkl")


def predict_delay(distance_km, traffic_level, stops, weather, departure_hour):
    input_data = [[
        distance_km,
        traffic_level,
        stops,
        weather,
        departure_hour
    ]]

    prediction = model.predict(input_data)
    return float(prediction[0])