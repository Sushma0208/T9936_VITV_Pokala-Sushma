import os
from pyexpat import features
import joblib
import pandas as pd


# ---------------------------------------------------------
# Load trained ML models
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_MODEL_PATH = os.path.join(
    BASE_DIR, "models", "temperature_model.pkl"
)

ANOMALY_MODEL_PATH = os.path.join(
    BASE_DIR, "models", "anomaly_detection_model.pkl"
)

ANOMALY_SCALER_PATH = os.path.join(
    BASE_DIR, "models", "anomaly_scaler.pkl"
)


temperature_model = joblib.load(TEMP_MODEL_PATH)
anomaly_model = joblib.load(ANOMALY_MODEL_PATH)
anomaly_scaler = joblib.load(ANOMALY_SCALER_PATH)


# ---------------------------------------------------------
# Tool 1: Temperature Prediction
# ---------------------------------------------------------

def predict_temperature(telemetry: dict) -> float:

    total_workload = (
        telemetry["cpu_utilization"]
        + telemetry["gpu_utilization"]
    ) / 2

    heat_load = (
        telemetry["power_consumption"]
        * total_workload
        / 100
    )

    data = pd.DataFrame([{
        "temperature": telemetry["temperature"],
        "cpu_utilization": telemetry["cpu_utilization"],
        "gpu_utilization": telemetry["gpu_utilization"],
        "power_consumption": telemetry["power_consumption"],
        "fan_speed": telemetry["fan_speed"],
        "airflow": telemetry["airflow"],
        "humidity": telemetry["humidity"],
        "cooling_load": telemetry["cooling_load"],
        "ambient_temperature": telemetry["ambient_temperature"],
        "total_workload": total_workload,
        "heat_load": heat_load,
        "temperature_change": telemetry.get(
            "temperature_change", 0.0
        ),
        "workload_change": telemetry.get(
            "workload_change", 0.0
        )
    }])

    predicted_temperature = temperature_model.predict(data)[0]

    return round(float(predicted_temperature), 2)


# ---------------------------------------------------------
# Tool 2: Anomaly Detection
# ---------------------------------------------------------

def detect_anomaly(telemetry: dict) -> dict:
    

    features = pd.DataFrame([{
    "temperature": telemetry["temperature"],
    "cpu_utilization": telemetry["cpu_utilization"],
    "gpu_utilization": telemetry["gpu_utilization"],
    "power_consumption": telemetry["power_consumption"],
    "fan_speed": telemetry["fan_speed"],
    "airflow": telemetry["airflow"],
    "humidity": telemetry["humidity"],
    "cooling_load": telemetry["cooling_load"],
    "ambient_temperature": telemetry["ambient_temperature"]
}])

    scaled_features = anomaly_scaler.transform(features)

    prediction = anomaly_model.predict(scaled_features)[0]
    score = anomaly_model.decision_function(scaled_features)[0]

    if prediction == -1:
        status = "anomaly"

        if score < -0.15:
            severity = "critical"
        elif score < -0.05:
            severity = "high"
        else:
            severity = "medium"

    else:
        status = "normal"
        severity = "normal"

    return {
        "status": status,
        "severity": severity,
        "score": round(float(score), 4)
    }


# ---------------------------------------------------------
# Tool 3: Root Cause Analysis
# ---------------------------------------------------------

def analyze_root_cause(telemetry: dict) -> dict:

    temperature = telemetry["temperature"]
    cpu = telemetry["cpu_utilization"]
    gpu = telemetry["gpu_utilization"]
    power = telemetry["power_consumption"]
    fan = telemetry["fan_speed"]
    airflow = telemetry["airflow"]
    cooling = telemetry["cooling_load"]

    if fan < 40 and airflow < 55:

        cause = "Fan failure"

        explanation = (
            "Fan speed is low and airflow is reduced, "
            "indicating a possible cooling fan failure."
        )

    elif airflow < 55 and fan >= 40:

        cause = "Reduced airflow"

        explanation = (
            "Airflow is below the expected level while "
            "fan speed remains active."
        )

    elif (cpu > 80 or gpu > 80) and power > 400:

        cause = "High computational workload"

        explanation = (
            "High CPU/GPU utilization combined with "
            "high power consumption is increasing heat generation."
        )

    elif cooling < 35 and temperature > 29:

        cause = "Insufficient cooling"

        explanation = (
            "Cooling load is relatively low while temperature "
            "is elevated."
        )

    elif temperature >= 32:

        cause = "Thermal overload"

        explanation = (
            "Temperature has reached a critical thermal level."
        )

    else:

        cause = "Unclassified thermal anomaly"

        explanation = (
            "The telemetry indicates abnormal behavior, "
            "but no specific root cause rule was triggered."
        )

    return {
        "root_cause": cause,
        "explanation": explanation
    }


# ---------------------------------------------------------
# Tool 4: Cooling Optimization
# ---------------------------------------------------------

def optimize_cooling(
    telemetry: dict,
    predicted_temperature: float
) -> dict:

    SAFE_TEMPERATURE = 30.0

    current_fan = telemetry["fan_speed"]

    if predicted_temperature < 28:

        action = "No change"
        energy_impact = "Minimum"

    elif predicted_temperature < 30:

        action = "Fan +5%"
        energy_impact = "Low"

    elif predicted_temperature < 31:

        action = "Fan +10%"
        energy_impact = "Moderate"

    elif predicted_temperature < 32:

        action = "Cooling +10%"
        energy_impact = "High"

    else:

        action = "Cooling +15%"
        energy_impact = "Very High"

    return {
        "recommended_action": action,
        "energy_impact": energy_impact,
        "safe_temperature_limit": SAFE_TEMPERATURE,
        "current_fan_speed": current_fan
    }