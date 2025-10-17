#!/bin/bash
# Script to build and test Docker image locally

set -e

IMAGE_NAME="diabetes-triage-ml"
VERSION=${1:-"dev"}

echo "🐳 Building Docker image: $IMAGE_NAME:$VERSION"

# Train model first
echo "Training model..."
python src/train.py

# Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME:$VERSION .

# Run container
echo "Starting container..."
docker run -d -p 8000:8000 --name test-$IMAGE_NAME $IMAGE_NAME:$VERSION

# Wait for container to be healthy
echo "Waiting for container to be healthy..."
sleep 5

# Test health endpoint
echo "Testing /health endpoint..."
curl -f http://localhost:8000/health || {
    echo "Health check failed!"
    docker logs test-$IMAGE_NAME
    docker stop test-$IMAGE_NAME
    docker rm test-$IMAGE_NAME
    exit 1
}

# Test prediction endpoint
echo "Testing /predict endpoint..."
curl -f -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }' || {
    echo "Prediction test failed!"
    docker logs test-$IMAGE_NAME
    docker stop test-$IMAGE_NAME
    docker rm test-$IMAGE_NAME
    exit 1
}

echo "✅ All tests passed!"
echo "Container is running at http://localhost:8000"
echo "To stop: docker stop test-$IMAGE_NAME && docker rm test-$IMAGE_NAME"
