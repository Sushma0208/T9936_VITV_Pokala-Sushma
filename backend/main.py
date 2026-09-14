from fastapi import FastAPI
from pydantic import BaseModel

import sys
import os

# Allow Python to find the agent package
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(
    os.path.join(BASE_DIR, "agent")
)

from tools import (
    predict_temperature,
    detect_anomaly,
    analyze_root_cause,
    optimize_cooling
)


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Data Center Cooling Optimization API",
    description=(
        "API for temperature prediction, anomaly detection, "
        "root-cause analysis and cooling recommendation."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Request Model
# ---------------------------------------------------------

class Telemetry(BaseModel):

    temperature: float
    cpu_utilization: float
    gpu_utilization: float
    power_consumption: float
    fan_speed: float
    airflow: float
    humidity: float
    cooling_load: float
    ambient_temperature: float

    temperature_change: float = 0.0
    workload_change: float = 0.0


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "status": "online",
        "service": "Data Center Cooling Optimization API"
    }


# ---------------------------------------------------------
# Cooling Analysis Endpoint
# ---------------------------------------------------------

@app.post("/analyze")
def analyze_cooling(telemetry: Telemetry):

    telemetry_data = telemetry.model_dump()

    # Temperature prediction
    predicted_temperature = predict_temperature(
        telemetry_data
    )

    # Anomaly detection
    anomaly_result = detect_anomaly(
        telemetry_data
    )

    # Root cause
    if anomaly_result["status"] == "anomaly":

        root_cause_result = analyze_root_cause(
            telemetry_data
        )

    else:

        root_cause_result = {
            "root_cause": "None",
            "explanation": "No thermal anomaly detected."
        }

    # Cooling optimization
    optimization_result = optimize_cooling(
        telemetry_data,
        predicted_temperature
    )

    return {

        "current_temperature":
            telemetry_data["temperature"],

        "predicted_temperature":
            predicted_temperature,

        "anomaly":
            anomaly_result,

        "root_cause":
            root_cause_result,

        "cooling_recommendation":
            optimization_result,

        "human_approval_required":
            True
    }