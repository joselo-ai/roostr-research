# ML Conviction Scoring Model - Architecture Design
**Built:** Feb 5, 2026  
**Owner:** Atlas (roostr ML Engineer AI)  
**Status:** 🟢 Prototype Ready for Training

---

## 🎯 MISSION

Replace rule-based conviction scoring with ML model that learns from:
1. Dan's $500→$500k (1000x) track record on $TAO
2. Historical signal performance data
3. Multi-source validation (reactions, trends, on-chain)
4. Green flags > Red flags methodology

**Goal:** Predict which signals will 2x+ within 30 days with >60% accuracy

---

## 🧠 MODEL ARCHITECTURE

### Approach: Gradient Boosting Ensemble (XGBoost)

**Why XGBoost over Deep Learning:**
- **Tabular data dominance:** Financial features are structured/tabular
- **Feature importance:** Interpretable - we can see WHY model scores high
- **Sample efficiency:** Works with smaller datasets (100-500 samples vs 10k+ for NN)
- **Fast inference:** <1ms prediction time for real-time scoring
- **Proven in finance:** Kaggle winners, hedge funds use GBM for alpha

**Architecture:**
```
Input: 45+ features (reactions, source, Dan endorsement, trends, on-chain, thesis)
  ↓
Feature Engineering Layer (ratios, interactions, temporal)
  ↓
XGBoost Classifier (Binary: Will it 2x in 30 days?)
  ↓
Output: Conviction probability (0-1) → Scale to 1-10 score
```

**Hyperparameters (starting point):**
- Max depth: 6 (prevent overfitting on small data)
- Learning rate: 0.05 (slower but more stable)
- N estimators: 100-300 (early stopping on validation)
- Min child weight: 3 (conservative splits)
- Subsample: 0.8 (row sampling for regularization)
- Colsample_bytree: 0.8 (feature sampling)

---

## 📊 FEATURE ENGINEERING (Dan's Green Flags Framework)

### Core Feature Categories

#### 1. Source Credibility (15 features)
**Dan's principle:** "Who's calling it matters more than what they're calling"

| Feature | Description | Dan Weight |
|---------|-------------|------------|
| `dan_endorsed` | Binary: Dan explicitly mentioned | 🟢 GREEN FLAG (+3) |
| `source_yieldschool` | Binary: From Yieldschool | +2 |
| `source_bluechips` | Binary: From Blue-Chips channel | +1.5 |
| `source_dumbmoney` | Binary: From Dumb Money | +1 |
| `mention_count` | Times mentioned across sources | +0.5 per mention |
| `multi_source` | Binary: 2+ sources | +2 |
| `source_reliability_score` | Historical win rate of source | 0-1 |
| `poster_historical_accuracy` | If we track individual posters | 0-1 |

**Dan's lesson:** His $TAO call worked because he has track record. Source credibility > thesis quality.

---

#### 2. Social Conviction (12 features)
**Dan's principle:** "Green flags > Red flags - look for overwhelming positives"

| Feature | Description | Dan Weight |
|---------|-------------|------------|
| `total_reactions` | Sum of all reactions | +0.1 per reaction |
| `fire_reactions` | 🔥 count | +0.15 per (strong conviction) |
| `rocket_reactions` | 🚀 count | +0.15 per |
| `reaction_velocity` | Reactions per hour since post | 🟢 Fast = early |
| `reaction_diversity` | Unique reactors (not bot spam) | +0.2 per unique |
| `comment_count` | Discussion volume | +0.1 per comment |
| `sentiment_score` | NLP on comments (0-1 positive) | 0-1 |
| `hype_ratio` | (🚀+🔥) / (total reactions) | >0.5 = hype |
| `thesis_quality_score` | Length + keywords (revenue, moat) | 0-1 |
| `link_count` | Research links shared | +0.5 per link |
| `emoji_spam_penalty` | 🚀🚀🚀🚀 = -1 (hype not conviction) | -1 if spam |
| `reaction_recency` | <24h old = fresh | 🟢 GREEN FLAG |

**Dan's lesson:** $TAO had overwhelming green flags (tech working, Dan's endorsement, rising mentions). No red flags (not pumped yet, real product).

---

#### 3. Market Timing (10 features)
**Dan's principle:** "Early is on-time, on-time is late"

| Feature | Description | Dan Weight |
|---------|-------------|------------|
| `google_trends_now` | Current search volume (0-100) | Base metric |
| `google_trends_7d_change` | % change last 7 days | 🟢 +50%+ rising |
| `google_trends_30d_change` | % change last 30 days | 🔴 +200%+ late |
| `trends_peak_ratio` | Current / all-time high | <0.5 = early |
| `message_age_hours` | Hours since first mention | <48h = fresh |
| `price_vs_mention` | Current price / price at mention | <1.1 = not pumped |
| `volume_spike` | Volume vs 30d avg | >3x = momentum |
| `new_token` | Days since token launch | <30d = early |
| `liquidity_level` | DEX liquidity ($) | >$100k = real |
| `holder_growth` | New holders last 7d | +10%+ = adoption |

**Dan's lesson:** $TAO wasn't mainstream when Dan called it. Google Trends were rising but not peaked. Perfect timing.

---

#### 4. On-Chain Signals (Crypto Only, 8 features)

| Feature | Description | Dan Weight |
|---------|-------------|------------|
| `whale_accumulation` | Top 10 wallets bought last 7d | 🟢 GREEN FLAG |
| `smart_money_holdings` | Known smart wallets hold | +2 |
| `liquidity_locked` | % liquidity locked | >50% = safer |
| `contract_verified` | Binary: verified on explorer | Must have |
| `honeypot_score` | Scam detection (0-1) | 0 = safe |
| `holder_concentration` | Top 10 hold % | <50% = distributed |
| `dex_listing_count` | Listings across DEXs | 2+ = liquid |
| `volume_authenticity` | Real vs wash trading | >0.8 = real |

**Dan's lesson:** On-chain validates off-chain hype. If smart money accumulating = early signal.

---

#### 5. Fundamental Quality (Stocks/Thesis, 10 features)

| Feature | Description | Dan Weight |
|---------|-------------|------------|
| `thesis_length` | Word count of thesis | >100 words = detailed |
| `thesis_keywords` | "revenue", "moat", "growth" count | +0.5 per keyword |
| `financial_metrics` | Mentions P/E, revenue, etc | +1 if present |
| `catalyst_mentioned` | "approval", "earnings", "launch" | 🟢 GREEN FLAG |
| `competitive_advantage` | "first mover", "patent", "network" | +1 |
| `addressable_market` | "$XB TAM" mentioned | +1 |
| `team_quality` | "experienced", "Y Combinator" | +0.5 |
| `partnerships` | Named partners (AT&T, etc) | +0.5 per partner |
| `regulatory_risk` | "FCC", "FDA", "approval" | 🔴 RED FLAG if blocked |
| `hype_language_penalty` | "moon", "lambo", "100x" | -1 per hype word |

**Dan's lesson:** $TAO had real tech (not vaporware). Product working = green flag. Hype without product = red flag.

---

### Feature Interactions (5 computed features)

These capture non-linear relationships:

1. **`dan_x_reactions`:** `dan_endorsed * total_reactions` (Dan + crowd = strongest)
2. **`early_momentum`:** `reaction_velocity * (1 - trends_peak_ratio)` (fast + early = best)
3. **`source_consensus`:** `multi_source * mention_count` (cross-validation)
4. **`conviction_quality`:** `reaction_diversity * thesis_quality_score` (real conviction not bots)
5. **`smart_timing`:** `whale_accumulation * (message_age_hours < 48)` (smart money early)

---

## 🎯 TARGET VARIABLE (What We're Predicting)

### Binary Classification: **Will it 2x+ in 30 days?**

**Label:** `hit_target` (0 or 1)

**Definition:**
- 1 = Price reached 2x (100% gain) within 30 days of signal
- 0 = Did not reach 2x within 30 days

**Why 2x / 30 days:**
- Aggressive enough to matter (2x = meaningful win)
- Short enough to validate fast (30 days = don't wait months)
- Dan's $TAO did 10x+ (2x is conservative baseline)

**Alternative targets (for future models):**
- Regression: Predict % gain in 30 days (continuous)
- Multi-class: <50% / 50-100% / 100-300% / >300% (risk tiers)

---

## 📦 TRAINING DATA FORMAT

### CSV Schema: `ml_training_data.csv`

```csv
ticker,source,date_found,dan_endorsed,mention_count,multi_source,total_reactions,fire_reactions,rocket_reactions,reaction_velocity,reaction_diversity,comment_count,sentiment_score,hype_ratio,thesis_quality_score,link_count,emoji_spam,reaction_recency,google_trends_now,google_trends_7d_change,google_trends_30d_change,trends_peak_ratio,message_age_hours,price_at_mention,current_price,price_vs_mention,volume_spike,new_token,liquidity_level,holder_growth,whale_accumulation,smart_money_holdings,liquidity_locked,contract_verified,honeypot_score,holder_concentration,dex_listing_count,volume_authenticity,thesis_length,thesis_keywords,financial_metrics,catalyst_mentioned,competitive_advantage,addressable_market,team_quality,partnerships,regulatory_risk,hype_language_penalty,dan_x_reactions,early_momentum,source_consensus,conviction_quality,smart_timing,hit_target
TAO,Yieldschool-YieldHub,2025-09-15,1,5,1,67,34,18,2.3,45,12,0.85,0.78,0.92,3,0,1,23,85,150,0.31,18,12.50,1250.00,1.05,4.2,0,850000,18,1,1,0.65,1,0,0.38,3,0.88,156,8,1,1,1,1,0.9,2,0,0,67,1.58,5,41.4,1,1
ASTS,DumbMoney,2025-11-20,0,2,0,52,28,14,1.8,38,8,0.78,0.81,0.88,2,0,1,45,65,95,0.52,24,8.20,14.80,1.12,2.1,0,0,0,0,0,0,0,0,0,0,0,124,6,1,1,1,1,0.85,1,0,0,0,0.86,2,33.44,0,0
```

**Key:**
- **Features:** Columns 4-52 (input variables)
- **Target:** Column 53 `hit_target` (0 or 1)
- **Metadata:** Columns 1-3 (ticker, source, date) - not used in training but for tracking

---

## 🏋️ TRAINING METHODOLOGY

### Phase 1: Bootstrap Training (Cold Start)

**Problem:** We don't have 1000 labeled signals yet (Day 1)

**Solution: Synthetic + Manual Labeling + Backtesting**

1. **Historical signals:** Scrape last 90 days from Yieldschool/Dumb Money
2. **Manual labeling:** Label 50-100 signals as hit/miss based on price history
3. **Synthetic data:** Augment with slight perturbations (±10% feature noise)
4. **Transfer learning:** Use public crypto datasets (Kaggle, Santiment)

**Initial training set:** 200-300 samples (mix of real + synthetic)

---

### Phase 2: Active Learning (Weeks 2-4)

**Process:**
1. Model scores all new signals (0-10)
2. Deploy trades on top 10% (highest scores)
3. Track outcomes for 30 days
4. Label as hit/miss and retrain weekly
5. Model improves as data accumulates

**Growth:** +50 new labeled signals per week → 500+ samples by Month 2

---

### Phase 3: Continuous Learning (Months 2-3)

**Production loop:**
- Retrain model every 7 days with new data
- A/B test new model vs old (deploy 50/50 split)
- Promote new model if accuracy +2% or better
- Archive old model versions for rollback

---

### Train/Validation/Test Split

**Split strategy:**
- **Train:** 70% of data (oldest signals)
- **Validation:** 15% (tune hyperparameters, prevent overfitting)
- **Test:** 15% (held out for final accuracy report)

**Time-based split:** Train on Month 1, validate on Month 2, test on Month 3 (prevent lookahead bias)

---

## 📈 ACCURACY TARGETS & VALIDATION

### Success Metrics

**Minimum Viable Performance (MVP):**
- **Precision:** >60% (60% of predicted winners actually win)
- **Recall:** >50% (catch 50% of all winners)
- **AUC-ROC:** >0.70 (model distinguishes winners from losers)
- **Conviction calibration:** Score 9-10 signals hit 2x at 70%+ rate

**Stretch Goals (Month 3):**
- **Precision:** >70%
- **Recall:** >60%
- **AUC-ROC:** >0.80
- **Conviction calibration:** Score 9-10 → 80%+ hit rate

---

### Validation Methods

#### 1. K-Fold Cross-Validation (Training Phase)
- 5-fold CV on training set
- Track mean + std of accuracy (detect high variance = overfitting)
- Use stratified folds (balanced hit/miss ratio)

#### 2. Backtesting (Historical Validation)
- Test model on last 90 days of historical data (before training)
- Simulate: "If we deployed top 10 signals, what P&L?"
- Compare to rule-based system (baseline)

#### 3. Paper Trading (Live Validation)
- Deploy top-scored signals in paper account
- Track 30-day outcomes
- Calculate Sharpe ratio, max drawdown, win rate

#### 4. Feature Importance Analysis
- SHAP values to explain predictions
- Verify model uses sensible features (Dan endorsement high, hype spam low)
- Detect if model overfitting to noise

---

### Monitoring & Drift Detection

**Track weekly:**
- **Feature distribution drift:** Are new signals different from training data?
- **Prediction drift:** Is model scoring consistently over time?
- **Outcome drift:** Are markets changing (crypto winter vs bull)?

**Alerts:**
- If test accuracy drops >5% → retrain immediately
- If feature drift >20% → collect more data in new regime
- If precision <55% for 2 weeks → investigate model failure

---

## 🏗️ IMPLEMENTATION STACK

### Core Libraries

```python
# ML Framework
import xgboost as xgb  # Gradient boosting
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import precision_score, recall_score, roc_auc_score, confusion_matrix

# Feature Engineering
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Model Interpretation
import shap  # SHAP values for feature importance

# Backtesting
import backtrader as bt  # Trading backtesting framework

# Data Collection
import requests  # API calls (Dexscreener, Google Trends)
from pytrends.request import TrendReq  # Google Trends
```

---

### File Structure

```
trading/ml/
├── conviction_model.py          # Main model class
├── feature_engineering.py       # Transform raw signals → features
├── train_model.py               # Training pipeline
├── backtest_model.py            # Backtesting framework
├── predict_signal.py            # Real-time scoring for new signals
├── data/
│   ├── ml_training_data.csv     # Labeled training data
│   ├── raw_signals.csv          # Unlabeled signals from scrapers
│   └── model_versions/          # Saved models by date
├── models/
│   ├── conviction_v1.pkl        # Trained XGBoost model
│   ├── scaler.pkl               # Feature scaler
│   └── feature_names.json       # Feature column order
├── reports/
│   ├── training_report.md       # Accuracy metrics
│   ├── feature_importance.png   # SHAP plot
│   └── backtest_results.csv     # Historical performance
└── ML_CONVICTION_MODEL_DESIGN.md  # This document
```

---

## 🔄 INTEGRATION WITH EXISTING SCRAPERS

### Current Flow (Rule-Based)
```
Scraper → Extract signals → Calculate conviction (rules) → Filter GREEN → Deploy
```

### New Flow (ML-Enhanced)
```
Scraper → Extract signals → Feature engineering → ML model scores → Rank by score → Deploy top 10%
```

### Hybrid Approach (Phase 1)
```
Scraper → Extract signals
  ↓
Rule-based score (baseline)
  ↓
ML score (parallel)
  ↓
Final score = 0.3 * rule + 0.7 * ML  (gradual transition)
  ↓
Deploy top signals
```

**Why hybrid:**
- Don't abandon working rules immediately
- Gradual transition builds confidence
- ML model might fail early (limited data)
- Fallback to rules if ML breaks

**Transition plan:**
- Week 1: 70% rules, 30% ML
- Week 2: 50/50
- Week 3: 30% rules, 70% ML
- Month 2: 100% ML (if accuracy >60%)

---

### Code Integration Points

#### 1. Yieldschool Scraper
**Current:** `_calculate_conviction(message, ticker) → int (1-10)`

**New:**
```python
def _calculate_conviction_ml(self, message, ticker, historical_data):
    # Extract features from message
    features = self.feature_engineer.extract_features(message, ticker, historical_data)
    
    # Load trained model
    model = self.load_model('models/conviction_v1.pkl')
    
    # Predict conviction probability
    prob = model.predict_proba([features])[0][1]  # P(hit_target=1)
    
    # Scale to 1-10
    ml_score = int(prob * 10)
    
    # Hybrid: combine with rule-based
    rule_score = self._calculate_conviction(message, ticker)
    final_score = int(0.3 * rule_score + 0.7 * ml_score)
    
    return final_score
```

#### 2. Dumb Money Scraper
**Current:** `_calculate_conviction(total_reactions, content) → int (1-10)`

**New:**
```python
def _calculate_conviction_ml(self, signal_dict):
    # Extract all features
    features = self.feature_engineer.extract_dumbmoney_features(signal_dict)
    
    # Predict
    model = self.load_model('models/conviction_v1.pkl')
    prob = model.predict_proba([features])[0][1]
    
    ml_score = int(prob * 10)
    
    # Hybrid
    rule_score = self._calculate_conviction(signal_dict['total_reactions'], signal_dict['content'])
    final_score = int(0.3 * rule_score + 0.7 * ml_score)
    
    return final_score, prob  # Return both score and raw probability
```

---

## 🧪 A/B TESTING FRAMEWORK

### Test: Rule-Based vs ML-Based Scoring

**Setup:**
- Collect 100 signals in 7 days
- **Group A (Control):** Deploy top 10 signals by rule-based score
- **Group B (Treatment):** Deploy top 10 signals by ML score
- Track 30-day outcomes for both groups

**Metrics:**
- Win rate (% that hit 2x)
- Avg % gain
- Max drawdown
- Sharpe ratio

**Decision:**
- If ML wins by >10% win rate → full rollout
- If ML loses → iterate on features, retrain
- If tie → keep hybrid (ensemble = safer)

---

### Test: Feature Ablation (Which Features Matter?)

**Setup:**
- Train 5 models, each with 1 feature category removed:
  1. No source credibility
  2. No social conviction
  3. No market timing
  4. No on-chain signals
  5. No fundamental quality

**Metrics:**
- Compare AUC-ROC across models
- Identify which category contributes most

**Outcome:**
- Drop low-value features (reduce overfitting)
- Double down on high-value features (collect more data)

---

## 📊 REPORTING & DASHBOARDS

### Weekly Training Report (Auto-Generated)

**File:** `ml/reports/training_report_YYYY-MM-DD.md`

**Sections:**
1. **Model Performance**
   - Accuracy, Precision, Recall, AUC-ROC
   - Confusion matrix
   - Calibration plot (predicted prob vs actual outcome)

2. **Feature Importance**
   - Top 10 features by SHAP value
   - Plot: Feature contribution to predictions

3. **Sample Predictions**
   - Show 5 high-conviction signals model scored 9-10
   - Show 5 low-conviction signals model scored 1-3
   - Explain why (feature breakdown)

4. **Model Drift**
   - Feature distribution changes
   - Prediction drift over time

5. **Recommendations**
   - Which features to collect more data on
   - Model improvements to test

---

### Live Conviction Scoreboard

**Add to `dashboard.html`:**

```html
<section id="ml-conviction">
  <h2>🧠 ML Conviction Scores (Live)</h2>
  <table>
    <tr>
      <th>Ticker</th>
      <th>Source</th>
      <th>ML Score</th>
      <th>Rule Score</th>
      <th>P(2x in 30d)</th>
      <th>Top Features</th>
    </tr>
    <tr>
      <td>$TAO</td>
      <td>Yieldschool</td>
      <td>9.2</td>
      <td>8.5</td>
      <td>78%</td>
      <td>dan_endorsed, multi_source, whale_accumulation</td>
    </tr>
  </table>
</section>
```

---

## 🚀 DEPLOYMENT PLAN

### Week 1: Build Foundation
- [ ] Implement feature engineering pipeline
- [ ] Build training data collection script
- [ ] Manually label 50 historical signals
- [ ] Train initial model (v0.1)
- [ ] Validate on backtested data

### Week 2: Integrate with Scrapers
- [ ] Add ML scoring to Yieldschool scraper
- [ ] Add ML scoring to Dumb Money scraper
- [ ] Deploy hybrid scoring (30% rule, 70% ML)
- [ ] Collect 50 new labeled signals from paper trades

### Week 3: A/B Test & Iterate
- [ ] Run A/B test (rule vs ML)
- [ ] Analyze feature importance
- [ ] Retrain model with Week 2 data (v0.2)
- [ ] Update dashboards with ML scores

### Month 2: Production Ready
- [ ] Achieve >60% precision on test set
- [ ] Deploy 100% ML scoring (retire rule-based)
- [ ] Automate weekly retraining
- [ ] Build monitoring alerts (drift detection)

---

## 🎯 NEXT STEPS (Tonight)

**Deliverables due by morning:**
1. ✅ ML model architecture design (this document)
2. ⏳ Feature engineering code (`feature_engineering.py`)
3. ⏳ Training data schema + sample data (`ml_training_data.csv`)
4. ⏳ Prototype model code (`conviction_model.py`)
5. ⏳ Training pipeline (`train_model.py`)
6. ⏳ Backtesting framework design
7. ⏳ Integration plan (update scrapers)

**Building now:** Prototype code + sample data

---

**Atlas, signing off.** 🤖 Building the rest now.
