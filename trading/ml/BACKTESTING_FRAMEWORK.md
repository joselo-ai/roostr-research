# Backtesting Framework for ML Conviction Model
**Author:** Atlas (roostr ML Engineer AI)  
**Date:** Feb 5, 2026  
**Status:** Design Complete → Implementation Next

---

## 🎯 PURPOSE

Validate ML conviction model on historical data before live deployment.

**Key questions:**
1. If we deployed top 10% ML-scored signals, what would P&L be?
2. Does ML beat rule-based scoring?
3. Which conviction threshold (7+, 8+, 9+) has best risk/reward?
4. What's the optimal position sizing per conviction level?

---

## 🏗️ ARCHITECTURE

### High-Level Flow

```
Historical Signals (90 days)
    ↓
Feature Engineering
    ↓
ML Model Scores (0-10)
    ↓
Trading Strategy (position sizing, stops, targets)
    ↓
Simulated Trades (paper)
    ↓
Performance Metrics (Sharpe, win rate, max DD)
```

### Components

1. **Historical Data Loader** - Load past signals from database
2. **Feature Time Machine** - Extract features as they would've been known at signal time (no lookahead)
3. **Model Scorer** - Score signals with trained model
4. **Strategy Engine** - Decide which signals to deploy (top 10%, conviction 8+, etc)
5. **Trade Simulator** - Simulate entries, exits, P&L tracking
6. **Performance Reporter** - Calculate metrics, generate charts

---

## 📊 HISTORICAL DATA REQUIREMENTS

### Minimum Data Needed

To backtest ML model, we need:

**Required:**
- Ticker symbol
- Date signal appeared
- Price at signal date
- Price 7/30/60 days later (outcomes)
- Source (Yieldschool, Dumb Money, etc)
- Reactions, Dan endorsement, mention count

**Nice to have:**
- Google Trends at signal date
- On-chain data (if crypto)
- Thesis text (for NLP features)

### Data Collection Strategy

**Phase 1: Manual Scraping (Tonight)**
- Scrape last 90 days from Yieldschool Discord
- Scrape last 90 days from Dumb Money Discord
- Extract tickers, reactions, dates
- Lookup historical prices (Yahoo Finance API, CoinGecko)
- Label outcomes (did it 2x in 30 days?)

**Target:** 50-100 historical signals labeled by morning

**Phase 2: Automated Pipeline (Week 1)**
- Daily scraper saves signals to database with timestamp
- Auto-fetch prices 7/30/60 days later
- Auto-label outcomes
- Grows to 500+ samples in Month 2

---

## 🧪 BACKTESTING SCENARIOS

### Scenario 1: Top 10% ML Scores
**Strategy:**
- Score all historical signals with ML model
- Deploy top 10% (highest conviction)
- Fixed position size ($5k per trade)
- 2% stop loss, 2x target (100% gain)

**Metrics:**
- Win rate
- Avg % gain per trade
- Max drawdown
- Sharpe ratio

---

### Scenario 2: Conviction Threshold Test
**Strategy:**
- Deploy ALL signals above threshold (7, 8, or 9)
- Compare performance at each threshold
- Find optimal cutoff

**Expected:**
- Conviction 9-10: High precision, low recall (few trades, high win rate)
- Conviction 7-8: Medium precision, high recall (more trades, acceptable win rate)

---

### Scenario 3: ML vs Rule-Based
**Strategy:**
- Run parallel backtests:
  - Group A: Deploy top 10 by rule-based score
  - Group B: Deploy top 10 by ML score
- Compare outcomes

**Success:**
- ML beats rule-based by >10% win rate → full rollout
- ML ties → keep hybrid (ensemble safer)
- ML loses → iterate on features

---

### Scenario 4: Position Sizing Optimization
**Strategy:**
- Test Kelly Criterion sizing vs fixed size
- Kelly: Size = (Win% * AvgWin - Loss% * AvgLoss) / AvgWin
- ML probability guides sizing (9-10 conviction = 2x size)

**Goal:**
- Maximize risk-adjusted returns (Sharpe ratio)
- Avoid over-leveraging (Kelly often too aggressive, use 25% Kelly)

---

## 📈 PERFORMANCE METRICS

### Primary Metrics

1. **Win Rate:** % of trades that hit 2x target
   - Target: >60% for conviction 9-10
   - Baseline: >50% overall

2. **Precision:** % of high-conviction calls that actually win
   - Critical for trust (don't want false positives)

3. **Recall:** % of actual winners we caught
   - Don't want to miss obvious 10x plays

4. **Sharpe Ratio:** (Avg Return - Risk-Free Rate) / Std Dev
   - Target: >1.5 (acceptable risk-adjusted returns)
   - >2.0 = excellent

5. **Max Drawdown:** Largest peak-to-trough loss
   - Target: <20% (per allocation rules)

6. **Profit Factor:** Gross Profit / Gross Loss
   - Target: >2.0 (winners 2x bigger than losers)

---

### Secondary Metrics

7. **Avg % Gain per Winner:** How much do winners make?
8. **Avg % Loss per Loser:** How much do losers lose?
9. **Avg Days to Target:** How long to 2x?
10. **Recovery Time:** Days to recover from max drawdown
11. **Consecutive Losses:** Longest losing streak (psychology test)

---

## 🔧 IMPLEMENTATION

### Code Structure

```python
# backtest_model.py

class Backtester:
    def __init__(self, model, historical_data, strategy):
        self.model = model  # Trained ML model
        self.data = historical_data  # Historical signals + outcomes
        self.strategy = strategy  # Trading rules
        
    def run_backtest(self):
        # 1. Score all historical signals
        # 2. Select signals per strategy
        # 3. Simulate trades
        # 4. Calculate metrics
        # 5. Generate report
        
    def simulate_trade(self, signal, entry_price, outcome_prices):
        # Simulate single trade
        # Entry at signal date
        # Exit at stop/target/time limit
        # Return P&L, win/loss
        
    def calculate_metrics(self, trades):
        # Win rate, Sharpe, max DD, etc
        
    def plot_equity_curve(self, trades):
        # Visualize cumulative P&L over time
        
    def generate_report(self):
        # Markdown report + charts
```

---

### Backtesting Script Usage

```bash
# Backtest ML model on historical data
python3 backtest_model.py \
    --model models/conviction_v0.1.pkl \
    --data data/historical_signals.csv \
    --strategy top10 \
    --position-size 5000 \
    --output reports/backtest_v0.1.md
```

**Strategies:**
- `top10` - Top 10% by ML score
- `threshold8` - All signals score 8+
- `threshold9` - All signals score 9+
- `hybrid` - Weighted combo of rule + ML

---

### Example Output

```
BACKTEST RESULTS: Conviction Model v0.1
========================================
Period: 2025-09-01 to 2025-12-01 (90 days)
Total Signals: 87
Deployed: 9 (top 10%)

PERFORMANCE
-----------
Win Rate: 66.7% (6/9 wins)
Avg Win: +127% ($6,350 avg)
Avg Loss: -18% ($900 avg)
Net P&L: +$32,400 (+72% on $45k deployed)
Sharpe Ratio: 2.1
Max Drawdown: -8.4%
Profit Factor: 7.1

BEST TRADES
-----------
1. $TAO +1000% ($50k gain)
2. $PENDLE +215% ($10.7k gain)
3. $RNDR +98% ($4.9k gain)

WORST TRADES
-----------
1. $XYZ -22% ($1.1k loss)
2. $ABC -18% ($900 loss)

CONVICTION BREAKDOWN
--------------------
Score 9-10: 4 trades, 75% win rate
Score 8-9: 3 trades, 66% win rate
Score 7-8: 2 trades, 50% win rate

CONCLUSION
----------
✓ ML model beats baseline (rule-based: 52% win rate)
✓ Exceeds 60% precision target
✓ Top conviction (9-10) signals most reliable
✓ Ready for live deployment
```

---

## 📊 VISUALIZATION

### Charts to Generate

1. **Equity Curve** - Cumulative P&L over time
   - Shows growth trajectory
   - Highlights drawdown periods

2. **Win Rate by Conviction** - Bar chart
   - X-axis: Conviction score (7, 8, 9, 10)
   - Y-axis: Win %
   - Validates calibration

3. **Distribution of Returns** - Histogram
   - Shows spread of gains/losses
   - Asymmetric = good (big winners, small losers)

4. **Feature Importance in Winners** - SHAP plot
   - Which features predicted winners best?
   - Dan endorsement, multi-source, whale accumulation

5. **Drawdown Chart** - Underwater plot
   - Shows time spent in drawdown
   - Recovery speed

---

## ⚠️ BACKTESTING PITFALLS (TO AVOID)

### 1. Lookahead Bias
**Problem:** Using information not available at signal time

**Example:** Scoring signal with Google Trends from 7 days later

**Solution:** Feature time machine - only use data known at signal date

---

### 2. Survivorship Bias
**Problem:** Only testing on signals that we noticed (survivorship)

**Example:** Missing 50 signals that bombed before we saw them

**Solution:** Include ALL signals scraped, not just ones we liked

---

### 3. Overfitting
**Problem:** Model memorizes training data, doesn't generalize

**Example:** 95% backtest accuracy, 45% live accuracy

**Solution:**
- Use out-of-sample test set (data model hasn't seen)
- Walk-forward testing (train on Month 1, test on Month 2, retrain, test Month 3)

---

### 4. Transaction Costs Ignored
**Problem:** Backtest shows +50%, but fees/slippage eat 10%

**Solution:**
- Assume 0.5% slippage per trade (realistic for illiquid altcoins)
- Assume 0.1% exchange fees
- Deduct from P&L

---

### 5. Liquidity Illusion
**Problem:** Backtest assumes we can enter $10k position instantly

**Reality:** Low-cap crypto often <$50k daily volume

**Solution:**
- Filter signals by liquidity (min $100k on DEX)
- Assume 2-5% slippage on large orders

---

## 🚀 DEPLOYMENT PLAN

### Week 1: Build Backtesting Framework
- [ ] Implement `Backtester` class
- [ ] Collect 50-100 historical signals (manual scraping)
- [ ] Run backtest on historical data
- [ ] Generate first backtest report

### Week 2: Validate & Iterate
- [ ] Compare ML vs rule-based backtest results
- [ ] If ML wins → proceed to live testing
- [ ] If ML loses → improve features, retrain
- [ ] Run ablation tests (which features matter?)

### Week 3: Live Paper Trading
- [ ] Deploy ML model to production
- [ ] Score new signals as they appear
- [ ] Track outcomes for 30 days
- [ ] Compare live results to backtest (detect drift)

### Month 2: Full Rollout
- [ ] If live results match backtest → full confidence
- [ ] Retire rule-based system (100% ML)
- [ ] Automate weekly retraining
- [ ] Build drift monitoring alerts

---

## 🔄 WALK-FORWARD TESTING

**Problem:** Single backtest = cherry-picking best period

**Solution:** Walk-forward (rolling window)

### Process

1. **Month 1 (Sep):** Train on synthetic data, test on Sep signals
2. **Month 2 (Oct):** Retrain with Sep outcomes, test on Oct signals
3. **Month 3 (Nov):** Retrain with Sep+Oct, test on Nov signals

**Metrics:** Average performance across all test periods

**Realistic:** Simulates real-world retraining schedule

---

## 📝 BACKTEST REPORT TEMPLATE

```markdown
# Backtest Report: Conviction Model v0.1

## Summary
- **Period:** Sep 1 - Dec 1, 2025 (90 days)
- **Strategy:** Top 10% ML scores, $5k per trade
- **Total Signals:** 87
- **Deployed:** 9 trades

## Performance
- **Win Rate:** 66.7% (6/9)
- **Net P&L:** +$32,400 (+72%)
- **Sharpe Ratio:** 2.1
- **Max Drawdown:** -8.4%

## Trades
[Table of all trades: ticker, entry, exit, P&L, conviction]

## Conviction Calibration
[Chart showing win rate by conviction score]

## ML vs Baseline
- **ML Model:** 66.7% win rate
- **Rule-Based:** 52% win rate
- **Improvement:** +14.7 percentage points

## Conclusion
✓ Model ready for live deployment
```

---

## 🎓 LEARNING FROM BACKTEST

### What to Look For

**Good signs:**
- High conviction (9-10) signals win most (>70%)
- Equity curve smooth upward (not erratic)
- Max drawdown <15%
- Sharpe >1.5

**Red flags:**
- Win rate <55% (not better than random)
- Huge variance (one 10x trade masks 9 losers)
- Max drawdown >25% (unacceptable risk)
- Model confidence uncalibrated (all scores 5-6, no differentiation)

**Action:**
- If green flags → deploy confidently
- If red flags → iterate on features, collect more data

---

## 🐓 NEXT STEPS (Tonight)

1. ✅ Design complete (this document)
2. ⏳ Implement `Backtester` class (backtest_model.py)
3. ⏳ Scrape 50 historical signals manually
4. ⏳ Run first backtest
5. ⏳ Generate backtest report

**Goal:** Have backtest results by morning to show G.

---

**Backtesting = confidence before deployment. No shortcuts.** 🐓
