# 🚀 Evolution Engine - Quick Start

## What This Is

**Autonomous trading strategy factory** that never stops learning.

- Generates 50 strategy variations per generation
- Backtests each one on real stock data (past year)
- Breeds the winners (top 10)
- Mutates 30% of their traits
- Injects 20% completely new DNA
- Flags strategies scoring ≥8.0/10 for your review

## Start It Now

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/evolution
python3 runner.py
```

Runs forever. Ctrl+C to stop (saves state).

## Check Progress

```bash
python3 status.py
```

## What Happens

**Every cycle (~30-40 min):**
1. Runs 5 generations
2. Tests ~250 strategy variations
3. Saves best performers
4. If any score ≥8.0/10 → creates `high_conviction_*.json`
5. Sleeps 5 min
6. Repeat

## When You See a Signal

1. Check `high_conviction_*.json` files
2. Review backtest results (ROI, win rate, drawdown)
3. If promising → submit to 18-agent deliberation
4. If agents approve → deploy to paper portfolio

## Integration

This **supplements** your manual hunting:
- Manual: Yieldschool, Dumb Money, Chart Fanatics, etc.
- Evolution: Discovers strategies you wouldn't think of

Both feed into the same 18-agent system.

## Files

- `latest.json` - Current state
- `generation_N.json` - Historical record
- `high_conviction_*.json` - Signals ready for review

## Current Setup

- Universe: Top 30 S&P 500 stocks
- Lookback: 1 year of data
- Population: 50 strategies/generation
- Mutation: 30% new traits
- Fresh blood: 20% completely new

## Next

Run it. Let it evolve. Check back in a few hours.

It's designed to run 24/7 in the background, constantly improving.
