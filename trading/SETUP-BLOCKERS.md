# Setup Blockers (Feb 9, 2026)

## 🔴 Blocked - Need Manual Input

### Discord Scraping
**Status:** Bot connected, but can't capture messages  
**Blocker:** Channel IDs not configured

**What's needed:**
1. Get Chart Fanatics channel IDs:
   - Right-click channel → Copy Channel ID (need Developer Mode enabled)
   - Update `/Users/agentjoselo/.openclaw/workspace/trading/config/discord_channels.json`
2. Get Dumb Money server access + channel IDs
3. Restart Discord listener after config update

**File:** `trading/config/discord_channels.json`

---

### Web Search
**Status:** Tool blocked  
**Blocker:** No Brave Search API key

**What's needed:**
1. Get API key from https://brave.com/search/api/
2. Run: `openclaw configure --section web`
3. Set `BRAVE_API_KEY` in Gateway environment

**Impact:** Can't research new signals (PLTR, TRV, RNDR fundamentals)

---

### Simmer Weather Trading
**Status:** API timing out all day  
**Blocker:** `api.simmer.markets` unresponsive

**What's needed:**
- Wait for Simmer API to recover, OR
- Contact Simmer support via https://t.me/+m7sN0OLM_780M2Fl

**Impact:** Weather markets not being scanned (low priority)

---

### X (Twitter) Posting
**Status:** Manual only  
**Blocker:** Chrome browser relay not attached

**What's needed:**
1. Open Chrome (profile with X logged in)
2. Click OpenClaw Browser Relay toolbar icon
3. Badge should turn ON (connected)

**Impact:** Evening marketing posts queued but not posted

**Drafted posts:**
- `marketing/evening-post-feb9.txt` (ready to post)

---

## 🟢 Working - No Blockers

- ✅ Price updater (CoinGecko for TAO/SOL)
- ✅ Dashboard auto-publishing (GitHub)
- ✅ Signals database (tracking 21 signals)
- ✅ Conviction docs (6 complete)
- ✅ Deployment readiness tracking
- ✅ Git automation (commits + pushes)

---

## 🟡 Partial - Workarounds Available

### Reddit Scraping
**Status:** Broken (API credentials missing)  
**Impact:** Low - Reddit signals already captured manually
**Workaround:** Manual Reddit monitoring for now

---

**Last updated:** 2026-02-09 18:30 EST
