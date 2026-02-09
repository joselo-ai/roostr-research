# Dumb Money Discord Scraping Guide
**Purpose:** Find high-conviction social arbitrage stock plays  
**Updated:** Feb 7, 2026

---

## 🎯 What We're Looking For

**Social Arbitrage = Community conviction → Market movement**

**Signal Criteria:**
- 🟢 **GREEN:** 25+ 🔥 or 🚀 reactions = Deploy capital
- 🟡 **YELLOW:** 15-24 reactions = Watch for catalyst
- 🔴 **RED:** <15 reactions = Noise, ignore

---

## 📋 Manual Scraping Process (Until Bot Ready)

### Step 1: Check Dumb Money Discord Daily
**Channels to monitor:**
- #stock-plays
- #earnings-plays
- #options-flow
- #swing-trades

### Step 2: Look for High-Reaction Posts
**What to count:**
- 🔥 Fire reactions (strong conviction)
- 🚀 Rocket reactions (momentum)
- 👍 Thumbs up (agreement)

**Example:**
```
Message: "$ASTS - Space Mobile launching satellites Q2. 
Undervalued at $8B market cap. PT $50"

Reactions: 34🔥 16🚀 8👍
Total high-conviction: 34+16 = 50 → GREEN
```

### Step 3: Extract Key Info
For each GREEN/YELLOW signal, note:
- Ticker: $ASTS
- Total reactions: 50 (34🔥 + 16🚀)
- Thesis: (copy from message)
- First seen: (date)
- Latest mention: (date)

### Step 4: Create Conviction Doc
Use template: `trading/conviction-docs/$TICKER-social-arb.md`

**Template structure:**
```markdown
# $TICKER - Social Arbitrage Conviction Doc
**Source:** Dumb Money Discord  
**Conviction:** GREEN (50 reactions)

## Community Metrics
- Fire: 34
- Rocket: 16
- Mentions: 12
- First seen: 2026-02-06

## Thesis
[Copy from Discord]

## Validation Checklist
- [ ] Google Trends (search spike?)
- [ ] Fundamentals (earnings, products)
- [ ] Social media (Twitter, TikTok)
- [ ] NOT mainstream (no CNBC yet)
- [ ] Entry price + stop loss

## Decision
- [ ] GREEN - Deploy $10-15k
- [ ] YELLOW - Watch 7 days
- [ ] RED - Pass
```

---

## 🤖 Automated Scraping (Coming Soon)

**Built:** `dumbmoney_researcher.py` (ready, needs Discord data)

**Once Discord bot is set up:**
1. Bot scrapes channels every 6 hours
2. Auto-generates conviction docs for GREEN signals
3. Pings you with: "New GREEN: $TICKER - 50 reactions - Review conviction doc"
4. You approve → Deploy capital

**For now:** Manual scraping daily until bot is live.

---

## 📊 Current Signals (Manual Tracking)

### GREEN Signals (25+ reactions)
- **$ASTS:** 34🔥 16🚀 (Feb 6) - Conviction doc created
- _(Add more as found)_

### YELLOW Signals (15-24 reactions)
- **$RNDR:** 18🔥 5🚀 (Feb 5) - Watching
- _(Add more as found)_

---

## 🎯 Next Steps

1. **Daily:** Check Dumb Money Discord manually
2. **Find GREEN:** 25+ 🔥/🚀 reactions
3. **Create doc:** Use template above
4. **Validate:** Google Trends + fundamentals
5. **Deploy:** $10-15k if GREEN confirmed
6. **Later:** Discord bot automates this entire flow

---

**Goal:** Find 2-3 GREEN social arbitrage plays per month  
**Target allocation:** $30k bucket (3 positions x $10k each)
