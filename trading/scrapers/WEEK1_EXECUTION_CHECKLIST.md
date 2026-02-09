# Week 1 Execution Checklist
**Scraper AI - Ready to Deploy**  
**Review Date:** Feb 5, 2026  
**Target Start:** Feb 6, 2026 (Tomorrow)  

---

## ✅ What's Ready NOW

### Infrastructure Built
- [x] **discord_fetcher.py** - Discord bot integration (fetch messages via API)
- [x] **data_quality_checker.py** - 3-layer validation system (filter garbage)
- [x] **daily_scrape_morning.sh** - Automated pipeline (end-to-end)
- [x] **Config auto-generation** - Creates blacklist + channel config automatically
- [x] **Logging system** - Daily logs + error tracking
- [x] **Quality reporting** - Daily quality metrics

### Documentation Written
- [x] **SCRAPER_ANALYSIS_REPORT.md** - Full analysis (42KB, comprehensive)
- [x] **README_INFRASTRUCTURE.md** - Setup guide + troubleshooting
- [x] **This checklist** - Week 1 execution plan

---

## 🔧 What Needs Setup (1-2 Hours)

### 1. Discord Bot Creation (30 min)
**Task:** Create bot, get token, add to servers  
**Owner:** Joselo or G  
**Steps:**
1. Go to https://discord.com/developers/applications
2. Create New Application → Add Bot
3. Copy bot token → Set `export DISCORD_BOT_TOKEN='token'`
4. Enable Message Content Intent + Server Members Intent
5. Generate OAuth URL (permissions: Read Messages, Read History)
6. Add bot to these servers:
   - Chart Fanatics ✅ (already have access)
   - Dumb Money ✅ (already have access)
   - Yieldschool ⚠️ (if accessible, else skip for now)

**Test:**
```bash
export DISCORD_BOT_TOKEN='your_token'
python3 discord_fetcher.py --hours 1
# Should fetch messages and create fetched_messages.json
```

---

### 2. Channel ID Configuration (15 min)
**Task:** Map Discord channel IDs to config  
**Owner:** Joselo or G  
**Steps:**
1. Enable Discord Developer Mode (Settings → Advanced)
2. Right-click each target channel → Copy ID
3. Edit `config/channel_ids.json`:
   ```json
   {
     "servers": {
       "chart_fanatics": {
         "guild_id": "YOUR_GUILD_ID",
         "channels": {
           "riz_eurusd": "PASTE_CHANNEL_ID_HERE"
         }
       },
       "dumbmoney": {
         "guild_id": "YOUR_GUILD_ID",
         "channels": {
           "main": "PASTE_CHANNEL_ID_HERE"
         }
       }
     }
   }
   ```

**Target Channels:**
- Chart Fanatics: Riz's EURUSD channel
- Dumb Money: Main discussion channel (high-conviction theses)
- (Yieldschool: Skip if login issues, add later)

---

### 3. Dependencies Installation (5 min)
**Task:** Install Python packages  
**Owner:** Run on server/laptop  
**Steps:**
```bash
pip install discord.py requests pytrends yfinance

# Verify
python3 -c "import discord; print('Discord.py OK')"
```

---

### 4. Update Existing Scrapers (30 min)
**Task:** Modify scrapers to accept Discord fetcher output  
**Owner:** Scraper AI (me) - will do tomorrow  
**Changes:**
- `yieldschool_scraper.py`: Add `--input fetched_messages.json` arg
- `dumbmoney_scraper.py`: Add `--input fetched_messages.json` arg
- Output to JSON instead of CSV directly

**Not blocking - can run manually first day if needed**

---

## 📅 Day-by-Day Plan

### Day 1 (Feb 6) - Foundation
**Morning (9 AM):**
- [ ] Set up Discord bot (Joselo/G)
- [ ] Configure channel IDs
- [ ] Test Discord fetcher: `python3 discord_fetcher.py --hours 24`

**Afternoon:**
- [ ] Scraper AI: Update yieldschool_scraper.py for JSON input
- [ ] Scraper AI: Update dumbmoney_scraper.py for JSON input
- [ ] Test scrapers with real fetched data

**Evening:**
- [ ] Run full pipeline manually: `./daily_scrape_morning.sh`
- [ ] Review logs, fix any errors
- [ ] Deploy first 1-2 signals if GREEN found

**Success Metric:** Pipeline runs end-to-end without crashes

---

### Day 2 (Feb 7) - Quality Framework
**Morning:**
- [ ] Review Day 1 signal quality (any false positives?)
- [ ] Expand ticker blacklist if needed
- [ ] Test data quality checker on 50+ signals

**Afternoon:**
- [ ] Scraper AI: Integrate real Dexscreener API
- [ ] Scraper AI: Integrate real Google Trends (pytrends)
- [ ] Test external validation on 5 sample signals

**Evening:**
- [ ] Run pipeline with validation enabled
- [ ] Compare GREEN signals (before/after validation)
- [ ] Document which signals were filtered and why

**Success Metric:** <10% false positive rate

---

### Day 3 (Feb 8) - Automation
**Morning:**
- [ ] Set up cron jobs for 3 daily runs
- [ ] Test cron execution (run midday manually)

**Afternoon:**
- [ ] Build notification system (Discord webhook or email)
- [ ] Test alert on GREEN signal

**Evening:**
- [ ] Monitor automated run (6 PM)
- [ ] Verify logs written correctly
- [ ] Check dashboard updated

**Success Metric:** Automated pipeline runs without manual intervention

---

### Day 4-5 (Feb 9-10) - Server Expansion
**Goals:**
- [ ] Join 5 Tier 1 servers (WhaleBotAlerts, TheTIE, etc.)
- [ ] Add channel IDs to config
- [ ] Test fetching from new servers
- [ ] Review signal quality from each source

**Success Metric:** 7+ servers actively scraped

---

### Day 6-7 (Feb 11-12) - Optimization
**Goals:**
- [ ] Profile pipeline (identify bottlenecks)
- [ ] Add parallel processing if needed
- [ ] Build signal consolidation (cross-source merging)
- [ ] Review Week 1 performance

**Success Metric:** Pipeline completes in <5 minutes

---

## 🎯 Week 1 Success Criteria

**Must-Have:**
- [x] Infrastructure built (Discord fetcher, quality checker, pipeline)
- [ ] Discord bot operational (fetching from 3+ servers)
- [ ] Data quality validation working (<10% false positives)
- [ ] Automated pipeline running daily (9 AM, 12 PM, 6 PM)
- [ ] 50+ signals collected and validated
- [ ] 5+ GREEN signals generated
- [ ] First 1-2 paper trades deployed from signals

**Nice-to-Have:**
- [ ] External validation integrated (Dex, Trends)
- [ ] Notification system (alerts on GREEN signals)
- [ ] 7+ servers scraped (Tier 1 list)
- [ ] Signal consolidation (multi-source boosting)

**Stretch Goals:**
- [ ] 100+ signals in database
- [ ] Twitter scraping (bonus source)
- [ ] ML-based scam detection

---

## ⚠️ Risk Mitigation

### Risk: Discord bot token leaked
**Mitigation:** Store in .env file (not git), rotate if exposed

### Risk: API rate limits (Dex, Trends)
**Mitigation:** Add caching layer, limit to 100 checks/day

### Risk: False positives slip through quality check
**Mitigation:** Manual review of first 50 signals, refine blacklist

### Risk: Scrapers crash mid-run
**Mitigation:** Error logging, retry logic, graceful fallback

### Risk: No GREEN signals generated (too strict)
**Mitigation:** Start with lower thresholds (conviction ≥7), raise later

---

## 🚀 Launch Readiness

### Pre-Flight Checklist (Run Before Day 1)
- [ ] Discord bot created and token saved
- [ ] Bot added to Chart Fanatics + Dumb Money
- [ ] Channel IDs configured in config/channel_ids.json
- [ ] Dependencies installed (discord.py, requests, pytrends)
- [ ] Test run: `python3 discord_fetcher.py --hours 1`
- [ ] Test run: `python3 data_quality_checker.py`
- [ ] Review logs directory created: `mkdir -p ../logs`
- [ ] Backup existing signals-database.csv: `cp ../signals-database.csv ../signals-database.backup.csv`

### Go/No-Go Decision (Morning of Day 1)
**GO if:**
- ✅ Discord bot fetching messages successfully
- ✅ Quality checker passing test signals
- ✅ Logs directory writable
- ✅ Joselo/G available to review first signals

**NO-GO if:**
- ❌ Discord bot permissions denied
- ❌ Critical dependencies missing
- ❌ No one available to review output

---

## 📞 Escalation

**If something breaks:**
1. Check error log: `cat ../logs/errors_$(date +%Y-%m-%d).log`
2. Review README_INFRASTRUCTURE.md troubleshooting section
3. Ping Scraper AI (me) with error details
4. Fallback: Run components manually (skip automation)

**If quality too low:**
1. Review quality report: `cat ../logs/quality_report_$(date +%Y-%m-%d).txt`
2. Identify top rejection reasons
3. Adjust thresholds in `data_quality_checker.py`
4. Re-run validation: `python3 data_quality_checker.py`

---

## 📊 Reporting (End of Week 1)

**Metrics to Track:**
- Total signals scraped
- GREEN / YELLOW / RED breakdown
- False positive rate (manual review of 20 random signals)
- Pipeline uptime (% successful runs)
- Processing speed (seconds per signal)
- Signal accuracy (did GREEN signals move as expected?)

**Deliverables:**
- Week 1 performance report
- Updated signal database (50+ entries)
- List of issues encountered + fixes applied
- Plan for Week 2 (Tier 2 servers, improvements)

---

## 💪 Ready to Execute

**Infrastructure:** ✅ Built  
**Documentation:** ✅ Complete  
**Blockers:** ⚠️ Discord bot setup (1 hour)  
**Timeline:** Can start tomorrow (Feb 6)  

**Scraper AI status: READY**  
**Awaiting:** G + Joselo approval to begin  

Let's ship this. 🐓
