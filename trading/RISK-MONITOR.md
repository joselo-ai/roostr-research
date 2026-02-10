# Risk Monitor - Stop Loss Protection

## ✅ Active Protection

**Status:** Operational and monitoring every 5 minutes

**Cron Job:** `a33fed8f-6b6e-4c38-8532-7597f063e3cb`  
**Interval:** Every 5 minutes (300,000ms)  
**Next check:** Auto-scheduled

## Current Stops

| Position | Entry | Stop | Current | Distance to Stop |
|----------|-------|------|---------|------------------|
| **TAO** | $176.05 | $140.84 | $159.01 | 11.4% above stop ✅ |
| **SOL** | $86.51 | $73.53 | $86.49 | 15.0% above stop ✅ |

## How It Works

1. **Check prices** every 5 minutes against CoinGecko cache
2. **Compare to stops** from signals database
3. **Alert if violated** - Telegram message + log file
4. **Warn if approaching** - Console warning at <5% from stop

## Alert System

**Violation detected:**
- 🚨 Immediate Telegram alert
- 📝 Log entry in `risk-alerts.log`
- 🔴 Exit code 1 triggers cron notification

**Alert message format:**
```
🚨 STOP LOSS VIOLATION 🚨

TAO: $138.50 (stop: $140.84)
Loss: -21.3% | BREACHED BY 1.7%

ACTION: Exit positions NOW!
```

## Manual Commands

**Check now:**
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
python3 apps/risk_monitor.py
```

**View alerts log:**
```bash
cat /Users/agentjoselo/.openclaw/workspace/trading/risk-alerts.log
```

**Disable monitoring:**
```bash
# Via OpenClaw cron
# cron disable <job-id>
```

## Warnings

**Approaching stop (within 5%):**
- TAO: Warns if below $147.88
- SOL: Warns if below $77.21

Console output only, no Telegram alert.

## Testing

**Simulate violation:**
1. Manually edit `.price_cache.json`
2. Set TAO price to $139.00 (below stop)
3. Run `python3 apps/risk_monitor.py`
4. Should trigger alert

**Reset:**
1. Run `python3 apps/price_updater.py`
2. Restores real prices

## Edge Cases Handled

- ✅ No price data available (skips check, warns)
- ✅ Multiple violations (alerts all)
- ✅ Parse errors (logs error, continues)
- ✅ Missing stop data (skips position)

## Next Enhancements

- [ ] Email alerts (backup to Telegram)
- [ ] SMS alerts (critical violations)
- [ ] Auto-exit orders (requires exchange API)
- [ ] Trailing stop adjustments

---

**Status:** Protecting portfolio 24/7 🐓
**Last manual test:** 2026-02-09 19:48 EST ✅
