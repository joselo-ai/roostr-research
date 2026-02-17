# Alpaca Autonomous Execution - Setup Guide

## ✅ Status: **Ready for API Keys**

Infrastructure built. Need Alpaca paper trading credentials to activate.

---

## Quick Start (5 minutes)

### 1. Get Alpaca Paper Trading Keys

1. Go to: https://app.alpaca.markets/signup
2. Create free account
3. Navigate to: **Paper Trading** → **API Keys**
4. Generate new API key pair
5. Copy both keys

### 2. Configure Keys

Edit: `trading/.alpaca.env`

```bash
ALPACA_API_KEY=your_actual_key_here
ALPACA_SECRET_KEY=your_actual_secret_here
ALPACA_PAPER=true
```

### 3. Test (Dry Run)

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
source venv/bin/activate
python3 apps/autonomous_executor.py --dry-run
```

Expected output:
```
🐓 Autonomous Executor - DRY RUN
🎯 Found X GREEN signals
🔍 DRY_RUN: TAO | Conv:8.5 | Would trade $6250
```

### 4. Go Live (Paper Trading)

```bash
python3 apps/autonomous_executor.py --live
```

Expected output:
```
🐓 Autonomous Executor - LIVE EXECUTION
✅ EXECUTED: TAO | Conv:8.5 | $6250 | Stop:$149.61
```

---

## Safeguards (Phase 1)

**Entry Criteria:**
- Conviction ≥ 8.0/10
- Catalyst score ≥ 5/10
- Status = GREEN in signals DB

**Risk Limits:**
- Max $10k per position (1% of $1M portfolio)
- Max 3 new trades per day
- Max 10 open positions
- 15% stop-loss on every trade
- Pause if down >2% intraday

**Position Sizing (Conviction-Weighted):**
- 8.0/10 → $5,000
- 9.0/10 → $7,500
- 10.0/10 → $10,000

---

## Automation (Cron)

Add to OpenClaw cron for hourly execution:

```json
{
  "name": "Autonomous Executor",
  "schedule": {
    "kind": "cron",
    "expr": "0 9-16 * * 1-5",
    "tz": "America/New_York"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Run autonomous executor: cd /Users/agentjoselo/.openclaw/workspace/trading && source venv/bin/activate && python3 apps/autonomous_executor.py --live"
  },
  "sessionTarget": "main"
}
```

Runs market hours (9 AM - 4 PM ET, Mon-Fri).

---

## Monitoring

**Execution Log:**
`trading/logs/execution.jsonl`

**Check Status:**
```bash
python3 apps/autonomous_executor.py --dry-run
```

**View Recent Executions:**
```bash
tail -n 20 trading/logs/execution.jsonl | jq
```

**Dashboard:**
All executed trades auto-update `dashboard.html`

---

## Safety Notes

1. **Paper trading only** for Phase 1 (no real money)
2. API keys never leave your machine
3. You retain kill-switch: disable cron or revoke API keys
4. Review execution log daily
5. Adjust safeguards in `apps/autonomous_executor.py` as needed

---

## Phase 2 (After 90 Days)

If Phase 1 succeeds (>20% returns, <15% DD, >60% win rate):

- Deploy $100k real capital
- Loosen safeguards (higher limits)
- Add live execution module

Phase 1 = Prove the system. Phase 2 = Scale it.

---

## Troubleshooting

**"Config not found"**
→ Create `trading/.alpaca.env` with API keys

**"API keys not configured"**
→ Replace `your_key_here` in `.alpaca.env`

**"Max positions reached"**
→ Close losing positions or increase `max_open_positions` in safeguards

**"Daily loss limit hit"**
→ System paused. Review + resume tomorrow

---

**Status:** Infrastructure complete. Waiting for API keys.

Once configured: `python3 apps/autonomous_executor.py --live`
