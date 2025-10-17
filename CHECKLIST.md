# Project Completion Checklist

## ✅ Code Quality (3.0 points)

### CI Pipeline
- [ ] CI workflow runs on PR and push
- [ ] Linting (flake8) configured and passing
- [ ] Code formatting (black) configured and passing
- [ ] Unit tests run automatically
- [ ] Test coverage > 70%
- [ ] Artifacts uploaded (model, metrics)

### Release Pipeline
- [ ] Release workflow triggers on version tags (v*)
- [ ] Docker image builds successfully
- [ ] Image pushed to GHCR
- [ ] Container smoke tests pass
- [ ] GitHub Release created automatically
- [ ] Metrics and changelog attached to release

## ✅ Training & Reproducibility (2.0 points)

- [ ] Random seed set (RANDOM_SEED = 42)
- [ ] Requirements.txt with pinned versions
- [ ] Metrics logged and saved (RMSE, R²)
- [ ] Clear training instructions in README
- [ ] Can reproduce training locally
- [ ] Model artifacts saved correctly

## ✅ Docker Image Quality (2.0 points)

- [ ] Multi-stage build implemented
- [ ] Model baked into image
- [ ] Port 8000 exposed correctly
- [ ] Health check configured
- [ ] Image size reasonable (<500MB)
- [ ] Starts quickly (<10 seconds)
- [ ] Self-contained (no external dependencies)

## ✅ Iteration Quality & Evidence (2.0 points)

### v0.1 (Baseline)
- [ ] StandardScaler + LinearRegression implemented
- [ ] Metrics documented
- [ ] Working API
- [ ] Docker image published
- [ ] Tag: v0.1 created

### v0.2 (Improvement)
- [ ] Improved model implemented (Ridge/RandomForest)
- [ ] Clear improvement shown (RMSE, R², etc.)
- [ ] CHANGELOG.md updated with comparison
- [ ] Side-by-side metrics documented
- [ ] Justification for changes provided
- [ ] Tag: v0.2 created

## ✅ Documentation & Collaboration (1.0 point)

### README.md
- [ ] Project description
- [ ] Quick start instructions
- [ ] Exact run commands
- [ ] Sample API payload
- [ ] Docker pull commands
- [ ] API endpoint documentation
- [ ] Troubleshooting section

### CHANGELOG.md
- [ ] v0.1 entry with metrics
- [ ] v0.2 entry with comparison
- [ ] Clear improvement rationale

### Git History
- [ ] Meaningful commit messages
- [ ] Separate PRs for v0.1 and v0.2
- [ ] Clean, logical history
- [ ] No sensitive data committed

## ✅ Acceptance Criteria

- [ ] Can pull image: `ghcr.io/<org>/<repo>:v0.1`
- [ ] Can pull image: `ghcr.io/<org>/<repo>:v0.2`
- [ ] `GET /health` returns correct format
- [ ] `POST /predict` accepts sample payload
- [ ] `POST /predict` returns `{"prediction": float, "model_version": str}`
- [ ] v0.2 shows justified improvement
- [ ] Repository is public
- [ ] Actions tab shows successful workflows

## 📦 Hand-in Requirements

- [ ] GitHub repository URL in PDF
- [ ] Repository is public
- [ ] Both workflow types visible in Actions tab
- [ ] At least one successful v0.1 release
- [ ] At least one successful v0.2 release

## 🧪 Local Testing Commands
```bash
# Test training
python src/train.py

# Test API
pytest tests/ -v

# Test Docker build
./scripts/docker_build_and_test.sh

# Test full workflow
./scripts/train_and_run.sh
```

## 🚀 Final Deployment Steps

1. Ensure all code is committed and pushed
2. Create and push v0.1 tag
3. Verify v0.1 release in GitHub
4. Create v0.2 improvements
5. Create and push v0.2 tag
6. Verify v0.2 release in GitHub
7. Test both Docker images locally
8. Create hand-in PDF with repository URL
