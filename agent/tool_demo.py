from tools import (
    predict_temperature,
    detect_anomaly,
    analyze_root_cause,
    optimize_cooling
)


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


print("\n--- TEMPERATURE PREDICTION ---")

predicted_temperature = predict_temperature(telemetry)

print(
    "Predicted Temperature:",
    predicted_temperature,
    "°C"
)


print("\n--- ANOMALY DETECTION ---")

anomaly = detect_anomaly(telemetry)

print(anomaly)


print("\n--- ROOT CAUSE ANALYSIS ---")

root_cause = analyze_root_cause(telemetry)

print(root_cause)


print("\n--- COOLING OPTIMIZATION ---")

optimization = optimize_cooling(
    telemetry,
    predicted_temperature
)

print(optimization)


print("\nALL TOOLS EXECUTED SUCCESSFULLY")