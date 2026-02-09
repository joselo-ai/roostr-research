# Quant Agent - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Verify Installation

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/agents
python3 test_quant_agent.py
```

You should see: `✅ ALL TESTS PASSED`

---

### Step 2: Run Your First Backtest

```bash
# Full analysis on all signals
cd /Users/agentjoselo/.openclaw/workspace/trading
python3 agents/quant_agent.py --mode full
```

**Output:** 
- Full report in `trading/reports/quant_report_*.txt`
- Trade details in `trading/reports/trades_*.csv`
- Metrics JSON in `trading/reports/metrics_*.json`

---

### Step 3: Test a Single Trade

```bash
# Quick backtest on TAO signal
python3 agents/quant_agent.py \
    --mode quick \
    --ticker TAO \
    --price 176.05 \
    --date 2026-02-06
```

**Example Output:**
```json
{
  "ticker": "TAO",
  "entry_price": 176.05,
  "exit_price": 140.84,
  "pnl": -691.00,
  "return_pct": -6.91,
  "hold_days": 15,
  "exit_reason": "STOP_LOSS"
}
```

---

## 📊 Reading the Report

### Key Metrics to Watch

1. **Win Rate** (aim for >50%)
   - Percentage of profitable trades
   - Higher is better, but quality matters more than quantity

2. **Sharpe Ratio** (aim for >1.0)
   - Risk-adjusted returns
   - >1.0 = good, >2.0 = excellent

3. **Maximum Drawdown** (keep under -20%)
   - Largest peak-to-trough loss
   - Measures worst-case scenario

4. **Profit Factor** (aim for >1.5)
   - Ratio of gross profits to losses
   - >2.0 is strong

### Sample Report Interpretation

```
Win Rate: 60%              ✅ Good - More wins than losses
Sharpe Ratio: 1.45         ✅ Strong - Good risk-adjusted returns
Max Drawdown: -12.5%       ✅ Acceptable - Controlled risk
Profit Factor: 2.1         ✅ Excellent - Winners outweigh losers
```

---

## 🔧 Common Commands

### Change Parameters

```bash
# More conservative (smaller positions, tighter stops)
python3 agents/quant_agent.py \
    --mode full \
    --position-size 0.05 \
    --stop-loss 0.10 \
    --take-profit 0.20

# More aggressive
python3 agents/quant_agent.py \
    --mode full \
    --position-size 0.20 \
    --stop-loss 0.30 \
    --take-profit 0.50
```

### Custom Starting Capital

```bash
python3 agents/quant_agent.py --mode full --capital 50000
```

---

## 📈 Interpreting Statistical Tests

### Information Coefficient (IC)

```
Pearson IC: 0.3456 (p=0.0234)
```

- **IC = 0.35** → Good predictive signal
- **p = 0.02** → Statistically significant (luck ruled out)

**Interpretation:** Your conviction scores correlate with actual returns. Trust the high-conviction signals!

### Monte Carlo Simulation

```
Percentile Rank: 75.5%
```

- **>95%** = Exceptional (top 5%)
- **75-95%** = Good performance
- **50-75%** = Average
- **<50%** = Below average (may be luck)

**Interpretation:** If your strategy ranks in top 25%, it's skill-based, not luck.

---

## 🎯 Next Steps

### Daily Workflow

1. **Morning**: Check new signals
   ```bash
   python3 agents/quant_agent.py --mode quick --ticker <TICKER> --price <PRICE> --date <DATE>
   ```

2. **Weekly**: Full strategy review
   ```bash
   python3 agents/quant_agent.py --mode full
   ```

3. **Monthly**: Parameter optimization
   - Test different stop-loss levels
   - Adjust position sizing
   - Review exit statistics

### Integration Tips

**Add to Price Updater:**
```python
# In update_prices_worker.py
from agents.quant_agent import QuantAgent

agent = QuantAgent()
result = agent.quick_backtest(ticker, price, date)
if result['return_pct'] > 10:
    print("🚀 Strong signal!")
```

**Add to Dashboard:**
```bash
python3 agents/dashboard_integration.py
```

---

## ❓ Troubleshooting

### "No module named 'pandas'"

```bash
pip3 install pandas numpy yfinance scipy matplotlib
```

### "No data found for ticker"

Crypto tickers need `-USD` suffix:
- TAO → TAO-USD
- SOL → SOL-USD
- ETH → ETH-USD

The agent handles this automatically.

### "Insufficient data for validation"

Need at least 3 trades. Deploy more signals first, then re-run backtest.

---

## 📚 Learn More

- **Full Documentation:** `README.md` in this folder
- **Sample Report:** `SAMPLE_BACKTEST_REPORT.txt`
- **Main Trading README:** `../README.md`

---

## 🎓 Pro Tips

1. **Start Conservative**
   - Use smaller position sizes initially
   - Tighten stop-losses until you're confident
   - Build up gradually as you gain experience

2. **Trust the Numbers**
   - If Sharpe ratio < 1.0, improve risk management
   - If win rate < 40%, review entry criteria
   - If max drawdown > 25%, reduce position sizes

3. **Keep Learning**
   - Review exit reasons - are you hitting stops or targets?
   - Check average hold time - too long means bad timing
   - Monitor correlation - avoid redundant signals

4. **Backtest Everything**
   - Never deploy without backtesting first
   - Quick backtest takes 10 seconds, could save thousands
   - Weekly full analysis keeps strategy on track

---

**Questions?** Check the main README or examine the sample reports.

**Ready to deploy?** Start with small positions and scale up as confidence grows.

**Remember:** Past performance doesn't guarantee future results, but it's better than guessing! 📊
