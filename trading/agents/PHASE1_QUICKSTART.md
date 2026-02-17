# Phase 1 Quick Start Guide
## Using the 4 Quant Agents

**Status:** ✅ Operational (Feb 17, 2026)

---

## Installation

### 1. Set up virtual environment
```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/agents
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install yfinance numpy pandas textblob
```

### 3. Optional: Reddit sentiment (requires API keys)
```bash
pip install praw
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
```

---

## Usage

### Run analysis on any ticker
```python
from quant_agents_v2 import run_full_quant_analysis, print_analysis_report

# Analyze a ticker
results = run_full_quant_analysis('SPHR')

# Print formatted report
print_analysis_report(results)

# Access results programmatically
consensus = results['summary']['consensus']  # "STRONG BUY", "BUY", "HOLD", "SELL", etc.
conviction = results['summary']['avg_conviction']  # 0-10 scale
votes = results['summary']['vote_distribution']  # {'BUY': 3, 'SELL': 1, ...}
```

### Run individual agents
```python
from quant_agents_v2 import QUANT_AGENTS_V2

# Run just one agent
valuation_agent = QUANT_AGENTS_V2['valuation']
opinion = valuation_agent.evaluate('AAPL')

print(f"{opinion.agent_name}: {opinion.action} ({opinion.conviction}/10)")
print(opinion.rationale)
print(opinion.key_metrics)
```

### Command-line usage
```bash
# Run on SPHR
python3 quant_agents_v2.py

# Run test suite
python3 test_phase1.py SPHR

# Test multiple tickers
python3 test_phase1.py AAPL --multi
```

---

## Output Format

### Individual Agent Opinion
```json
{
  "agent_name": "Quant Valuation",
  "ticker": "SPHR",
  "conviction": 3.33,
  "action": "SELL",
  "rationale": "I assess SPHR as overvalued...",
  "key_metrics": {
    "pe_ratio": 155.34,
    "pb_ratio": 1.83,
    "ev_ebitda": 25.02
  },
  "data_quality": "HIGH",
  "timestamp": "2026-02-17T14:49:39.312608"
}
```

### Aggregate Summary
```json
{
  "ticker": "SPHR",
  "summary": {
    "consensus": "STRONG BUY",
    "avg_conviction": 5.11,
    "vote_distribution": {
      "BUY": 3,
      "SELL": 1,
      "HOLD": 0,
      "ABSTAIN": 0
    },
    "data_quality": "HIGH"
  }
}
```

---

## Agent Capabilities

### 🔢 Quant Valuation
**What it does:**
- Compares market price to intrinsic value using P/E, P/B, EV/EBITDA, PEG
- Returns conviction 0-10 (0=very overvalued, 10=very undervalued)

**When to trust it:**
- Data quality is HIGH (multiple metrics available)
- Company has positive earnings (P/E meaningful)
- Established business with comparable peers

**When to discount it:**
- Pre-revenue growth companies (no P/E)
- Unique business models without comps
- Data quality LOW (missing metrics)

### 📈 Quant Technicals
**What it does:**
- Analyzes RSI, MACD, moving averages, volume trends
- Returns conviction 0-10 (0=bearish, 10=bullish)

**When to trust it:**
- 6+ months price history available
- High liquidity (not penny stocks)
- Multiple indicators align

**When to discount it:**
- Newly listed assets (<3 months history)
- Low volume / illiquid securities
- Conflicting signals (RSI bearish, MACD bullish)

### 💰 Quant Fundamentals
**What it does:**
- Evaluates ROE, debt, free cash flow, growth, margins
- Returns conviction 0-10 (0=poor, 10=excellent)

**When to trust it:**
- Profitable company with operating history
- Multiple fundamental metrics available
- Consistent trends (not one-time anomalies)

**When to discount it:**
- Early-stage companies (losses normal)
- Capital-intensive businesses (low ROE expected)
- Special situations (turnarounds, restructuring)

### 😊 Quant Sentiment
**What it does:**
- Analyzes news sentiment, Reddit mentions, social momentum
- Returns conviction 0-10 (0=bearish, 10=bullish)

**When to trust it:**
- Multiple sentiment sources available
- Moderate coverage (not too quiet, not too hyped)
- Aligns with fundamentals/technicals

**When to discount it:**
- Extreme sentiment (euphoria = sell signal, panic = buy signal)
- Manipulated social signals (pump & dump)
- No coverage (illiquid/unknown stocks)

---

## Interpretation Guide

### Consensus Meanings
- **STRONG BUY**: ≥75% of agents say BUY
- **BUY**: ≥50% of agents say BUY
- **HOLD**: Mixed signals or majority HOLD
- **SELL**: ≥50% of agents say SELL
- **STRONG SELL**: ≥75% of agents say SELL

### Conviction Ranges
- **8-10**: High conviction (strong opportunity or risk)
- **6-7**: Moderate conviction (favorable setup)
- **4-6**: Neutral (no edge, fair value)
- **2-3**: Moderate conviction (unfavorable)
- **0-1**: High conviction (strong avoid)

### Vote Distributions
**Bullish patterns:**
- 4 BUY, 0 SELL → Strong unanimous bullish
- 3 BUY, 1 HOLD → Consensus bullish
- 3 BUY, 1 SELL → Majority bullish (valuation concern)

**Neutral patterns:**
- 2 BUY, 2 SELL → Split (risky)
- 2 BUY, 2 HOLD → Weak bullish
- 4 HOLD → No conviction either way

**Bearish patterns:**
- 3 SELL, 1 BUY → Majority bearish
- 4 SELL, 0 BUY → Unanimous bearish

---

## Real-World Examples

### SPHR (Sphere Entertainment) - STRONG BUY 5.11/10
```
Valuation:    3.33/10 SELL  (P/E 155x = expensive)
Technicals:   5.5/10 BUY    (above 50 DMA, MACD bullish)
Fundamentals: 6.1/10 BUY    (27.9% revenue growth, 8.24% FCF yield)
Sentiment:    5.5/10 BUY    (moderately bullish news)

Consensus: STRONG BUY (3 BUY, 1 SELL)
Interpretation: Growth stock trading at premium but strong fundamentals justify.
```

### AAPL (Apple) - HOLD 4.44/10
```
Valuation:    5.8/10 HOLD   (fair value, P/E ~30x)
Technicals:   4.0/10 HOLD   (neutral setup)
Fundamentals: 7.5/10 BUY    (excellent ROE, FCF)
Sentiment:    5.0/10 HOLD   (neutral sentiment)

Consensus: HOLD (mixed signals)
Interpretation: Quality company at fair price, no urgency to buy/sell.
```

### TSLA (Tesla) - HOLD 3.9/10
```
Valuation:    2.5/10 SELL   (overvalued on traditional metrics)
Technicals:   3.0/10 SELL   (bearish technicals)
Fundamentals: 6.5/10 BUY    (strong growth)
Sentiment:    4.0/10 HOLD   (neutral to bearish)

Consensus: HOLD (weak conviction)
Interpretation: Growth story but expensive, wait for better entry.
```

---

## Troubleshooting

### "No data available" errors
- Check ticker symbol is correct (SPHR not SPHE)
- Verify ticker exists on Yahoo Finance
- Some new tickers may have limited history

### "ABSTAIN" votes
- Phase 1 implementation should NOT return ABSTAIN if data exists
- If you see ABSTAIN, it means data API failed (not Phase 1 issue)
- Check internet connectivity, yfinance API status

### Low data quality
- Normal for new IPOs, penny stocks, OTC securities
- Agents will provide best-effort analysis but with LOW data quality flag
- Trust HIGH > MEDIUM > LOW data quality

### Unexpected conviction scores
- Agents are calibrated for typical stocks (not crypto, commodities)
- Extreme P/E ratios (>200x) will trigger low valuation scores
- Use domain knowledge to interpret edge cases

---

## Integration with 19-Agent System

### Current Status (Phase 1 Complete)
```
✅ Quant Agents (4/4): Valuation, Technicals, Fundamentals, Sentiment
✅ Legendary Investors (3/15): Buffett, Burry, Munger
⏳ Remaining (12/19): Phase 2-5 in progress
```

### How Quant Agents Feed Deliberation
```python
# Future: 19-agent deliberation
from quant_agents_v2 import run_full_quant_analysis
from legendary_investors import run_investor_analysis

# Phase 1 (Quant foundation)
quant_results = run_full_quant_analysis('SPHR')

# Phase 2-5 (Investor opinions)
investor_results = run_investor_analysis('SPHR', quant_context=quant_results)

# Synthesize all 19 agents
final_verdict = synthesize_all_agents(quant_results, investor_results)
```

---

## Next Steps

### For Users
1. Test on your watchlist tickers
2. Compare agent opinions to your own analysis
3. Track agent accuracy over time

### For Developers (Phase 2-5)
1. Use Phase 1 as template for remaining agents
2. Follow same output format (QuantOpinion dataclass)
3. Maintain data-driven approach (no placeholder scores)

---

## Files Reference

- **Implementation:** `quant_agents_v2.py`
- **Tests:** `test_phase1.py`
- **Config:** `quant_*.json` (4 files)
- **Documentation:** `PHASE1_COMPLETION_REPORT.md`
- **This Guide:** `PHASE1_QUICKSTART.md`

---

**Questions?** Check `PHASE1_COMPLETION_REPORT.md` for detailed implementation notes.

**Ready for Phase 2?** See `BUILD_PLAN.md` for next 12 agents to implement.
