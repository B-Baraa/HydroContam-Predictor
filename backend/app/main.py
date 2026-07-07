from fastapi import FastAPI

app = FastAPI(
    title="HydroContam Cloud API",
    description="Water Quality Prediction API",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to HydroContam Cloud API 🚀",
        "status": "Running"
    }