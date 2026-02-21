# 🧬 roostr Strategy Evolution Engine

Autonomous genetic algorithm for discovering and evolving profitable trading strategies.

## Overview

This system runs 24/7, continuously:
1. Generating strategy variations (genetic mutations)
2. Backtesting them on historical stock data
3. Breeding the winners
4. Injecting 30% new genetic material
5. Flagging high-conviction strategies (8.0+/10) for deployment

## Architecture

### Components

- **strategy_dna.py** - Genetic representation of trading strategies
- **backtester.py** - Historical simulation engine
- **evolution_engine.py** - Genetic algorithm (selection, crossover, mutation)
- **runner.py** - Continuous evolution loop
- **status.py** - Check current progress

### Strategy Genes

Each strategy has DNA encoding:

**Entry Rules:**
- RSI threshold & period
- Volume spike requirement
- Price vs SMA crossover
- Minimum price filter

**Exit Rules:**
- Profit target %
- Stop loss %
- Max hold days
- Trailing stop (yes/no)

**Position Sizing:**
- Base allocation (2-10% of portfolio)
- Conviction-based scaling

**Filters:**
- Market cap minimum
- Trend requirements
- Earnings avoidance

### Evolution Process

```
Generation 0: 50 random strategies
    ↓
Backtest all → Calculate fitness
    ↓
Select top 10 (elite)
    ↓
Breed 30 offspring (crossover + mutate 30%)
    ↓
Add 10 completely new (20% fresh blood)
    ↓
Generation 1: 50 strategies (10 elite + 30 bred + 10 new)
    ↓
Repeat forever...
```

**Fitness Function:**
```
Fitness = (ROI × 0.4) + (Win% × 0.2) + (Sharpe × 0.3) - (MaxDD × 0.1)
```

## Usage

### Start Evolution (Continuous)

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/evolution
python3 runner.py
```

This runs forever in the background. Ctrl+C to stop gracefully (saves state).

### Check Status

```bash
python3 status.py
```

Shows:
- Current generation
- Best strategy ever
- Recent evolution progress
- Any high-conviction signals found

### Run Single Test (Development)

```bash
python3 evolution_engine.py
```

Runs 3 generations as a test.

## Output Files

- `latest.json` - Most recent generation data
- `generation_N.json` - Each generation's full state
- `high_conviction_TIMESTAMP.json` - Strategies scoring ≥8.0/10

## Integration with roostr Capital

**Automatic Signal Detection:**
- When a strategy scores ≥8.0/10 conviction, it's saved to `high_conviction_*.json`
- Joselo reviews these and can deploy via 18-agent deliberation
- This supplements (not replaces) manual signal hunting

**Deployment Flow:**
1. Evolution engine finds 8.0+ strategy
2. Joselo reviews backtest results
3. If promising, submit to 18-agent system
4. If agents approve (≥70% consensus), deploy to paper portfolio

## Tuning Parameters

In `runner.py` or `evolution_engine.py`:

- `population_size` - Total strategies per generation (50)
- `elite_size` - Top N to keep (10)
- `mutation_rate` - Probability of gene changes (0.30 = 30%)
- `new_blood_rate` - Fraction of completely new strategies (0.20 = 20%)

## Performance Notes

- Each generation takes ~5-10 minutes (50 strategies × 30 stocks)
- Runs 5 generations, then sleeps 5 min (to avoid overheating)
- Adjust `generations_per_cycle` and `sleep_between_cycles` in runner.py

## Current Universe

Testing on top 30 S&P 500 stocks for speed:
- AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, etc.

Expand in `backtester.py` → `get_sp500_tickers(limit=N)`

## Next Steps

1. **Run first evolution:** `python3 runner.py`
2. **Monitor progress:** `python3 status.py` (check every few hours)
3. **Review high-conviction signals:** Check `high_conviction_*.json` files
4. **Deploy winners:** Submit promising strategies to 18-agent system

---

**Built:** 2026-02-21  
**Status:** Operational, ready for deployment  
**Roadmap:** Multi-asset (crypto, forex), distributed computing, real-time adaptation
