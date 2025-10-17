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
