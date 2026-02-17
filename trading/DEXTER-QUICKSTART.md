# Dexter Integration Quick-Start Guide

**Get up and running with Dexter research in 5 minutes**

---

## ⚡ Quick Setup

### 1. Verify Installation

```bash
cd ~/.openclaw/workspace

# Check Dexter exists
ls dexter-research/

# Check Bun installed
~/.bun/bin/bun --version
```

### 2. Configure API Keys

```bash
cd dexter-research

# Copy example env
cp env.example .env

# Edit with your keys
nano .env
```

**Minimum required:**
```env
# Choose ONE LLM provider
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Financial data (optional for testing, required for real analysis)
FINANCIAL_DATASETS_API_KEY=fds_...
```

### 3. Test Dexter (Standalone)

```bash
cd dexter-research
~/.bun/bin/bun run run-research.ts "AAPL" "Analyze fundamentals"
```

Expected: JSON output with research data

### 4. Test Python Wrapper

```bash
cd ~/. openclaw/workspace/trading/apps
python3 -c "
from dexter_research import DexterResearchEngine
engine = DexterResearchEngine(timeout=60)
print('✅ Dexter Python wrapper OK')
"
```

### 5. Run Full Integration Test

```bash
cd trading/agents
python3 test_dexter_integration.py
```

---

## 🚀 Usage Examples

### Example 1: Research a Ticker

```python
from trading.apps.dexter_research import DexterResearchEngine

engine = DexterResearchEngine()

result = engine.research_ticker(
    ticker="NVDA",
    focus_areas=['fundamentals', 'valuation']
)

print(f"Recommendation: {result['recommendation']}")
print(f"Conviction: {result['conviction']}/10")
```

### Example 2: Run 18-Agent Debate with Dexter

```python
from trading.agents.debate_orchestrator_v2 import EnhancedDebateOrchestrator

signal = {
    "ticker": "NVDA",
    "price": 875.00,
    "catalyst": "AI demand surge",
    "description": "NVIDIA - AI chip leader"
}

orchestrator = EnhancedDebateOrchestrator(signal, use_dexter=True)
orchestrator.run_full_debate_with_dexter(rounds=1)
```

### Example 3: Disable Dexter (Use Original Orchestrator)

```python
# If you want to run without Dexter for comparison
orchestrator = EnhancedDebateOrchestrator(signal, use_dexter=False)
orchestrator.run_full_debate_with_dexter(rounds=1)
```

---

## 📊 Check Results

### Research Files

```bash
ls -lh trading/research/
# Look for: {TICKER}_dexter_*.json
```

### Discord Channels

1. **#research** - Dexter's full analysis
2. **#18-agents-debate** - Agent deliberation with Dexter data

---

## 🐛 Troubleshooting

### "Command not found: bun"

```bash
# Use full path
~/.bun/bin/bun --version

# Or add to PATH
echo 'export PATH="$HOME/.bun/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "API key not configured"

```bash
# Check .env file
cat dexter-research/.env | grep API_KEY
```

### "Dexter timeout"

Increase timeout:
```python
engine = DexterResearchEngine(timeout=300)  # 5 min
```

### "Module not found"

```bash
# Ensure you're in workspace
cd ~/.openclaw/workspace/trading/apps
python3 dexter_research.py
```

---

## ✅ Verification Checklist

- [ ] Bun installed and accessible
- [ ] Dexter dependencies installed (`bun install`)
- [ ] API keys configured in `.env`
- [ ] `run-research.ts` runs and outputs JSON
- [ ] Python wrapper imports successfully
- [ ] Test debate runs without errors
- [ ] Research files saved to `trading/research/`
- [ ] Discord channels show Dexter + agent posts

---

## 🎯 Next Steps

Once verified:

1. **Run on real signal:**
   ```bash
   python3 trading/apps/autonomous_pipeline.py
   ```

2. **Monitor Discord:**
   - #research for Dexter analysis
   - #18-agents-debate for ensemble discussion

3. **Review conviction docs:**
   ```bash
   ls trading/conviction-docs/
   ```

---

## 📞 Need Help?

See full documentation: `trading/DEXTER-INTEGRATION.md`

**Common issues:**
- Missing API keys → Check `.env`
- Timeout → Increase `timeout` parameter
- JSON parse error → Verify `run-research.ts` output
