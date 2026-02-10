# Smooth.sh Integration

## ✅ Setup Complete

**API Key:** Stored in `/.smooth-api-key`  
**Client:** `trading/apps/smooth_client.py`  
**Credits:** 491 remaining (free tier)

## Test Results

**Test 1:** X.com trending topics  
- Task: "Go to x.com and tell me #1 trending topic"
- Result: "Discord" ✅
- Duration: 60s
- Cost: 9 credits

## Use Cases for Hedge Fund Operations

### 1. Research Automation
**Script:** `trading/apps/research_scraper.py`

```bash
python3 research_scraper.py PLTR
```

Scrapes Yahoo Finance for:
- Price, P/E, revenue, EPS
- Analyst consensus + price targets
- 52-week high/low

**Output:** `trading/research/PLTR-fundamentals.txt`

### 2. Social Media Posting
**Script:** `trading/apps/social_poster.py` (to be built)

```python
from smooth_client import SmoothClient

client = SmoothClient()
task = """
Go to x.com, log in as @roostrcapital, and post this tweet:

"End of day 1 (Feb 9):

$TAO: $161.03 (-8.1% from entry)
$SOL: $87.01 (+0.6% from entry)

Portfolio: -$810 (-4.6% today)

Conviction unchanged. Building in public = showing red days too. 🐓"
"""

result = client.run_task(task)
```

### 3. Discord Signal Scraping
**Script:** `trading/apps/discord_monitor.py` (to be built)

Auto-scrape Dumb Money Discord hourly:
- Find messages with >20 reactions
- Extract ticker symbols
- Save to signals database

### 4. Whale Wallet Tracking
**Script:** `trading/apps/whale_monitor.py` (to be built)

Monitor Etherscan/Nansen for:
- Large BTC/ETH movements
- Whale wallet trades
- Unusual activity alerts

### 5. News Monitoring
**Script:** `trading/apps/news_monitor.py` (to be built)

Track Google News/Reuters for:
- Deployed positions (TAO, SOL)
- Watchlist tickers (PLTR, TRV, NVDA)
- Sector news (AI, crypto, energy)

## Cost Analysis

**Free tier:** 500 credits (~55 tasks)  
**Average task:** 9 credits (60s duration)  
**Daily usage estimate:** 
- Research: 3 tickers/day = 27 credits
- Social posts: 2/day = 18 credits
- Discord scraping: 1/day = 9 credits
- **Total:** ~54 credits/day

**Runway:** 9 days on free tier → Need paid plan

## Next Steps

1. ✅ Test PLTR research scraper
2. Build social poster (fix wrong evening tweet)
3. Build Discord monitor (replace manual scraping)
4. Deploy as cron jobs (automated daily)
5. Upgrade to paid tier when credits run low

---

**Status:** Operational and ready for production use 🚀
