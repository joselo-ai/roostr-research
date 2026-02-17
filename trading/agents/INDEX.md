# 🎭 18-Agent Debate System - File Index

## 📁 Quick Navigation

### 🚀 **START HERE**
- **`QUICKSTART.md`** - Quick start guide (read this first!)
- **`./debate.sh`** - One-command launcher
- **`./run_debate.py`** - Main CLI script

### 📚 **Documentation**
- **`README-18-AGENTS-DEBATE.md`** - Complete system documentation
- **`DELIVERY_SUMMARY.md`** - What was built & delivery checklist
- **`INDEX.md`** - This file (navigation guide)

### 🧪 **Testing**
- **`test_debate_system.py`** - Test suite (run before first use)
  - Tests: DNA cards, vote parsing, orchestrator, Discord, tallying
  - Status: ✅ 5/5 tests passing

### ⚙️ **Core System**
- **`debate_orchestrator.py`** - Main orchestrator class
  - Loads 18 DNA cards
  - Spawns sub-agents
  - Monitors debate
  - Tallies votes
  - Generates reports

- **`discord_utils.py`** - Discord integration utilities
  - `DiscordClient` - Send/search messages
  - `VoteParser` - Parse agent votes from posts
  - Vote tallying and consensus logic

### 🧬 **Agent DNA Cards** (18 total)
**Location:** `investors/`

#### Legendary Investors (12)
1. `warren_buffett.json` 🎩
2. `charlie_munger.json` 🧠
3. `michael_burry.json` 🔍
4. `benjamin_graham.json` 📊
5. `mohnish_pabrai.json` 🎯
6. `cathie_wood.json` 🚀
7. `phil_fisher.json` 🔬
8. `peter_lynch.json` 🏪
9. `bill_ackman.json` ⚡
10. `stan_druckenmiller.json` 🌊
11. `aswath_damodaran.json` 📈
12. `rakesh_jhunjhunwala.json` 🐂

#### Quant Agents (4)
13. `valuation_agent.json` 💰
14. `sentiment_agent.json` 📱
15. `fundamentals_agent.json` 📊
16. `technicals_agent.json` 📉

#### Special Agents (2)
17. `risk_manager.json` 🛡️
18. `portfolio_manager.json` ⚖️

### 📊 **Example Signals**
**Location:** `signals/`
- `asts_signal.json` - ASTS (AST SpaceMobile) test signal
- `example_value_stock.json` - Generic value stock template

---

## 🎯 Common Tasks

### Run a Debate
```bash
# Default ASTS signal
./debate.sh

# Custom signal
./debate.sh signals/asts_signal.json

# From research markdown
./debate.sh ../research/ASTS_brief.md
```

### Test the System
```bash
python3 test_debate_system.py
```

### Create New Signal
1. Copy `signals/example_value_stock.json`
2. Edit with your signal details
3. Run: `./debate.sh signals/your_signal.json`

### View Agent DNA
```bash
# Pretty print an agent's DNA
cat investors/warren_buffett.json | python3 -m json.tool

# Check all agents exist
ls -1 investors/*.json | wc -l  # Should be 18
```

### Monitor Debate
```bash
# Watch spawned sessions
openclaw sessions_list

# View specific agent log
openclaw sessions_log <session_id>

# Discord: #18-agents-debate channel
```

---

## 📝 File Descriptions

### Scripts

| File | Purpose | Executable |
|------|---------|------------|
| `debate.sh` | Simple wrapper for launching debates | ✅ |
| `run_debate.py` | Main CLI launcher with modes | ✅ |
| `debate_orchestrator.py` | Core orchestration logic | ✅ |
| `discord_utils.py` | Discord utilities (can run tests) | ✅ |
| `test_debate_system.py` | Test suite | ✅ |

### Documentation

| File | Content |
|------|---------|
| `QUICKSTART.md` | Quick start guide for first-time users |
| `README-18-AGENTS-DEBATE.md` | Complete system documentation |
| `DELIVERY_SUMMARY.md` | Delivery checklist and testing results |
| `INDEX.md` | This file - navigation guide |

### Data

| Location | Content |
|----------|---------|
| `investors/*.json` | 18 agent DNA cards |
| `signals/*.json` | Example signal files |

---

## 🔗 Integration Points

### With Trading System
```python
from trading.agents.debate_orchestrator import DebateOrchestrator

signal = {...}  # Your signal data
orchestrator = DebateOrchestrator(signal)
result = orchestrator.run_full_debate(rounds=2)
```

### With Discord
- **Debate Channel:** 1472692185106481417
- **Research Channel:** 1469016715421175919
- **Bot Token:** `/Users/agentjoselo/.openclaw/workspace/.discord-bot-token`

### With OpenClaw
- Uses `openclaw sessions_spawn` for sub-agents
- Uses `openclaw message` for Discord posting
- Uses `openclaw sessions_list` for monitoring

---

## 🎭 System Architecture

```
run_debate.py
    ↓
debate_orchestrator.py
    ├─→ Loads investors/*.json (18 DNA cards)
    ├─→ Posts signal to Discord
    ├─→ Spawns 18 sub-agents (openclaw sessions_spawn)
    │   └─→ Each agent:
    │       ├─ Reads signal
    │       ├─ Analyzes via DNA philosophy
    │       └─ Posts to Discord (openclaw message)
    ├─→ Monitors Discord for posts
    ├─→ Parses votes (discord_utils.VoteParser)
    ├─→ Tallies consensus
    └─→ Posts final report to #research
```

---

## ✅ Quick Checklist

Before your first debate, verify:

- [ ] All 18 DNA cards exist: `ls investors/*.json | wc -l` → 18
- [ ] Test suite passes: `python3 test_debate_system.py` → 5/5
- [ ] Scripts are executable: `ls -l *.sh *.py | grep "x"`
- [ ] Discord bot token exists: `ls ../.discord-bot-token`
- [ ] You have access to Discord channels

Then run:
```bash
./debate.sh
```

---

## 🚀 Next Steps

1. **Read:** `QUICKSTART.md`
2. **Test:** `python3 test_debate_system.py`
3. **Run:** `./debate.sh`
4. **Watch:** Discord #18-agents-debate
5. **Review:** Final report in #research

---

**The stage is set. The legends await. Let the debate begin.** 🎭
