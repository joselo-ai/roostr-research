# roostr Capital Dashboard - Complete Specification

**Version:** 1.0 (From Scratch)  
**Date:** Feb 17, 2026  
**Status:** SPEC ONLY - No code written yet

---

## Vision Statement

**Simple:** 18 AI agents scan stocks daily → debate → generate conviction scores → deploy trades ≥7/10 → show everything publicly.

**Goal:** ONE dashboard that shows the entire operation with full transparency. No mess, no confusion, auto-updating.

---

## Data Structure

### **Single Source of Truth:**

**File:** `trading/agent-decisions/YYYY-MM-DD.json`

**Format:**
```json
{
  "date": "2026-02-17",
  "scan_time": "09:00 EST",
  "stocks_scanned": 100,
  "signals": [
    {
      "ticker": "ACGL",
      "price": 117.43,
      "conviction": 8.5,
      "status": "APPROVED",
      "votes": {
        "BUY": 14,
        "HOLD": 3,
        "SELL": 1
      },
      "agent_deliberation": [
        {
          "agent": "Warren Buffett",
          "vote": "BUY",
          "score": 9,
          "reasoning": "Wonderful company at fair price. P/E 12 vs sector 18."
        },
        {
          "agent": "Charlie Munger",
          "vote": "BUY",
          "score": 9,
          "reasoning": "Quality business with pricing power."
        }
        // ... all 18 agents
      ],
      "deployment": {
        "deployed": true,
        "size": 15000,
        "entry": 117.43,
        "stop_loss": 108.03
      }
    }
    // ... top 5 signals
  ]
}
```

**Current Portfolio:** `trading/signals-database.csv` (already exists)

---

## Daily Workflow

### **Morning (9:00 AM EST):**
1. Agent scanner runs (`trading/agents/daily_scan.py`)
2. Scans 100+ stocks (S&P 500 + trending social)
3. All 18 agents vote on each stock
4. Top 5 opportunities identified
5. Saves to `agent-decisions/YYYY-MM-DD.json`

### **Midday (1:00 PM EST):**
1. Risk check (`apps/risk_monitor.py`)
2. Joselo reviews top 5
3. Validates conviction ≥7/10
4. Sets stop-loss levels
5. Marks APPROVED or REJECTED in JSON

### **Afternoon (3:00 PM EST):**
1. G executes approved trades
2. Updates `signals-database.csv` with new positions
3. Dashboard auto-refreshes

### **End of Day (4:00 PM EST):**
1. Publish updates to GitHub
2. Tweet summary
3. Dashboard shows final state

---

## Dashboard Structure

### **ONE Dashboard URL:**
- Public: `https://joselo-ai.github.io/roostr-research/`
- Purpose: Marketing + Operations (fully transparent)

### **Sections (in order):**

#### **1. Hero**
```
🐓 roostr Capital
"We hunt information asymmetries before Wall Street wakes up"

[🟢 LIVE] 18 AI Agents Operational
Last Scan: Today 9:00 AM EST (100+ stocks analyzed)
Next Scan: Tomorrow 9:00 AM EST
```

#### **2. Today's Operation Timeline**
```
9:00 AM - Agent Scanner     [✓ COMPLETE] or [⏳ PENDING]
1:00 PM - Risk Check        [✓ COMPLETE] or [⏳ PENDING]
3:00 PM - Execution         [✓ COMPLETE] or [⏳ PENDING]
4:00 PM - Publish           [✓ COMPLETE] or [⏳ PENDING]
```

#### **3. Top 5 Opportunities (Today's Scan)**
```
For each signal:
- Ticker + Price
- Conviction score (X/10)
- Agent votes (X BUY / X HOLD / X SELL)
- Status (APPROVED / REJECTED / PENDING)
- Lead agents + brief reasoning
- If APPROVED: Position size, stop-loss
```

#### **4. Agent Deliberation (Expandable)**
```
Click any signal → See full 18-agent debate
Terminal-style transcript:
  Warren Buffett: BUY 9/10 - "reasoning..."
  Charlie Munger: BUY 9/10 - "reasoning..."
  ... all 18 agents
  
ENSEMBLE RESULT: 8.5/10 → STRONG BUY
```

#### **5. Current Portfolio**
```
Active positions from signals-database.csv:
- Ticker
- Entry / Current price
- P&L ($ and %)
- Stop-loss
- Status (color-coded: green profit, red loss, yellow neutral)

Portfolio Summary:
Total Capital | Deployed | P&L | Win Rate
```

#### **6. 18-Agent System Grid**
```
Grid of all 18 agents:
- Name
- Specialty
- Status (✓ OPERATIONAL)
```

#### **7. Footer**
```
Links: GitHub | Twitter | Contact
"18 agents. 100 stocks scanned daily. Full transparency."
```

---

## Automation

### **What Runs When:**

**Hourly (0 * * * *):**
- `apps/price_updater.py` → Updates current prices in CSV
- `apps/dashboard_generator.py` → Regenerates dashboard HTML from data
- Git commit + push

**Daily (9:00 AM EST):**
- `agents/daily_scan.py` → 18-agent scan, saves JSON
- Dashboard auto-updates

**Every 5 minutes:**
- `apps/risk_monitor.py` → Check stop-losses
- Alert if violated

**Manual (as needed):**
- G approves/rejects signals (updates JSON)
- G executes trades (updates CSV)

---

## File Organization

```
roostr-research/
├── index.html                          ← ONE dashboard (auto-generated)
├── trading/
│   ├── signals-database.csv            ← Current portfolio (source of truth)
│   ├── agent-decisions/                ← Daily scan results
│   │   ├── 2026-02-17.json
│   │   ├── 2026-02-18.json
│   │   └── ...
│   ├── agents/
│   │   ├── daily_scan.py               ← 18-agent scanner
│   │   ├── legendary_investors_v2.py   ← Agent logic
│   │   └── deliberate.py               ← Ensemble voting
│   └── apps/
│       ├── price_updater.py            ← Hourly price updates
│       ├── risk_monitor.py             ← Stop-loss checks
│       └── dashboard_generator.py      ← HTML generator from JSON+CSV
└── command-center/                     ← DELETE (merged into main dashboard)
```

**Deletions:**
- `/trading/index.html` (old)
- `/trading/dashboard.html` (old)
- `/command-center/dashboard.html` (old)
- All old updater scripts

---

## Dashboard Generator Logic

**Script:** `apps/dashboard_generator.py`

**Input:**
1. Today's agent decisions: `agent-decisions/YYYY-MM-DD.json`
2. Current portfolio: `signals-database.csv`

**Output:**
1. `/index.html` (fully rendered dashboard)

**Process:**
1. Load JSON (today's scan + deliberation)
2. Load CSV (current positions + P&L)
3. Render HTML template with:
   - Operation timeline (✓ or ⏳ based on timestamps)
   - Top 5 signals (from JSON)
   - Agent deliberation (from JSON)
   - Current portfolio (from CSV)
   - Agent system status (hardcoded, all ✓ OPERATIONAL)
4. Write to `/index.html`
5. Git commit + push

**When it runs:**
- After daily scan (9 AM)
- After price update (hourly)
- After trade execution (manual trigger)

---

## Design Style

**Theme:** Terminal aesthetic (pitch deck style)

**Colors:**
- Background: `#0a0a0a` (dark)
- Accent: `#00ff00` (bright green)
- Text: `#ffffff` (white)
- Secondary: `#808080` (gray)
- Red: `#f87171` (loss)
- Yellow: `#fbbf24` (neutral)

**Typography:**
- Headings: `Inter Bold`
- Body: `Inter Regular`
- Code/Data: `JetBrains Mono`

**Mobile:** Fully responsive

---

## Phase 1: Build Plan (After Approval)

### **Step 1: Clean Slate**
1. Delete old dashboards
2. Create fresh file structure
3. Set up `agent-decisions/` folder

### **Step 2: Data Layer**
1. Create sample `2026-02-17.json` (demo data)
2. Validate CSV structure
3. Test data loading

### **Step 3: Dashboard Generator**
1. Write `dashboard_generator.py`
2. HTML template with all sections
3. Test with demo data

### **Step 4: Automation**
1. Connect to price updater (hourly)
2. Set up daily scan trigger (9 AM cron)
3. Git auto-commit

### **Step 5: Polish**
1. Mobile testing
2. Performance check
3. Documentation

---

## Questions Before Building

1. **Daily scan:** Do we run actual 18-agent scans now, or use demo data until ready?
2. **Agent decisions JSON:** Should I create sample files for last 7 days, or just today?
3. **Command center:** Delete completely, or keep locally (not on GitHub Pages)?
4. **Cron jobs:** Should I set up automated daily scans (9 AM), or manual trigger for now?
5. **Old data:** Keep `signals-database.csv` as-is, or clean/restructure?

---

## Success Criteria

✅ ONE dashboard URL that shows everything  
✅ Auto-updates hourly (prices) and daily (scans)  
✅ Full transparency (agent deliberation visible)  
✅ No confusion (clear data flow)  
✅ Mobile-friendly  
✅ Fast (<2 sec load time)  
✅ Zero maintenance (fully automated)  

---

**Status:** SPEC COMPLETE - Awaiting approval to build

**Next Step:** Review this spec → Answer 5 questions → Get "build" approval → Execute

**Timeline (once approved):** 2-3 hours to build, test, deploy
