# 🐓 roostr Capital - Mission Control

**Built:** February 20, 2026  
**Framework:** Next.js 15 + TypeScript + Tailwind CSS

---

## Mission Statement

**"Autonomous AI hedge fund that compounds capital 24/7 through systematic, disciplined, transparent execution."**

_Every tool, every decision, every line of code serves this mission._

---

## Mission Control Purpose

**Central hub for:**
1. Real-time portfolio monitoring
2. 18-agent system oversight
3. Custom tool deployment
4. Performance analytics
5. Risk management dashboard
6. Research pipeline visualization

**Philosophy:** When Joselo needs a tool that doesn't exist → build it in Mission Control

---

## Pages/Modules

### 1. Home Dashboard (`/`)
- Mission statement (prominent)
- Current portfolio status
- Today's P&L
- Active positions (live prices)
- 18-agent system status
- Recent signals/deployments

### 2. Agent Deliberations (`/agents`)
- Live 18-agent debates
- Conviction score history
- Agent performance tracking
- Deliberation visualizations
- Search conviction docs

### 3. Research Pipeline (`/research`)
- Daily opportunity scanner output
- Enhanced scanner results
- Nightly research reports
- Signal sources (Reddit, Discord, news)
- Deployment plan preview

### 4. Portfolio Performance (`/portfolio`)
- Historical P&L chart
- Position breakdown
- Win rate analytics
- Conviction vs outcome analysis
- Risk metrics (drawdown, Sharpe, etc.)

### 5. Risk Monitor (`/risk`)
- Real-time stop-loss tracking
- Position sizing compliance
- Portfolio heat map
- Risk alerts/notifications
- Kill switch (emergency exit)

### 6. Tools Builder (`/tools`)
- Custom tool generator
- API integrations
- Data connectors
- Workflow automation
- When Joselo needs something → build it here

### 7. Social/Marketing (`/marketing`)
- roostr Twitter feed
- Content calendar
- Performance reports
- Follower analytics
- Transparency dashboard

---

## Tech Stack

- **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind CSS
- **Data:** Read from `trading/` folder (positions.csv, conviction-docs/, etc.)
- **Real-time:** Poll every 10-30 seconds for updates
- **Charts:** Recharts or Chart.js
- **Deployment:** Vercel (auto-deploy from GitHub)

---

## Data Sources

Mission Control reads from:
```
trading/
├── positions.csv                  # Active positions
├── dashboard.html                 # Current prices/P&L
├── conviction-docs/               # Agent deliberations
├── daily-opportunities.json       # Scanner output
├── enhanced-opportunities.json    # Enhanced scanner
├── next-day-deployment-plan.md    # Nightly research
└── logs/
    ├── execution.jsonl            # Trade log
    └── performance-journal.jsonl  # Daily summaries
```

---

## Development Plan

**Phase 1 (Today):**
1. ✅ Create Next.js app
2. ✅ Add mission statement to homepage
3. Build basic dashboard (portfolio status)
4. Deploy to Vercel

**Phase 2 (This Week):**
- Agent deliberations viewer
- Research pipeline dashboard
- Performance charts

**Phase 3 (Next Week):**
- Tools builder
- Risk monitor
- Social/marketing hub

---

## Custom Tool Philosophy

**When Joselo needs a tool:**
1. Identify gap (e.g., "I need to track insider buying")
2. Build module in Mission Control (`/tools/insider-tracker`)
3. Add to navigation
4. Iterate based on usage

**Examples:**
- Earnings calendar tracker
- Unusual options flow monitor
- Sentiment aggregator (Reddit + Twitter + Discord)
- Analyst rating tracker
- SEC filing alerts

Mission Control becomes Joselo's **living toolbox**.

---

## Transparency

Mission Control is **public** (via GitHub Pages or Vercel):
- Full portfolio visibility
- Agent deliberations open
- Performance history transparent
- Builds trust for roostr Capital brand

---

🐓 **Mission Control = roostr Capital's command center**
