import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/cleaned_telemetry.csv"
)

MODEL_DIR = Path("models")

MODEL_FILE = (
    MODEL_DIR / "anomaly_detection_model.pkl"
)

SCALER_FILE = (
    MODEL_DIR / "anomaly_scaler.pkl"
)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Dataset records: {len(df)}"
)


# --------------------------------------------------
# Features used for anomaly detection
# --------------------------------------------------

features = [
    "temperature",
    "cpu_utilization",
    "gpu_utilization",
    "power_consumption",
    "fan_speed",
    "airflow",
    "humidity",
    "cooling_load",
    "ambient_temperature"
]


X = df[features].copy()


print("\nFeatures used for anomaly detection:")

for feature in features:
    print("-", feature)


# --------------------------------------------------
# Feature scaling
# --------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# --------------------------------------------------
# Isolation Forest
# --------------------------------------------------

print("\nTraining Isolation Forest...")

model = IsolationForest(
    n_estimators=200,
    contamination=0.10,
    random_state=42
)

model.fit(X_scaled)


print("Training complete!")


# --------------------------------------------------
# Predict anomalies
# --------------------------------------------------

predictions = model.predict(X_scaled)

scores = model.decision_function(
    X_scaled
)


# Isolation Forest:
#  1  = normal
# -1  = anomaly

df["anomaly_prediction"] = predictions

df["anomaly_score"] = scores


df["anomaly_status"] = df[
    "anomaly_prediction"
].map({
    1: "normal",
    -1: "anomaly"
})


# --------------------------------------------------
# Determine anomaly severity
# --------------------------------------------------

def determine_severity(row):

    if row["anomaly_status"] == "normal":
        return "normal"

    temperature = row["temperature"]

    if temperature >= 32:
        return "critical"

    elif temperature >= 29:
        return "high"

    else:
        return "medium"


df["anomaly_severity"] = df.apply(
    determine_severity,
    axis=1
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n========== ANOMALY RESULTS ==========")

print(
    df["anomaly_status"].value_counts()
)


print("\n========== ANOMALY SEVERITY ==========")

print(
    df["anomaly_severity"].value_counts()
)


# --------------------------------------------------
# Compare with simulator scenarios
# --------------------------------------------------

print(
    "\n========== SCENARIO vs ANOMALY =========="
)

comparison = pd.crosstab(
    df["scenario"],
    df["anomaly_status"]
)

print(comparison)


# --------------------------------------------------
# Save results
# --------------------------------------------------

OUTPUT_FILE = Path(
    "data/processed/anomaly_results.csv"
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Save model and scaler
# --------------------------------------------------

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    scaler,
    SCALER_FILE
)


print("\nModels saved successfully!")

print(
    f"Anomaly model: {MODEL_FILE}"
)

print(
    f"Scaler: {SCALER_FILE}"
)

print(
    f"Results: {OUTPUT_FILE}"
)


print(
    "\n========== ANOMALY DETECTION COMPLETE =========="
)