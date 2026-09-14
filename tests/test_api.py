from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


SAMPLE_TELEMETRY = {
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


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200


def test_analyze_endpoint():

    response = client.post(
        "/analyze",
        json=SAMPLE_TELEMETRY
    )

    assert response.status_code == 200

    data = response.json()

    assert "current_temperature" in data
    assert "predicted_temperature" in data
    assert "anomaly" in data
    assert "root_cause" in data
    assert "cooling_recommendation" in data
    assert "human_approval_required" in data


def test_analyze_temperature():

    response = client.post(
        "/analyze",
        json=SAMPLE_TELEMETRY
    )

    data = response.json()

    assert data["current_temperature"] == 30.5
    assert data["predicted_temperature"] > 0