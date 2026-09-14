import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SAFE_TEMPERATURE = 30.0

INPUT_FILE = Path(
    "data/processed/diagnosis_results.csv"
)

OUTPUT_FILE = Path(
    "data/processed/optimization_results.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

print("Loading diagnosis results...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Records loaded: {len(df)}"
)


# --------------------------------------------------
# Optimization function
# --------------------------------------------------

def optimize_cooling(row):

    predicted_temperature = (
        row["future_temperature_10min"]
    )

    current_temperature = (
        row["temperature"]
    )

    fan_speed = row["fan_speed"]

    cooling_load = row["cooling_load"]

    airflow = row["airflow"]


    # --------------------------------------------------
    # Candidate actions
    # --------------------------------------------------

    actions = [

        {
            "name": "No change",
            "temperature_reduction": 0.0,
            "energy_penalty": 0.0
        },

        {
            "name": "Increase fan by 5%",
            "temperature_reduction": 0.25,
            "energy_penalty": 2.5
        },

        {
            "name": "Increase fan by 10%",
            "temperature_reduction": 0.50,
            "energy_penalty": 5.0
        },

        {
            "name": "Increase cooling by 10%",
            "temperature_reduction": 0.70,
            "energy_penalty": 10.0
        },

        {
            "name": "Increase cooling by 15%",
            "temperature_reduction": 1.00,
            "energy_penalty": 15.0
        }
    ]


    candidates = []


    # --------------------------------------------------
    # Evaluate each action
    # --------------------------------------------------

    for action in actions:

        estimated_temperature = (
            predicted_temperature
            - action["temperature_reduction"]
        )

        candidates.append({

            "action":
                action["name"],

            "estimated_temperature":
                estimated_temperature,

            "energy_penalty":
                action["energy_penalty"]
        })


    # --------------------------------------------------
    # Determine whether intervention is required
    # --------------------------------------------------

    # Comfortable temperature
    if predicted_temperature < 28:

        best = candidates[0]


    # Mild thermal risk
    elif predicted_temperature < 30:

        # Prefer the lowest-energy action
        # that keeps temperature comfortable

        safe = [
            c for c in candidates
            if c["estimated_temperature"] <= 30
        ]

        best = min(
            safe,
            key=lambda x: x["energy_penalty"]
        ) if safe else candidates[1]


    # Moderate thermal risk
    elif predicted_temperature < 32:

        safe = [
            c for c in candidates
            if c["estimated_temperature"] <= 30
        ]

        if safe:

            best = min(
                safe,
                key=lambda x:
                x["energy_penalty"]
            )

        else:

            best = candidates[3]


    # Critical thermal risk
    else:

        best = candidates[4]


    return pd.Series({

        "predicted_temperature":
            round(
                predicted_temperature,
                2
            ),

        "recommended_action":
            best["action"],

        "estimated_temperature_after_action":
            round(
                best[
                    "estimated_temperature"
                ],
                2
            ),

        "energy_penalty":
            best[
                "energy_penalty"
            ]
    })


# --------------------------------------------------
# Run optimization
# --------------------------------------------------

print(
    "\nRunning cooling optimization..."
)


results = df.apply(
    optimize_cooling,
    axis=1
)


df = pd.concat(
    [
        df,
        results
    ],
    axis=1
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print(
    "\n========== RECOMMENDED ACTIONS =========="
)

print(
    df[
        "recommended_action"
    ].value_counts()
)


print(
    "\n========== SAMPLE OPTIMIZATION RESULTS =========="
)


columns = [

    "rack_id",

    "temperature",

    "predicted_temperature",

    "fan_speed",

    "airflow",

    "cooling_load",

    "recommended_action",

    "estimated_temperature_after_action",

    "energy_penalty"
]


print(
    df[
        columns
    ]
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
    "\nOptimization results saved to:"
)

print(
    OUTPUT_FILE
)


print(
    "\n========== COOLING OPTIMIZATION COMPLETE =========="
)