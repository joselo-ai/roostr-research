# Reddit API Setup Guide

## Quick Start (5 minutes)

### 1. Create Reddit App

1. Go to https://www.reddit.com/prefs/apps
2. Click **"create another app..."** at the bottom
3. Fill in:
   - **name**: `OpenClaw Trading Bot` (or any name)
   - **type**: Select **"script"**
   - **description**: `Social sentiment analysis for trading signals`
   - **about url**: Leave blank
   - **redirect uri**: `http://localhost:8080` (required but not used)
4. Click **"create app"**

### 2. Get Credentials

After creating the app, you'll see:
- **client_id**: The string under "personal use script" (14 characters)
- **client_secret**: The longer string labeled "secret" (~27 characters)

### 3. Configure Scraper

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/config
cp reddit_config.json.example reddit_config.json
```

Edit `reddit_config.json`:
```json
{
  "client_id": "abc123XYZ456",
  "client_secret": "xYz789-aBcDeF123456789",
  "user_agent": "OpenClaw Trading Bot v1.0 (by /u/your_reddit_username)"
}
```

**⚠️ Keep credentials private! This file is gitignored.**

### 4. Install Dependencies

```bash
pip install praw textblob
python -m textblob.download_corpora
```

### 5. Test Scraper

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/scrapers
python reddit_scraper.py
```

You should see output like:
```
🐓 Reddit Social Sentiment Scraper
✅ Reddit API initialized
🔍 Scraping 4 subreddits...
✅ wallstreetbets: Found 47 ticker mentions
✅ stocks: Found 23 ticker mentions
✅ investing: Found 12 ticker mentions
✅ stockmarket: Found 8 ticker mentions

📊 Total signals extracted: 90
...
```

---

## What Gets Scraped

### Subreddits Monitored
- **r/wallstreetbets** - High-risk, high-conviction plays
- **r/stocks** - General stock discussion
- **r/investing** - Long-term investment ideas
- **r/stockmarket** - Market analysis and trends

### Data Collected Per Ticker
- **Mentions**: Number of times mentioned across subreddits
- **Upvotes**: Total upvotes (community interest)
- **Comments**: Total comment engagement
- **Sentiment**: Positive/Negative/Neutral (TextBlob analysis)
- **Conviction Score**: 1-10 (based on engagement + sentiment)
- **Top Post**: Highest-upvoted post mentioning ticker

### Signal Scoring

**GREEN (Deploy Ready)**
- Conviction ≥ 8/10
- Positive sentiment
- Upvotes ≥ 500
- High community interest

**YELLOW (Watch List)**
- Conviction 5-7/10
- Mixed signals or moderate engagement
- Needs further research

**RED (Avoid)**
- Conviction < 5/10
- Negative sentiment
- Low engagement

### Unusual Volume Detection
Flags tickers with **3x+ normal mention volume** compared to 30-day average.

---

## Output

### CSV Export
Signals append to `signals-database.csv`:
```csv
Ticker,Source,Date_Found,Price_Entry,Conviction_Score,Status,Deployed,...
NVDA,Reddit,2026-02-08,,9,GREEN,NO,,,,,,,"Reddit mentions: 23 (r/wallstreetbets, r/stocks) | Sentiment: positive (0.65) | Engagement: 3420↑ 567💬 | 🚨 UNUSUAL VOLUME 4.2x | Top post: NVDA earnings beat..."
```

### Text Report
Saved to `reddit-sentiment-report.txt`:
```
🔥 REDDIT SOCIAL SENTIMENT REPORT
Generated: 2026-02-08 17:30:00 EST

📊 SUMMARY:
   Total tickers: 45
   🟢 GREEN (High conviction): 7
   🟡 YELLOW (Watch): 28
   🔴 RED (Avoid): 10
   🚨 Unusual volume: 3

🟢 GREEN SIGNALS (7):
1. $NVDA 🚨
   Mentions: 23 | Conviction: 9/10 | Sentiment: positive (0.65)
   Engagement: 3,420↑ 567💬
   Subreddits: r/wallstreetbets, r/stocks
   Top post: NVDA earnings beat expectations, AI demand through roof
   URL: https://reddit.com/r/wallstreetbets/...
```

---

## Integration with Signal Scraper

### Add to Cron Schedule

Edit `/Users/agentjoselo/.openclaw/workspace/trading/apps/signal_scraper.py`:

```python
SOURCES = {
    # ... existing sources ...
    
    "reddit": {
        "enabled": True,
        "script": "/Users/agentjoselo/.openclaw/workspace/trading/scrapers/reddit_scraper.py"
    }
}
```

### Cron Schedule (Every 6 Hours)
```bash
# 6 AM, 12 PM, 6 PM, 12 AM EST
0 6,12,18,0 * * * cd /Users/agentjoselo/.openclaw/workspace/trading/scrapers && python reddit_scraper.py >> ../reddit-scraper.log 2>&1
```

---

## API Limits

**Reddit Free Tier:**
- **60 requests/minute**
- **600 requests/10 minutes**

The scraper stays well within limits:
- ~4 subreddits × 100 posts = **400 requests max**
- Run every 6 hours = **~1,600 requests/day** (well under limits)

**No credit card required.**

---

## Troubleshooting

### Error: "PRAW not installed"
```bash
pip install praw
```

### Error: "Invalid credentials"
- Check `client_id` and `client_secret` in config
- Make sure no extra spaces or quotes
- Regenerate secret in Reddit app settings if needed

### Error: "429 Rate Limit"
- Wait 10 minutes
- Reduce `limit_per_sub` in scraper (default 100)
- Increase time between runs

### No signals found
- Check if subreddits are public (they are)
- Verify Reddit API is responding: `python -c "import praw; print('OK')"`
- Try increasing `limit_per_sub` or checking different `time_filter`

### Sentiment analysis not working
```bash
pip install textblob
python -m textblob.download_corpora
```

---

## Command Center Logging

Reddit scraper automatically logs to Command Center:

```python
from activity_logger import log_trading

log_trading("Reddit scraper", {
    "signals": 45,
    "green": 7,
    "unusual_volume": 3
})
```

Dashboard will show:
```
🔥 Reddit Social Signals: 45 tickers (7 GREEN, 3 unusual volume)
```

---

## Advanced Configuration

### Custom Subreddits

Edit `reddit_scraper.py`:
```python
self.subreddits = [
    'wallstreetbets',
    'stocks', 
    'investing',
    'stockmarket',
    'options',  # Add custom
    'pennystocks'  # Add custom
]
```

### Adjust Thresholds

```python
# Minimum engagement for signals
self.min_upvotes = 50  # Lower = more signals
self.min_comments = 10

# Conviction scoring
self.high_upvotes = 500  # Higher = stricter GREEN
```

### Time Filters

```python
# Daily: Most recent 24h
scraper.run(time_filter='day')

# Weekly: Last 7 days (more data, slower)
scraper.run(time_filter='week')
```

---

## Data Privacy

- **Read-only**: Scraper only reads public posts
- **No posting**: Never posts or comments
- **No personal data**: Doesn't access DMs or private subreddits
- **Anonymous**: Bot user agent identifies as trading bot

---

## Next Steps

1. ✅ Setup complete
2. Run initial scrape: `python reddit_scraper.py`
3. Review `reddit-sentiment-report.txt`
4. Cross-reference GREEN signals with other sources
5. Add to cron for automated collection
6. Monitor unusual volume flags for momentum plays

**Free social sentiment data = competitive edge.** 🚀
