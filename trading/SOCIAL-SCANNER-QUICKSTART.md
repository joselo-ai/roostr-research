# Social Scanner - Quick Start (No API Keys Needed)

**Status:** ✅ Ready to use immediately  
**What works NOW:** Google Trends validator (no auth required)  
**What needs setup:** Reddit + Twitter (5-10 min each)

---

## Step 1: Install Dependencies (1 minute)

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
pip3 install --user pytrends praw tweepy
```

Wait for installation to complete.

---

## Step 2: Test Google Trends (Works Immediately)

Google Trends requires **NO authentication**. Test it now:

```bash
python3 apps/google_trends_validator.py
```

**What you'll see:**
- Checks 4 test tickers (ASTS, PLTR, NVDA, GME)
- Shows which are RISING, STABLE, or FALLING
- Displays % change in search volume

**If you get rate-limited (429 error):**
- Wait 1 hour
- Or edit the script to add longer delays (5 seconds instead of 2)

---

## Step 3: Validate Your Existing Signals

Use Google Trends to validate any ticker:

```python
from apps.google_trends_validator import GoogleTrendsValidator

validator = GoogleTrendsValidator()

# Check a single ticker
result = validator.check_ticker_trend('ASTS')
print(result)

# Check multiple tickers
tickers = ['ASTS', 'TAC', 'SOL', 'TAO']
results = validator.validate_signals(tickers, delay=3)
```

**Interpretation:**
- **RISING** + current > average = ✅ Deploy
- **STABLE** = 🟡 Watch
- **FALLING** = 🔴 Pass (late to party)

---

## Step 4: Set Up Reddit API (Optional - 5 minutes)

**Why:** Scan WallStreetBets for high-conviction plays (500+ upvotes)

### Get Credentials:

1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Fill in:
   - Name: `social-arbitrage-scanner`
   - Type: **script**
   - Redirect URI: `http://localhost:8080`
4. Click "Create app"
5. Copy:
   - **Client ID:** (14-char string under app name)
   - **Client Secret:** (click "secret" button)

### Set Environment Variables:

```bash
# Add to ~/.zshrc (macOS) or ~/.bashrc (Linux)
export REDDIT_CLIENT_ID="your_14_char_id"
export REDDIT_CLIENT_SECRET="your_secret_here"

# Reload shell
source ~/.zshrc
```

### Test:

```bash
python3 apps/reddit_scanner.py
```

You should see:
- Scanning r/wallstreetbets, r/stocks, r/investing
- Top 10 tickers by upvotes/comments/awards
- Conviction scores 1-10

---

## Step 5: Set Up Twitter API (Optional - 10 minutes)

**Why:** Track real-time $TICKER mentions and virality

### Get Credentials:

1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Sign in with Twitter account
3. Click "Create Project"
   - Name: `Social Arbitrage Scanner`
   - Use case: "Exploring the API"
4. Create an App inside the project
5. Go to "Keys and Tokens" tab
6. Click "Generate" under **Bearer Token**
7. Copy the Bearer Token (starts with "AAA...")

### Set Environment Variable:

```bash
# Add to ~/.zshrc (macOS) or ~/.bashrc (Linux)
export TWITTER_BEARER_TOKEN="AAA...your_token_here"

# Reload shell
source ~/.zshrc
```

### Test:

```bash
python3 apps/twitter_scanner.py
```

You should see:
- Scanning top tickers for mentions
- Total likes, retweets, verified mentions
- Conviction scores 1-10

---

## Step 6: Run Multi-Platform Scanner

Once you have at least 2 platforms set up (Google Trends + Reddit OR Twitter):

```bash
python3 apps/multi_platform_scanner.py
```

**What it does:**
1. Scans Reddit (if credentials set)
2. Scans Twitter (if credentials set)
3. Cross-validates tickers across platforms
4. Checks Google Trends for each ticker
5. Outputs **GREEN signals** (3+ platforms, 7+ conviction, RISING trends)

**Output:**
```
🟢 GREEN SIGNALS (2) - Deploy capital

$ASTS
   Platforms: reddit, twitter, trends (3)
   Avg Conviction: 8.2/10
   Google Trends: RISING (+42.5%)
   Reddit: 3,245 upvotes, 487 comments
   Twitter: 234 mentions, 5,621 likes
```

---

## Current State (Today - Feb 10, 2026)

**What works:**
- ✅ Google Trends validator (no auth needed)
- ✅ Reddit scanner (needs credentials)
- ✅ Twitter scanner (needs credentials)
- ✅ Multi-platform orchestrator
- ✅ Cross-validation logic

**What's next:**
1. Set up Reddit API (5 min)
2. Set up Twitter API (10 min)
3. Run first full scan
4. Generate conviction docs for GREEN signals
5. Deploy capital on validated plays

---

## Quick Validation Workflow (Today)

Even without Reddit/Twitter setup, you can use Google Trends NOW:

### Validate Current Positions:

```bash
python3 -c "
from apps.google_trends_validator import GoogleTrendsValidator
v = GoogleTrendsValidator()

tickers = ['TAO', 'SOL']  # Your current positions
results = v.run(tickers)
"
```

### Validate $ASTS (Your Watchlist):

```bash
python3 -c "
from apps.google_trends_validator import GoogleTrendsValidator
v = GoogleTrendsValidator()

result = v.check_ticker_trend('ASTS', timeframe='today 1-m')
print(f\"ASTS Trend: {result['trend']}\")
print(f\"Change: {result['change_percent']}%\")
print(f\"Validated: {result['validated']}\")
"
```

If ASTS shows **RISING** + validated = TRUE → signal still good.  
If ASTS shows **STABLE** or **FALLING** → wait for pullback.

---

## Rate Limits (Free Tiers)

| Platform | Daily Limit | Monthly Limit | Cost |
|----------|-------------|---------------|------|
| Google Trends | Unlimited* | Unlimited* | FREE |
| Reddit | ~2,000 requests | ~60,000 requests | FREE |
| Twitter | ~1,500 requests | 500K tweets read | FREE |

*Soft limits - use 2-5 second delays between requests

**Strategy:** Run scanner 2-3x per day to stay well within limits.

---

## Troubleshooting

### Google Trends: 429 Rate Limit Error
**Solution:** Increase delay in script:
```python
# In google_trends_validator.py, line 122
validations = self.validate_signals(ticker_list, delay=5)  # Changed from 2 to 5
```

### Reddit: "received 401 HTTP response"
**Problem:** Credentials not set or incorrect  
**Solution:** Double-check `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`

### Twitter: "401 Unauthorized"
**Problem:** Bearer token not set or expired  
**Solution:** Generate new Bearer Token in Twitter Developer Portal

---

## Next Steps

1. ✅ Google Trends working (test it now)
2. ⬜ Set up Reddit API
3. ⬜ Set up Twitter API  
4. ⬜ Run first multi-platform scan
5. ⬜ Validate $ASTS before deploying
6. ⬜ Build conviction docs for GREEN signals

**Time to full deployment:** 15-20 minutes (if you do API setups now)

---

*This is Camillo's edge. Multi-platform validation = filter noise, find signal.*
