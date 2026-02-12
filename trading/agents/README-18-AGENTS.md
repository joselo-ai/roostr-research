# roostr 18-Agent Trading System
**Version:** 1.0.0  
**Date:** Feb 12, 2026  
**Status:** ✅ OPERATIONAL

---

## 🎯 Overview

The roostr 18-Agent System is a multi-agent AI architecture that evaluates every trade through 18 different perspectives before making deployment decisions.

### Agent Composition

**12 Legendary Investors:**
1. Warren Buffett (value, moat, quality)
2. Charlie Munger (multidisciplinary thinking, avoid stupidity)
3. Michael Burry (contrarian, deep value)
4. Ben Graham (margin of safety, quantitative value)
5. Mohnish Pabrai (asymmetric risk/reward)
6. Cathie Wood (innovation, disruption)
7. Phil Fisher (scuttlebutt research)
8. Peter Lynch (ten-baggers, consumer businesses)
9. Bill Ackman (concentrated bets, activist catalyst)
10. Stanley Druckenmiller (macro trends, asymmetry)
11. Aswath Damodaran (valuation, story to numbers)
12. Rakesh Jhunjhunwala (emerging markets, long-term growth)

**4 Quantitative Agents:**
1. Valuation Agent (price vs intrinsic value)
2. Sentiment Agent (social signals, engagement)
3. Fundamentals Agent (business quality, catalyst)
4. Technicals Agent (chart patterns, momentum)

**Risk Manager:** Joselo 🐓  
**Portfolio Manager:** Synthesizes all opinions → final decision

---

## 🚀 Quick Start

### Run on Existing Signal

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading

# Test with TAO
python3 agents/test_18_agents.py

# Evaluate any ticker from database
python3 agents/run_18_agents.py --from-database --ticker TAO

# Evaluate all signals
python3 agents/run_18_agents.py --scan-all
```

### Manual Signal Input

```bash
python3 agents/run_18_agents.py \
  --ticker AAPL \
  --price 175.50 \
  --catalyst "Strong earnings, iPhone sales growth, services expanding" \
  --source "Manual" \
  --asset-class stock
```

---

## 📊 How It Works

### Pipeline

```
Signal Input
   ↓
12 Legendary Investors (parallel evaluation)
   → Each scores 0-10 + BUY/SELL/HOLD + reasoning
   → Aggregate: consensus + avg conviction
   ↓
4 Quant Agents (parallel evaluation)
   → Each scores 0-10 + BUY/SELL/HOLD + metrics
   → Aggregate: consensus + avg score
   ↓
Combine (60% legendary + 40% quant)
   → Weighted conviction score
   ↓
Risk Manager (Joselo 🐓)
   → Validates stops, position sizing, portfolio risk
   → Adjusts conviction if concerns exist
   ↓
Portfolio Manager
   → Synthesizes all opinions
   → Generates conviction document
   → Final decision: BUY/SELL/HOLD
   ↓
Conviction Document (JSON)
   → Saved to conviction-docs/
   → Published to GitHub + Twitter
```

---

## 📈 Decision Logic

### Conviction Scale

- **9.5-10.0:** VERY HIGH → 20% allocation
- **9.0-9.5:** HIGH → 15% allocation
- **7.5-9.0:** HIGH → 10% allocation
- **7.0-7.5:** MEDIUM → 5% allocation
- **<7.0:** TOO LOW → HOLD (no deployment)

### Final Decision

- **BUY:** Conviction ≥7.5 + both consensus BUY, OR conviction ≥7.0 + majority BUY
- **SELL:** Conviction ≤3.5 + both consensus SELL, OR conviction ≤4.0 + majority SELL
- **HOLD:** Everything else

### Risk Manager Adjustments

- Conviction <7.0 → Cap at 5.0
- Crypto with conviction <8.0 → -1.0 adjustment
- Weak catalyst (<30 chars) → -0.5 adjustment
- No stop loss mentioned → Flag concern

---

## 📄 Output Format

### Conviction Document (JSON)

```json
{
  "ticker": "TAO",
  "timestamp": "2026-02-12T09:45:00",
  "signal_source": "Yieldschool",
  "catalyst": "AI + blockchain...",
  "entry_price": 176.05,
  
  "legendary_investors": {
    "consensus": "HOLD",
    "avg_conviction": 5.17,
    "votes": {"BUY": 0, "SELL": 0, "HOLD": 12},
    "individual_opinions": [...]
  },
  
  "quant_agents": {
    "consensus": "HOLD",
    "avg_score": 6.0,
    "votes": {"BUY": 2, "SELL": 0, "HOLD": 2},
    "individual_opinions": [...]
  },
  
  "combined_conviction": 5.5,
  "risk_validated_conviction": 4.0,
  "risk_concerns": [
    "Conviction <7.0, too low to deploy capital",
    "Crypto requires higher conviction (>=8.0)"
  ],
  
  "final_decision": "HOLD",
  "conviction_rating": "🟠 LOW",
  
  "reasoning": "Multi-agent consensus...",
  
  "position_sizing": null
}
```

---

## 🔧 Configuration

### Weights (in portfolio_manager.py)

```python
self.legendary_weight = 0.6  # 60% weight to legendary investors
self.quant_weight = 0.4      # 40% weight to quant agents
```

### Risk Limits (in portfolio_manager.py)

```python
self.max_position_pct = 0.20      # 20% max per position
self.max_portfolio_risk = 0.038   # 3.8% max portfolio loss
```

---

## 📚 Example: TAO Evaluation

**Input:**
- Ticker: TAO
- Price: $176.05
- Catalyst: "AI + blockchain, Yieldschool 8.5/10, strong fundamentals"
- Asset Class: Crypto

**Results:**
- Legendary Consensus: HOLD (5.17/10)
- Quant Consensus: HOLD (6.0/10)
- Combined: 5.5/10
- Risk Adjusted: 4.0/10
- **Final Decision: HOLD**

**Reasoning:**
- Crypto requires ≥8.0 conviction
- No stop loss mentioned in catalyst
- Need stronger conviction to deploy capital

---

## 🔄 Integration with Trading Infrastructure

### Daily Signal Evaluation

```bash
# In daily workflow (cron or manual)
cd /Users/agentjoselo/.openclaw/workspace/trading

# Evaluate all new signals
python3 agents/run_18_agents.py --scan-all

# Output: conviction-docs/*.json
# Then: Update signals-database.csv with agent decisions
```

### Auto-deployment

```python
# In deployment script
conviction_doc = run_18_agents(signal)

if conviction_doc['final_decision'] == 'BUY':
    position_size = conviction_doc['position_sizing']['position_size']
    stop_price = conviction_doc['position_sizing']['stop_price']
    
    # Execute trade
    deploy_capital(
        ticker=conviction_doc['ticker'],
        size=position_size,
        stop=stop_price
    )
```

---

## 📊 Performance Tracking

All conviction documents are saved with timestamps. Track:

- **Agent Accuracy:** How often do legendary investors vote correctly?
- **Conviction Calibration:** Do 9/10 signals perform better than 7/10?
- **Risk Manager Adjustments:** How often does risk manager override?

**Analysis Script (TODO):**
```bash
python3 agents/analyze_agent_performance.py --lookback 90days
```

---

## 🐛 Troubleshooting

### "No signals found for ticker"

Check signals-database.csv has entry for that ticker.

### "Conviction always HOLD"

Catalyst text may be too weak. Agents look for specific keywords:
- Valuation: "undervalued", "cheap", "bargain"
- Growth: "innovation", "disruption", "scaling"
- Value: "moat", "competitive advantage", "quality"
- Catalyst: "approval", "product launch", "partnership"

Improve catalyst text to get stronger agent opinions.

### Adjusting Agent Weights

Edit `portfolio_manager.py`:
```python
self.legendary_weight = 0.7  # Increase legendary influence
self.quant_weight = 0.3      # Decrease quant influence
```

---

## 🔮 Future Enhancements

- [ ] Connect to real LLMs (GPT-4, Claude) for deeper agent reasoning
- [ ] Add 6 more specialized agents (momentum, dividend, sector rotation)
- [ ] Agent learning (track accuracy, adjust weights dynamically)
- [ ] Interactive debate mode (agents argue with each other)
- [ ] Real-time signal ingestion (scrape → agents → deploy in one flow)

---

## 📞 Support

**Issues:** Report in trading/agents/ folder  
**Docs:** This file + individual agent .py files

---

**Built by:** Joselo 🐓  
**For:** roostr Capital  
**Inspired by:** virattt/ai-hedge-fund architecture

*"18 agents > 1 brain. Always."* 🐓
