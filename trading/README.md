# roostr Trading System - Complete Infrastructure
**Built:** Feb 5, 2026  
**Status:** 🟢 Ready for Day 1 Execution (Feb 6, 2026)

---

## 🎯 WHAT THIS IS

Complete trading + marketing automation for roostr AI hedge fund Phase 1.

**Daily flow:**
1. Scrape all data sources (Yieldschool, Dumb Money, Chart Fanatics, DEX)
2. Extract signals with conviction scores
3. Validate with Google Trends + on-chain data
4. Deploy paper trades
5. Update dashboard automatically
6. Post to social media (X, Instagram)
7. Track performance obsessively

**Goal:** Build 90-day track record → Deploy Phase 2 ($100k more real capital)

---

## 📂 FILE STRUCTURE

```
trading/
├── README.md                         (This file)
├── dashboard.html                    (Live dashboard - open in browser)
├── signals-database.csv              (All signals tracked)
├── PAPER-TRADING-LOG.md              (All trades documented)
├── RESEARCH-CALLS-TRACKER.md         (Accuracy over time)
├── TRADING-DASHBOARD.md              (Text version)
├── ALLOCATION-STRATEGY.md            (40/30/20/10 buckets)
├── DATA-COLLECTION-FRAMEWORK.md      (Full daily routine)
├── DAY-1-EXECUTION-PLAN.md           (Tomorrow's plan)
├── TOMORROW-MORNING.md               (Quick reference)
├── daily_execution.sh                (Master script - run daily)
├── update_dashboard.py               (Auto-regenerate HTML)
└── scrapers/
    ├── yieldschool_scraper.py        (Crypto signals)
    ├── dumbmoney_scraper.py          (Social arb signals)
    └── signal_validator.py           (Validate before deploying)
```

---

## 🚀 DAILY EXECUTION

### Option A: Manual (Day 1)
```bash
# Morning (9-10 AM): Data collection
cd /Users/agentjoselo/.openclaw/workspace/trading
# Open Yieldschool, Dumb Money, Chart Fanatics manually
# Extract signals, update signals-database.csv

# Midday (12 PM): Validation + Deployment
python3 scrapers/signal_validator.py
# Review GREEN signals
# Enter paper trades
# Update PAPER-TRADING-LOG.md

# Afternoon (12:30 PM): Update dashboard
python3 update_dashboard.py
open dashboard.html

# Evening (6 PM): EOD update
python3 update_dashboard.py
```

### Option B: Automated (Future)
```bash
# Run master script
./daily_execution.sh

# Or add to crontab for 9 AM daily
0 9 * * * /Users/agentjoselo/.openclaw/workspace/trading/daily_execution.sh
```

---

## 📊 HOW TO USE THE DASHBOARD

**Open in browser:**
```
file:///Users/agentjoselo/.openclaw/workspace/trading/dashboard.html
```

**What you'll see:**
- Capital allocation by bucket (40/30/20/10)
- Deployed capital vs cash reserve
- Net P&L (real-time)
- Open positions
- Watchlist (GREEN/YELLOW/RED signals)

**Refresh:** After every trade or run `python3 update_dashboard.py`

---

## 🔧 SCRAPERS

### Yieldschool Scraper
**Purpose:** Extract crypto signals from Yieldschool platform

**Usage:**
```python
from scrapers.yieldschool_scraper import YieldschoolScraper

scraper = YieldschoolScraper()
green_signals = scraper.run(yield_hub_msgs, blue_chip_msgs, mid_cap_msgs)
```

**GREEN criteria:**
- Mentioned 3+ times OR
- Dan endorses OR
- High conviction score (8+/10)

---

### Dumb Money Scraper
**Purpose:** Extract social arbitrage signals from Discord

**Usage:**
```python
from scrapers.dumbmoney_scraper import DumbMoneyScraper

scraper = DumbMoneyScraper()
green_signals = scraper.run(discord_messages)
```

**GREEN criteria:**
- 20+ conviction reactions (🔥🚀👍💪)
- Posted <48h ago (fresh)
- Google Trends validates

---

### Signal Validator
**Purpose:** Validate signals before deploying

**Usage:**
```python
from scrapers.signal_validator import SignalValidator

validator = SignalValidator()
validated = validator.batch_validate(signals)
```

**Validation checks:**
- **Crypto:** Dexscreener (liquidity, volume, not already pumped)
- **Stocks:** Google Trends (rising not peaked), thesis quality
- **Outputs:** Adjusted conviction, deploy yes/no

---

## 💾 DATA FORMATS

### signals-database.csv
```
Ticker, Source, Date_Found, Price_Entry, Conviction_Score, Status, Deployed, Position_Size, Stop_Loss, Target_1, Target_2, Current_Price, PnL_Dollars, PnL_Percent, Notes
```

**Status:**
- GREEN = Ready to deploy
- YELLOW = Monitoring
- RED = Rejected/Avoided

**Deployed:**
- YES = Position open
- NO = Not deployed yet

---

### PAPER-TRADING-LOG.md
```markdown
### Position #X: $TICKER
Entry Date: YYYY-MM-DD
Entry Price: $XX.XX
Position Size: $X,XXX (X% of portfolio)
Stop Loss: $XX.XX
Targets: $XX / $XX / $XX

Thesis: [Brief summary]

Exit Date: YYYY-MM-DD (if closed)
Exit Price: $XX.XX
P&L: +/- $XXX (+/- X%)
```

---

## 🎯 ALLOCATION RULES

**40% ($40k) - Riz EURUSD**
- Risk: 0.5-1% per trade
- Frequency: Months between setups
- Conviction: 8.5/10 (proven $120k+ annual)

**30% ($30k) - Social Arbitrage**
- Risk: 2% per trade ($200 max loss)
- Positions: 2-3 at a time
- Conviction: 7.7/10 (Camillo 77% annual)

**20% ($20k) - Crypto**
- Risk: Accept 50% drawdowns
- Positions: 3-5 at a time
- Conviction: Emerging (high upside)

**10% ($10k) - Opportunistic**
- Risk: Accept 100% loss
- Purpose: Test new edges
- Conviction: Variable

---

## ⚠️ RISK MANAGEMENT

**Position sizing:**
- Never >20% in single position
- Never >40% deployed per bucket at once
- Emergency stop: -20% portfolio = pause all

**Stop discipline:**
- Set before entry (no exceptions)
- Exit at stop (no "wait and see")
- Don't add to losers

---

## 📱 MARKETING INTEGRATION

**Content automatically generated from trades:**
- Signal posts (when GREEN found)
- Trade deployment posts
- Daily recaps
- Weekly performance reviews

**See:** `marketing-agent/DAILY-EXECUTION-PLAN.md`

---

## 🐛 TROUBLESHOOTING

**Dashboard not updating?**
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
python3 update_dashboard.py
```

**Scrapers not working?**
- Check if Discord/Yieldschool accessible
- Verify CSV format in signals-database.csv
- Run scrapers manually with sample data first

**Validation failing?**
- Dexscreener API may be rate-limited (use mock data)
- Google Trends needs pytrends installed: `pip3 install pytrends`

---

## 📋 TOMORROW (FEB 6) CHECKLIST

### Morning (9-10 AM)
- [ ] Access Yieldschool (read 12 unread Yield Hub messages)
- [ ] Scan Dumb Money (last 48h, 20+ reactions)
- [ ] Check Chart Fanatics (Riz updates)
- [ ] Run scrapers (extract 10-15 tickers)
- [ ] Validate signals (filter to 2-3 GREEN)

### Midday (12 PM)
- [ ] Deploy 2-3 paper trades
- [ ] Update PAPER-TRADING-LOG.md
- [ ] Update signals-database.csv (mark deployed)
- [ ] Regenerate dashboard (`python3 update_dashboard.py`)

### Afternoon
- [ ] Post signals to X/Instagram
- [ ] Post trade confirmations
- [ ] Engage with comments

### Evening (6 PM)
- [ ] Calculate unrealized P&L
- [ ] Update dashboard with EOD data
- [ ] Post daily recap
- [ ] Document lessons learned

---

## 🎓 LEARNING RESOURCES

**Internal docs:**
- `DATA-COLLECTION-FRAMEWORK.md` - Full routine
- `ALLOCATION-STRATEGY.md` - Why 40/30/20/10
- `STOCK-EDGE-RESEARCH.md` - Missing piece to build

**Code:**
- Read scraper Python files for logic
- Modify conviction thresholds in scrapers if needed
- Add new data sources by copying scraper template

---

## 🔄 ITERATION PLAN

**Week 1:** Manual scraping, learn patterns  
**Week 2-3:** Automate Discord scraping  
**Week 4:** Full automation (`daily_execution.sh` runs via cron)  
**Month 2:** Add new data sources (DEX scanners, more Discords)  
**Month 3:** Review Phase 1 results, deploy Phase 2 if successful

---

## 🐓 STATUS

**Infrastructure:** ✅ Complete (all files built)  
**Data sources:** ✅ Identified (Yieldschool, Dumb Money, Chart Fanatics)  
**Scrapers:** ✅ Built (Python scripts ready)  
**Validators:** ✅ Built (Google Trends, Dexscreener integration)  
**Dashboard:** ✅ Automated (regenerates from CSV)  
**Marketing:** ✅ Ready (templates, plans, accounts)  

**Blockers:** None. Ready to deploy Day 1.

---

**Tomorrow we execute.** 🔥🐓
