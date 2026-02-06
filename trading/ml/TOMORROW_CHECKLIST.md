# Tomorrow Morning Checklist - ML Model
**Date:** Feb 6, 2026  
**Owner:** G (with Atlas support)  
**Goal:** Get ML conviction model up and running

---

## ⏰ Option A: Quick Demo (15 minutes)

**Just want to see it work?**

```bash
# 1. Navigate to ML directory
cd /Users/agentjoselo/.openclaw/workspace/trading/ml

# 2. Install dependencies (5 min)
pip3 install -r requirements.txt

# 3. Train bootstrap model (2 min)
python3 train_model.py

# 4. Review results (5 min)
cat models/metadata_v0.1_bootstrap.json
cat reports/training_report_v0.1_bootstrap.md

# 5. Test feature extraction (3 min)
python3 feature_engineering.py
```

**What you'll see:**
- ✅ Model trained on 200 synthetic samples
- ✅ Accuracy ~75%, Precision ~70%
- ✅ Feature importance (dan_endorsed, multi_source top features)
- ✅ Sample predictions working

**Outcome:** Confidence that ML system works, ready for Phase 1

---

## ⏰ Option B: Full Integration (1-2 hours)

**Ready to integrate with scrapers?**

### Step 1: Install & Train (15 min)
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/ml

# Install
pip3 install -r requirements.txt

# Train
python3 train_model.py

# Verify
ls -lh models/
# Should see: conviction_v0.1_bootstrap.pkl, scaler_v0.1_bootstrap.pkl
```

---

### Step 2: Create ML Scorer Wrapper (30 min)

**Create:** `scrapers/ml_scorer.py`

Copy code from `INTEGRATION_PLAN.md` Section "1. Create ML Scorer Wrapper"

**Test it:**
```python
# In Python shell
from ml_scorer import MLScorer

scorer = MLScorer(model_version='v0.1_bootstrap')

# Test signal
signal = {
    'ticker': 'TEST',
    'source': 'Yieldschool',
    'message': 'High conviction. Dan accumulating. 🔥',
    'reactions': {'🔥': 30, '🚀': 15},
    'dan_endorsed': True,
    'mention_count': 3,
}

score, prob = scorer.score_signal(signal)
print(f"Score: {score}/10, Probability: {prob:.2%}")
# Should output: Score: 8-9/10, Probability: 70-80%
```

---

### Step 3: Update Yieldschool Scraper (30 min)

**Edit:** `scrapers/yieldschool_scraper.py`

Add at top:
```python
from ml_scorer import MLScorer
```

Add to `__init__`:
```python
try:
    self.ml_scorer = MLScorer(model_version='v0.1_bootstrap')
    self.use_ml = True
except Exception as e:
    print(f"ML not available: {e}")
    self.use_ml = False
```

Update `scrape_yield_hub()` to log both scores:
(See INTEGRATION_PLAN.md for full code)

---

### Step 4: Test Scraper (15 min)

```bash
cd scrapers

# Run scraper with sample data
python3 yieldschool_scraper.py

# Check output
# Should see both rule_score and ml_score logged
```

---

### Step 5: Deploy Phase 1 (Parallel Scoring)

**What Phase 1 means:**
- ML scores every signal
- Rule-based score also calculated
- **Deploy decisions still use rule-based** (safe)
- Both scores logged in `signals-database.csv`

**New CSV columns:**
```
conviction_rule, conviction_ml, conviction_ml_prob, conviction_final, scoring_method
```

**Run for 7 days, collect 50+ signals with dual scores**

---

## ⏰ Option C: Just Read (30 minutes)

**Not ready to code? Understand the system first:**

1. **Start here:** `README.md` (10 min)
   - What ML system does
   - How it works
   - Integration plan overview

2. **Read:** `DELIVERY_SUMMARY.md` (10 min)
   - What was delivered
   - Expected performance
   - Timeline

3. **Skim:** `ML_CONVICTION_MODEL_DESIGN.md` (10 min)
   - Feature engineering details
   - Dan's green flags → ML features
   - Training methodology

4. **Review:** `DEMO.md` (5 min)
   - Example: $TAO signal scored
   - ML vs rule-based comparison
   - Real-world flow

---

## 📋 What to Check

### ✅ Files Delivered (All in `trading/ml/`)

**Documentation:**
- [ ] README.md (overview)
- [ ] DELIVERY_SUMMARY.md (tonight's work)
- [ ] ML_CONVICTION_MODEL_DESIGN.md (full architecture)
- [ ] BACKTESTING_FRAMEWORK.md (validation strategy)
- [ ] INTEGRATION_PLAN.md (code changes)
- [ ] INSTALLATION.md (setup guide)
- [ ] DEMO.md (examples)
- [ ] TOMORROW_CHECKLIST.md (this file)

**Code:**
- [ ] feature_engineering.py (45+ features)
- [ ] conviction_model.py (XGBoost model)
- [ ] train_model.py (training pipeline)
- [ ] requirements.txt (dependencies)

**Data/Models:**
- [ ] data/ (empty, ready for training data)
- [ ] models/ (empty, ready for trained models)
- [ ] reports/ (empty, ready for training reports)

---

## 🎯 Decision Points

### After Quick Demo (Option A)

**Question:** Does ML model work? Are metrics reasonable?

- **Yes (Accuracy >70%)** → Proceed to Option B (integration)
- **No (Accuracy <65%)** → Review features, need more training data

---

### After Full Integration (Option B)

**Question:** Run Phase 1 for how long?

- **Recommended:** 7 days (collect 50+ signals)
- **Fast track:** 3 days (if confident, move to Phase 2)
- **Cautious:** 14 days (more data = more confidence)

---

### After Phase 1 (Week 1)

**Question:** Does ML beat rule-based?

**Compare:**
```
Rule-based win rate: X%
ML win rate: Y%
Agreement rate: Z%
```

**Decision:**
- **ML wins by >5%** → Proceed to Phase 2 (hybrid)
- **ML ties (±3%)** → Extend Phase 1, collect more data
- **ML loses** → Investigate features, retrain

---

## 🚨 Troubleshooting

### Issue: pip3 install fails
```bash
# Try:
python3 -m pip install -r requirements.txt

# Or install to user:
pip3 install --user -r requirements.txt
```

### Issue: xgboost won't compile
```bash
# Install pre-built wheel:
pip3 install xgboost --only-binary :all:
```

### Issue: Model training slow (>30 sec)
```python
# In train_model.py, reduce samples:
X, y = create_sample_training_data(n_samples=100)  # Instead of 200
```

### Issue: Import errors
```bash
# Make sure you're in right directory:
cd /Users/agentjoselo/.openclaw/workspace/trading/ml
python3 train_model.py
```

### Issue: ML scorer can't find model
```python
# Check model files exist:
ls -l models/conviction_v0.1_bootstrap.pkl

# If missing, retrain:
python3 train_model.py
```

---

## 📞 Need Help?

**Atlas (ML Engineer AI):**
- Available in OpenClaw agent system
- Can debug issues
- Can retrain models
- Can update features

**Documentation:**
- Technical: `ML_CONVICTION_MODEL_DESIGN.md`
- Integration: `INTEGRATION_PLAN.md`
- Setup: `INSTALLATION.md`

---

## 🎯 Success Criteria (End of Day)

**Minimum (Option A):**
- [ ] Dependencies installed
- [ ] Model trained successfully
- [ ] Test predictions work
- [ ] Understand how system works

**Good (Option B):**
- [ ] ML scorer integrated with scrapers
- [ ] Phase 1 deployed (parallel scoring)
- [ ] First dual-scored signals collected
- [ ] Ready for Week 1 testing

**Excellent:**
- [ ] All of Option B
- [ ] 10+ signals scored with both methods
- [ ] Early comparison (ML vs rule agreement)
- [ ] Confidence to proceed to Phase 2

---

## 📅 This Week Timeline

**Today (Feb 6):**
- Morning: Install + train (Option A or B)
- Afternoon: Test + integrate
- Evening: Review first results

**Feb 7-12 (Week 1):**
- Daily: Scrape signals, log dual scores
- End of week: Compare ML vs rule performance
- Decision: Proceed to Phase 2?

**Feb 13-19 (Week 2):**
- Switch to hybrid scoring (if ML validated)
- Deploy based on 30% rule + 70% ML
- Track outcomes

**Feb 20+ (Week 3):**
- Full ML rollout (if successful)
- Weekly retraining
- Production system running

---

## ✅ Quick Win Checklist

```bash
# Copy-paste this entire block:

cd /Users/agentjoselo/.openclaw/workspace/trading/ml

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Training bootstrap model..."
python3 train_model.py

echo "Testing feature extraction..."
python3 feature_engineering.py

echo "Done! Check results:"
echo "1. Model metrics: cat models/metadata_v0.1_bootstrap.json"
echo "2. Training report: cat reports/training_report_v0.1_bootstrap.md"
echo "3. Feature test: cat data/sample_features.csv"
```

**Expected runtime:** 5-10 minutes  
**Expected outcome:** Working ML system ready for integration

---

**Good luck! Atlas built this for you. Make it count.** 🐓🤖
