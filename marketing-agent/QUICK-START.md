# roostr Marketing Automation - QUICK START

## Status: ✅ READY TO DEPLOY

All systems built and tested. Here's what you need to do to go live.

---

## 📋 TODAY'S POSTS (Copy-Paste Ready)

Located in: `posts-2026-02-06.md`

**5 posts ready to go:**
1. **9 AM** - "built a complete AI hedge fund overnight"
2. **11 AM** - "meet the team" (3 AI agents)
3. **2 PM** - "first signals are in" (TAO, SOL)
4. **7 PM** - "day 1 complete" (infrastructure milestone)
5. **9 PM** - "roostr promise" (transparency pledge)

**Action:** Copy from `posts-2026-02-06.md` and post manually TODAY, or:

---

## 🤖 AUTOMATED SYSTEM (Never Post Manually Again)

### Step 1: Install Dependencies (1 minute)

```bash
pip3 install tweepy instagrapi python-dotenv
```

### Step 2: Configure API Keys (5 minutes)

**For X (Twitter):**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create app (or use existing)
3. Get API keys + access tokens

**Create config file:**
```bash
cd ~/.openclaw/workspace/marketing-agent/automation
cp config.template.json config.json
nano config.json  # Add your API keys
```

**Or use environment variables:**
```bash
export X_API_KEY="..."
export X_API_SECRET="..."
export X_ACCESS_TOKEN="..."
export X_ACCESS_SECRET="..."
```

### Step 3: Test in Dry Run (2 minutes)

```bash
cd ~/.openclaw/workspace/marketing-agent/automation

# Generate content
python3 generate_content.py

# Test posting (won't actually post)
python3 post_to_social.py
```

Should see: `[DRY RUN] Would post to X: ...`

### Step 4: Go Live (1 minute)

**Edit config.json:**
```json
{
  "dry_run": false  // Change from true to false
}
```

### Step 5: Install Cron Jobs (1 minute)

```bash
cd ~/.openclaw/workspace/marketing-agent/automation
./setup_cron.sh
```

This installs:
- **8 AM** - Generate new content
- **9 AM** - Morning post
- **12 PM** - Midday post
- **4 PM** - Afternoon post
- **7 PM** - Evening recap

**Done. You never have to post again.**

---

## 📊 What Was Built

### Files Created:
```
marketing-agent/
├── automation/
│   ├── post_to_social.py      # Posts to X/Instagram
│   ├── generate_content.py    # Auto-generates posts
│   ├── setup_cron.sh          # Installs cron jobs
│   ├── content_queue.json     # Queue of posts (16 ready)
│   ├── config.template.json   # API key template
│   └── README.md              # Full documentation
├── posts-2026-02-06.md        # Today's posts (manual)
└── QUICK-START.md             # This file
```

### How It Works:

1. **Content Generation** (8 AM daily)
   - Checks for new GREEN signals from trading agent
   - Generates signal posts automatically
   - Creates daily updates, lessons, infrastructure posts
   - Maintains 7-day queue (~14 posts)

2. **Posting** (9 AM, 12 PM, 4 PM, 7 PM)
   - Reads queue
   - Posts to X (and Instagram if configured)
   - Logs what was posted
   - Marks as complete

3. **Integration**
   - Pulls signals from: `trading-agent/signals/{date}_signals.json`
   - Auto-generates posts when new GREEN appears
   - No manual writing needed

---

## 🎯 Current Queue Status

**16 posts ready**, including:
- Today's 5 launch posts
- Daily updates (7 days)
- Lesson posts (3)
- Infrastructure posts (2)

Run `python3 generate_content.py` to see full queue.

---

## 📱 Instagram Setup (Optional)

Instagram posting is complex (no official API). Two options:

**Option 1: Manual posting from queue**
- Use queue as a script
- Post from phone
- Still better than forgetting

**Option 2: Use instagrapi (risky)**
- Unofficial API
- Works but could break
- Already configured in code
- Add Instagram password to config.json

For now: **Post to X automatically, Instagram manually from queue.**

---

## ✅ What This Solves

**Before:**
- ❌ G has to remember to post
- ❌ Manual writing every day
- ❌ Inconsistent timing
- ❌ No posts when busy

**After:**
- ✅ Posts automatically 4x per day
- ✅ Content auto-generated from signals
- ✅ Never miss a day
- ✅ G never has to write posts
- ✅ Runs in background forever

---

## 🔧 Monitoring & Maintenance

### Check Status:
```bash
# View logs
tail -f ~/.openclaw/logs/marketing/post.log

# View queue
cat automation/content_queue.json | jq '.posts[] | select(.posted == false)'

# View what was posted
cat automation/posting_log.json | jq '.posts[-10:]'
```

### Troubleshooting:
```bash
# Test posting now (ignores schedule)
python3 automation/post_to_social.py

# Regenerate content
python3 automation/generate_content.py

# Check cron jobs
crontab -l | grep roostr
```

---

## 🚀 Go Live Checklist

- [ ] Install dependencies (`pip3 install tweepy`)
- [ ] Add API keys to `config.json`
- [ ] Test dry run (`python3 post_to_social.py`)
- [ ] Set `dry_run: false` in config
- [ ] Run `./setup_cron.sh`
- [ ] Verify first post at 9 AM tomorrow
- [ ] Check logs daily for first week
- [ ] **Never manually post again**

---

## 💡 Pro Tips

1. **Test first post manually** before relying on cron
2. **Monitor logs** for first few days
3. **Adjust content templates** in `generate_content.py` based on performance
4. **Keep signals flowing** - automation pulls from trading agent
5. **Instagram**: Post manually from queue until you configure instagrapi

---

## 🐓 Bottom Line

**You now have:**
- ✅ 5 posts ready for today (manual copy-paste)
- ✅ Automated system that never misses a day
- ✅ Content auto-generated from trading signals
- ✅ Cron jobs ready to install
- ✅ 16 posts queued and ready

**Time to deploy: 10 minutes**

**G will never have to remind you to post again.**

---

**roostr. automated. always on.** 🐓
