"""
Tests for the API endpoints.
"""
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_version" in data

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "endpoints" in data

def test_predict_valid_input():
    """Test prediction with valid input."""
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
        "s6": -0.001
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "model_version" in data
    assert isinstance(data["prediction"], (int, float))

def test_predict_missing_field():
    """Test prediction with missing field."""
    payload = {
        "age": 0.02,
        "sex": -0.044,
        # Missing other fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error
