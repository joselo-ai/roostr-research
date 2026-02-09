# ROOSTR EDGE HEALTH DASHBOARD SPECIFICATION

## Purpose
Real-time monitoring of edge performance, decay detection, and portfolio risk management.

## Dashboard Sections

---

## 1. PORTFOLIO OVERVIEW (Top of Dashboard)

### Current State
```
Portfolio Value: $XX,XXX
All-Time High: $XX,XXX (Date)
Current Drawdown: -X.X% from ATH
Daily P&L: $XXX (+X.X%)
Weekly P&L: $XXX (+X.X%)
Monthly P&L: $XXX (+X.X%)
```

### Performance Metrics (30-Day Rolling)
```
Total Return: +XX.X%
Sharpe Ratio: X.XX
Win Rate: XX%
Avg R-Multiple: X.XR
Max Drawdown: -XX.X%
```

### Risk Status
```
Portfolio Heat: XX% (sum of all open position risks)
Daily Loss Used: X.X% / 4.0% (circuit breaker at 4%)
Margin Used: XX% (if using leverage)
```

**Alert Colors:**
- 🟢 Green: All systems normal
- 🟡 Yellow: Approaching limits (3% daily loss, 15% drawdown)
- 🟠 Orange: Risk elevated (>3.5% daily loss, 20% drawdown)
- 🔴 Red: STOP TRADING (4% daily loss, 25% drawdown)

---

## 2. EDGE PERFORMANCE MATRIX

| Edge | Allocation | 30d Return | Sharpe | Win Rate | Avg R | Drawdown | Status | Target | Variance |
|------|-----------|------------|--------|----------|-------|----------|--------|--------|----------|
| **Social Arb** | 30% | +12.5% | 2.1 | 62% | 2.2R | -8% | 🟢 | 35-60% | Within |
| **Technical** | 25% | +8.2% | 1.7 | 48% | 2.8R | -12% | 🟡 | 40-80% | Below |
| **Crypto Fund** | 30% | +24.1% | 1.5 | 33% | 8.5R | -15% | 🟢 | 80-300% | Within |
| **Multi-Val** | 15% | N/A | +0.5 | +17% | N/A | N/A | 🟢 | Filter | Active |
| **PORTFOLIO** | 100% | +14.8% | 1.9 | 54% | 3.1R | -10% | 🟢 | 65-110% | Strong |

**Status Key:**
- 🟢 Healthy: All metrics within target ranges
- 🟡 Watch: 1-2 metrics below target
- 🟠 Concern: 2-3 metrics below target OR drawdown >15%
- 🔴 Critical: 3+ metrics failed OR drawdown >20% → SUSPEND EDGE

**Alerts:**
- ⚠️ Technical edge win rate at lower bound (48% vs 45% minimum)
- ✅ Crypto edge performing within expected variance
- ✅ Multi-source validation adding +17% win rate (target: +15%)

---

## 3. EDGE DECAY DETECTION (90-Day Trend)

### Social Arbitrage
```
Sharpe Trend: 2.3 → 2.2 → 2.1 (↓ slight decline, within noise)
Win Rate Trend: 65% → 60% → 62% (stable)
Signal Lag: 6 days → 7 days → 8 days (⚠️ increasing, monitor)

Decay Score: 15/100 (0-30 = healthy, 30-60 = watch, 60+ = critical)
Status: 🟢 HEALTHY
Next Review: 2026-03-01
```

### Technical Discipline
```
Sharpe Trend: 2.0 → 1.8 → 1.7 (↓ declining, investigate)
Win Rate Trend: 52% → 50% → 48% (↓ at lower bound)
R-Multiple Trend: 2.5R → 2.7R → 2.8R (↑ good, compensating)

Decay Score: 42/100 (⚠️ elevated, review next 10 trades)
Status: 🟡 WATCH
Action: Review recent losing trades for pattern changes
```

### Crypto Fundamentals
```
Sharpe Trend: 1.4 → 1.6 → 1.5 (stable)
Win Rate Trend: 30% → 40% → 33% (high variance, expected)
R-Multiple Trend: 10R → 7R → 8.5R (↓ within range)

Decay Score: 8/100 (low, edge healthy)
Status: 🟢 HEALTHY
Note: Win rate <40% is expected (venture-style bets)
```

---

## 4. OPEN POSITIONS (Real-Time)

| ID | Edge | Asset | Entry | Current | P&L | R | Days | Risk $ | Target | Action |
|----|------|-------|-------|---------|-----|---|------|--------|--------|--------|
| 001 | Social | LULU | $320 | $345 | +7.8% | +1.5R | 12 | $200 | $352 (2R) | 🟢 Hold |
| 002 | Technical | EUR/USD | 1.0850 | 1.0920 | +5.2% | +2.1R | 2 | $150 | 1.0950 | 🟡 Near TP |
| 003 | Crypto | XYZ | $2.50 | $1.85 | -26% | -0.5R | 45 | $300 | $6.25 (5R) | 🟠 Drawdown |

**Summary:**
- Open Positions: 3
- Total Capital at Risk: $650 (6.5% of portfolio)
- Unrealized P&L: -$135 (-1.35%)
- Positions at/near stop: 1 (XYZ, approaching -0.5R)

**Alerts:**
- 🟠 XYZ position down -26%, monitor thesis integrity
- 🟡 EUR/USD near take-profit, consider scaling out 50%

---

## 5. TRADE HISTORY (Last 10 Trades)

| Date | Edge | Asset | Result | P&L | R | Hold | Win? |
|------|------|-------|--------|-----|---|------|------|
| 02/04 | Technical | GBP/USD | Closed | +$320 | +2.8R | 1d | ✅ |
| 02/03 | Social | TSLA | Closed | -$180 | -1.0R | 8d | ❌ |
| 02/01 | Crypto | ABC | Closed | +$1,240 | +12.4R | 42d | ✅ |
| 01/28 | Social | AAPL | Closed | +$410 | +2.1R | 14d | ✅ |
| 01/25 | Technical | USD/JPY | Closed | -$150 | -1.0R | 2d | ❌ |
| 01/22 | Crypto | DEF | Closed | -$250 | -0.5R | 18d | ❌ |
| 01/20 | Social | NKE | Closed | +$520 | +2.6R | 21d | ✅ |
| 01/18 | Technical | EUR/USD | Closed | +$280 | +1.9R | 1d | ✅ |
| 01/15 | Social | DIS | Closed | -$200 | -1.0R | 12d | ❌ |
| 01/12 | Crypto | GHI | Closed | +$3,100 | +15.5R | 90d | ✅ |

**Last 10 Trades:**
- Win Rate: 60% (6/10)
- Avg Win: +$1,228 (+5.9R)
- Avg Loss: -$195 (-0.9R)
- Net P&L: +$4,890

---

## 6. RISK LIMITS & CIRCUIT BREAKERS

### Current Status
```
✅ Daily Loss: 1.2% / 4.0% (safe)
✅ Portfolio Drawdown: -10% / -25% (safe)
✅ Portfolio Heat: 6.5% / 15% (safe)
✅ Max Position Size: 4.8% / 5.0% (safe)
✅ Edge Allocation: All within targets
```

### Triggered Alerts (None)
```
No circuit breakers triggered. All systems green.
```

### Historical Breaches (Last 90 Days)
```
- 2026-01-15: Daily loss limit hit (-4.2%) → Trading paused for 24h
- 2026-01-08: Social Arb drawdown -13% → Position sizing reduced by 50%
```

---

## 7. MULTI-SOURCE VALIDATION SCOREBOARD

### Active Signals (Monitoring)

| Asset | Google Trends | Dexscreener | Community | Score | Confidence | Action |
|-------|--------------|-------------|-----------|-------|------------|--------|
| LULU | +180% ✅ | N/A | High ✅ | 2/3 | 🟢 High | Entered |
| COIN | +60% 🟡 | Increasing ✅ | Medium 🟡 | 2/3 | 🟡 Med | Watchlist |
| XYZ (crypto) | +200% ✅ | +150% liq ✅ | High ✅ | 3/3 | 🟢 Very High | Entered |
| RIVN | -20% ❌ | N/A | Low ❌ | 0/3 | 🔴 Low | Rejected |

**Filter Performance:**
- Trades with 2-3 signals: 68% win rate
- Trades with 0-1 signals: 42% win rate
- Filter value add: +26% win rate improvement ✅

---

## 8. WEEKLY REVIEW CHECKLIST

### Completed This Week:
- [x] Review all closed trades (10 trades reviewed)
- [x] Update edge performance metrics
- [x] Check for edge decay signals
- [x] Rebalance portfolio allocations (no changes needed)
- [x] Review open positions (3 positions reviewed)
- [ ] Read financial news / market regime check
- [ ] Update MEMORY.md with key learnings

### Action Items for Next Week:
1. Monitor Technical edge (win rate at lower bound)
2. Review XYZ crypto position (down -26%)
3. Research 2 new Social Arb opportunities
4. Paper trade new Crypto thesis (ABC protocol)

---

## 9. MONTHLY DEEP DIVE (Auto-Generate Report)

**Report Date:** 2026-02-01 (Monthly)

### Portfolio Summary
```
Starting Balance: $10,000
Ending Balance: $11,485
Monthly Return: +14.85%
Monthly Sharpe: 2.1
Max Drawdown: -12%
Win Rate: 58%
Total Trades: 28
```

### Edge Breakdown
```
Social Arbitrage: +8.2% (9 trades, 67% win rate)
Technical Discipline: +4.1% (12 trades, 50% win rate)
Crypto Fundamentals: +2.5% (7 trades, 29% win rate, but 3x 10R+ winners)
```

### Top 5 Trades (Best R-Multiples)
1. ABC (Crypto): +15.5R, $3,100
2. GHI (Crypto): +12.4R, $1,240
3. DEF (Social): +5.2R, $1,040
4. LULU (Social): +3.8R, $760
5. EUR/USD (Technical): +2.9R, $435

### Worst 3 Trades (Biggest Losses)
1. JKL (Crypto): -1.0R, -$300 (thesis invalidated, team left)
2. TSLA (Social): -1.0R, -$200 (signal was false positive)
3. MNO (Social): -1.0R, -$180 (stopped out, correct decision)

### Key Learnings
1. Multi-source validation improved win rate by +19% this month ✅
2. Technical edge underperforming (50% vs 55% target) - need to review patterns
3. Crypto edge volatility high but R-multiples compensate (+12R avg on winners)
4. No discipline breaches (all stop losses honored) ✅

### Recommendations for Next Month
1. Reduce Technical allocation from 25% → 20% (underperforming)
2. Increase Crypto allocation from 30% → 35% (outperforming + low correlation)
3. Add 2 new social signal sources (TikTok, Instagram) to combat decay
4. Paper trade "DeFi 2.0" crypto thesis before going live

---

## 10. DATA SOURCES & AUTOMATION

### Data Collection (Automated)
- **Trade Logs:** Manual entry via Google Sheets / Notion (daily)
- **Portfolio Value:** Pulled from broker API (real-time)
- **Edge Metrics:** Calculated from trade logs (Python script, daily)
- **Google Trends:** API pull (weekly)
- **Dexscreener:** API pull (daily for active positions)
- **Community Sentiment:** Manual check (daily for open positions)

### Automation Wishlist (Phase 2)
- Auto-populate trade journal from broker API
- Real-time edge decay scoring
- Telegram/Discord alerts for circuit breakers
- Auto-generate monthly reports (PDF)

### Tools
- **Phase 1:** Google Sheets + manual entry
- **Phase 2:** Python + Pandas + Google Sheets API
- **Phase 3:** Grafana + InfluxDB (institutional-grade)

---

## DASHBOARD REFRESH FREQUENCY

| Section | Refresh Rate | Manual/Auto |
|---------|--------------|-------------|
| Portfolio Overview | Real-time (if API) or Daily | Auto |
| Edge Performance | Daily (after market close) | Auto |
| Edge Decay | Weekly (Sunday night) | Auto |
| Open Positions | Real-time or Intraday | Auto |
| Trade History | After each trade closed | Manual |
| Risk Limits | Real-time or Hourly | Auto |
| Multi-Source Signals | Daily (morning) | Semi-auto |
| Weekly Review | Weekly (Sunday) | Manual |
| Monthly Deep Dive | Monthly (1st of month) | Auto-generate |

---

## IMPLEMENTATION PRIORITY

**Week 1 (MVP):**
1. Google Sheets with manual entry
2. Portfolio Overview + Edge Performance sections
3. Position sizing calculator integration

**Week 2-4:**
4. Python scripts for automated metric calculation
5. Edge decay scoring algorithm
6. Multi-source validation tracker

**Month 2+:**
7. API integrations (broker, Google Trends, Dexscreener)
8. Telegram alerts for circuit breakers
9. Monthly auto-reports

---

**END OF DASHBOARD SPEC**

*"What gets measured, gets managed. What gets managed, gets optimized."*
