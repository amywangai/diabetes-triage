# Diabetes Progression Prediction Service

ML service for predicting diabetes disease progression to prioritize patient follow-ups.

## 🚀 Quick Start

### Using Docker (Recommended)

Pull and run the latest release:
```bash
# Pull the image
docker pull ghcr.io/<your-username>/diabetes-triage-ml:v0.1

# Run the container
docker run -p 8000:8000 ghcr.io/<your-username>/diabetes-triage-ml:v0.1
```

Access the API at `http://localhost:8000`

### Local Development

1. **Clone the repository**
```bash
   git clone https://github.com/<your-username>/diabetes-triage-ml.git
   cd diabetes-triage-ml
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Train the model**
```bash
   python src/train.py
```

5. **Run the API**
```bash
   python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## 📡 API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "model_version": "v0.1"
}
```

### Make Prediction
```bash
curl -X POST http://localhost:8000/predict \
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
  }'
```

**Response:**
```json
{
  "prediction": 152.5,
  "model_version": "v0.1"
}
```

**Input Fields:**
- `age`: Age (standardized)
- `sex`: Sex (standardized)
- `bmi`: Body mass index (standardized)
- `bp`: Average blood pressure (standardized)
- `s1`: Total serum cholesterol (standardized)
- `s2`: Low-density lipoproteins (standardized)
- `s3`: High-density lipoproteins (standardized)
- `s4`: Total cholesterol / HDL (standardized)
- `s5`: Log of serum triglycerides (standardized)
- `s6`: Blood sugar level (standardized)

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI.

## 🧪 Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🏗️ Architecture
```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   Nurse     │──────▶│  Dashboard   │──────▶│  ML Service  │
│  Dashboard  │      │  (Frontend)  │      │  (FastAPI)   │
└─────────────┘      └──────────────┘      └──────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │  Trained     │
                                            │  Model       │
                                            └──────────────┘
```

## 📊 Model Performance

### v0.1 (Baseline)
- **Model**: StandardScaler + LinearRegression
- **RMSE**: ~55.0
- **R²**: ~0.45

See `models/metrics.json` for detailed metrics.

## 🔄 CI/CD Pipeline

### Continuous Integration (PR/Push)
- Code linting (flake8, black)
- Unit tests
- Model training smoke test
- Artifact upload

### Release (Tag push)
- Model training with version tag
- Docker image build and push to GHCR
- Container smoke tests
- GitHub Release creation

## 📝 Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit
3. Push and create PR
4. CI pipeline runs automatically
5. After merge, create release: `git tag v0.x && git push --tags`
6. Release pipeline builds and publishes Docker image

## 🐛 Troubleshooting

### Model not found error
Ensure you've trained the model first:
```bash
python src/train.py
```

### Port already in use
Change the port:
```bash
docker run -p 8080:8000 ghcr.io/<your-username>/diabetes-triage-ml:v0.1
```

## 📚 Dataset

This project uses the scikit-learn diabetes dataset as a stand-in for de-identified EHR features. The target variable represents a quantitative measure of disease progression one year after baseline.

## 📄 License

MIT License

## 👥 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## 🔬 Benchmarking

Compare model versions:
```bash
python scripts/benchmark.py
```

This will output performance metrics for all trained models including:
- Accuracy metrics (RMSE, MAE, R²)
- Inference speed (ms per sample, throughput)
- Model size

## 🎯 Model Versions

### Version Comparison Table

| Version | Algorithm | RMSE | R² | Model Size | Notes |
|---------|-----------|------|-----|------------|-------|
| v0.1 | LinearRegression | 55.02 | 0.452 | ~5KB | Baseline |
| v0.2 | Ridge (α=10) | 54.12 | 0.467 | ~5KB | Better generalization |

### When to Use Each Version

- **v0.1**: Simplest model, fastest training, good for prototyping
- **v0.2**: Production-ready, better generalization, recommended for clinical use

## 🔐 Security Considerations

### Input Validation
- All API inputs are validated using Pydantic models
- Type checking ensures only numeric values are accepted
- Out-of-range values return clear error messages

### Container Security
- Runs as non-root user (in production setup)
- Minimal base image (Python slim)
- No sensitive data in image
- Regular security updates via base image

### Model Security
- Model file integrity should be verified
- Consider signing model artifacts in production
- Implement rate limiting for production deployments

## 🚀 Production Deployment

### Kubernetes Deployment

Example deployment manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: diabetes-ml-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: diabetes-ml
  template:
    metadata:
      labels:
        app: diabetes-ml
    spec:
      containers:
      - name: api
        image: ghcr.io/<your-username>/diabetes-triage-ml:v0.2
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_VERSION` | Model version to use | `v0.1` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `PORT` | API port | `8000` |

## 📈 Monitoring & Observability

### Metrics to Monitor

1. **Model Performance**
   - Prediction latency (p50, p95, p99)
   - Error rates
   - Model accuracy drift

2. **System Health**
   - API response times
   - Memory usage
   - CPU utilization
   - Request throughput

3. **Business Metrics**
   - Predictions per day
   - High-risk patient identification rate
   - False positive/negative rates

### Logging

Logs are structured and include:
- Timestamp
- Request ID
- Input features (anonymized)
- Prediction
- Inference time

## 🤝 Contributing Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names

### Testing Requirements
- Minimum 80% code coverage
- All tests must pass
- Include integration tests for new features

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(model): add Ridge regression for v0.2

- Implement Ridge with alpha=10
- Improve RMSE by 1.6%
- Maintain backward compatibility

Closes #42
```

## 🐛 Known Issues & Limitations

1. **Dataset Limitation**: Currently uses synthetic diabetes dataset. In production, would need real EHR data.
2. **Model Scope**: Predicts progression index, not specific clinical outcomes.
3. **Feature Engineering**: Minimal feature engineering applied. Could benefit from domain expert input.
4. **Calibration**: Scores not calibrated to clinical risk thresholds yet.

## 📚 References

- [Scikit-learn Diabetes Dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/<your-username>/diabetes-triage-ml/issues)
- **Discussions**: [GitHub Discussions](https://github.com/<your-username>/diabetes-triage-ml/discussions)

## 🏆 Acknowledgments

- Scikit-learn for the diabetes dataset
- FastAPI for the excellent web framework
- GitHub for Actions and Container Registry
