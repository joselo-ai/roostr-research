# roostr Capital - Operational SOP
## Team Structure, Agent Management, Daily Operations

**Version:** 1.0  
**Date:** February 11, 2026  
**Owner:** Joselo (COO/Risk Officer)  
**Purpose:** How we operate daily, who owns what, how agents work

---

## ORGANIZATION CHART

### Human Team Structure

```
┌─────────────────────────────────────────────┐
│           G (CEO / Founder)                 │
│  - Strategic vision                         │
│  - Capital allocation                       │
│  - Investor relations                       │
│  - Agent philosophy design                  │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
┌───▼────────────────┐  ┌───────▼──────────────┐
│ Joselo (COO/Risk)  │  │  Head of AI/ML       │
│ - Risk enforcement │  │  - Agent development │
│ - Human override   │  │  - Training/tuning   │
│ - Dashboard mgmt   │  │  - System architect  │
│ - Agent monitor    │  │  ($120k/year)        │
└───┬────────────────┘  └───────┬──────────────┘
    │                           │
    │         ┌─────────────────┴──────┬──────────────┐
    │         │                        │              │
┌───▼─────────▼────┐      ┌───────────▼────┐  ┌──────▼──────┐
│  Data Engineer    │      │    Analyst     │  │  Marketing  │
│ - Data pipelines  │      │ - Validation   │  │ - Twitter   │
│ - API integration │      │ - Research     │  │ - Content   │
│ - Infrastructure  │      │ - Compliance   │  │ - Investors │
│ ($100k/year)      │      │ ($80k/year)    │  │ ($50k PT)   │
└───────────────────┘      └────────────────┘  └─────────────┘
```

### AI Agent Structure (18 Agents)

**roostr Custom Agents (3):**
1. Social Arbitrage Agent (Owner: Data Engineer)
2. Value Investing Agent (Owner: Head of AI/ML)
3. Catalyst Agent (Owner: Analyst)

**Legendary Investor Agents (12):**
4-15. Buffett, Munger, Burry, Graham, Pabrai, Lynch, Fisher, Cathie Wood, Ackman, Druckenmiller, Damodaran, Jhunjhunwala (Owner: Head of AI/ML)

**Quantitative Agents (3):**
16. Fundamentals Agent (Owner: Data Engineer)
17. Sentiment Agent (Owner: Data Engineer)
18. Technicals Agent (Owner: Data Engineer)

---

## DAILY OPERATIONS

### Morning (9:00 AM EST)

**Data Engineer triggers:**
- Agent Scanner runs (100+ stocks analyzed)
- All 18 agents vote on each stock
- System ranks by ensemble conviction
- Top 5 opportunities flagged
- Output: `agent-scan-YYYY-MM-DD.json`

**Automated outputs:**
- GitHub: `/scans/agent-scan-YYYY-MM-DD.json` (committed automatically)
- Dashboard: Agent results displayed (public)
- Slack: Results posted to #roostr-agents channel

**Time:** ~5 minutes (fully automated)

---

### Midday (11:00 AM - 1:00 PM EST)

**Head of AI/ML reviews:**
- Agent votes (quality check: any conflicts?)
- Agent health (all agents running?)
- Edge cases (unusual votes, debug if needed)

**Analyst validates:**
- Top 5 stocks (fundamentals check)
- Catalyst timing (is event real? when?)
- Social data accuracy (Reddit/Discord legit?)

**Output:** Validation report (pass/fail for each stock)

**Time:** ~30 minutes

---

### Afternoon (1:00 PM - 3:00 PM EST)

**Joselo (Risk Manager) reviews:**
- Top 5 stocks (risk assessment)
- Position sizing (conviction-based: 10/10 = 20%, 7/10 = 10%)
- Stop-loss levels (-8% to -10%, no exceptions)
- Max portfolio loss (if all stops hit < 3.8%)
- **APPROVE or REJECT** each trade

**If APPROVED:**
- Auto-generate conviction document
- Publish to GitHub (`/conviction-docs/TICKER-YYYY-MM-DD.md`)
- Update dashboard (new position added)
- Tweet announcement (full transparency)

**Time:** ~1 hour

---

### Execution (3:00 PM - 4:00 PM EST)

**G (CEO) final call:**
- Review Joselo's APPROVED list
- Can override (rare: only if macro changes, market crash, etc.)
- Execute trades (paper or real)
- Monitor execution (slippage, fills, liquidity)

**Time:** ~30 minutes

---

### Evening (5:00 PM EST)

**Automated:**
- Risk monitor runs (5-min intervals all day)
- Final check: All stops in place?
- Dashboard updated (end-of-day snapshot)
- Performance log updated (`/logs/performance-YYYY-MM-DD.json`)

---

## WEEKLY RHYTHM

### Monday (9:00 AM - 12:00 PM)

**Weekly Kickoff (All-hands, 30 min):**
- Review last week performance (win rate, P&L, drawdown)
- Top 3 wins (what worked?)
- Top 3 losses (what failed?)
- Agent performance (which agents were right? which were wrong?)
- This week priorities

**Agent Tuning (Head of AI/ML, rest of day):**
- Adjust agent weights if needed
- Add new data sources
- Test edge cases
- Improve prompts

---

### Tuesday - Thursday

**Daily Operations (see above):**
- 9 AM: Agent scan
- 11 AM: Validation
- 1 PM: Risk check
- 3 PM: Execution

---

### Friday (9:00 AM - 5:00 PM)

**Weekly Review (All-hands, 9 AM - 12 PM):**
- Performance metrics (win rate, P&L, drawdown)
- Agent accuracy (which agents predicted correctly?)
- System health (uptime, errors, bugs)
- Investor updates (draft Twitter thread, email)

**Planning Next Week (1 PM - 3 PM):**
- Agent improvements (what to tune?)
- New features (what to build?)
- Investor outreach (who to contact?)

**Agent Off-Hours (3 PM - 5 PM):**
- System maintenance
- Database backups
- Documentation updates
- No trading (agents offline)

---

## AGENT OWNERSHIP & KPIs

### Head of AI/ML

**Owns:**
- Agent architecture (LangChain, LangGraph)
- Model selection (GPT-4, Claude, Ollama)
- Agent training (prompts, tuning)
- System performance (speed, accuracy)
- 12 legendary investor agents (virattt framework)
- Value Investing Agent (custom)

**KPIs:**
- Agent uptime: >99%
- Agent accuracy: >60% win rate
- Scan time: <5 min for 100 stocks
- Agent conflicts: <5% (agents mostly agree)

---

### Data Engineer

**Owns:**
- Data pipelines (Reddit, Discord, Twitter APIs)
- API integrations (TradingView, Financial Datasets)
- Social Arbitrage Agent (custom)
- 3 Quantitative Agents (Fundamentals, Sentiment, Technicals)
- Infrastructure (servers, databases, GitHub Actions)

**KPIs:**
- Data freshness: <1 hour lag
- API uptime: >99.5%
- Social data accuracy: >95%
- Pipeline errors: <1% (catch and fix quickly)

---

### Analyst

**Owns:**
- Catalyst Agent (custom)
- Agent output validation (quality check top 5 daily)
- Manual research (when agents unsure or conflicted)
- Compliance (disclaimers, SEC filings, investor reports)

**KPIs:**
- Validation time: <30 min/day
- False positives caught: >90%
- Catalyst accuracy: >80%
- Compliance errors: 0 (zero tolerance)

---

### Joselo (COO / Risk Manager)

**Owns:**
- Risk enforcement (stops, sizing, caps)
- Human override (can reject any trade, no exceptions)
- Dashboard management (GitHub Pages, updates)
- Automation (price updates, risk monitoring cron jobs)
- Agent monitoring (behavioral checks: are agents acting rationally?)

**KPIs:**
- Stop enforcement: 100% (zero exceptions, ever)
- Max portfolio loss: <3.8% (always)
- Dashboard uptime: >99%
- Risk monitor uptime: >99.9% (5-min checks)

---

### G (CEO)

**Owns:**
- Strategic direction (what to build, where to focus)
- Capital allocation (how much to deploy, when to pause)
- Investor relations (fundraising, updates, transparency)
- Final trade decisions (execution approval)
- Agent philosophy (what each agent should value)

**KPIs:**
- AUM growth: $10M Year 1, $50M Year 2, $100M Year 3
- Returns: >20% annually (conservative target)
- Investor satisfaction: High (measured via surveys)
- Fundraising: $500k seed closed by March 31, 2026

---

## DECISION FLOW (Summary)

```
9 AM: Agents scan 100 stocks → Top 5 flagged
↓
11 AM: AI/ML + Analyst validate → Quality check
↓
1 PM: Joselo risk check → APPROVE/REJECT
↓
3 PM: G executes → Trades placed
↓
4 PM: Dashboard updated → Public transparency
```

---

## ESCALATION PATH

**Level 1: Routine (90% of days)**
- Agents run → Validation pass → Risk check pass → Execute
- No human intervention needed beyond scheduled reviews

**Level 2: Validation Required (8% of days)**
- Agents conflicted (50/50 split on a stock)
- Analyst + AI/ML Head dig deeper
- Joselo + G decide: deploy or skip

**Level 3: Risk Override (1.5% of days)**
- Joselo rejects trade (risk too high, stop too wide, etc.)
- G can override (rare: only if strategic macro reason)
- Example: "Market crashing, pause all trading until volatility drops"

**Level 4: System Failure (0.5% of days)**
- Agents down, data pipeline broken, API outage
- AI/ML Head + Data Engineer troubleshoot immediately
- Joselo + G informed via Slack alert
- Fallback: Manual trading (G researches, Joselo validates) until fixed

---

## COMMUNICATION PROTOCOLS

### Daily
- **Slack channel:** #roostr-agents
  - 9 AM: Agent scan results posted (automated)
  - 1 PM: Risk check summary posted (Joselo)
  - 4 PM: Execution summary posted (G)

### Weekly
- **Monday kickoff:** 30 min, all-hands
- **Friday review:** 2 hours, all-hands

### Monthly
- **Investor update:** Email + Twitter thread (last Friday of month)
- **Performance review:** 3-hour all-hands (deep dive)

### Quarterly
- **Board meeting:** If investors want observer seat (lead investor)

---

## SCALING PLAN

### Current (Pre-Seed)
- **Team:** 2 people (G + Joselo)
- **Agents:** 18 (automated)
- **Capacity:** 100 stocks/day

### Post-Seed ($500k raised)
- **Team:** 6 people (+ AI lead, engineer, analyst, marketing)
- **Agents:** 18 (improved quality)
- **Capacity:** 100 stocks/day, higher accuracy

### Year 1 ($10M AUM)
- **Team:** 8 people (+ 2 analysts, compliance officer)
- **Agents:** 21 (add 3 sector-specific agents)
- **Capacity:** 200 stocks/day

### Year 2 ($50M AUM)
- **Team:** 12 people (+ traders, operations, legal)
- **Agents:** 25+ (international, sectors, crypto)
- **Capacity:** 500+ stocks/day

---

## KEY PRINCIPLES

1. **Agents do the heavy lifting** (scan 100+ stocks daily)
2. **Humans do validation** (quality check, fundamentals)
3. **Joselo enforces risk** (stops, sizing, discipline)
4. **G makes final calls** (execution, strategy)
5. **Full transparency** (everything public on GitHub)

---

**This SOP is a living document. Update as we learn, scale, and improve.**

**Owner:** Joselo 🐓  
**Last Updated:** February 11, 2026  
**Next Review:** March 1, 2026
