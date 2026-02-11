# Social Arbitrage Agent 🐓

**Version:** 1.0.0  
**Built:** February 11, 2026  
**Status:** ✅ Deployed

---

## Overview

The Social Arbitrage Agent scans Reddit, Discord, and Twitter for viral stock signals using engagement metrics. Inspired by Camillo's 77% annual returns from social arbitrage trading.

**Core Logic:**
- High engagement (upvotes, 🔥 reactions) = crowd attention
- Low market cap (<$5B) = room to run
- Catalyst present = reason for move
- Signal Score = engagement × catalyst_multiplier / market_cap

---

## Installation

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading

# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas requests yfinance
```

---

## Usage

### Manual Scan

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
source venv/bin/activate

# Basic scan (saves to signals-database.csv)
python agents/social_arbitrage_agent.py

# Custom parameters
python agents/social_arbitrage_agent.py \
    --min-engagement 30 \
    --max-market-cap 3000000000 \
    --min-conviction 7.0

# Test mode (no save, mock data)
python agents/social_arbitrage_agent.py --test --no-save
```

### Automated Daily Scan

```bash
# Run via shell script
./agents/run_social_scan.sh

# Or add to cron (9 AM daily)
0 9 * * * /Users/agentjoselo/.openclaw/workspace/trading/agents/run_social_scan.sh
```

---

## Configuration

### Environment Variables (Optional)

Set these for live Reddit scanning:

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_SECRET="your_secret"
export REDDIT_USER_AGENT="roostr-social-arb/1.0"
```

Without these, the agent uses mock data based on historical Dumb Money signals.

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `--min-engagement` | 20 | Minimum engagement score (upvotes + comments*2 + reactions*3) |
| `--max-market-cap` | 5e9 | Maximum market cap ($5B) |
| `--min-conviction` | 5.0 | Minimum conviction score (0-10) to report |
| `--no-save` | False | Skip saving to database |
| `--test` | False | Use mock data (no API calls) |

---

## Conviction Score Formula

```python
score = (engagement / 100) * catalyst_mult * cap_bonus

where:
  engagement = upvotes + comments*2 + fire*3 + rocket*3
  catalyst_mult = 2.0 if catalyst present, else 1.0
  cap_bonus = min(5.0, 5.0 / market_cap_billions)
  
capped at 10.0
```

### Examples

**ASTS (AST SpaceMobile):**
- Engagement: 666 (342 upvotes + 87*2 comments + 34*3 fire + 16*3 rocket)
- Market Cap: $4.2B
- Catalyst: FCC approval expected
- **Conviction: 10.0/10** ✅

**ACGL (Arch Capital):**
- Engagement: 250
- Market Cap: $28B (large)
- Catalyst: Insurance sector strength
- **Conviction: 0.9/10** ⚠️ (filtered out due to large cap)

**PLTR (Palantir):**
- Engagement: 800 (high)
- Market Cap: $42B (too large)
- **Filtered before scoring** 🔴

---

## Output

### Console Report

```
================================================================================
🐓 SOCIAL ARBITRAGE AGENT REPORT
================================================================================
Scan Date: 2026-02-11 09:00 EST
Signals Found: 2

📊 SIGNAL #1: ASTS
   Conviction: 10.0/10
   Source: Reddit-wallstreetbets
   Engagement: 666 points
      ├─ Upvotes: 342
      ├─ Comments: 87
      ├─ 🔥 Reactions: 34
      └─ 🚀 Reactions: 16
   Market Cap: $4.20B
   Catalyst: FCC approval expected Q1 2026
   Title: AST SpaceMobile: FCC approval imminent 🚀
   URL: https://reddit.com/r/wallstreetbets/...
```

### Database Output

Signals are appended to `signals-database.csv`:

| Ticker | Source | Date_Found | Conviction_Score | Status | Notes |
|---|---|---|---|---|---|
| ASTS | Reddit-wallstreetbets | 2026-02-11 | 10.0 | Monitoring | FCC approval expected Q1 2026 |

---

## Integration with roostr System

### 1. Daily Workflow

```
9:00 AM EST → Social Arb Agent scans Reddit/Discord
              ↓
          Finds 5-10 signals
              ↓
          Scores by conviction (0-10)
              ↓
          Saves high-conviction (>5/10) to database
              ↓
          18-agent ensemble votes on each
              ↓
          Quant Agent backtests
              ↓
          Joselo validates risk
              ↓
          G approves if >7/10
```

### 2. Agent Ensemble

Social Arb Agent is **Tier 1** (roostr-specific agent):
- Generates initial candidate list
- Other 17 agents vote on these candidates
- Ensemble conviction = weighted average of all votes

### 3. Dashboard Display

Signals appear in "Active Watchlist" with:
- 🐓 Social Arb badge
- Engagement metrics
- Conviction score
- Ensemble vote breakdown

---

## Testing

### Run Tests

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading
source venv/bin/activate
python agents/test_social_arb.py
```

### Expected Output

```
🧪 TESTING SOCIAL ARBITRAGE AGENT
================================================================================
✅ ASTS: High conviction (10.0/10) - small cap + high engagement
⚠️  ACGL: Medium conviction (0.9/10) - large cap penalty
🔴 PLTR: Filtered out - exceeds max market cap

✅ All tests passed. Agent logic validated.
```

---

## Known Limitations

### Current State (v1.0.0)

✅ **Working:**
- Conviction scoring logic
- Market cap filtering
- Engagement metrics
- Database integration
- Mock data mode

⚠️ **Not Yet Implemented:**
- Live Reddit API integration (requires credentials)
- Discord scraping
- Twitter/X scraping
- Real-time monitoring
- Exit signal generation

### Roadmap (v1.1.0)

- [ ] Reddit API integration (PRAW)
- [ ] Discord webhook listener
- [ ] Twitter API v2 integration
- [ ] Real-time monitoring (WebSocket)
- [ ] Exit signal detection (engagement drops)
- [ ] Sentiment analysis (bullish/bearish classification)

---

## Architecture

```
social_arbitrage_agent.py
├── SocialArbitrageAgent (main class)
│   ├── scan_reddit() → scrape Reddit posts
│   ├── extract_tickers() → find $TICKER mentions
│   ├── get_market_cap() → fetch via yfinance
│   ├── calculate_conviction_score() → score 0-10
│   ├── filter_signals() → min conviction threshold
│   ├── generate_report() → human-readable output
│   ├── save_to_database() → append to CSV
│   └── run_scan() → full pipeline
└── main() → CLI entry point
```

---

## Debugging

### Common Issues

**"No module named 'pandas'"**
```bash
source venv/bin/activate
pip install pandas requests yfinance
```

**"Reddit API credentials not set"**
- Expected in v1.0.0 (uses mock data)
- Set `REDDIT_CLIENT_ID` and `REDDIT_SECRET` for live scanning

**"No signals found"**
- Check `--min-conviction` threshold (lower it)
- Verify `--max-market-cap` isn't too low
- Run in `--test` mode to see mock data

---

## Performance Metrics

### Target (90-Day Validation)

| Metric | Target |
|---|---|
| Signals/Day | 5-10 |
| High-Conviction (>7/10) | 1-3/day |
| Win Rate | >60% |
| Avg Hold Period | 15-30 days |
| Avg Return | 15-25% |

### Historical Validation

Testing against known Dumb Money signals (2024-2025):

| Signal | Engagement | Conviction | Actual Result |
|---|---|---|---|
| ASTS | 666 | 10.0/10 | Monitored (FCC pending) |
| ACGL | 250 | 0.9/10 | Filtered (cap too large) |
| TAO | N/A | N/A | (Not social arb signal) |

---

## Contributing

To improve the agent:

1. **Add data sources:** Implement Discord, Twitter scrapers
2. **Enhance scoring:** Add sentiment analysis, options flow
3. **Exit signals:** Detect when engagement drops (sell signal)
4. **Backtesting:** Run on historical Reddit archives (Pushshift)

---

## Support

**Issues?** Check main trading README:  
`/Users/agentjoselo/.openclaw/workspace/trading/README.md`

**Questions?** Ask Joselo 🐓

---

**Built by:** Joselo (roostr Capital AI)  
**Inspired by:** Camillo's 77% social arb strategy  
**Purpose:** Scale signal discovery 10x without human bottleneck

*"The crowd is sometimes right. The edge is knowing when."*
