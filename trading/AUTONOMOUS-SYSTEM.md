# Autonomous Trading System

**Status:** ✅ Built (Phase 1)  
**Model:** Salience-loop based on G's trading framework  
**Conviction Threshold:** ≥8.0/10 for autonomous execution

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  🐓 AUTONOMOUS PIPELINE (4-hour cycles)                      │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
    │  SCAN  │      │  RESEARCH   │    │  DECIDE   │
    │  4h    │──────│ Perplexity  │────│ 18 Agents │
    │  cron  │      │  deep dive  │    │ Consensus │
    └────────┘      └─────────────┘    └───────────┘
                                              │
                                    ┌─────────▼─────────┐
                                    │   Conviction ≥8.0? │
                                    └─────────┬─────────┘
                                              │
                           ┌──────────────────┼──────────────────┐
                           │                  │                  │
                      ┌────▼─────┐      ┌─────▼──────┐    ┌─────▼─────┐
                      │ EXECUTE  │      │  MONITOR   │    │   CLOSE   │
                      │ Alpaca   │──────│  5min      │────│  At stop  │
                      │ Paper    │      │  checks    │    │  or exit  │
                      └──────────┘      └────────────┘    └─────┬─────┘
                                                                 │
                                                          ┌──────▼──────┐
                                                          │    LEARN    │
                                                          │  Salience   │
                                                          │    Loop     │
                                                          └─────────────┘
```

---

## Components

### 1. **autonomous_pipeline.py**
Main execution loop that runs 24/7.

**Cycle:** Every 4 hours
- ✅ Scan for new signals (signal_scraper.py)
- ✅ Monitor open positions (risk_monitor.py)
- ✅ Extract learnings daily at 4pm (salience_loop.py)

**Decision Flow:**
```
Signal found
  ↓
Research with Perplexity (deep dive)
  ↓
18-agent deliberation
  ↓
Conviction ≥ 8.0?
  ↓ YES
Execute trade (Alpaca paper)
  ↓
Monitor every 5min
  ↓
Close at stop-loss or exit signal
  ↓
Extract learning + update salience
```

### 2. **perplexity_research.py**
Structured deep research on every signal before deliberation.

**Requires:** `PERPLEXITY_API_KEY` environment variable

**Research Structure:**
- Fundamentals (business, revenue, growth)
- Catalysts (upcoming events, news)
- Technical setup (price action, support/resistance)
- Risk factors (company, sector, market)
- Enhanced conviction (adjusted from initial signal)

**Model:** `llama-3.1-sonar-large-128k-online`

### 3. **salience_loop.py**
Self-learning system that extracts patterns and manages knowledge.

**Salience Scoring (0-1):**
- Win with high conviction (≥8.0): +0.6 initial
- Win with low conviction (<8.0): +0.4 initial
- Loss with high conviction: +0.3 initial
- Loss with low conviction: +0.1 initial
- **Time decay:** -0.02 per week

**Knowledge Tiers:**
- **< 0.2:** Archive to `memory/failed-patterns.md` (avoid repeating)
- **0.2-0.8:** Active in `learnings.md` (reference during deliberation)
- **> 0.8:** Promote to `TRADING_DOCS/` (proven edge, cite in conviction docs)

**Run:** Daily at 4pm (market close)

---

## File Structure

```
trading/
├── apps/
│   ├── autonomous_pipeline.py   # Main 24/7 loop
│   ├── perplexity_research.py   # Deep research integration
│   ├── salience_loop.py         # Self-learning system
│   ├── signal_scraper.py        # (existing) Scan Reddit/Discord/Twitter
│   ├── risk_monitor.py          # (existing) Watch positions
│   └── autonomous_executor.py   # (existing) Execute trades via Alpaca
│
├── learnings.md                 # Active patterns (salience 0.2-0.8)
├── memory/
│   └── failed-patterns.md       # Archived low-salience patterns
├── TRADING_DOCS/                # Promoted high-salience patterns (>0.8)
├── research/                    # Perplexity research reports
├── salience-database.json       # Salience scores for all learnings
└── logs/
    └── execution.jsonl          # Pipeline event log
```

---

## Setup

### 1. **Environment Variables**

```bash
# Required for Perplexity research
export PERPLEXITY_API_KEY="pplx-xxxxx"

# Already configured (Alpaca paper trading)
# ALPACA_API_KEY, ALPACA_SECRET_KEY in trading/.alpaca.env
```

### 2. **Start Autonomous Pipeline**

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading

# Run in background (recommended)
nohup python3 apps/autonomous_pipeline.py > logs/pipeline.log 2>&1 &

# Or run in foreground (for testing)
python3 apps/autonomous_pipeline.py
```

### 3. **Monitor Logs**

```bash
# Watch pipeline events
tail -f logs/execution.jsonl

# Watch output log
tail -f logs/pipeline.log
```

### 4. **Stop Pipeline**

```bash
# Find process ID
ps aux | grep autonomous_pipeline

# Kill process
kill <PID>
```

---

## Current Status

**Phase 1: ✅ BUILT**
- [x] Autonomous pipeline skeleton
- [x] Perplexity research integration
- [x] Salience loop (self-learning)
- [x] Event logging
- [x] Documentation

**Phase 2: 🔄 TODO (Integration)**
- [ ] Connect pipeline → perplexity_research.py
- [ ] Connect pipeline → deliberation.py (18 agents)
- [ ] Connect pipeline → autonomous_executor.py --live
- [ ] Test full end-to-end flow with paper trading

**Phase 3: 🔄 TODO (Enhancements)**
- [ ] Perplexity API key setup
- [ ] Salience manual override (G can boost/penalty learnings)
- [ ] Dashboard visualization of salience scores
- [ ] Telegram alerts for autonomous executions

---

## Safety Controls

**Conviction Threshold:** Only execute if 18-agent consensus ≥ 8.0/10

**Position Limits:**
- Max $10k per position (1% of $1M paper portfolio)
- Conviction-weighted sizing (8.0/10 = $8k, 10/10 = $10k)

**Stop Loss:** Automatic 15% on every trade

**Spending Limits:**
- Paper trading only (Phase 1)
- Real money requires G approval + Phase 2 validation

**Kill Switch:**
- Stop pipeline process anytime
- Positions can be manually closed in Alpaca dashboard

---

## Next Steps

1. **Test Perplexity Integration**
   ```bash
   python3 apps/perplexity_research.py
   ```

2. **Test Salience Loop**
   ```bash
   python3 apps/salience_loop.py
   ```

3. **Run Full Pipeline** (when ready)
   ```bash
   python3 apps/autonomous_pipeline.py
   ```

4. **Get Perplexity API Key**
   - Sign up: https://www.perplexity.ai/pro
   - Generate key: https://www.perplexity.ai/settings/api
   - Add to environment: `export PERPLEXITY_API_KEY="pplx-xxxxx"`

---

**Built:** 2026-02-15  
**Model:** Based on G's salience-loop trading framework  
**Status:** Ready for testing & integration
