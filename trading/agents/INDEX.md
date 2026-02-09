# Quant Agent - File Index

Quick reference for all files in the Quant Agent system.

## 📁 Core System Files

### Main Agent
- **`quant_agent.py`** ⭐ Main agent orchestrating all analysis
  - Full strategy analysis
  - Quick single-trade backtesting
  - Position sizing calculations
  - Report generation
  - CLI interface

### Backtesting Engine
- **`../backtest.py`** ⭐ Core backtesting framework
  - Trade simulation
  - Historical data loading
  - Performance metrics
  - Equity curve tracking
  - Report generation

### Statistical Validation
- **`../validation.py`** ⭐ Statistical testing suite
  - Information Coefficient
  - Hypothesis testing
  - Monte Carlo simulation
  - Overfitting detection
  - Correlation analysis

## 📖 Documentation

### Getting Started
- **`QUICK_START.md`** 🚀 Start here! 5-minute guide
- **`README.md`** 📚 Complete documentation
- **`DELIVERY_SUMMARY.md`** 📦 What was built & why
- **`INDEX.md`** 📑 This file

### Examples & Templates
- **`example_usage.py`** 💡 7 working examples
- **`SAMPLE_BACKTEST_REPORT.txt`** 📊 Sample output
- **`dashboard_integration.py`** 🔌 Dashboard integration code

## 🧪 Testing & Validation

- **`test_quant_agent.py`** ✅ Automated test suite
- **`../requirements.txt`** 📦 Python dependencies

## 📂 Output Directories

- **`../reports/`** 📁 Generated backtest reports
  - `quant_report_*.txt` - Full analysis reports
  - `trades_*.csv` - Detailed trade logs
  - `metrics_*.json` - Performance metrics

## 🔧 Module Structure

```
trading/
├── agents/
│   ├── __init__.py              # Module initialization
│   ├── quant_agent.py           # ⭐ MAIN AGENT
│   ├── dashboard_integration.py # Dashboard updates
│   ├── test_quant_agent.py      # Test suite
│   ├── example_usage.py         # Examples
│   ├── README.md                # Full docs
│   ├── QUICK_START.md           # Quick guide
│   ├── DELIVERY_SUMMARY.md      # What was built
│   ├── INDEX.md                 # This file
│   └── SAMPLE_BACKTEST_REPORT.txt
│
├── backtest.py                  # ⭐ BACKTESTING ENGINE
├── validation.py                # ⭐ STATISTICAL VALIDATION
├── requirements.txt             # Dependencies
│
└── reports/                     # Auto-generated outputs
    ├── quant_report_*.txt
    ├── trades_*.csv
    └── metrics_*.json
```

## 🚀 Quick Commands

### First Time Setup
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
pip3 install -r requirements.txt
python3 agents/test_quant_agent.py
```

### Run Full Analysis
```bash
python3 agents/quant_agent.py --mode full
```

### Quick Single Trade
```bash
python3 agents/quant_agent.py --mode quick --ticker TAO --price 176.05 --date 2026-02-06
```

### Run Examples
```bash
python3 agents/example_usage.py
python3 agents/example_usage.py --example 1  # Run specific example
```

### Update Dashboard
```bash
python3 agents/dashboard_integration.py
```

## 📚 Learning Path

**New to backtesting?**
1. Read `QUICK_START.md`
2. Run `example_usage.py --example 1`
3. Check `SAMPLE_BACKTEST_REPORT.txt`
4. Run `agents/quant_agent.py --mode full`

**Ready to deploy?**
1. Test with `--mode quick` on each signal
2. Review metrics in reports/
3. Adjust position sizes based on Kelly Criterion
4. Integrate with dashboard

**Want to customize?**
1. Read `README.md` sections on customization
2. Check `example_usage.py --example 3` for config
3. Compare strategies with example 6
4. Build your own config

## 🎯 File Purposes

### When to use each file:

**`quant_agent.py`**
- Full strategy analysis
- Command-line backtesting
- Position sizing calculations

**`backtest.py`**
- Custom backtesting logic
- Trade simulation
- Performance calculations

**`validation.py`**
- Statistical significance testing
- Overfitting detection
- Signal quality analysis

**`dashboard_integration.py`**
- Auto-update dashboard
- Backtest new signals automatically
- Log to Command Center

**`example_usage.py`**
- Learn how to use the system
- Copy-paste code snippets
- See best practices

**`test_quant_agent.py`**
- Verify installation
- Debug issues
- Validate changes

## 📊 Output Files Explained

### `quant_report_*.txt`
Full analysis report with:
- Summary statistics
- Performance metrics
- Risk analysis
- Recommendations

### `trades_*.csv`
Detailed trade log:
- Entry/exit dates and prices
- P&L per trade
- Hold days
- Exit reasons

### `metrics_*.json`
Structured performance data:
- Win rate, Sharpe, drawdown
- Fee and slippage costs
- Exit reason breakdown
- Machine-readable format

## 🔗 Related Files

### Existing Trading System
- `../signals-database.csv` - Signal data source
- `../update_dashboard.py` - Main dashboard
- `../price_fetcher.py` - Price updates
- `../ml/conviction_model.py` - Conviction scoring

### Integration Points
- Dashboard updates via `dashboard_integration.py`
- Signal validation in scrapers
- Command Center activity logging

## 📖 Documentation Map

**Need to...**

| Task | File to Read |
|------|--------------|
| Get started quickly | `QUICK_START.md` |
| Understand everything | `README.md` |
| See code examples | `example_usage.py` |
| See sample output | `SAMPLE_BACKTEST_REPORT.txt` |
| Understand what was built | `DELIVERY_SUMMARY.md` |
| Find a specific file | `INDEX.md` (this file) |
| Verify it works | `test_quant_agent.py` |
| Integrate with dashboard | `dashboard_integration.py` |
| Customize backtesting | `../backtest.py` |
| Add statistical tests | `../validation.py` |

## 🎓 Code Examples by Use Case

### "I want to backtest a signal"
→ See `example_usage.py` example 1

### "I want full strategy analysis"
→ See `example_usage.py` example 2

### "I want custom parameters"
→ See `example_usage.py` example 3

### "I want position sizing advice"
→ See `example_usage.py` example 4

### "I want statistical validation"
→ See `example_usage.py` example 5

### "I want to compare strategies"
→ See `example_usage.py` example 6

### "I want trade details"
→ See `example_usage.py` example 7

## 🆘 Troubleshooting

**Issue:** Can't import modules
→ Check `test_quant_agent.py` output

**Issue:** Missing dependencies
→ Run `pip3 install -r requirements.txt`

**Issue:** No data for ticker
→ See `README.md` troubleshooting section

**Issue:** Understanding metrics
→ See `QUICK_START.md` report interpretation

**Issue:** Want to customize
→ See `README.md` customization section

## 📞 Support Resources

1. **Documentation:** `README.md` (comprehensive)
2. **Quick Guide:** `QUICK_START.md` (essentials)
3. **Examples:** `example_usage.py` (working code)
4. **Tests:** `test_quant_agent.py` (verify setup)

## ⭐ Key Files at a Glance

**Must Read:**
- `QUICK_START.md` - Get going in 5 minutes
- `README.md` - Complete reference

**Most Used:**
- `quant_agent.py` - Main agent
- `example_usage.py` - How to use it

**Reference:**
- `SAMPLE_BACKTEST_REPORT.txt` - Example output
- `DELIVERY_SUMMARY.md` - What you got

**Testing:**
- `test_quant_agent.py` - Verify it works

**Integration:**
- `dashboard_integration.py` - Connect to dashboard

---

**Total Files:** 13
**Total Documentation:** ~1,500 lines
**Total Code:** ~2,858 lines
**Test Coverage:** 6/6 passing

**Start Here:** `QUICK_START.md` 🚀
