#!/bin/bash
# Script to train model and run API locally

set -e

echo "🚀 Starting local development setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Train model
echo "Training model..."
python src/train.py

# Run tests
echo "Running tests..."
pytest tests/ -v

# Start API
echo "Starting API server..."
echo "API will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
