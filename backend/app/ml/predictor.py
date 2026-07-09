import pickle
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "api_model.pkl", "rb") as f:
    model = pickle.load(f)

with open(BASE_DIR / "api_features.pkl", "rb") as f:
    FEATURES = pickle.load(f)


def predict_water(
    temperature,
    ph,
    nitrate,
    conductivity,
    turbidity,
    wqi,
    coliform,
):

    input_data = pd.DataFrame([{
        "Temperature": temperature,
        "pH": ph,
        "Nitrate (mg/ L)": nitrate,
        "Conductivity (mho/ Cm)": conductivity,
        "Turbidity": turbidity,
        "WQI": wqi,
        "Total Coliform (MPN/ 100 mL)": coliform,
    }])

    input_data = input_data[FEATURES]

    prediction = int(model.predict(input_data)[0])

    probability = float(model.predict_proba(input_data)[0][1])

    return prediction, probability