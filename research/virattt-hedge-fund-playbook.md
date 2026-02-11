# @virattt AI Hedge Fund Playbook

**Source:** https://x.com/virattt | https://github.com/virattt/ai-hedge-fund  
**Project Stats:** 45.7k stars | 8k forks  
**Purpose:** Educational AI-powered hedge fund proof of concept  
**Extracted:** Feb 11, 2026

---

## Overview

Virat Singh (@virattt) created an AI-powered hedge fund system that uses **multi-agent collaboration** to make trading decisions. This is NOT a real trading system — it's a research/educational proof of concept that demonstrates how AI agents can work together to analyze stocks and generate trading signals.

**Key Innovation:** Instead of one AI making all decisions, this system uses **18 specialized agents** that each bring a different investment philosophy, then synthesizes their inputs into final trading decisions.

---

## The Agent Architecture

### 1. **Famous Investor Agents (12)**

Each agent embodies the investment philosophy of a legendary investor:

#### Value Investing School:
- **Ben Graham Agent** — "The godfather of value investing, only buys hidden gems with a margin of safety"
- **Charlie Munger Agent** — "Warren Buffett's partner, only buys wonderful businesses at fair prices"
- **Warren Buffett Agent** — "The oracle of Omaha, seeks wonderful companies at a fair price"
- **Michael Burry Agent** — "The Big Short contrarian who hunts for deep value"
- **Mohnish Pabrai Agent** — "The Dhandho investor, who looks for doubles at low risk"

#### Growth Investing School:
- **Cathie Wood Agent** — "The queen of growth investing, believes in the power of innovation and disruption"
- **Phil Fisher Agent** — "Meticulous growth investor who uses deep 'scuttlebutt' research"
- **Peter Lynch Agent** — "Practical investor who seeks 'ten-baggers' in everyday businesses"

#### Activist/Macro School:
- **Bill Ackman Agent** — "An activist investor, takes bold positions and pushes for change"
- **Stanley Druckenmiller Agent** — "Macro legend who hunts for asymmetric opportunities with growth potential"

#### Valuation School:
- **Aswath Damodaran Agent** — "The Dean of Valuation, focuses on story, numbers, and disciplined valuation"

#### International:
- **Rakesh Jhunjhunwala Agent** — "The Big Bull of India"

### 2. **Analysis Agents (4)**

These agents perform quantitative analysis:

- **Valuation Agent** — Calculates intrinsic value and generates trading signals
- **Sentiment Agent** — Analyzes market sentiment and generates trading signals
- **Fundamentals Agent** — Analyzes fundamental data and generates trading signals
- **Technicals Agent** — Analyzes technical indicators and generates trading signals

### 3. **Risk & Portfolio Management (2)**

- **Risk Manager** — Calculates risk metrics and sets position limits
- **Portfolio Manager** — Makes final trading decisions and generates orders

---

## The Decision-Making Workflow

```
Input (Tickers, Date Range, Portfolio State)
    ↓
[START NODE]
    ↓
[All Selected Analyst Agents Run in Parallel]
    ├→ Value Investors analyze
    ├→ Growth Investors analyze
    ├→ Quantitative Agents analyze
    └→ Each generates signals + reasoning
    ↓
[Risk Management Agent]
    ├→ Calculates risk metrics
    ├→ Sets position limits
    └→ Validates constraints
    ↓
[Portfolio Manager]
    ├→ Synthesizes all signals
    ├→ Makes final decisions
    └→ Generates orders (Buy/Sell/Hold)
    ↓
Output (Trading decisions + analyst signals)
```

**Key Insight:** The system doesn't just average opinions — it uses a **LangGraph state machine** where each agent's output flows into the next stage, allowing the Risk Manager and Portfolio Manager to have full context of ALL analyst reasoning before making final calls.

---

## Technical Stack

### Core Framework:
- **LangChain + LangGraph** — Agent orchestration and state management
- **Python** — Primary language
- **Poetry** — Dependency management

### LLM Support:
- OpenAI (GPT-4o, GPT-4o-mini)
- Anthropic (Claude)
- Groq
- DeepSeek
- **Ollama** (local LLMs) — Can run entirely offline

### Data Sources:
- **Financial Datasets API** — Market data
- Free data for: AAPL, GOOGL, MSFT, NVDA, TSLA (no API key needed)
- Paid API key required for other tickers

### Interfaces:
- **CLI** — Command-line interface for automation/scripting
- **Web App** — User-friendly UI (full-stack app)

---

## The Playbook (How to Use This Yourself)

### Phase 1: Setup
```bash
# Clone the repo
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund

# Set up API keys
cp .env.example .env
# Edit .env to add:
# - OPENAI_API_KEY (or other LLM provider)
# - FINANCIAL_DATASETS_API_KEY (optional for non-free tickers)

# Install dependencies
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

### Phase 2: Run Analysis
```bash
# Basic run (analyze 3 stocks)
poetry run python src/main.py --ticker AAPL,MSFT,NVDA

# With reasoning visible
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning

# Historical backtest
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA

# Custom date range
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01

# Local LLMs (no API key needed)
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --ollama
```

### Phase 3: Interpret Output
The system generates:
1. **Individual analyst signals** — Each agent's buy/sell/hold recommendation + reasoning
2. **Risk metrics** — Position limits, margin requirements, exposure calculations
3. **Final portfolio decision** — Synthesized trading orders with rationale

---

## Key Design Principles

### 1. **Ensemble Decision Making**
- No single agent has final authority
- Diversity of thought (value vs growth vs macro)
- Risk management acts as a guardrail
- Portfolio manager synthesizes everything

### 2. **Transparency & Explainability**
- Every agent documents its reasoning
- `--show-reasoning` flag reveals thought process
- Backtester shows historical performance
- Educational focus (not black-box)

### 3. **Modularity**
- Agents can be added/removed easily
- Custom analysts can be created
- Swap LLM providers without code changes
- Run locally (Ollama) or cloud (OpenAI/Anthropic)

### 4. **Safety First**
- Does NOT execute real trades
- Risk manager enforces limits
- Margin requirements built in
- Clear disclaimers everywhere

---

## What Makes This Approach Different

### Traditional Quant Funds:
- Backtested algorithms
- Statistical arbitrage
- High-frequency trading
- Often opaque

### @virattt's Approach:
- **Simulated human reasoning** (not just math)
- **Multi-perspective analysis** (12 legendary investors)
- **Explainable decisions** (see exactly why each agent voted a certain way)
- **Adaptable** (swap agents, change LLMs, customize logic)

**Core Philosophy:** "What if you could assemble a team of the world's greatest investors to analyze every trade together?"

---

## Practical Applications

### For Learning:
- Study how different investment philosophies approach the same stock
- Compare value vs growth vs momentum strategies
- Understand risk management frameworks

### For Research:
- Test hypothesis: "Does ensemble decision-making beat single-agent AI?"
- Backtest historical performance of different agent combinations
- Experiment with custom analyst agents

### For Real Trading (CAREFULLY):
- Use signals as **one input** among many
- Never blindly follow AI recommendations
- Validate with your own research
- Consult financial advisors

---

## Limitations & Caveats

1. **NOT financial advice** — Educational proof of concept only
2. **No real-time data** — Uses historical/delayed data
3. **LLM limitations** — Models can hallucinate, make errors
4. **Market dynamics** — AI doesn't predict black swans, regime changes
5. **Execution gaps** — No slippage, liquidity, or transaction cost modeling
6. **Regulatory** — Not a registered investment advisor

**From the repo:** "This project is for educational and research purposes only. Not intended for real trading or investment. No investment advice or guarantees provided. Creator assumes no liability for financial losses."

---

## How This Maps to roostr Capital

### What We Can Learn:

#### 1. **Multi-Agent Architecture**
- We're already building this (Conviction scoring, Signal validation)
- Consider: Should we add "legendary investor" personas to challenge our own theses?
- Example: Run our $ACGL conviction doc through a "Charlie Munger agent" — would he agree?

#### 2. **Ensemble Decision Making**
- We have manual ensemble (Yieldschool + Dumb Money + Chart Fanatics + Manual research)
- Could formalize: Each source = an "agent" with scoring weights
- Risk manager (you, Joselo) synthesizes and enforces stops

#### 3. **Backtesting Infrastructure**
- virattt has `backtester.py` — we should build one
- Test signals historically: How would our current playbook have performed in 2023? 2024?
- Validate conviction scoring accuracy

#### 4. **Transparency & Documentation**
- Every trade = conviction doc (we do this)
- Every agent = reasoning trail (virattt does this)
- Could add: "Agent analysis log" for each signal (what would Buffett say? What would Munger say?)

### What We DON'T Want:

1. **Over-automation** — We're human-in-the-loop by design
2. **Black-box decisions** — We want conviction, not blind AI faith
3. **Complexity for complexity's sake** — Keep it simple, keep it sharp

### Potential Integration:

**roostr Signal Validator v2:**
```
Input: New signal ($ASTS, $ACGL, etc.)
    ↓
[Fundamental Agent] → Analyzes financials
[Sentiment Agent] → Reddit, Discord, social activity
[Technical Agent] → Chart patterns, RSI, volume
[Catalyst Agent] → News, events, earnings
[Conviction Agent] → Generates score + doc
    ↓
[Risk Manager (Joselo)] → Validates against portfolio rules
    ↓
[Decision] → Deploy / Hold / Reject
```

This is basically what we're doing manually — but virattt's code gives us a blueprint for **formalizing and scaling** it.

---

## Bottom Line

**virattt's playbook:** Build a team of AI agents that simulate legendary investors, let them debate, then synthesize their insights into trading decisions with transparent reasoning and built-in risk management.

**Core Takeaway:** The power isn't in any single agent — it's in the **collective intelligence** + **risk guardrails** + **human oversight**.

**For roostr:** We're already doing this manually. His code gives us a framework to:
1. Formalize our signal validation process
2. Add backtesting infrastructure
3. Scale analysis (run 10 stocks through the system in parallel)
4. Maintain transparency (every decision = conviction doc)

**Action Items:**
1. ✅ Document virattt's playbook (this file)
2. Clone repo, run experiments locally
3. Build roostr-specific agents (Yieldschool Agent, Dumb Money Agent, Riz Agent)
4. Integrate backtesting into our workflow
5. Consider: Multi-agent conviction scoring (Buffett score + Munger score + Druckenmiller score = weighted average)

---

**Repository:** https://github.com/virattt/ai-hedge-fund  
**X/Twitter:** https://x.com/virattt  
**Status:** Active development, 45.7k stars, MIT licensed

**Extracted by:** Joselo 🐓  
**Date:** Feb 11, 2026  
**Location:** `/Users/agentjoselo/.openclaw/workspace/research/virattt-hedge-fund-playbook.md`
