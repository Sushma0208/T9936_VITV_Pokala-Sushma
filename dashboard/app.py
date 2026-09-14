import os
import requests
import streamlit as st
import pandas as pd

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/analyze"
)

st.set_page_config(
    page_title="Data Center Cooling Agent",
    page_icon="❄️",
    layout="wide"
)


st.title("❄️ Data Center Cooling Optimization Agent")
st.caption(
    "Agentic AI-based thermal anomaly detection and cooling decision support"
)

st.divider()


# ---------------------------------------------------------
# TELEMETRY INPUT
# ---------------------------------------------------------

st.subheader("📡 Data Center Telemetry")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=60.0,
        value=30.5,
        step=0.1
    )

    cpu_utilization = st.slider(
        "CPU Utilization (%)",
        0,
        100,
        85
    )

    gpu_utilization = st.slider(
        "GPU Utilization (%)",
        0,
        100,
        78
    )

    power_consumption = st.number_input(
        "Power Consumption (W)",
        min_value=0.0,
        value=520.0,
        step=10.0
    )


with col2:
    fan_speed = st.slider(
        "Fan Speed (%)",
        0,
        100,
        45
    )

    airflow = st.number_input(
        "Airflow",
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    humidity = st.slider(
        "Humidity (%)",
        0,
        100,
        55
    )

    cooling_load = st.slider(
        "Cooling Load (%)",
        0,
        100,
        40
    )


with col3:
    ambient_temperature = st.number_input(
        "Ambient Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=26.0,
        step=0.1
    )

    temperature_change = st.number_input(
        "Temperature Change",
        value=0.4,
        step=0.1
    )

    workload_change = st.number_input(
        "Workload Change",
        value=5.0,
        step=1.0
    )


st.divider()


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

if st.button("🔍 Analyze Cooling Conditions", type="primary"):

    telemetry = {
        "temperature": temperature,
        "cpu_utilization": cpu_utilization,
        "gpu_utilization": gpu_utilization,
        "power_consumption": power_consumption,
        "fan_speed": fan_speed,
        "airflow": airflow,
        "humidity": humidity,
        "cooling_load": cooling_load,
        "ambient_temperature": ambient_temperature,
        "temperature_change": temperature_change,
        "workload_change": workload_change
    }

    try:
        response = requests.post(
            API_URL,
            json=telemetry,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        st.session_state["analysis_result"] = result

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to FastAPI. "
            "Make sure the Uvicorn server is running."
        )

    except requests.exceptions.RequestException as error:
        st.error(f"❌ API request failed: {error}")


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]

    st.divider()
    st.subheader("🧠 Agent Analysis")

    # Main metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Temperature",
            f"{result['current_temperature']:.2f} °C"
        )

    with col2:
        st.metric(
            "Predicted Temperature",
            f"{result['predicted_temperature']:.2f} °C"
        )

    with col3:
        anomaly = result["anomaly"]

        st.metric(
            "Anomaly Status",
            anomaly["status"].upper()
        )


    # Anomaly information
    st.subheader("🚨 Anomaly Detection")

    anomaly = result["anomaly"]

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Status:**", anomaly["status"])
        st.write("**Severity:**", anomaly["severity"])
        st.write("**Anomaly Score:**", anomaly["score"])

    with col2:
        if anomaly["severity"].lower() == "critical":
            st.error("🔴 CRITICAL THERMAL CONDITION")

        elif anomaly["severity"].lower() == "high":
            st.warning("🟠 HIGH THERMAL RISK")

        elif anomaly["severity"].lower() == "medium":
            st.warning("🟡 MEDIUM THERMAL RISK")

        else:
            st.success("🟢 NORMAL CONDITION")


    # Root cause
    st.subheader("🔍 Root Cause Analysis")

    root_cause = result["root_cause"]

    st.info(
        f"**Probable Root Cause:** {root_cause['root_cause']}\n\n"
        f"{root_cause['explanation']}"
    )


    # Cooling recommendation
    st.subheader("💡 Cooling Optimization")

    recommendation = result["cooling_recommendation"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Recommended Action**")
        st.success(
            recommendation["recommended_action"]
        )

    with col2:
        st.write("**Energy Impact**")
        st.warning(
            recommendation["energy_impact"]
        )

    with col3:
        st.write("**Safe Temperature Limit**")
        st.metric(
            "Limit",
            f"{recommendation['safe_temperature_limit']:.1f} °C"
        )


    # Human approval
    st.subheader("🛡 Human Approval")

    if result["human_approval_required"]:

        st.warning(
            "Human approval is required before applying the recommended "
            "cooling action."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Approve Recommendation"):
                st.success(
                    "Recommendation approved by operator."
                )

        with col2:
            if st.button("❌ Reject Recommendation"):
                st.error(
                    "Recommendation rejected by operator."
                )

    else:
        st.success(
            "No human approval is required."
        )


st.divider()

st.caption(
    "Decision-support system only — does not directly control physical "
    "data-center cooling infrastructure."
)