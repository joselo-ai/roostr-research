# Dexter Integration Plan
**Adding Deep Financial Research to roostr's 18-Agent System**

---

## 🎯 What is Dexter?

**Dexter** (by [@virattt](https://github.com/virattt)) is an autonomous financial research agent that:
- Takes complex financial questions
- Breaks them into structured research tasks
- Uses real-time financial data (income statements, balance sheets, cash flow)
- Self-validates and iterates until confident
- Outputs data-backed answers

**Think:** Claude Code, but for financial research.

**Why it matters:** Our agents currently use rule-based logic or simple prompts. Dexter brings **deep fundamental analysis** with real financial data.

---

## 🚀 How We'll Integrate

### Option 1: Add Dexter as 19th Agent (Recommended)

**Name:** Dexter Research Agent  
**Role:** Deep fundamental analysis using real-time financial data  
**When to use:** For stock signals that need detailed financial analysis

**Integration:**
```python
class DexterResearchAgent:
    """Autonomous research agent for deep fundamental analysis"""
    
    def __init__(self):
        self.dexter_client = DexterAPI()  # Call Dexter via API or local
    
    def evaluate(self, signal):
        # Ask Dexter to analyze the company
        query = f"Analyze {signal.ticker}: Is it undervalued? What's the moat? Growth outlook?"
        
        # Dexter breaks this into tasks:
        # 1. Get income statements (5 years)
        # 2. Calculate revenue/earnings growth
        # 3. Get balance sheet (debt, equity)
        # 4. Compare to industry peers
        # 5. Identify competitive moat
        
        research = self.dexter_client.research(query, ticker=signal.ticker)
        
        # Dexter returns structured analysis
        conviction = self.calculate_conviction(research)
        
        return {
            "agent": "Dexter Research",
            "conviction": conviction,
            "vote": "BUY" if conviction >= 7 else "HOLD",
            "reasoning": research.summary,
            "data": research.raw_data  # Include full financial statements
        }
```

**New Agent Count:** 19 agents (12 legendary + 4 quant + Dexter + 2 risk/portfolio)

---

### Option 2: Enhance Existing Fundamentals Agent

**Current Fundamentals Agent:** Rule-based (checks if "strong fundamentals" in catalyst)  
**Upgraded:** Uses Dexter to pull real financial data

**Pros:** Keep 18-agent count, just make Fundamentals Agent way smarter  
**Cons:** Dexter does more than fundamentals (also does valuation, competitive analysis)

**We prefer Option 1** (19th agent) because Dexter deserves its own voice in the ensemble.

---

## 🔧 Technical Setup

### Prerequisites
- **Runtime:** Bun (JavaScript/TypeScript)
- **APIs:**
  - OpenAI API key (we already have)
  - Financial Datasets API key (get from https://financialdatasets.ai)
  - Exa API key (optional, for web search)

### Installation

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/agents

# Clone Dexter
git clone https://github.com/virattt/dexter.git dexter-research
cd dexter-research

# Install Bun (if not already)
curl -fsSL https://bun.com/install | bash

# Install dependencies
bun install

# Set up environment
cp env.example .env
# Edit .env with API keys
```

### Python Wrapper

Since our agents are Python and Dexter is TypeScript, we need a bridge:

```python
# agents/dexter_bridge.py
import subprocess
import json

class DexterBridge:
    """Bridge between Python agents and Dexter (TypeScript)"""
    
    def research(self, query: str, ticker: str) -> dict:
        """Run Dexter research and return results"""
        
        # Call Dexter via subprocess
        result = subprocess.run(
            ['bun', 'run', 'src/cli.ts', '--query', query, '--ticker', ticker],
            cwd='/Users/agentjoselo/.openclaw/workspace/trading/agents/dexter-research',
            capture_output=True,
            text=True
        )
        
        # Parse JSON output
        return json.loads(result.stdout)
```

---

## 📊 Example: Dexter Analyzing PGR

**Input:**
```python
signal = {
    "ticker": "PGR",
    "price": 245.50,
    "catalyst": "Progressive Insurance - strong moat, P/E 15.2"
}
```

**Dexter's Research Plan:**
1. Get PGR income statements (last 5 years)
2. Calculate revenue growth rate
3. Calculate profit margin trends
4. Get balance sheet (debt/equity ratio)
5. Compare P/E to industry average
6. Identify competitive moat (insurance pricing power)
7. Summarize: Is it undervalued?

**Dexter's Output:**
```json
{
  "ticker": "PGR",
  "summary": "Progressive Insurance shows strong fundamentals. Revenue grew 12% CAGR over 5 years. Profit margin steady at 8-10%. Debt/equity ratio 0.3 (low). P/E 15.2 vs industry 18.5 = 18% discount. Competitive moat: Direct-to-consumer model (Flo ads) + usage-based pricing (Snapshot). Recommendation: BUY.",
  "conviction": 8.5,
  "data": {
    "revenue_growth_cagr": 0.12,
    "profit_margin": 0.09,
    "debt_equity_ratio": 0.3,
    "pe_ratio": 15.2,
    "industry_pe": 18.5,
    "moat_score": 8
  }
}
```

**Dexter Agent Vote:** 8.5/10 BUY

**Impact on Final Decision:**
- Before: Fundamentals Agent voted 7.0/10 HOLD (rule-based, no real data)
- After: Dexter Agent votes 8.5/10 BUY (real financial data)
- Combined conviction increases → more likely to deploy

---

## 🎯 Benefits

### 1. Real Financial Data
- Current: Agents rely on catalyst text (subjective)
- With Dexter: Pull actual income statements, balance sheets, cash flow
- **Result:** Data-backed decisions, not guesses

### 2. Deeper Analysis
- Current: "Strong fundamentals" keyword detection
- With Dexter: "Revenue grew 12% CAGR, profit margin 9%, debt/equity 0.3"
- **Result:** Know WHY it's a good investment

### 3. Self-Validation
- Dexter checks its own work, iterates until confident
- If data is inconclusive, it flags it
- **Result:** Higher quality research

### 4. Institutional-Grade Data
- Financial Datasets API = same data pros use
- Not scraping Yahoo Finance or Google
- **Result:** Compete with institutional funds

---

## 📈 Integration Timeline

### Week 1: Setup
- [ ] Install Bun runtime
- [ ] Clone Dexter repo
- [ ] Get Financial Datasets API key
- [ ] Test Dexter locally (query: "Analyze AAPL fundamentals")

### Week 2: Build Bridge
- [ ] Create `dexter_bridge.py` (Python → TypeScript)
- [ ] Create `DexterResearchAgent` class
- [ ] Integrate into `run_18_agents.py` (now 19 agents)
- [ ] Test on PGR signal

### Week 3: Production
- [ ] Run Dexter on all value stock signals
- [ ] Compare Dexter vote vs Fundamentals Agent vote
- [ ] Update conviction docs to include Dexter analysis
- [ ] Deploy first Dexter-approved signal

### Week 4: Optimize
- [ ] Cache financial data (don't re-fetch every time)
- [ ] Parallelize Dexter with other agents (run async)
- [ ] Add Dexter analysis to dashboard
- [ ] Tweet about "19th agent: Dexter joins the team"

---

## 💰 Cost Analysis

### API Costs

**Financial Datasets API:**
- Free tier: AAPL, NVDA, MSFT (3 tickers)
- Paid: $49/month for 100 tickers
- **We need:** ~50 tickers/month (value stocks)
- **Cost:** $49/month

**OpenAI API (Dexter uses GPT-4):**
- Current: ~$0.02/signal (GPT-4o-mini)
- With Dexter: ~$0.10/signal (GPT-4 for deep research)
- **Increase:** 5x per signal, but only for high-priority signals
- **Strategy:** Only run Dexter on signals >5.0/10 initial conviction

**Total Added Cost:** $49/month + ~$50/month API calls = **$100/month**

**ROI:** If Dexter improves conviction accuracy by 10% → worth it.

---

## 🔮 Future Enhancements

### Multi-Agent Research Teams
- Dexter + Buffett Agent debate on valuation
- Dexter pulls data, Buffett interprets through his lens
- Consensus = stronger conviction

### Custom Research Queries
- Ask Dexter: "Compare PGR vs ALL (competitors) on moat strength"
- Dexter analyzes both, ranks them
- Deploy capital to the better one

### Real-Time Monitoring
- Dexter watches deployed positions
- If fundamentals deteriorate (revenue drops, margins shrink) → flag for exit
- Proactive risk management

---

## 📞 Next Steps

**Immediate (This Week):**
1. Install Bun + clone Dexter repo
2. Get Financial Datasets API key
3. Test Dexter on AAPL (free tier)

**Short-term (Next 2 Weeks):**
1. Build Python bridge
2. Integrate as 19th agent
3. Test on PGR, ALL, KTB (our deployed value stocks)

**Long-term (Next Month):**
1. Use Dexter for all value stock signals
2. Compare Dexter accuracy vs rule-based Fundamentals Agent
3. If Dexter wins, replace Fundamentals Agent or keep both (19 agents)

---

## 🤝 Credit

**Dexter:** Built by [@virattt](https://twitter.com/virattt)  
**roostr Integration:** Designed by Joselo 🐓  
**Inspiration:** virattt also built the [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) that inspired our 18-agent architecture

---

**Let's add deep financial research to our stack. 19 agents > 18 agents. Always.**

🐓
