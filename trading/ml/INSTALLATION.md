# Installation Guide - ML Conviction Model

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 500MB disk space (for ML libraries)

---

## 🚀 Quick Install

```bash
# Navigate to ML directory
cd /Users/agentjoselo/.openclaw/workspace/trading/ml

# Install dependencies
pip3 install -r requirements.txt

# Test installation
python3 -c "import xgboost, sklearn, pandas; print('✓ All dependencies installed')"
```

---

## 📋 Dependencies Breakdown

### Core ML Libraries
- **xgboost** - Gradient boosting framework (model core)
- **scikit-learn** - ML utilities (train/test split, metrics)
- **pandas** - Data manipulation
- **numpy** - Numerical computing

### Feature Engineering
- **pytrends** - Google Trends API (market timing features)
- **requests** - HTTP requests (API calls)

### Backtesting
- **backtrader** - Trading backtesting framework

### Model Interpretation
- **shap** - SHAP values for feature importance

---

## ⚠️ Common Issues

### Issue: pip3 not found
```bash
# Install pip
python3 -m ensurepip --upgrade
```

### Issue: Permission denied
```bash
# Install to user directory
pip3 install --user -r requirements.txt
```

### Issue: xgboost compile error
```bash
# Install pre-built wheel
pip3 install xgboost --only-binary :all:
```

### Issue: scikit-learn version conflict
```bash
# Upgrade scikit-learn
pip3 install --upgrade scikit-learn
```

---

## ✅ Verify Installation

Run test script:

```bash
python3 << 'EOF'
import sys

deps = {
    'xgboost': '2.0.0',
    'sklearn': '1.3.0',
    'pandas': '2.0.0',
    'numpy': '1.24.0',
}

print("Checking dependencies...\n")

for pkg, min_version in deps.items():
    try:
        if pkg == 'sklearn':
            import sklearn
            version = sklearn.__version__
        else:
            mod = __import__(pkg)
            version = mod.__version__
        
        print(f"✓ {pkg:15s} {version:10s} (min: {min_version})")
    except ImportError:
        print(f"✗ {pkg:15s} NOT INSTALLED")
        sys.exit(1)

print("\n✅ All dependencies installed correctly!")
EOF
```

---

## 🏃 First Run

After installation, test the full pipeline:

```bash
# Train bootstrap model on synthetic data
python3 train_model.py

# Should output:
# - Training metrics
# - Feature importance
# - Saved model files to models/

# Check output files
ls -lh models/
# Should see:
# - conviction_v0.1_bootstrap.pkl
# - scaler_v0.1_bootstrap.pkl
# - features_v0.1_bootstrap.json
```

---

## 🐛 Troubleshooting

### Model training slow?
XGBoost uses all CPU cores by default. On Mac M1/M2:
```bash
# Training 200 samples should take <10 seconds
# If >30 seconds, might be CPU throttling
```

### Memory issues?
Reduce dataset size in `train_model.py`:
```python
# Change from:
X, y = create_sample_training_data(n_samples=200)

# To:
X, y = create_sample_training_data(n_samples=100)
```

### Import errors?
Make sure you're in the right directory:
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/ml
python3 train_model.py
```

---

## 📦 Offline Installation (No Internet)

If installing on server without internet:

```bash
# On machine WITH internet:
pip3 download -r requirements.txt -d ./packages/

# Copy ./packages/ to target machine

# On target machine:
pip3 install --no-index --find-links=./packages/ -r requirements.txt
```

---

## 🔄 Uninstall

To remove all ML dependencies:

```bash
pip3 uninstall -y xgboost scikit-learn pandas numpy pytrends backtrader shap requests python-dateutil
```

---

## ✅ Installation Complete!

Next steps:
1. Read `README.md` for system overview
2. Run `python3 train_model.py` to train first model
3. Test predictions with sample signals
4. Integrate with scrapers (see `INTEGRATION_PLAN.md`)

---

**Questions?** Check main README.md or contact Atlas (ML Engineer AI) 🤖
