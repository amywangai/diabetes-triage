"""
Integration tests for end-to-end workflows.
"""

import pytest
import subprocess
import time
import requests
from pathlib import Path


def test_training_pipeline():
    """Test complete training pipeline."""
    # Run training script
    result = subprocess.run(["python", "src/train.py"], capture_output=True, text=True)

    assert result.returncode == 0
    assert "Training complete!" in result.stdout

    # Check artifacts were created
    assert Path("models/model.pkl").exists()
    assert Path("models/metrics.json").exists()


def test_api_startup():
    """Test that API can start successfully."""
    # This test assumes model has been trained
    if not Path("models/model.pkl").exists():
        pytest.skip("Model not trained yet")

    # Start API in background
    process = subprocess.Popen(
        [
            "python",
            "-m",
            "uvicorn",
            "src.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8001",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Wait for startup
        time.sleep(3)

        # Test health endpoint
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    finally:
        # Cleanup
        process.terminate()
        process.wait(timeout=5)


def test_end_to_end_prediction():
    """Test complete prediction workflow."""
    if not Path("models/model.pkl").exists():
        pytest.skip("Model not trained yet")

    # Start API
    process = subprocess.Popen(
        [
            "python",
            "-m",
            "uvicorn",
            "src.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8002",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(3)

        # Make prediction request
        payload = {
            "age": 0.02,
            "sex": -0.044,
            "bmi": 0.06,
            "bp": -0.03,
            "s1": -0.02,
            "s2": 0.03,
            "s3": -0.02,
            "s4": 0.02,
            "s5": 0.02,
            "s6": -0.001,
        }

        response = requests.post(
            "http://127.0.0.1:8002/predict", json=payload, timeout=5
        )

        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "model_version" in data
        assert isinstance(data["prediction"], (int, float))

    finally:
        process.terminate()
        process.wait(timeout=5)
