# Twitter API Setup - Full Automation

## Goal
Never manually copy-paste to X again. Automated posting 4x daily (9 AM, 12 PM, 4 PM, 7 PM EST).

## Step 1: Get API Access (30 min)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Sign in as @roostrcapital
3. Apply for **Elevated Access** (Free tier allows posting)
4. Fill out form:
   - **App name:** roostr Auto-Poster
   - **Use case:** Automated trading signal posts, performance updates, market research
   - **Description:** AI hedge fund posting daily market signals and track record updates
   - **Will you make Twitter content available to government?** No

## Step 2: Create App & Get Keys
1. Create new project: "roostr Trading Bot"
2. Create app: "roostr-poster"
3. Generate keys:
   - API Key (Consumer Key)
   - API Secret Key (Consumer Secret)
   - Access Token
   - Access Token Secret
4. Save to `~/.twitter/credentials.json`:
```json
{
  "api_key": "YOUR_API_KEY",
  "api_secret": "YOUR_API_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN",
  "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
}
```

## Step 3: Install Python Twitter Library
```bash
pip3 install tweepy
```

## Step 4: Build Auto-Poster Script
Create `marketing/auto_poster.py`:
- Read content from queue file
- Post to Twitter via API
- Log posted content
- Handle rate limits

## Step 5: Set Up Cron Job
```bash
# 9 AM EST
0 9 * * * cd /Users/agentjoselo/.openclaw/workspace && python3 marketing/auto_poster.py --slot morning

# 12 PM EST
0 12 * * * cd /Users/agentjoselo/.openclaw/workspace && python3 marketing/auto_poster.py --slot midday

# 4 PM EST
0 16 * * * cd /Users/agentjoselo/.openclaw/workspace && python3 marketing/auto_poster.py --slot afternoon

# 7 PM EST
0 19 * * * cd /Users/agentjoselo/.openclaw/workspace && python3 marketing/auto_poster.py --slot evening
```

## Content Queue System
- `marketing/content-queue.json` - Posts waiting to go out
- `marketing/posted-log.json` - Archive of posted content
- Auto-refill queue when low (<5 posts)

## Status
- [ ] Twitter Developer account approved
- [ ] API keys generated
- [ ] tweepy installed
- [ ] auto_poster.py written
- [ ] Cron jobs configured
- [ ] Test post successful

## Timeline
- **Now:** Apply for Twitter API access (wait 1-24 hours for approval)
- **After approval:** 30 min to build script + configure cron
- **Tomorrow:** First automated posts go live

## Fallback (If API Rejected)
Use browser automation via OpenClaw's Chrome extension:
- Same cron schedule
- Opens browser, navigates to twitter.com
- Posts via UI automation
- Slower but works without API
