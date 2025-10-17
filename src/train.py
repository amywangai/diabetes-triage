"""
Training script for diabetes progression prediction model.
"""
import os
import pickle
import json
from pathlib import Path
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.1")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)


def load_data():
    """Load the diabetes dataset."""
    print("Loading diabetes dataset...")
    diabetes = load_diabetes(as_frame=True)
    X = diabetes.frame.drop(columns=["target"])
    y = diabetes.frame["target"]
    return X, y


def train_model_v01(X_train, y_train):
    """Train baseline model: StandardScaler + LinearRegression."""
    print("Training v0.1 model: StandardScaler + LinearRegression")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    return {"scaler": scaler, "model": model}


def evaluate_model(pipeline, X_test, y_test):
    """Evaluate model performance."""
    X_test_scaled = pipeline["scaler"].transform(X_test)
    y_pred = pipeline["model"].predict(X_test_scaled)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        "rmse": float(rmse),
        "r2": float(r2),
        "n_test": len(y_test)
    }
    
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.3f}")
    
    return metrics


def save_artifacts(pipeline, metrics):
    """Save model, scaler, and metrics."""
    model_path = MODEL_DIR / "model.pkl"
    metrics_path = MODEL_DIR / "metrics.json"
    
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
    
    metrics_with_version = {
        "version": MODEL_VERSION,
        "metrics": metrics,
        "random_seed": RANDOM_SEED
    }
    
    with open(metrics_path, "w") as f:
        json.dump(metrics_with_version, f, indent=2)
    
    print(f"Model saved to {model_path}")
    print(f"Metrics saved to {metrics_path}")


def main():
    """Main training pipeline."""
    # Load data
    X, y = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )
    
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Train model
    #if MODEL_VERSION == "v0.1":
       # pipeline = train_model_v01(X_train, y_train)
    #else:
        # Will implement v0.2 later
        #pipeline = train_model_v01(X_train, y_train)

    # Train model
    if MODEL_VERSION == "v0.1":
        pipeline = train_model_v01(X_train, y_train)
    elif MODEL_VERSION == "v0.2":
        pipeline = train_model_v02(X_train, y_train)
    else:
        # Fallback for unknown versions
        print(f"Warning: Unknown model version {MODEL_VERSION}. Defaulting to v0.1.")
        pipeline = train_model_v01(X_train, y_train)   

    
    # Evaluate
    metrics = evaluate_model(pipeline, X_test, y_test)
    
    # Save
    save_artifacts(pipeline, metrics)
    
    print("Training complete!")


if __name__ == "__main__":
    main()



import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge  # <-- Ridge
from sklearn.ensemble import RandomForestRegressor  # <--  RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_model_v02(X_train, y_train):
    """
    Train improved model: StandardScaler + Ridge with optimized alpha.
    Also includes RandomForest as alternative.
    """
    print("Training v0.2 model: StandardScaler + Ridge (alpha=10)")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Use Ridge regression with regularization

    model = Ridge(alpha=10.0, random_state=RANDOM_SEED)
    model.fit(X_train_scaled, y_train)
    
    return {"scaler": scaler, "model": model, "type": "ridge"}
