## 🧠 Machine Learning Pipeline

- **Datasets fused:** groundwater nitrate, water potability, and water quality datasets merged into a single `fused_dataset.csv`
- **Target:** `risk_label` (binary: 0 = Safe, 1 = High contamination risk)
- **Models trained:** Random Forest, Decision Tree, Logistic Regression
- **Imbalance handling:** SMOTE applied to balance safe vs. contaminated classes
- **Model selection:** best F1-score on the contaminated class (not raw accuracy)
- **Deployment model:** a separate, lightweight model (`api_model.pkl`) trained only on the 7 features available in the live dashboard (Temperature, pH, Nitrate, Conductivity, Turbidity, WQI, Total Coliform), keeping the original 39-feature academic model untouched

## 🔌 Backend (FastAPI)

**Endpoints:**
| Method | Path       | Description                      |
|--------|-----------|-----------------------------------|
| GET    | `/`       | Health check                      |
| POST   | `/predict`| Returns prediction + probability  |

**Example request body:**
```json
{
  "temperature": 25.0,
  "ph": 7.0,
  "nitrate": 20.0,
  "conductivity": 500.0,
  "turbidity": 2.0,
  "wqi": 40.0,
  "coliform": 50.0
}
```

**Example response:**
```json
{
  "prediction": "Safe",
  "probability": 41.12
}
```

---

## 📊 Frontend (Streamlit)

- Manual sliders simulate live IoT sensor readings
- Optional **OpenWeather API** integration for current temperature/humidity/conditions
- Rule-based scientific validation against WHO safety thresholds (nitrate, pH, conductivity, turbidity, coliform, WQI)
- Visualizations: **Risk Gauge**, **Radar Chart**, **Safe Limits Comparison Bar Chart**
- Sends sensor values to the FastAPI backend via `POST /predict` and displays the returned prediction

> Note: the rule-based analysis and the ML model are intentionally independent — the rules encode strict WHO thresholds (e.g. any detectable coliform = risk), while the model reflects patterns learned from the training data. The two can disagree, which is expected and shown transparently to the user.

---

## 🐳 Running with Docker

Both services are containerized and orchestrated with Docker Compose.

**Build and start everything:**
```bash
docker compose build
docker compose up
```

**Run in the background:**
```bash
docker compose up -d
```

**Check status / logs:**
```bash
docker compose ps
docker compose logs -f
```

**Stop everything:**
```bash
docker compose down
```

Once running:
- Backend → [http://localhost:8000](http://localhost:8000) (docs at `/docs`)
- Frontend → [http://localhost:8501](http://localhost:8501)

---

## 💻 Running Locally (without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd deploy
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deployment

Both services are deployed independently on **[Render](https://render.com)** as Dockerized web services:

- **Backend (FastAPI):** [https://hydrocontam-predictor-dhav.onrender.com](https://hydrocontam-predictor-dhav.onrender.com)
  ([interactive API docs](https://hydrocontam-predictor-dhav.onrender.com/docs))
- **Frontend (Streamlit):** [https://frontend-rmpc.onrender.com](https://frontend-rmpc.onrender.com)

> Note: both run on Render's free tier, which spins down after 15 minutes of inactivity. The first request after idling may take 30–60 seconds to respond while the service wakes up — this is expected behavior, not an error.

---

## 🚀 Tech Stack

`Python` · `scikit-learn` · `imbalanced-learn (SMOTE)` · `FastAPI` · `Uvicorn` · `Streamlit` · `Plotly` · `Pandas` / `NumPy` · `Docker` / `Docker Compose` · `OpenWeather API`

---

## 📌 Status

✅ Data preprocessing & fusion · ✅ Feature engineering · ✅ Model training & evaluation · ✅ Model selection · ✅ FastAPI backend · ✅ Streamlit frontend · ✅ IoT simulation · ✅ Scientific threshold analysis · ✅ Weather integration · ✅ Docker containerization · ✅ Cloud deployment (Render)
