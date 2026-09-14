from agent.tools import (
    predict_temperature,
    detect_anomaly,
    analyze_root_cause,
    optimize_cooling,
)


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
    "workload_change": 5,
}


def test_temperature_prediction():

    prediction = predict_temperature(SAMPLE_TELEMETRY)

    assert isinstance(prediction, float)
    assert prediction > 0


def test_anomaly_detection():

    result = detect_anomaly(SAMPLE_TELEMETRY)

    assert "status" in result
    assert "severity" in result
    assert "score" in result

    assert result["status"] in ["normal", "anomaly"]


def test_root_cause_analysis():

    result = analyze_root_cause(SAMPLE_TELEMETRY)

    assert "root_cause" in result
    assert "explanation" in result

    assert isinstance(result["root_cause"], str)


def test_cooling_optimization():

    prediction = predict_temperature(SAMPLE_TELEMETRY)

    result = optimize_cooling(
        SAMPLE_TELEMETRY,
        prediction
    )

    assert "recommended_action" in result
    assert "energy_impact" in result
    assert "safe_temperature_limit" in result

    assert isinstance(
        result["recommended_action"],
        str
    )