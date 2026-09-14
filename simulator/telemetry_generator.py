import csv
import random
import math
from datetime import datetime, timedelta
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

NUM_RACKS = 5
RECORDS_PER_RACK = 500

OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "telemetry_dataset.csv"


# --------------------------------------------------
# Telemetry Generator
# --------------------------------------------------

def generate_telemetry():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    start_time = datetime.now().replace(
        second=0,
        microsecond=0
    )

    rows = []

    for rack_number in range(1, NUM_RACKS + 1):

        rack_id = f"R{rack_number:02d}"

        # Each rack has slightly different characteristics
        base_temperature = random.uniform(23, 25)
        temperature = base_temperature

        rack_factor = random.uniform(0.9, 1.1)

        for i in range(RECORDS_PER_RACK):

            timestamp = start_time + timedelta(
                minutes=i
            )

            # --------------------------------------------------
            # Time-based workload pattern
            # --------------------------------------------------

            daily_pattern = (
                15
                * math.sin(
                    2 * math.pi * i / 180
                )
            )

            cpu = (
                50
                + daily_pattern
                + random.gauss(0, 8)
            )

            gpu = (
                40
                + daily_pattern * 0.8
                + random.gauss(0, 10)
            )

            cpu = max(5, min(100, cpu))
            gpu = max(0, min(100, gpu))


            # --------------------------------------------------
            # Abnormal scenarios
            # --------------------------------------------------

            scenario = "normal"

            # Different timing for each rack
            offset = rack_number * 20

            # High workload
            if 100 + offset <= i < 140 + offset:

                cpu = random.uniform(80, 98)
                gpu = random.uniform(75, 95)

                scenario = "high_workload"


            # Fan degradation
            elif 220 + offset <= i < 255 + offset:

                cpu = random.uniform(60, 80)
                gpu = random.uniform(50, 75)

                scenario = "fan_failure"


            # Reduced airflow
            elif 320 + offset <= i < 355 + offset:

                cpu = random.uniform(65, 85)
                gpu = random.uniform(60, 85)

                scenario = "reduced_airflow"


            # Cooling reduction
            elif 410 + offset <= i < 440 + offset:

                cpu = random.uniform(70, 90)
                gpu = random.uniform(65, 90)

                scenario = "cooling_reduction"


            # --------------------------------------------------
            # Ambient conditions
            # --------------------------------------------------

            ambient_temperature = (
                30
                + 3 * math.sin(
                    2 * math.pi * i / 300
                )
                + random.gauss(0, 0.5)
            )

            humidity = (
                50
                + random.gauss(0, 4)
            )

            humidity = max(
                30,
                min(70, humidity)
            )


            # --------------------------------------------------
            # Fan speed
            # --------------------------------------------------

            if scenario == "fan_failure":

                fan_speed = random.uniform(
                    15,
                    35
                )

            elif scenario == "reduced_airflow":

                fan_speed = random.uniform(
                    45,
                    60
                )

            elif scenario == "cooling_reduction":

                fan_speed = random.uniform(
                    40,
                    55
                )

            else:

                # Fan responds partially to workload
                fan_speed = (
                    50
                    + cpu * 0.15
                    + random.gauss(0, 3)
                )

                fan_speed = max(
                    40,
                    min(90, fan_speed)
                )


            # --------------------------------------------------
            # Power consumption
            # --------------------------------------------------

            power = (
                180
                + cpu * 2.2
                + gpu * 2.8
                + random.gauss(0, 15)
            )

            power *= rack_factor

            power = max(
                150,
                power
            )


            # --------------------------------------------------
            # Airflow
            # --------------------------------------------------

            airflow = (
                fan_speed * 0.95
                + random.gauss(0, 4)
            )

            if scenario == "reduced_airflow":

                airflow *= random.uniform(
                    0.45,
                    0.65
                )

            elif scenario == "fan_failure":

                airflow *= random.uniform(
                    0.35,
                    0.55
                )

            airflow = max(
                15,
                min(100, airflow)
            )


            # --------------------------------------------------
            # Cooling load
            # --------------------------------------------------

            cooling_load = (
                25
                + power * 0.08
                - fan_speed * 0.12
                + random.gauss(0, 3)
            )

            if scenario == "cooling_reduction":

                cooling_load *= 0.65

            cooling_load = max(
                10,
                min(100, cooling_load)
            )


            # --------------------------------------------------
            # Thermal behavior
            # --------------------------------------------------

            heat_generation = (
                power * 0.012
            )

            cooling_effect = (
                airflow * 0.018
                + cooling_load * 0.025
            )

            ambient_effect = (
                ambient_temperature
                - 30
            ) * 0.04

            workload_effect = (
                cpu * 0.002
                + gpu * 0.0025
            )


            # Temperature changes gradually
            temperature_change = (
                heat_generation
                - cooling_effect
                + ambient_effect
                + workload_effect
                + random.gauss(0, 0.08)
            )


            # Thermal inertia
            temperature = (
                temperature * 0.92
                + (
                    temperature
                    + temperature_change
                ) * 0.08
            )


            # Additional abnormal temperature effect
            if scenario == "fan_failure":

                temperature += random.uniform(
                    0.05,
                    0.15
                )

            elif scenario == "reduced_airflow":

                temperature += random.uniform(
                    0.03,
                    0.12
                )

            elif scenario == "cooling_reduction":

                temperature += random.uniform(
                    0.04,
                    0.12
                )


            # Keep temperature realistic
            temperature = max(
                21,
                min(38, temperature)
            )


            # --------------------------------------------------
            # Energy cost
            # --------------------------------------------------

            energy_cost = (
                power * 0.01
                + cooling_load * 0.06
                + random.gauss(0, 0.5)
            )

            energy_cost = max(
                0,
                energy_cost
            )


            # --------------------------------------------------
            # Store record
            # --------------------------------------------------

            rows.append({

                "timestamp":
                    timestamp.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "rack_id":
                    rack_id,

                "temperature":
                    round(
                        temperature,
                        2
                    ),

                "cpu_utilization":
                    round(
                        cpu,
                        2
                    ),

                "gpu_utilization":
                    round(
                        gpu,
                        2
                    ),

                "power_consumption":
                    round(
                        power,
                        2
                    ),

                "fan_speed":
                    round(
                        fan_speed,
                        2
                    ),

                "airflow":
                    round(
                        airflow,
                        2
                    ),

                "humidity":
                    round(
                        humidity,
                        2
                    ),

                "cooling_load":
                    round(
                        cooling_load,
                        2
                    ),

                "ambient_temperature":
                    round(
                        ambient_temperature,
                        2
                    ),

                "energy_cost":
                    round(
                        energy_cost,
                        2
                    ),

                "scenario":
                    scenario
            })


    # --------------------------------------------------
    # Save CSV
    # --------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        fieldnames = rows[0].keys()

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)


    print(
        "\nTelemetry dataset generated successfully!"
    )

    print(
        f"File: {OUTPUT_FILE}"
    )

    print(
        f"Total records: {len(rows)}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    generate_telemetry()