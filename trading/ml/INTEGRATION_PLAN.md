# ML Model Integration Plan
**Author:** Atlas (roostr ML Engineer AI)  
**Date:** Feb 5, 2026  
**Status:** Ready for Implementation

---

## 🎯 GOAL

Integrate ML conviction model with existing scrapers (Yieldschool, Dumb Money) to replace rule-based scoring.

**Transition:** Rule-based → Hybrid → 100% ML over 3 weeks

---

## 📋 INTEGRATION PHASES

### Phase 1: Parallel Scoring (Week 1)
**What:** Run ML model alongside existing rules, compare outputs

**Changes:**
- Add ML scoring to scrapers (doesn't affect deployment yet)
- Log both scores side-by-side
- Deploy based on rule-based (existing behavior)
- Track which signals ML would've picked

**Risk:** Zero (no production impact)

**Deliverable:** Data on ML vs rule-based agreement

---

### Phase 2: Hybrid Scoring (Week 2)
**What:** Weighted average of rule + ML (30% rule, 70% ML)

**Changes:**
- Final score = 0.3 * rule_score + 0.7 * ml_score
- Deploy top signals by hybrid score
- Track outcomes

**Risk:** Low (still using proven rules)

**Deliverable:** Live validation of ML model

---

### Phase 3: Full ML Rollout (Week 3)
**What:** 100% ML scoring, retire rule-based

**Changes:**
- Deploy signals purely by ML score
- Rule-based score deprecated (logged for audit only)
- Weekly retraining with new data

**Risk:** Medium (full dependency on ML)

**Deliverable:** Production ML conviction system

---

## 🔧 CODE INTEGRATION

### Current Architecture

```
scrapers/
├── yieldschool_scraper.py     (rule-based conviction)
├── dumbmoney_scraper.py       (rule-based conviction)
└── signal_validator.py        (validation layer)

Conviction flow:
  Message → _calculate_conviction() → Score (1-10) → Deploy if >8
```

---

### New Architecture (Phase 1)

```
scrapers/
├── yieldschool_scraper.py     (+ ML scoring)
├── dumbmoney_scraper.py       (+ ML scoring)
├── signal_validator.py        (unchanged)
└── ml_scorer.py               (NEW - wrapper for model)

ml/
├── models/
│   ├── conviction_v0.1.pkl
│   ├── scaler_v0.1.pkl
│   └── features_v0.1.json
├── feature_engineering.py
├── conviction_model.py
└── ml_scorer.py (NEW)

Conviction flow:
  Message → _calculate_conviction_rule() → Rule score
          ↓
        _calculate_conviction_ml() → ML score
          ↓
        Log both, use rule for now
```

---

### New Architecture (Phase 3 - Final)

```
scrapers/
├── yieldschool_scraper.py     (ML primary)
├── dumbmoney_scraper.py       (ML primary)
└── signal_validator.py        (unchanged)

ml/
├── models/ (weekly updates)
├── feature_engineering.py
├── conviction_model.py
└── ml_scorer.py

Conviction flow:
  Message → Feature Engineering → ML Model → Score (1-10) → Deploy if >8
```

---

## 📝 CODE CHANGES

### 1. Create ML Scorer Wrapper

**File:** `scrapers/ml_scorer.py`

```python
#!/usr/bin/env python3
"""
ML Scorer - Wrapper for conviction model
Simple interface for scrapers to get ML scores

Author: Atlas
"""

import sys
sys.path.append('../ml')

from feature_engineering import FeatureEngineer
from conviction_model import ConvictionModel
import pandas as pd


class MLScorer:
    """Wrapper for ML conviction scoring"""
    
    def __init__(self, model_path='../ml/models', model_version='v0.1'):
        """Load trained model"""
        self.engineer = FeatureEngineer()
        self.model = ConvictionModel(model_version=model_version)
        self.model.load(model_dir=model_path, version=model_version)
        
        print(f"Loaded ML model {model_version}")
    
    def score_signal(self, signal_dict):
        """
        Score a single signal
        
        Args:
            signal_dict: Dict with keys like:
                - ticker, source, message, reactions, dan_endorsed, etc.
        
        Returns:
            (ml_score, probability)
            ml_score: 1-10 integer
            probability: 0-1 float (P(2x in 30d))
        """
        # Extract features
        features = self.engineer.extract_features(signal_dict)
        
        # Convert to DataFrame (model expects this)
        feature_df = pd.DataFrame([features])
        
        # Get score
        ml_score, prob = self.model.score_signal(feature_df)
        
        return ml_score, prob
    
    def batch_score(self, signals):
        """Score multiple signals"""
        scores = []
        for signal in signals:
            score, prob = self.score_signal(signal)
            scores.append({'ticker': signal['ticker'], 'ml_score': score, 'ml_prob': prob})
        
        return scores
```

---

### 2. Update Yieldschool Scraper

**File:** `scrapers/yieldschool_scraper.py`

**Changes:**

```python
from ml_scorer import MLScorer

class YieldschoolScraper:
    def __init__(self):
        self.signals = []
        self.output_file = '../signals-database.csv'
        
        # NEW: Initialize ML scorer
        try:
            self.ml_scorer = MLScorer(model_path='../ml/models', model_version='v0.1')
            self.use_ml = True
        except Exception as e:
            print(f"ML scorer not available: {e}")
            self.use_ml = False
    
    def _calculate_conviction(self, message: str, ticker: str) -> int:
        """
        OLD: Rule-based conviction (keep for Phase 1)
        """
        score = 3  # Base score
        
        if '🔥' in message:
            score += 1
        if '🚀' in message:
            score += 1
        # ... existing logic
        
        return min(score, 10)
    
    def _calculate_conviction_ml(self, message: str, ticker: str, full_signal_data: dict) -> tuple:
        """
        NEW: ML-based conviction
        
        Returns:
            (ml_score, probability)
        """
        if not self.use_ml:
            return None, None
        
        # Build signal dict for ML scorer
        signal_dict = {
            'ticker': ticker,
            'source': full_signal_data.get('source', 'Yieldschool'),
            'message': message,
            'reactions': full_signal_data.get('reactions', {}),
            'dan_endorsed': full_signal_data.get('dan_endorsed', False),
            'mention_count': full_signal_data.get('mention_count', 1),
            'total_reactions': sum(full_signal_data.get('reactions', {}).values()),
            'message_age_hours': 24,  # Default
            # ... add more fields as available
        }
        
        # Get ML score
        ml_score, ml_prob = self.ml_scorer.score_signal(signal_dict)
        
        return ml_score, ml_prob
    
    def _calculate_conviction_hybrid(self, message: str, ticker: str, full_signal_data: dict) -> int:
        """
        PHASE 2: Hybrid scoring (30% rule, 70% ML)
        """
        # Get rule-based score
        rule_score = self._calculate_conviction(message, ticker)
        
        # Get ML score
        ml_score, ml_prob = self._calculate_conviction_ml(message, ticker, full_signal_data)
        
        if ml_score is None:
            # ML not available, fallback to rules
            return rule_score
        
        # Weighted average
        hybrid_score = int(0.3 * rule_score + 0.7 * ml_score)
        
        # Log for comparison
        print(f"[{ticker}] Rule: {rule_score}, ML: {ml_score} (p={ml_prob:.2f}), Hybrid: {hybrid_score}")
        
        return hybrid_score
    
    def scrape_yield_hub(self, messages: List[str]) -> List[Dict[str, Any]]:
        """
        UPDATED: Use hybrid scoring (Phase 2)
        """
        signals = []
        
        for msg in messages:
            tickers = self._extract_tickers(msg)
            
            for ticker in tickers:
                # Gather all signal data
                dan_endorsed = 'Dan' in msg or '@Dan' in msg
                reactions = self._extract_reactions(msg)  # New helper
                
                full_signal_data = {
                    'source': 'Yieldschool-YieldHub',
                    'dan_endorsed': dan_endorsed,
                    'reactions': reactions,
                    'mention_count': 1,  # Will aggregate later
                }
                
                # PHASE 1: Use rule-based, log ML
                rule_score = self._calculate_conviction(msg, ticker)
                ml_score, ml_prob = self._calculate_conviction_ml(msg, ticker, full_signal_data)
                
                conviction_score = rule_score  # Phase 1: still using rules
                
                # PHASE 2: Switch to hybrid
                # conviction_score = self._calculate_conviction_hybrid(msg, ticker, full_signal_data)
                
                # PHASE 3: Switch to pure ML
                # conviction_score = ml_score if ml_score else rule_score
                
                signals.append({
                    'ticker': ticker,
                    'source': 'Yieldschool-YieldHub',
                    'conviction_score': conviction_score,
                    'rule_score': rule_score,           # Log for audit
                    'ml_score': ml_score,               # Log for audit
                    'ml_probability': ml_prob,          # Log for audit
                    'dan_endorsed': dan_endorsed,
                    # ... rest of fields
                })
        
        return signals
```

---

### 3. Update Dumb Money Scraper

**File:** `scrapers/dumbmoney_scraper.py`

**Similar changes:**

```python
from ml_scorer import MLScorer

class DumbMoneyScraper:
    def __init__(self):
        # ... existing init
        
        # NEW: ML scorer
        try:
            self.ml_scorer = MLScorer()
            self.use_ml = True
        except:
            self.use_ml = False
    
    def _calculate_conviction_hybrid(self, signal_dict) -> int:
        """Hybrid scoring for Dumb Money signals"""
        
        # Rule-based
        rule_score = self._calculate_conviction(
            signal_dict['total_reactions'], 
            signal_dict['content']
        )
        
        # ML-based
        if self.use_ml:
            ml_score, ml_prob = self.ml_scorer.score_signal(signal_dict)
            
            # Hybrid
            hybrid_score = int(0.3 * rule_score + 0.7 * ml_score)
            
            print(f"[{signal_dict['ticker']}] Rule: {rule_score}, ML: {ml_score}, Hybrid: {hybrid_score}")
            
            return hybrid_score
        else:
            return rule_score
```

---

## 📊 LOGGING & MONITORING

### What to Track (Phase 1-2)

**CSV columns to add:**
- `conviction_rule` - Rule-based score (1-10)
- `conviction_ml` - ML score (1-10)
- `conviction_ml_prob` - ML probability (0-1)
- `conviction_final` - Final score used for deployment
- `scoring_method` - "rule" / "hybrid" / "ml"

**Purpose:**
- Compare rule vs ML performance
- Track which signals each method would pick
- Validate ML calibration (score 9 → actually 90% win rate?)

---

### Dashboard Updates

**Add to `dashboard.html`:**

```html
<section id="ml-performance">
  <h2>🧠 ML Model Performance</h2>
  
  <h3>Score Comparison (Last 30 Days)</h3>
  <table>
    <tr>
      <th>Ticker</th>
      <th>Rule Score</th>
      <th>ML Score</th>
      <th>Final Score</th>
      <th>Outcome</th>
    </tr>
    <!-- Auto-populated from signals-database.csv -->
  </table>
  
  <h3>Conviction Calibration</h3>
  <p>Score 9-10: 75% hit 2x (expected 70%+) ✓</p>
  <p>Score 7-8: 58% hit 2x (expected 50%+) ✓</p>
  
  <h3>ML vs Rule-Based Win Rate</h3>
  <p>ML: 68% (34/50 signals)</p>
  <p>Rules: 54% (27/50 signals)</p>
  <p>Improvement: +14 percentage points 🚀</p>
</section>
```

---

## ⚠️ ROLLBACK PLAN

**If ML fails in production:**

### Early Warning Signs
- ML win rate <50% (worse than random)
- ML picks obviously bad signals (scams, already pumped)
- ML scores all 5-6 (no differentiation)

### Immediate Actions
1. **Revert to rule-based scoring** (uncomment old code)
2. **Pause new ML deployments** (let existing positions close)
3. **Diagnose failure:**
   - Feature drift? (markets changed)
   - Model bug? (prediction error)
   - Training data issue? (garbage in, garbage out)

### Rollback Code (One-Liner)

```python
# In scrapers, change from:
conviction_score = self._calculate_conviction_ml(...)

# Back to:
conviction_score = self._calculate_conviction(...)  # Rule-based
```

**Time to rollback:** <5 minutes

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Deployment (Tonight)

- [ ] Train model on synthetic data (v0.1)
- [ ] Test model predictions (smoke test)
- [ ] Create `ml_scorer.py` wrapper
- [ ] Unit test ML scorer
- [ ] Verify model files exist and load correctly

### Phase 1: Parallel Scoring (Day 1-7)

- [ ] Add ML scoring to Yieldschool scraper
- [ ] Add ML scoring to Dumb Money scraper
- [ ] Deploy still uses rule-based scores
- [ ] Log both scores in database
- [ ] Collect 50+ signals with dual scores

### Phase 2: Hybrid Scoring (Day 8-14)

- [ ] Switch to hybrid scoring (30% rule, 70% ML)
- [ ] Deploy signals based on hybrid scores
- [ ] Track outcomes daily
- [ ] Compare win rate to pure rule-based
- [ ] Collect 50+ more signals

### Phase 3: Full ML Rollout (Day 15-21)

- [ ] If ML proves better → 100% ML scoring
- [ ] Retire rule-based (keep for audit logs only)
- [ ] Weekly retraining on new data
- [ ] Monitor for drift

### Month 2: Production Maturity

- [ ] Automated weekly retraining (cron job)
- [ ] A/B testing framework (test new models vs old)
- [ ] Drift detection alerts
- [ ] Performance dashboards

---

## 📈 SUCCESS METRICS

### Phase 1 Success (Parallel)
- ✅ ML model runs without errors
- ✅ Dual scores logged for 50+ signals
- ✅ ML scores show reasonable distribution (not all 5s)

### Phase 2 Success (Hybrid)
- ✅ Hybrid win rate ≥ rule-based win rate
- ✅ No catastrophic failures (scam signals deployed)
- ✅ Conviction calibration holds (score 9 → 70%+ wins)

### Phase 3 Success (Full ML)
- ✅ ML win rate >60%
- ✅ Beats rule-based by ≥10 percentage points
- ✅ No drift detected (performance stable)
- ✅ G approves full rollout 🐓

---

## 🐓 EXECUTION TIMELINE

**Tonight (Feb 5):**
- Build ML scorer wrapper
- Test integration with sample data
- Deploy to dev environment

**Tomorrow (Feb 6):**
- Morning: Scrape signals, test ML scoring in parallel
- Afternoon: Review ML vs rule outputs
- Evening: Report findings to G

**Week 1 (Feb 6-12):**
- Run Phase 1 (parallel scoring)
- Collect 50+ dual-scored signals
- Validate ML performance

**Week 2 (Feb 13-19):**
- Switch to Phase 2 (hybrid scoring)
- Track live outcomes
- A/B test results

**Week 3 (Feb 20-26):**
- Full rollout (Phase 3) if successful
- Weekly retraining begins

**Month 2 (March):**
- Production system running smoothly
- 500+ signals labeled
- Model accuracy improving with data

---

## 🎓 LESSONS TO CAPTURE

### What to Document

1. **Agreement Rate:** How often do rule vs ML pick same signals?
   - High agreement = ML learned rules (good start)
   - Low agreement = ML found new patterns (interesting)

2. **Disagreement Analysis:** When they disagree, who's right?
   - ML picks signal rules reject → track outcome
   - Rules pick signal ML rejects → track outcome

3. **Feature Importance:** Which features matter most in production?
   - Compare to training feature importance
   - Add/remove features based on live data

4. **Failure Modes:** What breaks the model?
   - Scam signals scored high?
   - Obvious winners scored low?
   - Fix in next training iteration

---

**Integration is the final 20% that makes ML useful. Let's ship it.** 🐓
