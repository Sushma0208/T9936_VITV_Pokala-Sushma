import pandas as pd
from pathlib import Path


# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_FILE = Path("data/processed/telemetry_dataset.csv")
OUTPUT_FILE = Path("data/processed/cleaned_telemetry.csv")


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original records: {len(df)}")


# --------------------------------------------------
# Convert timestamp
# --------------------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])


# --------------------------------------------------
# Sort data
# --------------------------------------------------

df = df.sort_values(
    by=["rack_id", "timestamp"]
).reset_index(drop=True)


# --------------------------------------------------
# Remove duplicate records
# --------------------------------------------------

duplicates = df.duplicated().sum()

print(f"Duplicate records: {duplicates}")

df = df.drop_duplicates()


# --------------------------------------------------
# Handle missing values
# --------------------------------------------------

print("\nMissing values before cleaning:")
print(df.isnull().sum())

numeric_columns = df.select_dtypes(
    include=["number"]
).columns

df[numeric_columns] = df[numeric_columns].interpolate(
    method="linear"
)

df[numeric_columns] = df[numeric_columns].fillna(
    df[numeric_columns].median()
)


# --------------------------------------------------
# Feature engineering
# --------------------------------------------------

# Workload
df["total_workload"] = (
    df["cpu_utilization"] * 0.5
    + df["gpu_utilization"] * 0.5
)


# Heat load indicator
df["heat_load"] = (
    df["power_consumption"]
    * df["total_workload"]
    / 100
)


# Temperature change
df["temperature_change"] = (
    df.groupby("rack_id")["temperature"]
    .diff()
)


# Workload change
df["workload_change"] = (
    df.groupby("rack_id")["total_workload"]
    .diff()
)


# Fill first-row NaN values created by diff()
df["temperature_change"] = (
    df["temperature_change"].fillna(0)
)

df["workload_change"] = (
    df["workload_change"].fillna(0)
)


# --------------------------------------------------
# Create future temperature target
# --------------------------------------------------

# Since records are generated every minute,
# shift by 10 = temperature 10 minutes in the future.

df["future_temperature_10min"] = (
    df.groupby("rack_id")["temperature"]
    .shift(-10)
)


# Remove rows where future temperature is unavailable
df = df.dropna(
    subset=["future_temperature_10min"]
)


# --------------------------------------------------
# Save cleaned dataset
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Final information
# --------------------------------------------------

print("\n========== PREPROCESSING COMPLETE ==========")

print(f"Final records: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nNew features created:")

print("- total_workload")
print("- heat_load")
print("- temperature_change")
print("- workload_change")
print("- future_temperature_10min")

print(f"\nSaved dataset:")
print(OUTPUT_FILE)

print("\nFinal dataset preview:")
print(df.head())

print("\n=============================================")