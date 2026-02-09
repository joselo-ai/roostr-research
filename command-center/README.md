# 🐓 Joselo Command Center

**Real-time activity tracker** — Every task, decision, and automation run logged and visualized.

## Quick Start

```bash
# Start the dashboard server
cd /Users/agentjoselo/.openclaw/workspace/command-center
python3 server.py
```

Then open: **http://localhost:8001/dashboard.html**

## Features

✅ **Live Activity Feed** — Every action logged in real-time  
✅ **Category Tracking** — Trading, Marketing, Research, Automation, Decisions  
✅ **Auto-refresh** — Updates every 5 seconds  
✅ **Statistics** — Total actions by category and status  
✅ **Terminal-style UI** — Green-on-black hacker aesthetic  

## Activity Categories

- **Trading:** Price updates, position changes, P&L tracking
- **Marketing:** Tweets, content generation, engagement
- **Research:** Signal discovery, conviction docs, analysis
- **Automation:** Cron runs, scrapers, scheduled tasks
- **Decision:** Strategic choices, deployments, pivots

## Logging API

```python
from activity_logger import log_trading, log_marketing, log_research, log_automation, log_decision

# Log a trading action
log_trading("Price update", {"TAO": 165.67, "SOL": 87.05, "P&L": -543})

# Log automation
log_automation("Signal scraper", {"new_signals": 0})

# Log a decision
log_decision("Deploy ACGL", {"amount": "$12,000", "conviction": "8.5/10"})

# Log with error status
log_research("Conviction doc", {"ticker": "FAIL"}, status="error")
```

## Files

- `dashboard.html` — Web dashboard
- `activity_logger.py` — Python logging library
- `activity-log.jsonl` — Activity log (append-only)
- `stats.json` — Running statistics
- `server.py` — Simple HTTP server
- `integrate_logging.py` — Integrate into existing scripts

## Integration

Already integrated into:
- `trading/apps/price_updater.py`
- `trading/apps/signal_scraper.py`
- `trading/apps/daily_summary.py`

All automation runs are automatically logged.

## Demo Mode

```bash
# Test the logger
python3 activity_logger.py

# Generate sample activities
python3 -c "
from activity_logger import *
log_trading('Paper trade deployed', {'ticker': 'TAO', 'amount': '$10k'})
log_marketing('Tweet posted', {'url': 'https://x.com/roostrcapital/status/123'})
log_research('Conviction doc written', {'ticker': 'ACGL', 'rating': '8.5/10'})
log_automation('Cron executed', {'job': 'price_updater'})
log_decision('Strategic pivot', {'from': 'Forex', 'to': 'Value Stocks'})
"

# View in dashboard
python3 server.py
```

---

**Built:** Feb 8, 2026  
**Purpose:** Complete visibility into Joselo's operations  
**Status:** 🟢 Live
