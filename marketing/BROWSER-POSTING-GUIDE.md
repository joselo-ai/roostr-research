# Twitter Browser Posting Guide

**Free alternative to $100/month API tier**

---

## How It Works

1. **Script identifies** next tweet based on time slot
2. **You manually post** to X (or automate with OpenClaw browser tool)
3. **Script marks** tweet as posted in queue

---

## Daily Workflow

### Step 1: Check what needs posting

```bash
cd /Users/agentjoselo/.openclaw/workspace/marketing
python3 twitter_browser_poster.py
```

**Output:**
```
🐓 Twitter Browser Auto-Poster
============================================================
📅 Current slot: midday (14:00)

📝 Tweet to post:
   ID: w3-2
   Date: 2026-02-19

💬 Text (227 chars):
------------------------------------------------------------
Position check (Day 8):
...
------------------------------------------------------------

🔗 Reply to: https://x.com/roostrcapital/status/2022053449681314006
```

### Step 2: Post to X

**If standalone tweet:**
1. Go to https://x.com/compose/tweet
2. Copy/paste the text
3. Click "Post"

**If reply (has "Reply to" URL):**
1. Open the reply-to URL in browser
2. Click "Reply"
3. Copy/paste the text
4. Click "Reply"

### Step 3: Mark as posted

After posting, copy the new tweet URL and run:

```bash
python3 mark_posted.py w3-2 https://x.com/roostrcapital/status/NEW_TWEET_ID
```

**Example:**
```bash
python3 mark_posted.py w3-2 https://x.com/roostrcapital/status/2023456789012345678
```

**Output:**
```
✅ Marked w3-2 as posted
   URL: https://x.com/roostrcapital/status/2023456789012345678
   Time: 2026-02-19T12:05:30
```

---

## Posting Schedule

| Slot | Time | When to Run |
|------|------|-------------|
| **Morning** | 9 AM | Run at 9 AM, post immediately |
| **Midday** | 12 PM | Run at 12 PM, post immediately |
| **Afternoon** | 4 PM | Run at 4 PM, post immediately |
| **Evening** | 7 PM | Run at 7 PM, post immediately |

---

## Automation (Future)

To fully automate via OpenClaw browser tool:

1. **Navigate to X:** `browser.navigate("https://x.com")`
2. **Click compose:** Find and click "Post" button
3. **Type text:** `browser.type(tweet_text)`
4. **Post:** Click "Post" button
5. **Extract URL:** Get new tweet URL from page
6. **Mark posted:** Run `mark_posted.py` automatically

**For now:** Manual posting is faster than building full browser automation.

---

## Current Status

✅ **Working:**
- Tweet identification (correct slot)
- Text extraction
- Reply-to handling
- Posted tracking

❌ **Not automated yet:**
- Actual posting to X (manual step)
- URL extraction (you provide it)

**Trade-off:** 2 minutes/day manual work vs $100/month API cost.

---

## Files

| File | Purpose |
|------|---------|
| `twitter_browser_poster.py` | Identifies next tweet, shows text |
| `mark_posted.py` | Updates queue after you post |
| `content-queue.json` | All tweets (posted + unposted) |
| `posted-log.json` | History of all posted tweets |
| `.twitter-credentials.json` | API keys (not used for browser method) |

---

## Quick Reference

**See what needs posting:**
```bash
python3 twitter_browser_poster.py
```

**After posting manually:**
```bash
python3 mark_posted.py <tweet_id> <new_url>
```

**Check queue status:**
```bash
cat content-queue.json | grep '"posted": false' | wc -l
```

---

**Next:** Run `twitter_browser_poster.py` at scheduled times, post manually, mark as posted.

**Alternative:** Pay $100/month for X API Basic tier = full automation.
