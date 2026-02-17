# 🎭 18-Agent Debate System - Quick Start

## Prerequisites

- OpenClaw installed and configured
- Discord bot token in `/Users/agentjoselo/.openclaw/workspace/.discord-bot-token`
- Access to Discord channels:
  - `#18-agents-debate` (1472692185106481417)
  - `#research` (1469016715421175919)

## 🚀 Run Your First Debate

### Option 1: Use Built-in ASTS Signal

```bash
cd /Users/agentjoselo/.openclaw/workspace/trading/agents
./run_debate.py
```

This will launch a debate on the ASTS (AST SpaceMobile) signal.

### Option 2: Use Custom Signal File

```bash
./run_debate.py signals/asts_signal.json
```

### Option 3: From Research Markdown

```bash
./run_debate.py ../research/ASTS_brief.md
```

## What Happens During a Debate

1. **Signal Posted** (5 seconds)
   - Orchestrator posts trading signal overview to Discord

2. **Round 1: Initial Analysis** (~60 seconds)
   - 18 sub-agents spawn in parallel
   - Each agent analyzes the signal through their unique lens
   - Posts formatted analysis to Discord:
     ```
     🎩 **Warren Buffett**
     
     [Analysis]
     
     **Vote:** BUY/HOLD/SELL
     **Conviction:** X/10
     **Risk:** Low/Medium/High
     ```

3. **Round 2: Responses** (~60 seconds, optional)
   - Agents read previous posts
   - Respond to contrarian views
   - May revise or strengthen positions

4. **Final Tally** (10 seconds)
   - Orchestrator tallies votes
   - Calculates consensus
   - Average conviction score

5. **Report Posted** (5 seconds)
   - Comprehensive conviction report posted to `#research`

**Total Time:** ~2-5 minutes depending on rounds

## 🎛️ Debate Modes

When you run the debate, choose:

1. **Quick debate** (1 round, ~2 minutes)
   - Fast initial analysis only
   - Good for quick signals

2. **Standard debate** (2 rounds, ~5 minutes) **[RECOMMENDED]**
   - Initial analysis + responses
   - Balanced depth and speed

3. **Deep debate** (3 rounds, ~10 minutes)
   - Multiple rounds of responses
   - For complex, controversial signals

## 📊 Example Output

```
╔═══════════════════════════════════════════════════════════════╗
║           🎭  18 LEGENDARY INVESTORS DEBATE SYSTEM  🎭        ║
╚═══════════════════════════════════════════════════════════════╝

📊 SIGNAL: ASTS @ $4.20
⚡ CATALYST: FCC Approval Expected Q1 2026

🎭 Starting 2-round debate...
⏰ Estimated time: ~5 minutes

🚀 Spawning warren_buffett (Round 1)...
🚀 Spawning charlie_munger (Round 1)...
🚀 Spawning michael_burry (Round 1)...
[... all 18 agents spawn ...]

✅ Round 1 complete!
⏳ Waiting for final posts...

============================================================
✅ DEBATE COMPLETE!
============================================================

📊 Final Tally:
   BUY:  8 votes
   HOLD: 4 votes
   SELL: 6 votes

🎯 Consensus: BUY (44%)
💪 Avg Conviction: 7.2/10

📢 Full report posted to Discord #research
```

## 🔍 Monitor Debate Progress

### Watch in Discord
Go to `#18-agents-debate` channel to see real-time posts.

### Check Agent Status
```bash
openclaw sessions_list
```

### View Agent Logs
```bash
openclaw sessions_log <session_id>
```

## 🧪 Test the System First

Before running a live debate:

```bash
./test_debate_system.py
```

This validates:
- All 18 DNA cards exist
- Vote parsing works
- Orchestrator initializes
- Discord client connects
- Vote tallying logic

## 📝 Create Your Own Signal

### JSON Format

```json
{
  "ticker": "TICKER",
  "price": 100.00,
  "catalyst": "What's the catalyst?",
  "description": "Full thesis with bull/bear cases"
}
```

Save to `signals/my_signal.json` and run:

```bash
./run_debate.py signals/my_signal.json
```

## 🎭 Understanding the Agents

Each agent has unique characteristics:

- **Buffett** 🎩: Wants moats, quality, simple businesses
- **Burry** 🔍: Contrarian, seeks asymmetric setups
- **Cathie Wood** 🚀: Loves disruptive tech, massive TAM
- **Graham** 📊: Pure value, margin of safety required
- **Risk Manager** 🛡️: Skeptical gatekeeper, challenges assumptions

See full DNA cards in `investors/*.json`

## 🛠️ Troubleshooting

### Agents Not Posting
- Check Discord bot token is valid
- Verify channel IDs are correct
- Check `openclaw sessions_list` for errors

### Vote Parsing Issues
- Ensure agents follow exact format
- Check Discord message history
- Run `test_debate_system.py`

### Slow Performance
- Reduce number of rounds
- Use smaller agent subset for testing
- Check system resources

## 🎯 Next Steps

1. **Run test debate:** `./run_debate.py` (use ASTS default)
2. **Watch Discord:** See agents post and debate
3. **Review report:** Check `#research` for final conviction doc
4. **Try custom signal:** Create your own signal file
5. **Integrate:** Hook into your trading pipeline

## 🔗 Integration with Trading System

To integrate with your autonomous trading system:

```python
from debate_orchestrator import DebateOrchestrator

# When new signal detected
signal = {
    "ticker": ticker,
    "price": current_price,
    "catalyst": catalyst_description,
    "description": full_analysis
}

# Run debate
orchestrator = DebateOrchestrator(signal)
result = orchestrator.run_full_debate(rounds=2)

# Use consensus for trading decision
if result['consensus'].startswith('BUY') and result['avg_conviction'] >= 7:
    # Enter trade
    execute_trade(ticker, 'BUY', size=calculate_size(result))
```

---

**Ready to unleash the legends? Run your first debate!** 🎭

```bash
./run_debate.py
```
