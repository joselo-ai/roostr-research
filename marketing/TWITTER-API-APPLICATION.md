# Twitter API Application - Action Required

**Date:** Feb 12, 2026  
**Account:** @roostrcapital  
**Purpose:** Automate daily trading posts

---

## 🎯 Apply for Twitter Elevated API Access

### Step 1: Access Developer Portal
1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Sign in with @roostrcapital credentials:
   - Email: agentjoselo@gmail.com
   - Password: RoostrCapital2026!

### Step 2: Apply for Elevated Access
1. Click "Apply for Elevated" (if available) or "Projects & Apps"
2. Select "Elevated" tier (FREE)
3. Fill out application form:

**How will you use the Twitter API?**
```
I operate @roostrcapital, a transparent trading research account sharing 
investment signals, portfolio updates, and market analysis. I need API 
access to automate:

1. Daily trading signal posts (stock picks with conviction scores)
2. Portfolio performance updates (positions, P&L, risk metrics)
3. Market research threads (investment theses, data analysis)

All content is original research, non-promotional, and educational. 
Goal: Build in public, share wins AND losses, help retail traders 
make better decisions.

No spam, no bots pretending to be human, no mass following/unfollowing. 
Just authentic trading content on a schedule.
```

**Will your app use Tweet, Retweet, Like, Follow, or Direct Message functionality?**
```
Yes - Tweet functionality only.

I will post original trading content (signals, updates, analysis) 
to my own timeline. No retweets, no likes, no follows, no DMs.
```

**Do you plan to analyze Twitter data?**
```
No. I only need to POST content (Tweets), not analyze or read Twitter data.
```

**Will your product, service, or analysis make Twitter content or derived 
information available to a government entity?**
```
No.
```

---

### Step 3: Wait for Approval
- **Timeline:** Usually 1-24 hours (sometimes instant)
- **Email notification:** Will be sent to agentjoselo@gmail.com
- **Check status:** developer.twitter.com/en/portal/dashboard

---

### Step 4: After Approval - Create App & Get Keys

1. Go to Projects & Apps
2. Create new app: "roostr Capital Bot"
3. App environment: Production
4. Generate keys and save them:

```bash
# Create secure credentials file
cat > /Users/agentjoselo/.openclaw/workspace/marketing/.twitter-api-keys << 'EOF'
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
ACCESS_TOKEN=your_access_token_here
ACCESS_TOKEN_SECRET=your_access_token_secret_here
EOF

chmod 600 /Users/agentjoselo/.openclaw/workspace/marketing/.twitter-api-keys
```

---

### Step 5: Install Tweepy

```bash
cd /Users/agentjoselo/.openclaw/workspace/marketing
python3 -m pip install --user tweepy
```

---

### Step 6: Test API Connection

```python
# Test script: marketing/test_twitter_api.py
import tweepy
import os

# Load credentials
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Test
print(f"Authenticated as: @{api.verify_credentials().screen_name}")
print("✅ Twitter API working!")
```

---

### Step 7: Update Cron Jobs

Replace browser automation with API calls in:
- `marketing/CRON-JOBS.md`
- Update job payloads to use `twitter_api_poster.py` script

---

## 📋 Application Checklist

- [ ] Apply for Elevated API access
- [ ] Wait for approval email
- [ ] Create app in developer portal
- [ ] Save API keys securely
- [ ] Install tweepy
- [ ] Test API connection
- [ ] Update cron jobs to use API
- [ ] Delete old browser automation scripts

---

**Status:** ⏸️ Waiting for manual application submission  
**Next:** Apply at developer.twitter.com TODAY
