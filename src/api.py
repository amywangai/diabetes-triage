"""
FastAPI service for diabetes progression prediction.
"""
import pickle
import json
from pathlib import Path
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np

# Load model and metadata
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "model.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"

# Initialize FastAPI
app = FastAPI(
    title="Diabetes Progression Prediction API",
    description="ML service for predicting diabetes disease progression",
    version="0.1.0"
)

# Global variables
model_pipeline = None
model_metadata = None


def load_model():
    """Load the trained model and metadata."""
    global model_pipeline, model_metadata
    
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    
    with open(MODEL_PATH, "rb") as f:
        model_pipeline = pickle.load(f)
    
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r") as f:
            model_metadata = json.load(f)
    else:
        model_metadata = {"version": "unknown"}
    
    print(f"Model loaded: {model_metadata.get('version', 'unknown')}")


# Load model on startup
load_model()


class PredictionInput(BaseModel):
    """Input schema for prediction."""
    age: float = Field(..., description="Age (standardized)")
    sex: float = Field(..., description="Sex (standardized)")
    bmi: float = Field(..., description="Body mass index (standardized)")
    bp: float = Field(..., description="Average blood pressure (standardized)")
    s1: float = Field(..., description="Total serum cholesterol (standardized)")
    s2: float = Field(..., description="Low-density lipoproteins (standardized)")
    s3: float = Field(..., description="High-density lipoproteins (standardized)")
    s4: float = Field(..., description="Total cholesterol / HDL (standardized)")
    s5: float = Field(..., description="Log of serum triglycerides (standardized)")
    s6: float = Field(..., description="Blood sugar level (standardized)")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionOutput(BaseModel):
    """Output schema for prediction."""
    prediction: float = Field(..., description="Predicted progression score")
    model_version: str = Field(..., description="Model version used")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_version": model_metadata.get("version", "unknown")
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """
    Predict diabetes progression score.
    
    Higher scores indicate greater disease progression risk.
    """
    try:
        # Convert input to array
        feature_names = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
        X = np.array([[getattr(input_data, f) for f in feature_names]])
        
        # Make prediction
        X_scaled = model_pipeline["scaler"].transform(X)
        prediction = float(model_pipeline["model"].predict(X_scaled)[0])
        
        return PredictionOutput(
            prediction=prediction,
            model_version=model_metadata.get("version", "unknown")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "service": "Diabetes Progression Prediction",
        "version": model_metadata.get("version", "unknown"),
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
