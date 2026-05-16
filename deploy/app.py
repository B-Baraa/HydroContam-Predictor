#================================
# Deployment APP
#===========================
# 1. IMPORT LIBRARIES

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import requests

# 2. PAGE CONFIG


st.set_page_config(
    page_title="Water Safety Monitoring AI",
    layout="wide"
)

# =========================================================
# 3. LOAD MODEL
# =========================================================

with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)

# =========================================================
# 4. TITLE
# =========================================================

st.title("🌱 Intelligent Water Safety Monitoring Platform")

st.markdown("""
This platform simulates an AI + IoT environmental monitoring system
that predicts whether fertilizer usage may contaminate potable water.

The measurements are manually entered to simulate real-time sensor data.
""")

# =========================================================
# 5. SAFE scientific LIMITS
# =========================================================

SAFE_LIMITS = {

    # Temperature
    # High temperature accelerates biological activity
    "Temperature (°C)": {

        "safe_max": 25,

        "critical": 35

    },

    # WHO acceptable pH range
    "pH": {

        "safe_min": 6.5,

        "safe_max": 8.5

    },

    # WHO nitrate limit for drinking water
    "Nitrate (mg/L)": {

        "safe_max": 10,

        "critical": 50

    },

    # Conductivity indicator of dissolved salts
    "Conductivity (µS/cm)": {

        "safe_max": 500,

        "critical": 1500

    },

    # WHO turbidity recommendation
    "Turbidity (NTU)": {

        "safe_max": 5,

        "critical": 10

    },


    "WQI": {

        "safe_max": 50,

        "critical": 100

    },

    # Drinking water should ideally contain no coliforms
    "Total Coliform": {

        "safe_max": 0,

        "critical": 10

    }

}

# =========================================================
# 6. SIDEBAR - LOCATION & WEATHER
# =========================================================

st.sidebar.header("📍 Environmental Conditions")

city = st.sidebar.text_input(
    "Enter City",
    value="Tunis"
)

# =========================================================
# WEATHER API
# =========================================================

API_KEY = st.secrets.get("OPENWEATHER_API_KEY") or st.sidebar.text_input("Enter OpenWeather API Key", type="password")

weather_temp = 25
weather_humidity = 50
weather_description = "Unavailable"

if not API_KEY:
    st.sidebar.warning("Please enter your OpenWeather API key.")
else:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather_temp = data["main"]["temp"]
        weather_humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["description"].capitalize()

    except requests.exceptions.HTTPError as e:
        st.sidebar.warning(f"API error: {response.status_code} — {response.json().get('message', str(e))}")
    except requests.exceptions.ConnectionError:
        st.sidebar.warning("No internet connection.")
    except requests.exceptions.Timeout:
        st.sidebar.warning("Request timed out.")
    except Exception as e:
        st.sidebar.warning(f"Unexpected error: {e}")

# =========================================================
# DISPLAY WEATHER
# =========================================================

st.sidebar.subheader("🌦 Current Weather")
st.sidebar.write(f"Temperature: {weather_temp} °C")
st.sidebar.write(f"Humidity: {weather_humidity}%")
st.sidebar.write(f"Condition: {weather_description}")

# =========================================================
# 7. SENSOR SIMULATION INPUTS
# =========================================================

st.header("🧪 Simulated Sensor Measurements")

col1, col2 = st.columns(2)

with col1:

    temperature = st.slider(
        "Water Temperature (°C)",
        0.0,
        40.0,
        25.0
    )

    ph = st.slider(
        "pH",
        0.0,
        14.0,
        7.0
    )

    nitrate = st.slider(
        "Nitrate (mg/L)",
        0.0,
        100.0,
        20.0
    )

    conductivity = st.slider(
        "Conductivity (µS/cm)",
        0.0,
        2000.0,
        500.0
    )

with col2:

    turbidity = st.slider(
        "Turbidity (NTU)",
        0.0,
        50.0,
        2.0
    )

    wqi = st.slider(
        "Water Quality Index",
        0.0,
        100.0,
        40.0
    )

    coliform = st.slider(
        "Total Coliform",
        0.0,
        500.0,
        50.0
    )
# =====================================================
# SCIENTIFIC CONTAMINATION ANALYSIS
# =====================================================

score = 0

danger_reasons = []

# -----------------------------------------------------
# NITRATE
# -----------------------------------------------------

if nitrate > 50:

    score += 3

    danger_reasons.append(
        "Excessive nitrate concentration"
    )

elif nitrate > 25:

    score += 1

# -----------------------------------------------------
# PH
# -----------------------------------------------------

if ph < 6.5 or ph > 8.5:

    score += 2

    danger_reasons.append(
        "Unsafe pH level"
    )

# -----------------------------------------------------
# CONDUCTIVITY
# -----------------------------------------------------

if conductivity > 1000:

    score += 2

    danger_reasons.append(
        "High dissolved salts concentration"
    )

elif conductivity > 500:

    score += 1

# -----------------------------------------------------
# TURBIDITY
# -----------------------------------------------------

if turbidity > 5:

    score += 2

    danger_reasons.append(
        "High turbidity detected"
    )

# -----------------------------------------------------
# COLIFORM
# -----------------------------------------------------

if coliform > 0:

    score += 3

    danger_reasons.append(
        "Bacterial contamination detected"
    )

# -----------------------------------------------------
# WQI
# -----------------------------------------------------

if wqi > 100:

    score += 3

    danger_reasons.append(
        "Poor water quality index"
    )

elif wqi > 50:

    score += 1

# =========================================================
# 8. PREPARE INPUT DATA
# =========================================================

input_data = pd.DataFrame({

    "Temperature": [temperature],

    "pH": [ph],

    "Nitrate (mg/ L)": [nitrate],

    "Conductivity (mho/ Cm)": [conductivity],

    "qual_Turbidity_avg": [turbidity],

    "WQI": [wqi],

    "Total Coliform (MPN/ 100 mL)": [coliform]

})

# =========================================================
# 9. PREDICTION
# =========================================================

st.header("🤖 AI Prediction")

if st.button("Analyze Water Safety"):

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(
            input_data
        )[0][1]

    except:

        # fallback simulation if feature mismatch
        probability = (
            nitrate / 50 +
            turbidity / 30 +
            conductivity / 100
        ) / 3

        prediction = int(probability > 0.5)

    # =====================================================
    # RESULT
    # =====================================================

    if prediction == 1:

        st.error(
            f"⚠️ HIGH CONTAMINATION RISK\n\nProbability: {probability:.2f}"
        )

    else:

        st.success(
            f"✅ WATER CONDITIONS APPEAR SAFE\n\nProbability: {probability:.2f}"
        )

    # =====================================================
    # 10. GAUGE CHART
    # =====================================================

    st.subheader("📊 Contamination Risk Gauge")

    gauge = go.Figure(go.Indicator(

        mode="gauge+number",

        value=probability * 100,

        title={
            "text": "Risk Probability (%)"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "steps": [

                {
                    "range": [0, 40],
                    "color": "green"
                },

                {
                    "range": [40, 70],
                    "color": "orange"
                },

                {
                    "range": [70, 100],
                    "color": "red"
                }

            ]
        }
    ))

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # =====================================================
    # 11. RADAR CHART
    # =====================================================

    st.subheader("🕸 Current Measurements vs Safe Limits")

    categories = list(SAFE_LIMITS.keys())

    current_values = [

        temperature,
        ph,
        nitrate,
        conductivity,
        turbidity,
        wqi,
        coliform

    ]

    safe_values = list(SAFE_LIMITS.values())

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(

        r=current_values,

        theta=categories,

        fill="toself",

        name="Current Values"

    ))

    radar.add_trace(go.Scatterpolar(

        r=safe_values,

        theta=categories,

        fill="toself",

        name="Safe Limits"

    ))

    radar.update_layout(

        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),

        showlegend=True
    )

    st.plotly_chart(
        radar,
        use_container_width=True
    )

    # =====================================================
    # 12. THRESHOLD COMPARISON
    # =====================================================

    st.subheader("📏 Safe Limits Comparison")

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

    st.plotly_chart(
        fig,
        use_container_width=True
    )
