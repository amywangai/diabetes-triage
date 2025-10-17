# Changelog

All notable changes to this project will be documented in this file.

## [v0.1] - 2025-01-XX

### Added
- Initial release with baseline model
- StandardScaler + LinearRegression pipeline
- FastAPI service with `/health` and `/predict` endpoints
- Docker containerization with multi-stage build
- GitHub Actions CI/CD pipeline
- Comprehensive test suite

### Model Performance
- **Algorithm**: StandardScaler + LinearRegression
- **RMSE**: 55.02
- **R²**: 0.452
- **Training set size**: 353 samples
- **Test set size**: 89 samples

### Features
- Reproducible training with fixed random seed (42)
- JSON error handling for invalid inputs
- Health check endpoint
- Interactive API documentation (Swagger UI)
- Docker health checks
- Model versioning

### Technical Details
- Python 3.10
- FastAPI for API framework
- scikit-learn for ML
- Multi-stage Docker build for smaller images (~200MB)
- Automated testing in CI pipeline
