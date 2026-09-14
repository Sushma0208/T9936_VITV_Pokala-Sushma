import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/cleaned_telemetry.csv"
)

MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "temperature_model.pkl"


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort chronologically
df = df.sort_values(
    by=["timestamp", "rack_id"]
).reset_index(drop=True)

print(f"Dataset records: {len(df)}")


# --------------------------------------------------
# Features
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
    "ambient_temperature",
    "total_workload",
    "heat_load",
    "temperature_change",
    "workload_change"
]

target = "future_temperature_10min"


X = df[features]
y = df[target]


# --------------------------------------------------
# Chronological train-test split
# --------------------------------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\n========== DATA SPLIT ==========")

print("Training records:", len(X_train))
print("Testing records :", len(X_test))

print(
    "Training period:",
    df["timestamp"].iloc[0],
    "to",
    df["timestamp"].iloc[split_index - 1]
)

print(
    "Testing period :",
    df["timestamp"].iloc[split_index],
    "to",
    df["timestamp"].iloc[-1]
)


# --------------------------------------------------
# Create XGBoost model
# --------------------------------------------------

print("\nTraining XGBoost model...")


model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)


# --------------------------------------------------
# Train
# --------------------------------------------------

model.fit(
    X_train,
    y_train
)

print("Training complete!")


# --------------------------------------------------
# Prediction
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


print("\n========== MODEL PERFORMANCE ==========")

print(f"MAE  : {mae:.3f} °C")
print(f"RMSE : {rmse:.3f} °C")
print(f"R²   : {r2:.3f}")

print("========================================")


# --------------------------------------------------
# Feature importance
# --------------------------------------------------

print("\n========== FEATURE IMPORTANCE ==========")

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print(
    importance.to_string(index=False)
)


# --------------------------------------------------
# Save model
# --------------------------------------------------

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

print("\nModel saved successfully!")

print(
    f"Model location: {MODEL_FILE}"
)