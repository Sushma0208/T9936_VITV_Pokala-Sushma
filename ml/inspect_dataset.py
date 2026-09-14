import pandas as pd
from pathlib import Path


# Dataset path
DATASET_PATH = Path("data/processed/telemetry_dataset.csv")


# Check whether dataset exists
if not DATASET_PATH.exists():
    raise FileNotFoundError(
        "Dataset not found. Run simulator/telemetry_generator.py first."
    )


# Load dataset
df = pd.read_csv(DATASET_PATH)


print("\n========== DATASET INFORMATION ==========")

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Column Names:")
for column in df.columns:
    print("-", column)

print("\n3. First 5 Rows:")
print(df.head())

print("\n4. Data Types:")
print(df.dtypes)

print("\n5. Missing Values:")
print(df.isnull().sum())


print("\n========== NUMERICAL RANGES ==========")

columns_to_check = [
    "temperature",
    "cpu_utilization",
    "gpu_utilization",
    "power_consumption",
    "fan_speed",
    "airflow",
    "humidity",
    "cooling_load",
    "ambient_temperature",
    "energy_cost"
]

for column in columns_to_check:
    print(
        f"{column}: "
        f"Min = {df[column].min():.2f}, "
        f"Max = {df[column].max():.2f}, "
        f"Mean = {df[column].mean():.2f}"
    )


print("\n========== SCENARIO DISTRIBUTION ==========")

print(df["scenario"].value_counts())


print("\n========== TEMPERATURE BY SCENARIO ==========")

print(
    df.groupby("scenario")["temperature"]
    .agg(["mean", "min", "max"])
    .round(2)
)


print("\n========== VALIDATION COMPLETE ==========")