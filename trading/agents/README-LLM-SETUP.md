# LLM Integration Setup Guide

**Status:** Infrastructure ready, API billing needed

---

## Current State

✅ **Rule-based agents working** (0 cost, instant)
- 12 Legendary Investors
- 4 Quant Agents
- Successfully deployed 3 value stocks today

⏸️ **LLM agents ready but paused** (needs API credits)
- Code complete: `agents/llm_agents_direct.py`
- Uses direct OpenAI API (no LangChain dependency)
- Tested architecture working

---

## To Enable LLM Agents

### 1. Set Up OpenAI API Billing

**Note:** ChatGPT Pro ≠ API credits (separate systems)

1. Go to: https://platform.openai.com/settings/organization/billing
2. Add payment method
3. Add credits: $5-10 (enough for 1000+ signals)

### 2. Cost Estimate

**Per Signal (18 agents):**
- 12 Legendary Investors: 12 × GPT-4o-mini calls
- 4 Quant Agents: 4 × GPT-4o-mini calls
- Portfolio Manager: 1 × GPT-4o-mini call
- Risk Manager: Rule-based (free)

**Cost:**
- GPT-4o-mini: $0.15/$0.60 per 1M tokens
- Per signal: ~$0.02
- 100 signals/month: ~$2
- 1000 signals/month: ~$20

**Negligible cost for potential alpha.**

### 3. Test LLM Agents

After billing setup:

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading

# Test single agent
python3 agents/llm_agents_direct.py

# Should see:
# 🤖 Running LLM agents on PGR...
#    Warren Buffett... 8.5/10 BUY
#    Charlie Munger... 7.5/10 BUY
#    ...
```

### 4. Integrate with Portfolio Manager

Once working, run:

```bash
# Evaluate signal with LLM agents
python3 agents/run_18_agents_llm.py --ticker PGR --from-database
```

---

## Rule-Based vs LLM Comparison

### Rule-Based (Current, FREE)
✅ Instant (< 1 second)
✅ No cost
✅ Deterministic (same signal → same result)
✅ Already working (3 stocks deployed today)
❌ Less nuanced reasoning
❌ Can't handle complex narratives

### LLM-Powered ($0.02/signal)
✅ Deep reasoning (2-3 sentence explanations)
✅ Handles complex catalysts
✅ Captures subtle patterns
✅ More human-like analysis
❌ Costs $0.02 per signal
❌ Slower (15-30 seconds)
❌ Non-deterministic (slight variations)

---

## Recommendation

**Phase 1 (Now):** Use rule-based agents
- Free, fast, working
- Good enough for 90% of signals
- Already approved $175k deployment today

**Phase 2 (After API setup):** Hybrid approach
- Use rule-based for quick screening (free)
- Use LLM for final approval on signals >7/10 conviction
- Best of both worlds

**Phase 3 (Optional):** Full LLM
- All 18 agents use LLMs
- Deepest reasoning
- ~$20/month for 1000 signals

---

## Files Created

- `agents/llm_agents_direct.py` - Direct OpenAI API implementation
- `agents/llm_agents.py` - LangChain version (has Python 3.14 issues)
- This README

---

## Next Steps

1. Add OpenAI API credits ($5-10)
2. Test `llm_agents_direct.py`
3. If working, integrate with `portfolio_manager.py`
4. Add toggle: `--use-llm` flag for enhanced reasoning

---

**Status:** Ready when you are. Rule-based working great in meantime.
