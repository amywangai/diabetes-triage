# Changelog

## [v0.2] - 2025-01-XX

### Changed
- **Improved model**: Switched from LinearRegression to Ridge regression with regularization (alpha=10)
- Enhanced generalization through L2 regularization
- Slightly reduced model complexity

### Model Performance Comparison

#### v0.2 (Ridge)
- **Algorithm**: StandardScaler + Ridge (alpha=10)
- **RMSE**: 54.12 (**↓ 1.6% improvement**)
- **R²**: 0.467 (**↑ 3.3% improvement**)
- **Model size**: ~5KB (similar to v0.1)

#### v0.1 (Baseline)
- **Algorithm**: StandardScaler + LinearRegression
- **RMSE**: 55.02
- **R²**: 0.452

### Rationale
The Ridge regression model provides better generalization by penalizing large coefficients, reducing overfitting risk. This is particularly important for clinical applications where model stability across different patient populations is crucial.

### Technical Changes
- Added Ridge regression with cross-validated alpha parameter
- Maintained same preprocessing pipeline for consistency
- No changes to API interface (backward compatible)
- Docker image size remains ~200MB

---

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
