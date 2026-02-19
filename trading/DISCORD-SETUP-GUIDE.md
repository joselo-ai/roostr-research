# Discord Data Sources Setup Guide
**roostr Capital - Automated Signal Hunting from Discord**

## What This Does

Automatically scans Discord servers (Dumb Money, Yieldschool, Chart Fanatics) for trading signals:
- **Dumb Money:** Social arbitrage (stocks with viral engagement)
- **Yieldschool:** Dan's crypto fundamental analysis
- **Chart Fanatics:** Riz's EURUSD + pro trader setups

Signals feed into the 18-agent deliberation system for validation.

---

## Prerequisites

✅ **Already set up:**
- Discord bot token (stored at `~/.openclaw/workspace/.discord-bot-token`)
- Discord.py library installed
- Dumb Money scraper built (`trading/scrapers/dumbmoney_scraper.py`)

🔲 **You need to provide:**
- Discord server IDs
- Channel IDs for each data source
- Bot invite links (if bot not already in servers)

---

## Step 1: Enable Discord Developer Mode

1. Open Discord (desktop or web, NOT mobile)
2. Click ⚙️ **Settings** (bottom left)
3. Go to **Advanced** (left sidebar)
4. Enable **Developer Mode** (toggle ON)
5. Close settings

---

## Step 2: Get Server & Channel IDs

### For Each Server (Dumb Money, Yieldschool, Chart Fanatics):

**Get Server (Guild) ID:**
1. Right-click the server icon (left sidebar)
2. Click **Copy ID**
3. Paste into `trading/config/discord_sources.json`

**Get Channel IDs:**
1. Right-click any channel name (e.g., #trade-ideas)
2. Click **Copy ID**
3. Paste into `trading/config/discord_sources.json`

Example:
```json
"dumbmoney": {
  "guild_id": "123456789012345678",
  "channels": {
    "main": "234567890123456789",
    "alerts": "345678901234567890"
  },
  "enabled": true
}
```

---

## Step 3: Invite Bot to Servers (If Needed)

If the roostr bot is not already in these servers, you need to invite it.

**Bot Invite URL:**
```
https://discord.com/api/oauth2/authorize?client_id=1469016616711884913&permissions=67584&scope=bot
```

**Permissions needed:**
- Read Messages/View Channels
- Read Message History
- Add Reactions (optional, for monitoring)

**How to invite:**
1. Open URL above in browser
2. Select server (must have "Manage Server" permission)
3. Click **Authorize**
4. Complete CAPTCHA

Repeat for each server: Dumb Money, Yieldschool, Chart Fanatics.

---

## Step 4: Configure Channel IDs

Edit: `trading/config/discord_sources.json`

```json
{
  "dumbmoney": {
    "name": "Dumb Money",
    "guild_id": "PASTE_SERVER_ID_HERE",
    "channels": {
      "main": "PASTE_MAIN_CHANNEL_ID",
      "alerts": "PASTE_ALERTS_CHANNEL_ID"
    },
    "enabled": true,
    "min_reactions": 10
  },
  "yieldschool": {
    "name": "Yieldschool",
    "guild_id": "PASTE_SERVER_ID_HERE",
    "channels": {
      "yield_hub": "PASTE_CHANNEL_ID",
      "blue_chips": "PASTE_CHANNEL_ID",
      "mid_caps": "PASTE_CHANNEL_ID"
    },
    "enabled": true
  },
  "chart_fanatics": {
    "name": "Chart Fanatics",
    "guild_id": "PASTE_SERVER_ID_HERE",
    "channels": {
      "trade_ideas": "PASTE_CHANNEL_ID",
      "riz": "PASTE_CHANNEL_ID"
    },
    "enabled": true
  }
}
```

Set `"enabled": true` when ready to activate.

---

## Step 5: Test Each Scraper

### Test Dumb Money:
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/scrapers
python3 dumbmoney_scraper.py \
  --channels CHANNEL_ID_1,CHANNEL_ID_2 \
  --hours 24 \
  --min-reactions 10 \
  --output test-dumbmoney.json
```

**Expected output:**
```
✅ Connected as Joselo Monitor
📊 Scanning #main (last 24h)...
   Scanned 342 messages, found 12 signals

📊 FOUND 8 UNIQUE TICKERS

  NVDA   | Conviction: 8.5/10 | Reactions: 47 | Mentions: 3
  TSLA   | Conviction: 7.2/10 | Reactions: 31 | Mentions: 2
  ...
```

### Test Yieldschool (when ready):
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/scrapers
python3 yieldschool_scraper.py \
  --channels YIELD_HUB_ID,BLUE_CHIPS_ID \
  --hours 48 \
  --output test-yieldschool.json
```

### Test Chart Fanatics (when ready):
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/scrapers
python3 chartfanatics_scraper.py \
  --channels TRADE_IDEAS_ID,RIZ_ID \
  --hours 24 \
  --output test-chartfanatics.json
```

---

## Step 6: Enable in Daily Signal Hunter

Once scrapers are working, they'll auto-run daily at 7 AM via:
```bash
python3 apps/daily_signal_hunter.py
```

The hunter will:
1. Scan all enabled Discord sources
2. Score signals (0-10 conviction)
3. Classify: GREEN (≥8.0), YELLOW (5.0-7.9), RED (<5.0)
4. Trigger 18-agent deliberation on GREEN signals
5. Send Telegram report

---

## Troubleshooting

### Bot Not in Server
**Error:** `❌ No access to channel CHANNEL_ID (check bot permissions)`

**Fix:** Invite bot using URL from Step 3

### Invalid Channel ID
**Error:** `❌ Channel CHANNEL_ID not found`

**Fix:** 
1. Verify Developer Mode is enabled
2. Right-click channel → Copy ID again
3. Make sure ID is numeric (no quotes in command line)

### Rate Limiting
**Error:** `429 Too Many Requests`

**Fix:** Bot is scanning too fast. Scrapers have built-in 0.5s delays. If issue persists, reduce scan frequency.

### Token Expired
**Error:** `Invalid Discord token`

**Fix:** Bot token may have been regenerated. Get new token from Discord Developer Portal.

---

## What Happens After Setup

### Daily Automation (7 AM):
```
Daily Signal Hunter
  ↓
Scans: Dumb Money + Yieldschool + Chart Fanatics + Reddit + others
  ↓
Scores signals (0-10)
  ↓
GREEN signals (≥8.0) → 18-Agent Deliberation
  ↓
Telegram report + Dashboard update
```

### Manual Trigger (anytime):
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading

# Run full scan now
python3 apps/daily_signal_hunter.py

# Check results
cat hunting-log.jsonl | tail -10 | jq
cat signals-database.csv
```

---

## File Locations

| File | Purpose |
|------|---------|
| `trading/config/discord_sources.json` | Channel IDs config |
| `trading/scrapers/dumbmoney_scraper.py` | Dumb Money social arb |
| `trading/scrapers/yieldschool_scraper.py` | Yieldschool crypto (TODO) |
| `trading/scrapers/chartfanatics_scraper.py` | Chart Fanatics forex (TODO) |
| `trading/apps/daily_signal_hunter.py` | Master daily scanner |
| `~/.openclaw/workspace/.discord-bot-token` | Bot authentication |
| `trading/hunting-log.jsonl` | All signals scored |
| `trading/signals-database.csv` | GREEN signals (≥8.0) |

---

## Next Steps

1. ✅ Get Dumb Money channel IDs
2. ✅ Get Yieldschool channel IDs
3. ✅ Get Chart Fanatics channel IDs
4. ✅ Update `discord_sources.json`
5. ✅ Test each scraper individually
6. ✅ Run full signal hunter
7. ✅ Verify signals appear in `signals-database.csv`
8. ✅ Confirm 18-agent deliberation triggers

---

**Status:** Ready for Discord channel IDs

**Once configured:** Fully automated daily signal hunting from all 3 Discord sources
