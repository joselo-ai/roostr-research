# TradingView Webhooks - Real-Time Alerts

**Status:** ✅ Server ready (Feb 10, 2026)  
**Next:** Configure alerts on TradingView

## What This Does

TradingView → Webhook Server → Telegram

**Examples:**
- "TAO crosses above $160" → Instant Telegram alert
- "SOL RSI drops below 30" → Telegram notification
- "PLTR breaks $140 resistance" → Alert
- Custom strategy triggers → Alert

## Architecture

```
TradingView Alert Fires
    ↓
POST http://YOUR_IP:5555/webhook
    ↓
Webhook Server receives
    ↓
Logs to tradingview-alerts.log
    ↓
Queues message in telegram-queue.txt
    ↓
Telegram sender (cron) picks up
    ↓
Sends to Telegram via OpenClaw
```

## Files Created

1. **`apps/tradingview_webhook.py`** - Flask server listening on port 5555
2. **`apps/telegram_sender.py`** - Cron job to send queued alerts
3. **`tradingview-alerts.log`** - All alerts logged here
4. **`telegram-queue.txt`** - Current alert waiting to send

## Starting the Server

### Option 1: Background (Recommended)

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
nohup python3 apps/tradingview_webhook.py > webhook.log 2>&1 &
echo $! > webhook.pid
```

Check status:
```bash
ps aux | grep tradingview_webhook
```

Stop:
```bash
kill $(cat webhook.pid)
```

### Option 2: Foreground (Testing)

```bash
python3 apps/tradingview_webhook.py
```

## TradingView Setup

### 1. Create an Alert

1. Open TradingView chart (e.g., TAOUSD on Binance)
2. Click **Alert** button (bell icon)
3. Set conditions:
   - Example: "TAO crossing $160"
   - Example: "RSI(14) < 30"

### 2. Configure Webhook

**Webhook URL:**
```
http://YOUR_PUBLIC_IP:5555/webhook
```

**Message Format (recommended):**
```
🚨 {{ticker}} Alert

Price: ${{close}}
Time: {{time}}
Interval: {{interval}}

Condition: [Your condition here]
```

**TradingView Placeholders:**
- `{{ticker}}` - Symbol (e.g., TAOUSD)
- `{{close}}` - Current price
- `{{time}}` - Alert timestamp
- `{{interval}}` - Timeframe (e.g., 1h)
- `{{volume}}` - Current volume

### 3. Test the Alert

Send a test webhook from TradingView or use curl:

```bash
curl -X POST http://localhost:5555/webhook \
  -H "Content-Type: application/json" \
  -d '{"message": "TEST: TAO crossed $160"}'
```

## Endpoints

### POST /webhook
Receives TradingView alerts (main endpoint)

### GET /health
Health check
```bash
curl http://localhost:5555/health
```

### GET /alerts
View recent alerts
```bash
curl http://localhost:5555/alerts
```

## Cron Integration (Auto-Send to Telegram)

Add to cron (every minute):
```bash
* * * * * cd /Users/agentjoselo/.openclaw/workspace/trading && python3 apps/telegram_sender.py >> telegram_sender.log 2>&1
```

Or via OpenClaw cron:
```bash
openclaw cron add --schedule "* * * * *" \
  --payload systemEvent \
  --text "Check TradingView queue and send alerts" \
  --session main
```

## Firewall / Port Forwarding

If your Mac is behind a router, you need to:

1. **Find your local IP:**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. **Forward port 5555** in router settings:
   - External: 5555
   - Internal: YOUR_LOCAL_IP:5555
   - Protocol: TCP

3. **Find public IP:**
   ```bash
   curl ifconfig.me
   ```

4. **Use in TradingView:**
   ```
   http://YOUR_PUBLIC_IP:5555/webhook
   ```

## Security Notes

⚠️ **This server is currently OPEN** (no authentication).

**For production, add:**
1. API key verification
2. HTTPS (SSL/TLS)
3. Rate limiting
4. IP whitelisting

## Example Alerts to Set Up

### 1. Price Breakouts
- **TAO > $160:** "TAO breakout above resistance"
- **SOL < $80:** "SOL support break"

### 2. RSI Extremes
- **TAO RSI < 30:** "TAO oversold (RSI < 30)"
- **SOL RSI > 70:** "SOL overbought (RSI > 70)"

### 3. Stop Loss Proximity
- **TAO < $145:** "TAO approaching stop ($140.84)"
- **SOL < $78:** "SOL approaching stop ($73.53)"

### 4. Custom Strategy
- **MACD cross + RSI < 40:** "TAO bullish divergence signal"

## Testing Checklist

- [ ] Server starts without errors
- [ ] Health check returns 200
- [ ] Test webhook receives POST
- [ ] Alert logged to tradingview-alerts.log
- [ ] Message queued in telegram-queue.txt
- [ ] Telegram sender picks up queue
- [ ] Alert delivered to Telegram

## Next Steps

**Phase 1 (Today):**
- ✅ Webhook server built
- [ ] Start server in background
- [ ] Configure first TradingView alert (TAO > $160)
- [ ] Test end-to-end delivery

**Phase 2 (This week):**
- Add authentication (API key)
- Set up 5-10 critical alerts
- Enable HTTPS for public access

**Phase 3 (Later):**
- Multi-ticker monitoring
- Custom alert templates
- Alert history dashboard

---

**Built:** Feb 10, 2026 09:55 EST  
**Deployed by:** Joselo 🐓  
**Port:** 5555  
**Status:** Ready for configuration
