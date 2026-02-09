# Quant Agent - Statistical Analysis & Backtesting System

**Version:** 1.0.0  
**Author:** OpenClaw Trading System  
**Purpose:** Production-grade quantitative analysis and strategy validation

---

## 🎯 Overview

The Quant Agent is a specialized AI system for rigorous backtesting and statistical validation of trading strategies. It provides institutional-quality analysis tools for retail traders.

### Key Features

✅ **Comprehensive Backtesting**
- Realistic trade simulation with fees and slippage
- Stop-loss and take-profit management
- Position sizing optimization
- Historical price data from yfinance

✅ **Statistical Validation**
- Information Coefficient (IC) analysis
- Hypothesis testing (t-tests, p-values)
- Sharpe ratio significance testing
- Monte Carlo simulations
- Overfitting detection

✅ **Performance Metrics**
- Win rate, profit factor, Sharpe ratio
- Maximum drawdown, CAGR
- Risk-adjusted returns
- Trade distribution analysis

✅ **Risk Management**
- Kelly Criterion position sizing
- Risk/reward calculation
- Portfolio-level risk metrics

---

## 📦 Installation

### Prerequisites

```bash
# Required Python packages
pip install pandas numpy yfinance scipy matplotlib

# Or install from requirements
cd /Users/agentjoselo/.openclaw/workspace/trading
pip install -r requirements.txt
```

### Directory Structure

```
trading/
├── agents/
│   ├── __init__.py
│   ├── quant_agent.py          # Main agent
│   └── README.md               # This file
├── backtest.py                 # Backtesting engine
├── validation.py               # Statistical validation
├── reports/                    # Generated reports
└── signals-database.csv        # Signal data
```

---

## 🚀 Quick Start

### 1. Full Strategy Analysis

```python
from agents.quant_agent import QuantAgent

# Initialize agent
agent = QuantAgent()

# Run full analysis on your signals
report = agent.analyze_strategy(signals_source='database')
print(report)

# Results saved to: trading/reports/
```

### 2. Quick Single-Trade Backtest

```python
# Test a single trade idea
result = agent.quick_backtest(
    ticker='SOL',
    entry_price=86.51,
    entry_date='2026-02-06'
)

print(f"P&L: ${result['pnl']:.2f}")
print(f"Return: {result['return_pct']:.2f}%")
```

### 3. Custom Configuration

```python
from backtest import BacktestConfig

config = BacktestConfig(
    starting_capital=100000,      # $100k starting capital
    position_size_pct=0.10,       # 10% per position
    commission_pct=0.001,         # 0.1% commission
    slippage_pct=0.0005,          # 0.05% slippage
    stop_loss_pct=0.20,           # 20% stop loss
    take_profit_pct=0.30,         # 30% take profit
    max_hold_days=90              # Max 90 days hold
)

agent = QuantAgent(config)
```

---

## 💻 Command Line Usage

### Full Analysis

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading

# Run full backtest on default signals database
python agents/quant_agent.py --mode full

# Use custom signals file
python agents/quant_agent.py --mode full --signals path/to/signals.csv

# Custom parameters
python agents/quant_agent.py \
    --mode full \
    --capital 50000 \
    --position-size 0.15 \
    --stop-loss 0.15 \
    --take-profit 0.40
```

### Quick Backtest

```bash
# Test single trade
python agents/quant_agent.py \
    --mode quick \
    --ticker TAO \
    --price 176.05 \
    --date 2026-02-06
```

---

## 📊 Understanding the Output

### Backtest Report

```
╔══════════════════════════════════════════════════════════════╗
║          BACKTEST PERFORMANCE REPORT                         ║
╚══════════════════════════════════════════════════════════════╝

📊 SUMMARY STATISTICS
──────────────────────────────────────────────────────────────
Total Trades:              25
Winning Trades:            15 (60.0%)
Losing Trades:             10
Average Hold Period:       32.5 days

💰 PROFIT & LOSS
──────────────────────────────────────────────────────────────
Initial Capital:           $100,000.00
Final Equity:              $115,230.50
Total P&L:                 $15,230.50
Total Return:              15.23%
CAGR:                      18.45%

⚠️  RISK METRICS
──────────────────────────────────────────────────────────────
Maximum Drawdown:          -12.5%
Sharpe Ratio:              1.45
Win Rate:                  60.0%
```

### Key Metrics Explained

**Win Rate:** Percentage of profitable trades (aim for >50%)

**Profit Factor:** Ratio of gross profits to gross losses (>1.5 is good)

**Sharpe Ratio:** Risk-adjusted return (>1.0 is good, >2.0 is excellent)

**Maximum Drawdown:** Largest peak-to-trough decline (keep under 20%)

**CAGR:** Compound Annual Growth Rate (annualized return)

---

## 📈 Statistical Validation

### Information Coefficient (IC)

Measures correlation between predictions (conviction scores) and actual returns.

- **IC > 0.10:** Strong predictive signal
- **IC > 0.05:** Good signal
- **IC < 0:** Bad signal (inverse relationship)

```python
# IC is automatically calculated if conviction scores exist
validation = agent.run_validation()
print(validation['ic'])
```

### Hypothesis Testing

Tests if strategy returns are statistically significant (not due to luck).

- **p-value < 0.05:** Statistically significant
- **p-value < 0.01:** Highly significant

### Monte Carlo Simulation

Randomly reorders trades 1000 times to test robustness.

- **Percentile Rank > 95%:** Performance is likely skill-based
- **Percentile Rank < 50%:** Performance may be luck-based

---

## 🎲 Position Sizing

### Kelly Criterion

The agent calculates optimal position sizes using the Kelly Criterion:

```python
sizing = agent.calculate_position_sizing(
    ticker='TAO',
    entry_price=176.05,
    risk_per_trade=0.02  # 2% risk per trade
)

print(f"Recommended shares: {sizing['recommended_shares']}")
print(f"Position value: ${sizing['recommended_value']:.2f}")
```

**Output:**
```json
{
  "ticker": "TAO",
  "entry_price": 176.05,
  "current_equity": 100000,
  "recommended_shares": 45.2,
  "recommended_value": 7956.66,
  "recommended_pct_portfolio": 7.96,
  "risk_reward_ratio": 1.5
}
```

---

## 🔬 Advanced Usage

### Walk-Forward Validation

Test strategy consistency across time periods:

```python
from validation import SignalValidator

validator = SignalValidator()
wf_results = validator.walk_forward_validation(
    signals_df,
    window_size=20,  # 20 trades training
    test_size=5      # 5 trades testing
)

for window in wf_results['windows']:
    print(f"Window {window['window_id']}: {window['test_period']}")
```

### Overfitting Detection

Compare train vs. test performance:

```python
# Run backtest on training data
train_metrics = agent.backtester.calculate_metrics()

# Run backtest on test data (holdout set)
# ... load test signals ...
test_metrics = agent.backtester.calculate_metrics()

# Check for overfitting
overfitting = validator.detect_overfitting(train_metrics, test_metrics)
print(overfitting['assessment'])
```

### Correlation Analysis

Identify redundant signals:

```python
corr_matrix = validator.correlation_matrix(signals_df)
print(corr_matrix)

# High correlation (>0.7) suggests signals are redundant
```

---

## 📁 Output Files

All reports are saved to `trading/reports/`:

```
reports/
├── quant_report_2026-02-08_17-30-00.txt    # Full analysis report
├── trades_2026-02-08_17-30-00.csv          # All trades details
└── metrics_2026-02-08_17-30-00.json        # Metrics as JSON
```

---

## 🔄 Integration with Command Center

### Auto-run on New Signals

Add to your trading workflow:

```python
# In your signal scraper
from agents.quant_agent import QuantAgent

def process_new_signal(signal):
    # Save signal to database
    save_signal_to_db(signal)
    
    # Quick backtest
    agent = QuantAgent()
    result = agent.quick_backtest(
        ticker=signal['ticker'],
        entry_price=signal['price'],
        entry_date=signal['date']
    )
    
    # Log to Command Center
    log_to_dashboard({
        'signal': signal,
        'backtest': result,
        'recommendation': 'DEPLOY' if result['return_pct'] > 10 else 'SKIP'
    })
```

### Scheduled Analysis

Add to cron or daily workflow:

```bash
# Run daily backtest at 6 PM
0 18 * * * cd /Users/agentjoselo/.openclaw/workspace/trading && python agents/quant_agent.py --mode full
```

---

## 🛠️ Customization

### Custom Exit Logic

Modify `backtest.py` to add custom exit conditions:

```python
def simulate_trade(self, ...):
    # ... existing code ...
    
    # Add custom exit: RSI overbought
    if row['RSI'] > 70:
        exit_date = date
        exit_price = row['Close']
        exit_reason = 'RSI_OVERBOUGHT'
        break
```

### Custom Metrics

Add your own performance metrics:

```python
def calculate_custom_metrics(self, trades_df):
    # Example: Consecutive wins/losses
    consecutive_wins = 0
    max_consecutive_wins = 0
    
    for trade in trades_df.itertuples():
        if trade.pnl_net > 0:
            consecutive_wins += 1
            max_consecutive_wins = max(max_consecutive_wins, consecutive_wins)
        else:
            consecutive_wins = 0
    
    return {'max_consecutive_wins': max_consecutive_wins}
```

---

## 📚 Theory & Methodology

### Backtesting Best Practices

1. **Realistic Assumptions:**
   - Always include commissions and slippage
   - Use actual historical prices (not adjusted)
   - Account for market hours and liquidity

2. **Avoid Look-Ahead Bias:**
   - Only use data available at decision time
   - Don't peek into the future

3. **Out-of-Sample Testing:**
   - Reserve 20-30% of data for validation
   - Never optimize on test data

4. **Position Sizing:**
   - Use consistent sizing methodology
   - Account for portfolio constraints

### Statistical Significance

A strategy is considered statistically valid if:

- **Sharpe Ratio:** > 1.0 (preferably > 1.5)
- **Win Rate:** > 50% OR high profit factor
- **P-Value:** < 0.05 (95% confidence)
- **Monte Carlo:** Percentile rank > 75%
- **IC:** > 0.05 (signal quality)

### Overfitting Red Flags

🚩 **Warning Signs:**
- Train win rate 80%, test win rate 45%
- Strategy has >10 parameters
- Performance degrades on recent data
- Only works on specific time period

---

## 🐛 Troubleshooting

### "No data found for ticker"

**Problem:** yfinance can't find the ticker symbol.

**Solution:** 
- Check ticker format (crypto needs `-USD` suffix)
- Verify ticker is valid and publicly traded
- Try alternative data source

```python
# Manual data loading
from backtest import Backtester
bt = Backtester()
data = bt.load_historical_data('SOL', '2026-01-01', '2026-02-01')
print(data.head())
```

### "Insufficient data for IC calculation"

**Problem:** Not enough trades with conviction scores.

**Solution:** 
- Ensure signals have `Conviction_Score` column
- Need at least 3 trades with scores
- Skip IC test if not applicable

### Low Sharpe Ratio

**Problem:** Risk-adjusted returns are poor.

**Possible Causes:**
- High volatility relative to returns
- Inconsistent performance
- Too many losing trades

**Solutions:**
- Tighten entry criteria
- Improve risk management
- Reduce position sizes
- Add stop-loss discipline

---

## 📖 Example Workflow

### Complete Analysis Pipeline

```python
#!/usr/bin/env python3
"""
Daily Quant Analysis Workflow
"""

from agents.quant_agent import QuantAgent
from backtest import BacktestConfig
import pandas as pd

def daily_analysis():
    # 1. Load latest signals
    signals = pd.read_csv('signals-database.csv')
    new_signals = signals[signals['Date_Found'] == pd.Timestamp.today().strftime('%Y-%m-%d')]
    
    print(f"📊 Found {len(new_signals)} new signals today")
    
    # 2. Quick backtest each new signal
    agent = QuantAgent()
    
    for _, signal in new_signals.iterrows():
        if pd.notna(signal['Price_Entry']):
            result = agent.quick_backtest(
                ticker=signal['Ticker'],
                entry_price=signal['Price_Entry'],
                entry_date=signal['Date_Found']
            )
            
            print(f"{signal['Ticker']}: {result['return_pct']:+.2f}%")
    
    # 3. Run full strategy analysis weekly
    if pd.Timestamp.today().weekday() == 4:  # Friday
        print("📈 Running weekly strategy review...")
        report = agent.analyze_strategy()
        
        # Email report or post to Discord
        send_report(report)

if __name__ == '__main__':
    daily_analysis()
```

---

## 🎓 Learning Resources

### Recommended Reading

- **"Evidence-Based Technical Analysis"** by David Aronson
- **"Quantitative Trading"** by Ernest Chan
- **"Advances in Financial Machine Learning"** by Marcos López de Prado

### Key Concepts

- **Information Coefficient:** Correlation metric for signal quality
- **Sharpe Ratio:** Risk-adjusted return measure
- **Kelly Criterion:** Optimal position sizing formula
- **Walk-Forward Analysis:** Rolling window validation
- **Monte Carlo:** Randomization-based robustness testing

---

## 🔮 Future Enhancements

**Planned Features:**

- [ ] Multi-timeframe backtesting
- [ ] Portfolio-level optimization
- [ ] Machine learning integration
- [ ] Real-time performance tracking
- [ ] Automated parameter optimization
- [ ] Walk-forward optimization
- [ ] Transaction cost analysis (market impact)
- [ ] Regime detection (bull/bear markets)

---

## 📞 Support

**Issues or Questions?**

Check the main trading README: `/Users/agentjoselo/.openclaw/workspace/trading/README.md`

**Contributing:**

Improvements welcome! Follow the existing code style and add tests.

---

## 📄 License

Part of the OpenClaw Trading System  
For personal use only

---

**Last Updated:** 2026-02-08  
**Quant Agent Version:** 1.0.0  

*"In God we trust. All others must bring data."* — W. Edwards Deming
