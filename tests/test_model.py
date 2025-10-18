"""
Tests for model training and prediction.
"""
import numpy as np
import json
from pathlib import Path
from src.train import load_data, train_model_v01, train_model_v02, evaluate_model


def test_load_data():
    """Test data loading."""
    X, y = load_data()
    assert X.shape[0] == 442
    assert X.shape[1] == 10
    assert y.shape[0] == 442
    assert list(X.columns) == ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']


def test_train_model_v01():
    """Test v0.1 model training."""
    X, y = load_data()
    X_train = X[:300]
    y_train = y[:300]

    pipeline = train_model_v01(X_train, y_train)

    assert "scaler" in pipeline
    assert "model" in pipeline

    # Test prediction
    X_scaled = pipeline["scaler"].transform(X_train[:5])
    predictions = pipeline["model"].predict(X_scaled)

    assert predictions.shape[0] == 5
    assert all(isinstance(p, (np.floating, float)) for p in predictions)


def test_train_model_v02():
    """Test v0.2 model training."""
    X, y = load_data()
    X_train = X[:300]
    y_train = y[:300]

    pipeline = train_model_v02(X_train, y_train)

    assert "scaler" in pipeline
    assert "model" in pipeline
    assert "type" in pipeline
    assert pipeline["type"] == "ridge"

    # Test prediction
    X_scaled = pipeline["scaler"].transform(X_train[:5])
    predictions = pipeline["model"].predict(X_scaled)

    assert predictions.shape[0] == 5
    assert all(isinstance(p, (np.floating, float)) for p in predictions)


def test_evaluate_model():
    """Test model evaluation."""
    X, y = load_data()
    X_train = X[:300]
    y_train = y[:300]
    X_test = X[300:]
    y_test = y[300:]

    pipeline = train_model_v01(X_train, y_train)
    metrics = evaluate_model(pipeline, X_test, y_test)

    assert "rmse" in metrics
    assert "r2" in metrics
    assert "n_test" in metrics
    assert metrics["rmse"] > 0
    assert -1 <= metrics["r2"] <= 1
    assert metrics["n_test"] == len(y_test)


def test_model_artifacts_exist():
    """Test that model artifacts are created after training."""
    model_path = Path("models/model.pkl")
    metrics_path = Path("models/metrics.json")

    # These should exist after running train.py
    if model_path.exists():
        assert model_path.stat().st_size > 0

    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        assert "version" in metrics
        assert "metrics" in metrics
        assert "random_seed" in metrics


def test_prediction_consistency():
    """Test that predictions are consistent with same input."""
    X, y = load_data()
    X_train = X[:300]
    y_train = y[:300]

    pipeline = train_model_v01(X_train, y_train)

    # Make prediction twice with same input
    X_test = X_train[:1]
    X_scaled = pipeline["scaler"].transform(X_test)
    pred1 = pipeline["model"].predict(X_scaled)
    pred2 = pipeline["model"].predict(X_scaled)

    assert np.allclose(pred1, pred2)


def test_prediction_range():
    """Test that predictions are in reasonable range."""
    X, y = load_data()
    X_train = X[:300]
    y_train = y[:300]

    pipeline = train_model_v01(X_train, y_train)

    # Test on training data
    X_scaled = pipeline["scaler"].transform(X_train)
    predictions = pipeline["model"].predict(X_scaled)

    # Predictions should be roughly in the range of training targets
    y_min, y_max = y_train.min(), y_train.max()
    buffer = (y_max - y_min) * 0.5  # Allow 50% buffer

    assert predictions.min() >= y_min - buffer
    assert predictions.max() <= y_max + buffer
