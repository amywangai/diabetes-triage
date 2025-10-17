"""
Tests for model training and prediction.
"""
import numpy as np
from src.train import load_data, train_model_v01


def test_load_data():
    """Test data loading."""
    X, y = load_data()
    assert X.shape[0] == 442
    assert X.shape[1] == 10
    assert y.shape[0] == 442


def test_train_model():
    """Test model training."""
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
