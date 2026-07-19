# HydroRisk Prediction System
# Deployment APP
# =========================================================

# 1. IMPORT LIBRARIES
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# 2. PAGE CONFIG
st.set_page_config(
    page_title="Water Safety Monitoring AI",
    layout="wide"
)

# 3. TITLE
st.title("🌱 Intelligent Water Safety Monitoring Platform")

st.markdown("""
This platform simulates an AI + IoT environmental monitoring system
that predicts whether fertilizer usage may contaminate potable water.

The measurements are manually entered to simulate real-time sensor data.
""")

# 4. SAFE SCIENTIFIC LIMITS
SAFE_LIMITS = {
    "Temperature (°C)": {"safe_max": 25, "critical": 35},
    "pH": {"safe_min": 6.5, "safe_max": 8.5},
    "Nitrate (mg/L)": {"safe_max": 10, "critical": 50},
    "Conductivity (µS/cm)": {"safe_max": 500, "critical": 1500},
    "Turbidity (NTU)": {"safe_max": 5, "critical": 10},
    "WQI": {"safe_max": 50, "critical": 100},
    "Total Coliform": {"safe_max": 0, "critical": 10},
}

# 5. SIDEBAR WEATHER
st.sidebar.header("📍 Environmental Conditions")

city = st.sidebar.text_input("Enter City", value="Tunis")

try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except Exception:
    API_KEY = st.sidebar.text_input(
        "Enter OpenWeather API Key (optional)",
        type="password"
    )

weather_temp = 25
weather_humidity = 50
weather_description = "Unavailable"

if API_KEY:
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather_temp = data["main"]["temp"]
        weather_humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["description"].capitalize()

    except Exception as e:
        st.sidebar.warning(f"Weather error: {e}")
else:
    st.sidebar.warning("Enter OpenWeather API key")

st.sidebar.subheader("🌦 Current Weather")
st.sidebar.write(f"Temperature: {weather_temp} °C")
st.sidebar.write(f"Humidity: {weather_humidity}%")
st.sidebar.write(f"Condition: {weather_description}")

# 6. SENSOR INPUTS
st.header("🧪 Simulated Sensor Measurements")

col1, col2 = st.columns(2)

with col1:
    temperature = st.slider("Water Temperature (°C)", 0.0, 40.0, 25.0)
    ph = st.slider("pH", 0.0, 14.0, 7.0)
    nitrate = st.slider("Nitrate (mg/L)", 0.0, 100.0, 20.0)
    conductivity = st.slider("Conductivity (µS/cm)", 0.0, 2000.0, 500.0)

with col2:
    turbidity = st.slider("Turbidity (NTU)", 0.0, 50.0, 2.0)
    wqi = st.slider("Water Quality Index", 0.0, 300.0, 40.0)
    coliform = st.slider("Total Coliform", 0.0, 500.0, 50.0)

# 7. SCIENTIFIC ANALYSIS
score = 0
danger_reasons = []

if nitrate > 50:
    score += 3
    danger_reasons.append("Nitrate exceeds limit (50 mg/L)")
elif nitrate > 10:
    score += 1
    danger_reasons.append("Nitrate above recommended level")

if ph < 6.5 or ph > 8.5:
    score += 2
    danger_reasons.append("Unsafe pH level")

if conductivity > 1000:
    score += 2
    danger_reasons.append("High dissolved salts")
elif conductivity > 500:
    score += 1

if turbidity > 5:
    score += 2
    danger_reasons.append("High turbidity")

if coliform > 0:
    score += 3
    danger_reasons.append("Bacterial contamination")

if wqi > 100:
    score += 3
    danger_reasons.append("Poor water quality index")
elif wqi > 50:
    score += 1

if danger_reasons:
    st.warning("Detected problems:")
    for reason in danger_reasons:
        st.write("⚠️", reason)
else:
    st.success("No major contamination indicators detected")

# =========================================================
# 8. AI PREDICTION
# =========================================================
st.header("🤖 AI Prediction")

if st.button("Analyze Water Safety"):
    st.write("DEBUG - values being sent:", temperature, ph, nitrate, conductivity, turbidity, wqi, coliform)
    try:
        response = requests.post(
    "https://hydrocontam-predictor-dhav.onrender.com/predict",
    json={
        "temperature": float(temperature),
        "ph": float(ph),
        "nitrate": float(nitrate),
        "conductivity": float(conductivity),
        "turbidity": float(turbidity),
        "wqi": float(wqi),
        "coliform": float(coliform)
    },
    timeout=30  # bumped up since Render free tier can be slow to wake

        )

        response.raise_for_status()
        data = response.json()

        prediction = data["prediction"]
        probability = data["probability"] / 100  # backend returns a 0-100 percentage

    except Exception as e:
        st.error(f"Could not connect to API.\n\n{e}")
        st.stop()

    # =====================================================
    # RESULT
    # =====================================================
    is_high_risk = prediction == 1 or prediction == "High Contamination Risk"

    if is_high_risk:
        st.error(
            f"⚠️ HIGH CONTAMINATION RISK\n\n"
            f"Probability: {probability * 100:.2f}%"
        )
    else:
        st.success(
            f"✅ WATER APPEARS SAFE\n\n"
            f"Probability: {probability * 100:.2f}%"
        )

    # =====================================================
    # 9. GAUGE
    # =====================================================
    st.subheader("📊 Contamination Risk Gauge")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            title={"text": "Risk Probability (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 40], "color": "green"},
                    {"range": [40, 70], "color": "orange"},
                    {"range": [70, 100], "color": "red"}
                ]
            }
        )
    )
    st.plotly_chart(gauge, use_container_width=True)

    # =====================================================
    # 10. RADAR CHART
    # =====================================================
    categories = list(SAFE_LIMITS.keys())

    current_values = [
        temperature, ph, nitrate, conductivity, turbidity, wqi, coliform
    ]

    safe_values = [
        v.get("safe_max", v.get("safe_min", 0))
        for v in SAFE_LIMITS.values()
    ]

    radar = go.Figure()
    radar.add_trace(
        go.Scatterpolar(
            r=current_values,
            theta=categories,
            fill="toself",
            name="Current Values"
        )
    )
    radar.add_trace(
        go.Scatterpolar(
            r=safe_values,
            theta=categories,
            fill="toself",
            name="Safe Limits"
        )
    )
    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    st.plotly_chart(radar, use_container_width=True)

    # =====================================================
    # 11. BAR CHART
    # =====================================================
    compare_df = pd.DataFrame({
        "Parameter": categories,
        "Current": current_values,
        "Safe Limit": safe_values
    })

    fig = px.bar(
        compare_df,
        x="Parameter",
        y=["Current", "Safe Limit"],
        barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)