from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Load model
model1 = joblib.load("model_final_rf.pkl")

#Input Schema
class AccidentInput(BaseModel):
    weather_condition: str
    lighting_condition: str
    roadway_surface_cond: str
    road_defect: str
    traffic_control_device: str
    trafficway_type: str
    alignment: str
    intersection_related_i: str
    first_crash_type: str
    prim_contributory_cause: str
    damage: str

    num_units: int
    crash_hour: int
    crash_day_of_week: int
    crash_month: int

@app.get("/")
def home():
    return{"message: Accident Severity Prediction API"}

@app.post("/predict")
def predict(data: AccidentInput):

    input_df = pd.DataFrame([{
        "weather_condition":      data.weather_condition,
        "lighting_condition":     data.lighting_condition,
        "roadway_surface_cond":   data.roadway_surface_cond,
        "road_defect":            data.road_defect,
        "traffic_control_device": data.traffic_control_device,
        "trafficway_type":        data.trafficway_type,
        "alignment":              data.alignment,
        "intersection_related_i": data.intersection_related_i,
        "first_crash_type":       data.first_crash_type,
        "prim_contributory_cause":data.prim_contributory_cause,
        "damage":                 data.damage,
        "num_units":              data.num_units,
        "crash_hour":             data.crash_hour,
        "crash_day_of_week":      data.crash_day_of_week,
        "crash_month":            data.crash_month,
    }])

    prediction = model1.predict(input_df)[0]
    probabilities = model1.predict_proba(input_df)[0]
    classes = model1.classes_

    confidence = {
        str(cls): round(float(prob) * 100, 1)
        for cls, prob in zip(classes, probabilities)
    }

    return {
        "predicted_severity": str(prediction),
        "confidence": confidence
    }