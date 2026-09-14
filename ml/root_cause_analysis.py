import pandas as pd
from pathlib import Path


# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/anomaly_results.csv"
)

OUTPUT_FILE = Path(
    "data/processed/diagnosis_results.csv"
)


# --------------------------------------------------
# Load anomaly results
# --------------------------------------------------

print("Loading anomaly results...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Records loaded: {len(df)}"
)


# --------------------------------------------------
# Root-cause analysis function
# --------------------------------------------------

def identify_root_cause(row):

    temperature = row["temperature"]
    cpu = row["cpu_utilization"]
    gpu = row["gpu_utilization"]
    power = row["power_consumption"]
    fan = row["fan_speed"]
    airflow = row["airflow"]
    cooling = row["cooling_load"]

    # --------------------------------------------------
    # Normal condition
    # --------------------------------------------------

    if row["anomaly_status"] == "normal":

        return (
            "Normal operation",
            "No significant abnormal behavior detected"
        )


    # --------------------------------------------------
    # Fan failure
    # --------------------------------------------------

    if fan < 40 and airflow < 55:

        return (
            "Possible fan failure",
            "Low fan speed is associated with reduced airflow"
        )


    # --------------------------------------------------
    # Reduced airflow
    # --------------------------------------------------

    if airflow < 55 and fan >= 40:

        return (
            "Reduced airflow",
            "Airflow is low despite the fan operating"
        )


    # --------------------------------------------------
    # High workload
    # --------------------------------------------------

    if cpu > 80 or gpu > 80:

        if power > 400:

            return (
                "High computational workload",
                "High CPU/GPU utilization is associated with increased power consumption"
            )


    # --------------------------------------------------
    # Cooling reduction
    # --------------------------------------------------

    if cooling < 35 and temperature > 29:

        return (
            "Insufficient cooling",
            "Cooling load is low while rack temperature is elevated"
        )


    # --------------------------------------------------
    # High temperature
    # --------------------------------------------------

    if temperature >= 32:

        return (
            "Thermal overload",
            "Rack temperature has reached a critical level"
        )


    # --------------------------------------------------
    # General anomaly
    # --------------------------------------------------

    return (
        "Unclassified thermal anomaly",
        "Sensor values show abnormal behavior but no single dominant cause was identified"
    )


# --------------------------------------------------
# Apply root-cause analysis
# --------------------------------------------------

print("\nRunning root-cause analysis...")

results = df.apply(
    identify_root_cause,
    axis=1
)


df["root_cause"] = [
    result[0]
    for result in results
]

df["diagnostic_explanation"] = [
    result[1]
    for result in results
]


# --------------------------------------------------
# Display results
# --------------------------------------------------

print(
    "\n========== ROOT-CAUSE DISTRIBUTION =========="
)

print(
    df["root_cause"].value_counts()
)


print(
    "\n========== SAMPLE DIAGNOSES =========="
)

columns = [
    "rack_id",
    "temperature",
    "cpu_utilization",
    "gpu_utilization",
    "fan_speed",
    "airflow",
    "cooling_load",
    "anomaly_status",
    "root_cause"
]

print(
    df[columns]
    .head(20)
    .to_string(index=False)
)


# --------------------------------------------------
# Save results
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print(
    "\nDiagnosis results saved to:"
)

print(
    OUTPUT_FILE
)


print(
    "\n========== ROOT-CAUSE ANALYSIS COMPLETE =========="
)