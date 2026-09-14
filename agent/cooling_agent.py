from langchain_ollama import ChatOllama

from tools import (
    predict_temperature,
    detect_anomaly,
    analyze_root_cause,
    optimize_cooling
)


# ---------------------------------------------------------
# Single Local AI Agent
# ---------------------------------------------------------

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# ---------------------------------------------------------
# Telemetry Input
# ---------------------------------------------------------

telemetry = {
    "temperature": 30.5,
    "cpu_utilization": 85,
    "gpu_utilization": 78,
    "power_consumption": 520,
    "fan_speed": 45,
    "airflow": 50,
    "humidity": 55,
    "cooling_load": 40,
    "ambient_temperature": 26,
    "temperature_change": 0.4,
    "workload_change": 5
}


# ---------------------------------------------------------
# Agent Tool Orchestration
# ---------------------------------------------------------

print("\n========================================")
print("DATA CENTER COOLING AGENT")
print("========================================")

print("\n[1] Analyzing telemetry...")


# Temperature prediction
predicted_temperature = predict_temperature(telemetry)

print(
    f"Predicted temperature: "
    f"{predicted_temperature} °C"
)


# Anomaly detection
anomaly_result = detect_anomaly(telemetry)

print(
    f"Anomaly status: "
    f"{anomaly_result['status']}"
)

print(
    f"Anomaly severity: "
    f"{anomaly_result['severity']}"
)


# Root cause analysis
if anomaly_result["status"] == "anomaly":

    root_cause_result = analyze_root_cause(
        telemetry
    )

else:

    root_cause_result = {
        "root_cause": "None",
        "explanation": "No thermal anomaly detected."
    }


print(
    f"Root cause: "
    f"{root_cause_result['root_cause']}"
)


# Cooling optimization
optimization_result = optimize_cooling(
    telemetry,
    predicted_temperature
)


print(
    f"Recommended action: "
    f"{optimization_result['recommended_action']}"
)


# ---------------------------------------------------------
# Prepare Results for Local LLM
# ---------------------------------------------------------

analysis = f"""
You are the decision-support component of a
Data Center Cooling Optimization System.

Analyze the following telemetry and tool results.

TELEMETRY:
{telemetry}

TEMPERATURE PREDICTION:
Predicted temperature = {predicted_temperature} °C

ANOMALY DETECTION:
Status = {anomaly_result['status']}
Severity = {anomaly_result['severity']}
Score = {anomaly_result['score']}

ROOT CAUSE:
{root_cause_result['root_cause']}
Explanation = {root_cause_result['explanation']}

COOLING OPTIMIZATION:
Recommended action = {optimization_result['recommended_action']}
Energy impact = {optimization_result['energy_impact']}
Safe temperature limit = {optimization_result['safe_temperature_limit']} °C

Prepare a concise professional recommendation.

Include exactly these sections:

1. Current Temperature
2. Predicted Temperature
3. Anomaly Status
4. Anomaly Severity
5. Probable Root Cause
6. Recommended Cooling Action
7. Energy Impact
8. Explanation
9. Human Approval

Do not change or invent any values from the
tool results.

The system is a recommendation system.
It must not directly control physical cooling equipment.
Human approval is required before implementing
the recommended action.
"""


# ---------------------------------------------------------
# Local LLM Reasoning / Explanation
# ---------------------------------------------------------

print("\n[2] Local AI agent is generating explanation...")

response = llm.invoke(analysis)


# ---------------------------------------------------------
# Final Result
# ---------------------------------------------------------

print("\n========================================")
print("AGENT RECOMMENDATION")
print("========================================")

print(response.content)

print("\n========================================")
print("ANALYSIS COMPLETE")
print("========================================")
