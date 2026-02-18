# roostr Capital - Market Analysis Framework
**Complete Methodology for Opportunity Discovery & Evaluation**

Last Updated: February 18, 2026

---

## Table of Contents
1. [Investment Philosophy](#investment-philosophy)
2. [Data Sources](#data-sources)
3. [Analysis Framework](#analysis-framework)
4. [Conviction Scoring System](#conviction-scoring-system)
5. [Risk Management](#risk-management)
6. [Position Sizing](#position-sizing)
7. [18-Agent Deliberation Process](#18-agent-deliberation-process)

---

## Investment Philosophy

### Core Principle
**Information asymmetry = profit opportunity**

We hunt markets where we can know something before the crowd:
- Social signals before Wall Street analyst reports
- On-chain crypto data before exchange listings
- Technical setups before retail panic/euphoria
- Fundamental value before institutional rerating

### Strategy Allocation
| Strategy | Allocation | Why |
|----------|------------|-----|
| **Value Investing** | 40% ($40k) | Buffett/Graham methodology, high conviction stocks |
| **Social Arbitrage** | 30% ($30k) | Camillo's 77% annual return model |
| **Crypto Fundamentals** | 20% ($20k) | Dan's $500→$500k methodology |
| **Opportunistic** | 10% ($10k) | Riz setups, airdrops, special situations |

**Phase 1:** $100k paper trading (current)  
**Success Criteria:** >20% returns, <15% drawdown, >60% win rate over 90 days

---

## Data Sources

### Primary Intelligence Sources

#### 1. **Yieldschool** (Crypto Fundamentals)
- **Access:** Discord server (paid membership)
- **Channels:**
  - `#yield-hub`: Dan's high-conviction crypto picks
  - `#blue-chips`: BTC/ETH/SOL analysis
  - `#mid-caps`: 10-100M market cap opportunities
  - `#live-sessions`: Real-time market commentary
- **Methodology:** Dan's $500→$500k framework
  - Category creation (new narrative)
  - Novel technology (not just a fork)
  - Supply dynamics (low float, high lockup)
  - Institutional interest
  - Community conviction
- **Validation:** Atlas ML model (45+ features)
- **How We Use It:** Extract signals, validate with on-chain data, score conviction

#### 2. **Dumb Money** (Social Arbitrage)
- **Access:** Discord server (free)
- **Signal Detection:** Emoji reactions
  - 20+ 👍 = strong social signal
  - 5+ 🔥 = catalyst confirmation
  - Combined reactions = higher conviction
- **Methodology:** Chris Camillo's social arbitrage (77% annual return)
  - Consumer behavior changes → earnings impact
  - Social media trends → stock price lag (3-6 months)
  - Reddit/TikTok mentions → institutional coverage
- **How We Use It:** Track stocks with high engagement, validate with fundamentals, front-run Wall Street

#### 3. **Chart Fanatics** (Technical Edge)
- **Access:** Discord server (paid)
- **Primary Focus:** Riz's EURUSD methodology
  - $120k+ annual on prop accounts
  - Months between setups (patience > volume)
  - 0.5-1% risk per trade, 5:1 R:R minimum
  - Liquidity sweeps + HTF alignment
- **Setup Criteria:**
  - Daily/weekly timeframe alignment
  - Liquidity sweep (stop hunt)
  - Institutional order blocks
  - 5:1 minimum risk/reward
- **How We Use It:** Monitor for GREEN signals (Riz explicitly calls trades), deploy allocated capital

#### 4. **Dexter** (Fundamental Research Agent)
- **Technology:** virattt/dexter (15k+ stars on GitHub)
- **Data Source:** Financial Datasets API (institutional-grade)
- **Capabilities:**
  - Income statements, balance sheets, cash flow
  - SEC filings (10-K, 10-Q, 8-K)
  - Insider trades
  - Analyst estimates
  - DCF valuation models
- **Integration:** Python wrapper at `trading/apps/dexter_research.py`
- **How We Use It:** Feed to 18-agent system for fundamental debate

#### 5. **Dexscreener** (On-Chain Crypto Intelligence)
- **Use Case:** Crypto validation layer
- **Metrics Tracked:**
  - Liquidity depth
  - Volume trends (24h, 7d, 30d)
  - Holder distribution
  - DEX pair health
- **How We Use It:** Validate Yieldschool signals aren't pump-and-dumps

#### 6. **Google Trends** (Retail Interest Validation)
- **Use Case:** Confirm social signals aren't overhyped
- **Logic:**
  - Trending up = early (good for entry)
  - Peaked = late (avoid or exit)
  - Flat = no retail FOMO yet (ideal)
- **How We Use It:** Final validation before GREEN status

#### 7. **Reddit** (Social Sentiment Scraper)
- **Subreddits Monitored:**
  - r/wallstreetbets (meme stocks, retail momentum)
  - r/stocks (fundamental discussions)
- **Metrics:**
  - Post upvotes (>1000 = viral)
  - Comment sentiment
  - Velocity (how fast it's spreading)
- **How We Use It:** Automated scraper (`trading/apps/reddit_scraper.py`), feeds conviction system

---

## Analysis Framework

### Signal Discovery Process

```
1. DATA COLLECTION (Daily)
   ↓
   Yieldschool new posts
   Dumb Money reactions
   Chart Fanatics setups
   Reddit trending stocks
   Dexscreener new pairs
   
2. INITIAL FILTER
   ↓
   Yieldschool: Dan posted?
   Dumb Money: >20 reactions?
   Chart Fanatics: Riz called it?
   Reddit: >1k upvotes + catalyst?
   
3. VALIDATION LAYER
   ↓
   Dexter: Pull financials
   Dexscreener: Check liquidity
   Google Trends: Retail interest?
   
4. 18-AGENT DELIBERATION
   ↓
   12 Legendary Investors debate
   4 Quant Agents score metrics
   Risk Manager (Joselo) gates decision
   Portfolio Manager sizes position
   
5. CONVICTION SCORING
   ↓
   ≥8.0/10 = GREEN (deploy)
   5.0-7.9/10 = YELLOW (watch)
   <5.0/10 = RED (avoid)
   
6. RISK APPROVAL
   ↓
   Joselo + Hull dual-layer approval
   Position sizing formula
   Stop loss placement
   
7. EXECUTION
   ↓
   Alpaca API (paper Phase 1)
   Auto stop-loss at entry
   Dashboard update
   Conviction doc published
```

---

## Conviction Scoring System

### Formula (0-10 Scale)

```python
conviction_score = (
    source_quality * 2.0 +      # Max 2.0 (Yieldschool Dan = 2.0, Reddit = 0.5)
    catalyst_strength * 2.0 +   # Max 2.0 (FCC approval = 2.0, earnings = 1.5)
    fundamental_score * 2.0 +   # Max 2.0 (P/E, ROE, debt, growth)
    technical_score * 2.0 +     # Max 2.0 (RSI, volume, breakout)
    social_validation * 2.0     # Max 2.0 (20+ reactions = 2.0, trends = 1.0)
) / 10.0
```

### Thresholds

| Score | Status | Action |
|-------|--------|--------|
| **≥8.0** | 🟢 GREEN | Deploy capital (high conviction) |
| **7.0-7.9** | 🟡 YELLOW+ | Strong watch, needs minor confirmation |
| **5.0-6.9** | 🟡 YELLOW | Monitor, gather more data |
| **<5.0** | 🔴 RED | Avoid or exit |

### Score Components Breakdown

#### Source Quality (0-2.0)
- **2.0:** Yieldschool Dan, Chart Fanatics Riz
- **1.5:** Dumb Money + multiple validators
- **1.0:** Reddit viral + fundamentals
- **0.5:** Single unvalidated source

#### Catalyst Strength (0-2.0)
- **2.0:** FDA approval, FCC decision, major partnership
- **1.5:** Earnings beat, buyback announcement
- **1.0:** Analyst upgrade, insider buying
- **0.5:** General sector trend

#### Fundamental Score (0-2.0)
**Stocks:**
- P/E ratio (<10 = +0.5, <15 = +0.3)
- ROE (>20% = +0.5, >15% = +0.3)
- Debt/Equity (<0.3 = +0.5, <0.5 = +0.3)
- Growth (>20% = +0.5)

**Crypto:**
- Category creation (+0.8)
- Novel tech (+0.6)
- Supply dynamics (+0.4)
- Community strength (+0.2)

#### Technical Score (0-2.0)
- Breakout from consolidation (+0.5)
- Volume surge (>2x average = +0.5)
- RSI (30-50 = +0.5, oversold recovery)
- HTF alignment (daily/weekly = +0.5)

#### Social Validation (0-2.0)
- Dumb Money reactions (20+ = +1.0, 10-19 = +0.5)
- Reddit upvotes (>1000 = +0.5)
- Google Trends (rising = +0.3, stable = +0.2)
- Multiple platforms (+0.5)

---

## Risk Management

### Position-Level Rules

1. **Stop Loss (Mandatory)**
   - Stocks: -8% to -15% (based on volatility)
   - Crypto: -15% to -20% (higher volatility tolerance)
   - Set at entry, never widened

2. **Position Sizing**
   - Max 20% per position (10/10 conviction only)
   - Typical 5-10% per position
   - Min 2% (testing new edge)

3. **Portfolio-Level Rules**
   - Max 10% total risk (if all stops hit simultaneously)
   - Max 10 open positions
   - Max 100% deployed per strategy bucket

4. **Execution Discipline**
   - No entries without written conviction doc
   - No trades after 3 PM EST (avoid close volatility)
   - No revenge trading after stop-loss
   - Pause all trading if down >2% intraday

### Daily Limits (Safeguards)
- Max 3 new positions per day
- Max 10 total open positions
- Auto-pause if portfolio down >5% from peak

---

## Position Sizing

### Conviction-Weighted Formula

```python
position_size = base_capital * (conviction_score / 10.0) * bucket_allocation

Example:
- Portfolio: $100,000
- Bucket: Value (40% = $40,000)
- Signal: $ALL (10/10 conviction)
- Position: $40,000 * (10/10) * 0.5 = $20,000 (20% of portfolio)

- Signal: $PGR (9/10 conviction)
- Position: $40,000 * (9/10) * 0.5 = $18,000 → round to $15,000 (15%)

- Signal: $KTB (7.5/10 conviction)
- Position: $30,000 * (7.5/10) = $22,500 → cap at $10,000 (10%)
```

### Position Size Caps
| Conviction | Max Position Size | Typical Use Case |
|------------|------------------|------------------|
| 10/10 | 20% | Buffett-level conviction (rare) |
| 9/10 | 15% | Strong multi-source validation |
| 8/10 | 10% | Good setup, solid thesis |
| 7/10 | 7% | Testing new edge |
| 6/10 | 5% | Speculative, low risk |
| <6/10 | No trade | Insufficient conviction |

---

## 18-Agent Deliberation Process

### Agent Roster

#### Legendary Investors (12)
1. **Warren Buffett** - Value investing, moats, management quality
2. **Charlie Munger** - Mental models, inversion, patience
3. **Michael Burry** - Contrarian deep value, macro analysis
4. **Benjamin Graham** - Net-nets, margin of safety, quantitative value
5. **Mohnish Pabrai** - Cloning, checklist investing, asymmetric bets
6. **Cathie Wood** - Disruptive innovation, long-term vision
7. **Phil Fisher** - Quality growth, scuttlebutt method
8. **Peter Lynch** - 10-baggers, consumer insight, growth at reasonable price
9. **Bill Ackman** - Activist value, catalyst-driven, concentration
10. **Stanley Druckenmiller** - Macro + micro, position sizing, flexibility
11. **Aswath Damodaran** - Valuation rigor, DCF modeling, narrative vs numbers
12. **Rakesh Jhunjhunwala** - Emerging market value, conviction sizing, patience

#### Quant Agents (4)
1. **Valuation Agent** - DCF, multiples, comps analysis
2. **Sentiment Agent** - Social signals, Google Trends, Reddit metrics
3. **Fundamentals Agent** - Financial ratios, growth rates, balance sheet health
4. **Technicals Agent** - RSI, volume, breakouts, support/resistance

#### Risk & Execution (2)
1. **Risk Manager (Joselo)** - Portfolio-level risk, position sizing, stop-loss enforcement
2. **John C. Hull** - Quantitative risk (VaR, Expected Shortfall, Greeks, stress testing)

### Deliberation Flow

```
1. SIGNAL INPUT
   ↓
   New opportunity detected
   Pull all available data (Dexter, Dexscreener, social)
   
2. LEGENDARY INVESTOR DEBATE
   ↓
   Each agent analyzes from their framework
   Buffett: "Does it have a moat?"
   Burry: "Is the market overlooking something?"
   Munger: "What's the base rate? Invert the problem."
   Pabrai: "Who else won with this pattern?"
   Druckenmiller: "What's the macro context?"
   
3. QUANT SCORING
   ↓
   Valuation: DCF = $X, current = $Y, upside = Z%
   Sentiment: 20 reactions, trending +15%
   Fundamentals: P/E 5.4, ROE 39%, debt 0.2x
   Technicals: RSI 45, breakout confirmed
   
4. CONSENSUS VOTE
   ↓
   Each agent votes 0-10
   Average = preliminary conviction score
   
5. RISK GATEKEEPING
   ↓
   Joselo: "Does this fit portfolio risk budget?"
   Hull: "What's the VaR? Tail risk?"
   If approved → size position
   If rejected → back to watch list
   
6. CONVICTION DOC GENERATION
   ↓
   Auto-generate markdown report
   Bull case, bear case, catalysts, risks
   Publish to GitHub (full transparency)
   
7. EXECUTION APPROVAL
   ↓
   Final human approval (G)
   Or auto-execute if conviction ≥9.0 (future)
```

### Example Deliberation Output

See `trading/agents/signals/AAPL_DELIBERATION_REPORT.md` for full format.

**Summary:**
- **Consensus Score:** 8.5/10
- **Bull Votes:** Buffett (9/10), Lynch (9/10), Pabrai (8/10)
- **Bear Votes:** Burry (7/10 - valuation concern)
- **Risk Assessment:** Joselo approved, Hull flagged macro headwinds
- **Decision:** GREEN - Deploy $15k (15% position)

---

## Practical Application Examples

### Example 1: $ALL (Allstate) - Value Play

**Discovery:**
- Source: Stock screener (P/E < 10, ROE > 20%)
- Validation: Buffett agent scored 10/10 (insurance moat, buyback catalyst)

**Analysis:**
- P/E: 5.45 (vs sector 12x) → +0.5 fundamental
- ROE: 39.52% → +0.5 fundamental
- Catalyst: $4B buyback → +2.0 catalyst
- Debt/Equity: 0.28 → +0.5 fundamental
- Technical: Breakout from consolidation → +0.5 technical

**Conviction Score:** 10/10 (rare)

**Position:** $20,000 (20% of portfolio, highest conviction)

**Stop Loss:** $XXX (-10%)

**Thesis:** Undervalued insurance leader with capital return catalyst. Buffett playbook.

---

### Example 2: $TAO (Bittensor) - Crypto Fundamentals

**Discovery:**
- Source: Yieldschool Dan (2.0 source quality)
- Category: AI + crypto infrastructure (novel)

**Analysis:**
- Category creation: Decentralized ML → +0.8 fundamental
- Novel tech: Not a fork → +0.6 fundamental
- Supply dynamics: Low float → +0.4 fundamental
- Community: Strong builder focus → +0.2 fundamental
- Validation: Atlas ML model 45+ features → +1.0 technical
- Social: Yieldschool community consensus → +1.0 social

**Conviction Score:** 9/10

**Position:** $10,000 (10% of portfolio)

**Stop Loss:** $140.84 (-20%)

**Thesis:** Dan's $500→$500k methodology. Category creation, pre-institutional adoption.

---

### Example 3: $ASTS (Declined) - Insufficient Conviction

**Discovery:**
- Source: Reddit (1000+ upvotes)
- Catalyst: FCC approval expected Q1

**Analysis:**
- Catalyst strength: Regulatory approval → +2.0 catalyst
- Social validation: Reddit viral → +1.0 social
- Fundamentals: Unprofitable, speculative → +0.5 fundamental
- Technical: No clear entry → +0.5 technical
- Source quality: Reddit (unvalidated) → +0.5 source

**Conviction Score:** 4.5/10 (RED)

**Decision:** AVOID. Catalyst-driven hype without fundamental support. Wait for FCC decision, then reassess.

---

## Tools & Infrastructure

### Automated Systems
1. **Signal Scraper** (`apps/signal_scraper.py`)
   - Runs hourly
   - Checks Yieldschool, Dumb Money, Reddit
   - Outputs `new-signals.txt`

2. **Price Updater** (`apps/price_updater.py`)
   - TradingView API
   - Hourly price + RSI updates
   - Auto-commits to GitHub

3. **Risk Monitor** (`apps/risk_monitor.py`)
   - Every 5 minutes
   - Checks all positions vs stop-loss
   - Telegram alert if violated

4. **19-Agent Deliberation** (`agents/legendary_investors_v2.py`)
   - On-demand or automated (future)
   - Generates conviction docs
   - Discord #research channel output

5. **Dashboard** (`dashboard.html`)
   - Live portfolio tracking
   - Public: https://joselo-ai.github.io/roostr-research/trading/
   - Auto-updated every 5 min

### Data Storage
- **Signals Database:** `signals-database.csv`
- **Performance Journal:** `performance-journal.jsonl`
- **Conviction Docs:** `agents/signals/*.md`
- **Daily Memory:** `memory/YYYY-MM-DD.md`

---

## Key Documents Reference

| Document | Purpose | Location |
|----------|---------|----------|
| ALLOCATION-STRATEGY.md | Strategy buckets, fund sizing | `trading/` |
| DATA-COLLECTION-FRAMEWORK.md | Data sources, scraping methods | `trading/` |
| ALPACA-SETUP.md | Trading API configuration | `trading/` |
| PAPER-TRADING-LOG.md | Live position tracking | `trading/` |
| QUICKSTART_19_AGENTS.md | Agent system usage | `trading/agents/` |
| Deliberation reports | Full agent debates | `trading/agents/signals/` |

---

## Daily Workflow

### Morning (9 AM)
1. Run signal scraper
2. Review new opportunities
3. Check Riz for EURUSD setups
4. Update dashboard

### Midday (12 PM)
1. Price updates
2. Check portfolio P&L
3. Scan for deployment priorities

### Afternoon (4 PM)
1. Position reviews
2. Stop-loss checks
3. Update conviction docs

### Evening (7 PM)
1. Daily summary
2. Commit to GitHub
3. Plan tomorrow's research

---

## Success Metrics (Phase 1)

**Target (90 days):**
- Return: >20%
- Max Drawdown: <15%
- Win Rate: >60%
- Conviction Accuracy: ≥8.0/10 signals perform as expected

**Current Status (Day 12):**
- Portfolio: $100k paper
- Deployed: $17.5k (17.5%)
- P&L: +$75 (+0.43%)
- Positions: 2 (TAO, SOL)
- Win Rate: 50% (TAO winning, SOL testing)

**Next Milestone:**
- Deploy remaining buckets (Riz EURUSD, Social Arb)
- Hit 5+ positions by Day 30
- First 10/10 conviction trade closed profitably

---

**End of Framework Document**

*This document evolves as we refine our edge. All updates committed to GitHub.*

*For questions or clarifications, see `/trading/README.md` or ask Joselo directly.*
