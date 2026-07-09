from fastapi import FastAPI
from pydantic import BaseModel

from app.ml.predictor import predict_water

app = FastAPI(title="HydroContam Cloud API")


class WaterSample(BaseModel):
    temperature: float
    ph: float
    nitrate: float
    conductivity: float
    turbidity: float
    wqi: float
    coliform: float


@app.get("/")
def home():
    return {"message": "HydroContam API Running 🚀"}


@app.post("/predict")
def predict(sample: WaterSample):

    prediction, probability = predict_water(
        sample.temperature,
        sample.ph,
        sample.nitrate,
        sample.conductivity,
        sample.turbidity,
        sample.wqi,
        sample.coliform,
    )

    result = "Safe"

    if prediction == 1:
        result = "High Contamination Risk"

    return {
        "prediction": result,
        "probability": round(probability * 100, 2),
    }