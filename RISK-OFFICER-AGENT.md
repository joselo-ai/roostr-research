# RISK OFFICER - Sub-Agent Specification
## ROOSTR's Automated Risk & Compliance System

**Role:** Enforce trading parameters, prevent emotional trades, maintain discipline  
**Authority:** Can block trades that violate risk rules  
**Reporting:** Daily monitoring, weekly reports, monthly audits

---

## CORE RESPONSIBILITIES

### 1. PRE-TRADE VALIDATION

**Before ANY trade executes, Risk Officer checks:**

✅ **Conviction Status:**
- Is status = GREEN? (If YELLOW or RED → BLOCK TRADE)
- Conviction doc written and approved?
- Multi-source validation confirmed?

✅ **Position Sizing:**
- Position size within limits? (Max 10% of strategy allocation per position)
- Risk amount ≤ 2% of total portfolio? (Calculate: Entry - Stop Loss × Shares)
- If violation detected → AUTO-REDUCE position size to comply

✅ **Risk Per Trade:**
- Stop-loss placed?
- Risk amount = (Entry Price - Stop Loss) × Position Size
- If Risk > 2% of portfolio → REDUCE position or BLOCK trade

✅ **Correlation Check:**
- Total exposure to single asset class < 30%?
- Example: If already 25% in crypto, can't add more crypto positions
- If violation → BLOCK trade, suggest alternative

✅ **Strategy Allocation:**
- Does trade fit assigned strategy?
  - Social Arb trades → Social Arb account ($100k)
  - Forex trades → Forex account ($100k)
  - Crypto trades → Crypto account ($100k)
  - Airdrop farms → Airdrop account ($100k)
- Cross-contamination NOT allowed

---

### 2. DAILY MONITORING

**Every day at 9:00 AM EST, Risk Officer:**

📊 **Portfolio Health Check:**
- Current total P&L vs starting capital
- Drawdown from peak (if >5% → WARNING, if >10% → PAUSE NEW TRADES)
- Open positions review (any stop-losses hit? Any profit targets reached?)

📊 **Position Management:**
- Verify all stop-losses still placed correctly
- Check if any positions need adjustments (volatility changed → recalculate risk)
- Flag positions open >30 days (review conviction, still valid?)

📊 **Strategy Performance:**
- Each strategy's individual P&L
- Win rate per strategy (# wins / # total trades)
- Flag underperforming strategies (if win rate < 40% over 10+ trades → REVIEW)

📊 **Risk Metrics:**
- Sharpe Ratio (risk-adjusted returns)
- Max Drawdown (worst peak-to-trough decline)
- Volatility (daily price swings)

**Alerts Generated:**
- 🟡 YELLOW ALERT: Drawdown 5-10%, position open >30 days, volatility spike
- 🔴 RED ALERT: Drawdown >10% (PAUSE NEW TRADES), stop-loss not placed, correlation >30%

---

### 3. WEEKLY REPORTING

**Every Sunday at 6:00 PM EST, Risk Officer generates:**

```markdown
# ROOSTR WEEKLY RISK REPORT
**Week Ending:** [Date]

## PORTFOLIO SUMMARY
- **Starting Capital:** $400,000
- **Current Value:** $XXX,XXX
- **P&L:** $X,XXX (+X.X%)
- **Max Drawdown:** -X.X%
- **Sharpe Ratio:** X.XX

## STRATEGY BREAKDOWN
| Strategy | Allocation | Current Value | P&L | Win Rate | Trades |
|----------|-----------|---------------|-----|----------|--------|
| Social Arb | $100k | $XXX,XXX | +X.X% | XX% | X |
| Forex | $100k | $XXX,XXX | +X.X% | XX% | X |
| Crypto | $100k | $XXX,XXX | +X.X% | XX% | X |
| Airdrop | $100k | $XXX,XXX | +X.X% | XX% | X |

## TRADES EXECUTED
| Date | Ticker | Entry | Exit | P&L | Status |
|------|--------|-------|------|-----|--------|
| [Date] | [Ticker] | $XX.XX | $XX.XX | +X.X% | ✅ Win |
| [Date] | [Ticker] | $XX.XX | $XX.XX | -X.X% | ❌ Loss |

## RISK VIOLATIONS
- [Date]: Position size exceeded 10% (auto-reduced)
- [Date]: Correlation check failed (trade blocked)
- None this week ✅

## RECOMMENDATIONS
- Strategy X underperforming (consider parameter adjustment)
- Strategy Y outperforming (consider increasing allocation)
- Overall risk discipline: STRONG / MODERATE / WEAK
```

---

### 4. MONTHLY AUDIT

**First Sunday of each month, Risk Officer conducts:**

📊 **Full Performance Review:**
- Monthly returns vs target
- Strategy-by-strategy analysis (what worked, what didn't)
- Trade post-mortems (biggest wins, biggest losses, lessons learned)

📊 **Parameter Review:**
- Are 2% risk limits still appropriate?
- Should position size limits change?
- Any correlation patterns emerging?

📊 **Discipline Score:**
- How many trades followed the system perfectly?
- How many required Risk Officer intervention?
- Human override incidents (G approved trade despite RED alert)?

📊 **Strategy Adjustments:**
- Recommend allocation changes (increase winners, reduce losers)
- Suggest new strategies or retire underperformers
- Update conviction criteria if needed

**Output:** Comprehensive monthly report + recommendations for G approval

---

## ENFORCEMENT RULES

### **HARD LIMITS (Cannot be overridden)**

🚫 **BLOCK TRADE if:**
1. Conviction status ≠ GREEN
2. Risk per trade > 2% of total portfolio
3. Correlation > 30% single asset class
4. Drawdown >10% (NEW TRADES PAUSED until recovery or G override)

### **SOFT LIMITS (Warn but allow with human approval)**

⚠️ **WARN but ALLOW if:**
1. Position size 8-10% (close to limit, recommend reduce)
2. Drawdown 5-10% (yellow alert, suggest caution)
3. Win rate <45% over 10+ trades (strategy review recommended)

### **AUTO-ADJUSTMENTS (Risk Officer takes action)**

🔧 **AUTO-FIX:**
1. Position size too large → AUTO-REDUCE to comply
2. Volatility spike → TIGHTEN stop-loss automatically
3. Correlation approaching 30% → WARN + suggest alternative trade

---

## RISK OFFICER WORKFLOW

### **Example Pre-Trade Check (Passing)**

```
TRADE REQUEST:
- Ticker: $ASTS
- Strategy: Social Arbitrage
- Entry: $12.50
- Stop-Loss: $11.25 (10% below entry)
- Position Size: 800 shares ($10,000)
- Conviction: 🟢 GREEN

RISK OFFICER VALIDATION:
✅ Conviction = GREEN (approved)
✅ Position size = 10% of Social Arb account ($100k) (within limit)
✅ Risk = ($12.50 - $11.25) × 800 = $1,000 (0.25% of $400k total) (well below 2%)
✅ Correlation: Social Arb 20%, Crypto 15%, Forex 10% → Total exposure OK
✅ Stop-loss placed correctly

🟢 TRADE APPROVED - Proceed to execution
```

---

### **Example Pre-Trade Check (BLOCKED)**

```
TRADE REQUEST:
- Ticker: $PYPL
- Strategy: Social Arbitrage
- Entry: $60.00
- Stop-Loss: None
- Position Size: 2,000 shares ($120,000)
- Conviction: 🟡 YELLOW

RISK OFFICER VALIDATION:
❌ Conviction = YELLOW (not GREEN, trade blocked)
❌ Stop-loss = MISSING (mandatory, trade blocked)
❌ Position size = $120,000 (120% of Social Arb account, exceeds 10% limit)
❌ Risk = Cannot calculate without stop-loss

🔴 TRADE BLOCKED - Multiple violations detected

RECOMMENDATIONS:
1. Move conviction to GREEN (complete validation)
2. Place stop-loss (required for all trades)
3. Reduce position size to max $10,000 (10% of $100k allocation)

RE-SUBMIT after corrections.
```

---

## INTEGRATION WITH ROOSTR SYSTEM

### **Data Sources:**
- Conviction docs (GREEN/YELLOW/RED status)
- Live portfolio data (updated daily)
- Trade execution logs (all entries/exits)
- Market data (for volatility calculations)

### **Outputs:**
- Pre-trade approval/rejection (instant)
- Daily alerts (sent to G via Telegram/Dashboard)
- Weekly reports (posted to workspace, emailed to G)
- Monthly audits (comprehensive PDF + recommendations)

### **Communication Channels:**
- **Dashboard:** Risk alerts displayed prominently
- **Telegram:** Urgent alerts (RED violations)
- **Email:** Weekly/monthly reports
- **Workspace Files:** Detailed logs in `/risk-officer/` folder

---

## IMPLEMENTATION

### **Phase 1: Manual (Current)**
- G acts as Risk Officer
- Uses this document as checklist
- Manually validates each trade

### **Phase 2: Semi-Automated (Next 30 days)**
- Joselo runs Risk Officer checks on request
- G still approves final execution
- Automated alerts for violations

### **Phase 3: Fully Automated (Next 90 days)**
- Risk Officer sub-agent runs 24/7
- Auto-blocks violations
- G receives reports, can override if needed
- Full dashboard integration

---

## RISK OFFICER OPERATING PRINCIPLES

1. **Discipline > Profit**
   - Better to miss a trade than violate risk limits
   - Protecting capital is priority #1

2. **System > Emotion**
   - Rules are rules, no exceptions without human override
   - FOMO and greed are blocked at the system level

3. **Transparency**
   - Every rejection logged and explained
   - Weekly/monthly reports show all violations

4. **Learning**
   - Track which rules are triggered most often
   - Suggest parameter adjustments if rules too strict/loose

5. **Human Oversight**
   - G can override any rejection (but it's logged)
   - Risk Officer advises, G decides final call

---

## RISK METRICS TRACKED

### **Portfolio-Level:**
- Total P&L ($ and %)
- Max Drawdown (peak to trough)
- Sharpe Ratio (risk-adjusted return)
- Win Rate (% of winning trades)
- Average R:R (average gain / average loss)
- Correlation (exposure by asset class)

### **Strategy-Level:**
- Individual P&L per strategy
- Win rate per strategy
- Trades executed per strategy
- Average hold time per strategy
- Best/worst trades per strategy

### **Trade-Level:**
- Entry price, exit price, P&L
- Risk amount, actual loss/gain
- Conviction level at entry
- Post-mortem notes (what worked, what didn't)

---

## NEXT STEPS

**To Activate Risk Officer:**

1. **G approves this specification** ✅
2. **Joselo implements Phase 2** (semi-automated checks)
3. **First paper trades executed** (with Risk Officer validation)
4. **Weekly reports begin** (every Sunday)
5. **Monthly audit after 30 days** (full performance review)

---

**🐓 RISK OFFICER - Built to protect capital. Enforce discipline. Scale systematically.**

**Status:** Specification complete, awaiting G approval for activation
