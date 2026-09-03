import random
from datetime import datetime

def generate_telemetry(rack_id):
    cpu = random.uniform(20, 80)
    gpu = random.uniform(20, 80)
    temperature = random.uniform(22, 27)
    humidity = random.uniform(40, 60)
    power = random.uniform(300, 600)
    fan_speed = random.uniform(40, 70)
    airflow = random.uniform(70, 90)
    cooling_load = random.uniform(40, 70)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rack_id": rack_id,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "cpu_utilization": round(cpu, 2),
        "gpu_utilization": round(gpu, 2),
        "power_consumption": round(power, 2),
        "fan_speed": round(fan_speed, 2),
        "airflow": round(airflow, 2),
        "cooling_load": round(cooling_load, 2),
    }


if __name__ == "__main__":
    for rack in range(1, 6):
        data = generate_telemetry(f"R{rack:02d}")
        print(data)