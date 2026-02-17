# Dexter Research Engine Integration

**Production-Ready Integration of Dexter into roostr's 18-Agent Trading System**

---

## 🎯 Overview

**Dexter** (by [@virattt](https://github.com/virattt/dexter)) is now integrated as the **research engine** for roostr's 18-agent trading system.

### What This Means

**Before:** Agents debated based on catalyst text + rule-based logic
**After:** Agents debate WITH institutional-grade financial data from Dexter

**Impact:**
- ✅ Real income statements, balance sheets, cash flow
- ✅ Automated DCF valuation
- ✅ SEC filings analysis
- ✅ Competitive landscape research
- ✅ Self-validating research with audit trail

---

## 🏗️ Architecture

### Research Pipeline Flow

```
1. Signal arrives (ticker + catalyst)
   ↓
2. Dexter Research Engine (2-3 min deep dive)
   • Financial data: 5yr revenue/earnings/margins
   • Balance sheet: debt, cash, equity
   • Valuation: P/E, P/FCF, DCF estimate
   • SEC filings: 10-K, 10-Q analysis
   • News & sentiment: Latest catalysts
   • Risk assessment: What could go wrong?
   ↓
3. Dexter posts research to #research channel
   ↓
4. 18 Agents spawn WITH Dexter's data in their prompts
   ↓
5. Agents debate, citing specific financial metrics
   ↓
6. Final conviction doc includes Dexter research link
```

### Key Components

1. **`dexter-research/`** - Dexter codebase (TypeScript + Bun)
2. **`trading/apps/dexter_research.py`** - Python wrapper
3. **`trading/agents/debate_orchestrator_v2.py`** - Enhanced orchestrator
4. **`trading/research/`** - Research output storage

---

## 📦 Installation

### Prerequisites

- **Bun runtime** (JavaScript/TypeScript)
- **API Keys:**
  - OpenAI API (or Anthropic) - for LLM
  - Financial Datasets API - for real-time financial data
  - Exa/Tavily (optional) - for web search

### Step 1: Verify Dexter Installation

```bash
cd ~/.openclaw/workspace/dexter-research
ls -la  # Should see src/, package.json, etc.
```

✅ **Status:** Dexter already cloned and dependencies installed

### Step 2: Install Bun Runtime

```bash
# Check if installed
which bun

# If not installed:
curl -fsSL https://bun.sh/install | bash
```

✅ **Status:** Bun installed at `~/.bun/bin/bun`

### Step 3: Configure API Keys

Edit `dexter-research/.env`:

```bash
cd dexter-research
nano .env
```

**Required keys:**

```env
# LLM Provider (choose one)
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Financial Data (REQUIRED for real analysis)
FINANCIAL_DATASETS_API_KEY=fds_...

# Web Search (Optional but recommended)
EXASEARCH_API_KEY=...
TAVILY_API_KEY=...
```

**Get API Keys:**
- **Financial Datasets:** https://financialdatasets.ai (free tier: 3 tickers)
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/
- **Exa:** https://exa.ai/

### Step 4: Test Dexter

```bash
cd dexter-research
bun run run-research.ts "AAPL" "Analyze Apple's fundamentals"
```

Expected output: JSON with research data

---

## 💬 Discord Chat Interface (NEW)

**Direct Q&A with Dexter via Discord**

Monitor `#dexter-research` channel for questions and respond with research:

### Start the Bot

```bash
cd dexter-research

# Background (recommended)
./start_discord_bot.sh bg

# Foreground (see logs)
./start_discord_bot.sh
```

### Usage

Post questions in Discord `#dexter-research`:

```
What is AAPL's revenue?
```

```
Analyze $TSLA fundamentals
```

```
NVDA valuation vs peers
```

Dexter responds within 30-60 seconds with:
- Summary
- Key financials
- Valuation metrics
- Risks & catalysts
- Recommendation

**Full Documentation:** `dexter-research/DISCORD-CHAT.md`

---

## 🚀 Usage

### Programmatic Usage (Python)

```python
from trading.apps.dexter_research import DexterResearchEngine

# Initialize engine
engine = DexterResearchEngine(timeout=180)

# Run research
result = engine.research_ticker(
    ticker="ASTS",
    focus_areas=['fundamentals', 'valuation', 'risks', 'catalysts']
)

# Results
print(f"Recommendation: {result['recommendation']}")
print(f"Conviction: {result['conviction']}/10")
print(f"Summary: {result['summary']}")

# Save to file
engine.save_research(result)  # → trading/research/ASTS_dexter_*.json
```

### Integrated 18-Agent Debate

```python
from trading.agents.debate_orchestrator_v2 import EnhancedDebateOrchestrator

signal = {
    "ticker": "ASTS",
    "price": 4.20,
    "catalyst": "FCC Approval Expected Q1 2026",
    "description": "..."
}

# Run Dexter-enhanced debate
orchestrator = EnhancedDebateOrchestrator(signal, use_dexter=True)
orchestrator.run_full_debate_with_dexter(rounds=2)
```

**What happens:**
1. Dexter researches ASTS (2-3 min)
2. Posts research to #research Discord channel
3. Spawns 18 agents with Dexter's data in their prompts
4. Agents debate, citing real financial metrics
5. Final conviction doc links to Dexter research file

---

## 📊 Example: ASTS Research Flow

### Input Signal

```python
{
    "ticker": "ASTS",
    "price": 4.20,
    "catalyst": "FCC Approval Expected Q1 2026",
    "description": "AST SpaceMobile - space-based cellular broadband"
}
```

### Dexter Research (Automated)

**Query sent to Dexter:**
```
Analyze ASTS: FCC Approval Expected Q1 2026

Provide:
1. Fundamentals: Revenue/earnings growth, margins, ROIC
2. Financial health: Balance sheet, cash flow, debt
3. Valuation: P/E, P/FCF vs peers, DCF estimate
4. Competitive moat vs SpaceX Starlink
5. Catalyst analysis: FCC approval significance
6. Key risks
7. Investment recommendation: BUY/HOLD/SELL with conviction
```

**Dexter Output (Example):**

```json
{
  "ticker": "ASTS",
  "recommendation": "BUY",
  "conviction": 7.5,
  "summary": "ASTS is a pre-revenue satellite telecom play with significant upside if FCC approval comes through. Key partnerships (AT&T, Vodafone) provide validation. Technology proven with BlueBird. Main risk: SpaceX competition and capital intensity.",
  "financials": {
    "revenue_2024": "$0M (pre-revenue)",
    "cash_position": "$280M",
    "burn_rate": "$45M/quarter",
    "runway": "~6 quarters"
  },
  "valuation": {
    "market_cap": "$1.2B",
    "enterprise_value": "$950M",
    "dcf_estimate": "N/A (pre-revenue)",
    "tam": "$1.4T (mobile connectivity market)"
  },
  "catalysts": [
    "FCC approval (Q1 2026 expected)",
    "BlueWalker 3 expansion",
    "Carrier partnership announcements"
  ],
  "risks": [
    "FCC rejection (binary risk)",
    "SpaceX Starlink direct-to-phone competition",
    "Capital requirements ($2B+ for full constellation)",
    "Technology execution risk"
  ]
}
```

### Agent Debate (Enhanced)

**Warren Buffett Agent receives this prompt:**

```
You are Warren Buffett 🏦

[Investment philosophy...]

TRADING SIGNAL:
Ticker: ASTS
Catalyst: FCC Approval Expected Q1 2026

🔬 DEXTER RESEARCH DATA (Institutional-Grade):

Dexter's Recommendation: BUY
Dexter's Conviction: 7.5/10

Key Financials:
- Revenue: $0M (pre-revenue)
- Cash: $280M
- Burn rate: $45M/quarter
- Runway: ~6 quarters

Valuation:
- Market cap: $1.2B
- TAM: $1.4T

Catalysts:
- FCC approval (Q1 2026)
- BlueWalker 3 expansion

Risks:
- FCC rejection (binary)
- SpaceX competition
- $2B+ capital requirements

---

YOUR TASK:
Analyze through YOUR lens, using Dexter's data.

Post your analysis to #18-agents-debate.
Cite specific financial metrics.
```

**Buffett's Response (Example):**

```
🏦 Warren Buffett

I'm generally skeptical of pre-revenue space plays - they violate my "invest in 
businesses you understand" principle. However, Dexter's data shows ASTS has:

1. Strong partnerships (AT&T, Vodafone = 2.8B subscribers)
2. Proven technology (BlueBird satellite functional)
3. 6-quarter cash runway (sufficient for FCC decision)

BUT: This is a binary bet on FCC approval. Not my style. And SpaceX competition 
with deeper pockets is concerning. The $2B capital requirement post-approval is 
another red flag - they'll need to dilute shareholders.

**Key Data I'm Using:**
• Cash position: $280M vs $45M/quarter burn = 6Q runway
• TAM: $1.4T is massive, but execution risk is high
• Market cap: $1.2B seems rich for pre-revenue

**Vote:** HOLD
**Conviction:** 4/10
**Risk:** High
```

**Michael Burry Agent (Contrarian):**

```
🐻 Michael Burry

Everyone's bearish on pre-revenue space plays. That's exactly when I get interested.

Dexter's data shows ASTS is mispriced:
• $1.2B market cap vs $1.4T TAM = 0.08% market capture pricing
• If they capture just 1% of TAM → $14B revenue potential
• FCC approval odds underpriced (I'd say 60-70%, market pricing ~30%)

SpaceX risk is overblown - ASTS partners ARE the carriers. Starlink competes 
WITH carriers; ASTS works FOR them. Different model.

**Key Data I'm Using:**
• TAM: $1.4T (massive asymmetry)
• Market cap: $1.2B (cheap if approved)
• Partnership validation: AT&T doesn't partner with junk

**Vote:** BUY
**Conviction:** 8/10
**Risk:** High (but asymmetric payoff)
```

### Final Conviction Doc

```markdown
# Investment Conviction Report: ASTS

## Dexter Research Summary
- Recommendation: BUY
- Conviction: 7.5/10
- Research file: trading/research/ASTS_dexter_20260215_153000.json

## Agent Votes
- BUY: 10 votes (avg conviction: 7.2)
- HOLD: 6 votes (avg conviction: 5.1)
- SELL: 2 votes (avg conviction: 3.5)

## Consensus: BUY
**Final Conviction:** 6.8/10

## Key Arguments (Citing Dexter Data)
- Bull: 1% of $1.4T TAM = $14B revenue potential vs $1.2B market cap
- Bull: Carrier partnerships validate technology (AT&T, Vodafone)
- Bull: FCC approval odds underpriced by market
- Bear: Pre-revenue with $2B+ capital needs = dilution risk
- Bear: SpaceX competition (though different business model)

## Risk Assessment
- Binary catalyst: FCC approval or rejection
- Capital intensity: $2B+ needed post-approval
- Execution risk: Full constellation buildout unproven

## Deployment Decision: HOLD
Wait for FCC decision clarity. Consider 2% position if approval confirmed.
```

---

## 🔧 Technical Details

### File Structure

```
workspace/
├── dexter-research/              # Dexter codebase
│   ├── src/                      # TypeScript source
│   ├── run-research.ts           # Programmatic runner (NEW)
│   ├── discord_chat.py           # Discord chat bot (NEW)
│   ├── start_discord_bot.sh      # Bot launcher (NEW)
│   ├── .env                      # API keys
│   ├── DISCORD-CHAT.md           # Discord bot docs (NEW)
│   └── package.json
│
└── trading/
    ├── apps/
    │   └── dexter_research.py    # Python wrapper (NEW)
    │
    ├── agents/
    │   ├── debate_orchestrator.py           # Original orchestrator
    │   └── debate_orchestrator_v2.py        # Dexter-enhanced (NEW)
    │
    └── research/
        └── {TICKER}_dexter_*.json   # Research outputs
```

### Python API Reference

#### `DexterResearchEngine`

**Methods:**

```python
research_ticker(ticker, question=None, focus_areas=None)
# Run deep research on a ticker
# Returns: Dict with financial data, valuation, risks, etc.

save_research(research_data, output_dir=None)
# Save research to JSON file
# Returns: Path to saved file
```

**Example:**

```python
engine = DexterResearchEngine(timeout=180)

result = engine.research_ticker(
    ticker="PGR",
    focus_areas=['fundamentals', 'valuation', 'moat']
)

# Access data
print(result['recommendation'])  # 'BUY'
print(result['conviction'])      # 8.5
print(result['financials'])      # {...}
print(result['valuation'])       # {...}
print(result['risks'])           # [...]
```

#### `EnhancedDebateOrchestrator`

**Methods:**

```python
run_dexter_research()
# Phase 1: Run Dexter research
# Returns: Research dict

post_dexter_summary()
# Phase 2: Post to #research channel

run_full_debate_with_dexter(rounds=2)
# Complete flow: Dexter → 18 agents → conviction doc
```

---

## 📈 Performance & Cost

### Research Time
- **Dexter research:** 2-3 minutes per ticker
- **18-agent debate:** 1-2 minutes (with Dexter data)
- **Total:** 3-5 minutes end-to-end

### API Costs

**Per Signal (with Dexter):**
- Dexter research: ~$0.10 (GPT-4 + Financial Datasets API)
- 18 agents (enhanced): ~$0.20 (GPT-4o-mini)
- **Total:** ~$0.30/signal

**Monthly (50 signals):**
- Dexter: $5
- Agents: $10
- Financial Datasets API: $49 (100 tickers/month)
- **Total:** ~$64/month

**ROI:** If Dexter improves conviction accuracy by 10%, easily worth it.

---

## ✅ Testing

### Test 1: Dexter Research (Standalone)

```bash
cd trading/apps
python3 dexter_research.py
```

Expected output:
```
🔍 Starting Dexter research on ASTS...
✅ Research complete in 2.3s
💾 Research saved to trading/research/ASTS_dexter_*.json

Ticker: ASTS
Recommendation: BUY
Conviction: 7.5/10
```

### Test 2: Integrated Debate

```bash
cd trading/agents
python3 debate_orchestrator_v2.py
```

Expected flow:
1. ✅ Dexter research runs (2-3 min)
2. ✅ Research posted to #research
3. ✅ Signal overview posted to #18-agents-debate
4. ✅ 18 agents spawn with Dexter data
5. ✅ Agents post analyses citing financial metrics
6. ✅ Final conviction doc generated

### Test 3: ASTS Full Integration

```python
from trading.agents.debate_orchestrator_v2 import EnhancedDebateOrchestrator

signal = {
    "ticker": "ASTS",
    "price": 4.20,
    "catalyst": "FCC Approval Expected Q1 2026",
    "description": "AST SpaceMobile - space-based cellular broadband"
}

orchestrator = EnhancedDebateOrchestrator(signal, use_dexter=True)
orchestrator.run_full_debate_with_dexter(rounds=2)
```

Check:
- [ ] Dexter research completes
- [ ] Research posted to Discord #research
- [ ] 18 agents reference Dexter data
- [ ] Agents cite specific financial metrics
- [ ] Final doc links to Dexter research file

---

## 🎯 Success Criteria

✅ **Dexter researches ticker in <3 minutes**
✅ **Returns: financials, filings, news, valuation, competitive analysis**
✅ **18 agents cite Dexter's data in their arguments**
✅ **Discord shows: Dexter research → Agent debate → Consensus**
✅ **Research files saved to trading/research/**

---

## 🚨 Troubleshooting

### Issue: "Bun not found"

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Restart shell
exec $SHELL
```

### Issue: "Financial Datasets API key required"

```bash
# Get free API key
# Visit: https://financialdatasets.ai
# Add to dexter-research/.env:
FINANCIAL_DATASETS_API_KEY=fds_...
```

### Issue: "Dexter timeout"

```python
# Increase timeout
engine = DexterResearchEngine(timeout=300)  # 5 minutes
```

### Issue: "Research output not JSON"

Dexter's `run-research.ts` should output JSON. If not, check:
```bash
cd dexter-research
bun run run-research.ts "AAPL" "test" | jq .
```

---

## 📚 Next Steps

### Phase 1: ✅ Complete
- [x] Install Dexter
- [x] Create Python wrapper
- [x] Integrate with orchestrator
- [x] Test with ASTS
- [x] Documentation

### Phase 2: Production Enhancements
- [ ] Full Dexter agent integration (beyond run-research.ts)
- [ ] Cache financial data (avoid re-fetching)
- [ ] Parallel execution (Dexter + agents async)
- [ ] Dashboard integration (show Dexter research in real-time)
- [ ] Historical analysis (backtest Dexter recommendations)

### Phase 3: Advanced Features
- [ ] Multi-ticker comparison (Dexter compares PGR vs ALL)
- [ ] Real-time monitoring (Dexter watches deployed positions)
- [ ] Custom research templates (earnings, M&A, regulatory)
- [ ] Agent-Dexter debate (agents question Dexter's assumptions)

---

## 📞 Support

**Issues?**
- Dexter repo: https://github.com/virattt/dexter
- roostr integration: Check trading/agents/DEXTER-INTEGRATION.md

**Credits:**
- **Dexter:** Built by [@virattt](https://twitter.com/virattt)
- **Integration:** roostr team
- **Inspiration:** virattt's [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)

---

## 🐓 Conclusion

**You now have institutional-grade financial research powering your 18-agent trading system.**

Before: Agents debated based on vibes and catalyst keywords.
After: Agents debate with real income statements, balance sheets, and valuations.

**This is the edge.**

Let's deploy some capital. 🚀

---

**Integration Status:** ✅ Production-Ready
**Test Signal:** ASTS
**Delivered:** 2026-02-15
