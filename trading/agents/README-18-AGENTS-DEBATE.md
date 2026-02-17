# 🎭 18 Legendary Investors Debate System

## Overview

This system spawns 18 separate AI sub-agents, each embodying a legendary investor's philosophy, to debate trading signals in real-time on Discord. **This is not simulated** - these are actual OpenClaw sub-agents posting, reading each other's messages, and responding.

## The 18 Agents

### Legendary Investors (12)
1. **Warren Buffett** 🎩 - Value, long-term, moat focus
2. **Charlie Munger** 🧠 - Mental models, quality businesses
3. **Michael Burry** 🔍 - Contrarian, deep research, asymmetric bets
4. **Benjamin Graham** 📊 - Pure value, margin of safety
5. **Mohnish Pabrai** 🎯 - Concentrated bets, low-risk high-return
6. **Cathie Wood** 🚀 - Disruptive innovation, long-term growth
7. **Phil Fisher** 🔬 - Growth at reasonable price, scuttlebutt
8. **Peter Lynch** 🏪 - Invest in what you know, earnings growth
9. **Bill Ackman** ⚡ - Activist, catalyst-driven, concentrated
10. **Stan Druckenmiller** 🌊 - Macro, reflexivity, position sizing
11. **Aswath Damodaran** 📈 - Valuation precision, DCF models
12. **Rakesh Jhunjhunwala** 🐂 - Emerging markets, high conviction

### Quant Agents (4)
13. **Valuation Agent** 💰 - DCF, multiples, fair value
14. **Sentiment Agent** 📱 - Social media, news, momentum
15. **Fundamentals Agent** 📊 - Financials, ratios, business quality
16. **Technicals Agent** 📉 - Charts, RSI, volume, patterns

### Control Agents (2)
17. **Risk Manager (Joselo)** 🛡️ - Final veto, risk assessment
18. **Portfolio Manager** ⚖️ - Position sizing, allocation

## Architecture

### Components

1. **Agent DNA Cards** (`trading/agents/investors/*.json`)
   - JSON files defining each agent's personality, philosophy, and decision framework
   - Used to build prompts for sub-agent spawns

2. **Orchestrator** (`debate_orchestrator.py`)
   - Main control script
   - Spawns 18 sub-agents in parallel
   - Monitors Discord for responses
   - Tallies votes and generates final report

3. **Discord Integration** (`discord_utils.py`)
   - Discord API wrapper using OpenClaw message tool
   - Vote parser to extract decisions from agent posts
   - Message formatting utilities

4. **Run Script** (`run_debate.py`)
   - CLI interface to launch debates
   - Can load signals from files or use built-in examples

## Debate Flow

```
1. Orchestrator posts signal → Discord #18-agents-debate
2. Round 1: All 18 agents post initial analysis (parallel spawns)
   ├─ Each agent analyzes through their unique lens
   ├─ Posts formatted analysis to Discord
   └─ Includes: Vote (BUY/HOLD/SELL), Conviction (0-10), Risk (Low/Med/High)
3. Round 2: Agents respond to contrarian views (optional)
   ├─ Agents read previous posts
   └─ May challenge or expand on points
4. Round 3: Final votes + conviction scores (optional)
5. Orchestrator tallies consensus
6. Risk Manager (Joselo) posts final verdict
7. Conviction doc generated → Discord #research
```

## Usage

### Quick Start

```bash
# Run debate on ASTS (default signal)
./run_debate.py

# Run debate on custom signal
./run_debate.py signals/my_signal.json

# Run debate from markdown research
./run_debate.py research/ASTS_brief.md
```

### Signal Format (JSON)

```json
{
  "ticker": "ASTS",
  "price": 4.20,
  "catalyst": "FCC Approval Expected Q1 2026",
  "description": "Full description of the investment thesis, bull/bear cases, etc."
}
```

### Discord Output Format

Each agent posts in this format:

```
🎩 **Warren Buffett**

This is a speculative pre-revenue business. I don't understand 
satellite technology well enough. Without earnings, moat evidence, 
or clear path to profitability, this violates my core principles.

**Vote:** SELL
**Conviction:** 8/10
**Risk:** High
```

## Technical Details

### Sub-Agent Spawning

Each agent is spawned using OpenClaw's `sessions_spawn`:

```python
openclaw sessions_spawn \
    --label "warren_buffett_round1" \
    --task "Analyze ASTS and post to Discord..." \
    --background
```

### Discord Posting

Agents use OpenClaw's message tool to post:

```python
openclaw message \
    --action send \
    --target 1472692185106481417 \
    --message "🎩 **Warren Buffett**\n\n[analysis]"
```

### Vote Tallying

The orchestrator:
1. Searches Discord messages after each round
2. Parses votes using regex patterns
3. Tallies BUY/HOLD/SELL votes
4. Calculates average conviction
5. Determines consensus

## Configuration

### Discord Channels

- **Debate Channel:** `#18-agents-debate` (1472692185106481417)
- **Research Channel:** `#research` (1469016715421175919)

### Customization

1. **Add New Agent:**
   - Create DNA card in `investors/new_agent.json`
   - Add to `AGENT_ORDER` in `debate_orchestrator.py`

2. **Modify Debate Flow:**
   - Edit `run_debate_round()` in orchestrator
   - Adjust timing, rounds, or agent order

3. **Change Output Format:**
   - Modify `build_agent_prompt()` to change post format
   - Update `VoteParser` in `discord_utils.py` to match

## Testing

### Test Vote Parsing

```bash
python discord_utils.py
```

### Dry Run (No Discord)

```python
orchestrator = DebateOrchestrator(signal)
orchestrator.post_signal_overview()  # Test signal posting only
```

### Single Agent Test

Spawn one agent manually to test:

```bash
openclaw sessions_spawn \
    --label "test_buffett" \
    --task "You are Warren Buffett. Analyze ASTS and post to Discord #18-agents-debate..."
```

## Monitoring

### Watch Active Sessions

```bash
openclaw sessions_list
```

### View Agent Output

```bash
openclaw sessions_log <session_id>
```

### Discord Logs

All debate messages are in Discord channel history.

## Troubleshooting

### Agents Not Posting

- Check OpenClaw API token is valid
- Verify Discord channel ID is correct
- Check agent DNA cards exist and are valid JSON
- Review sub-agent logs: `openclaw sessions_log`

### Vote Parsing Fails

- Ensure agents follow exact format
- Check `VoteParser.parse_agent_post()` regex
- Manually test parser with sample posts

### Spawning Errors

- Verify OpenClaw version supports sessions_spawn
- Check system resources (18 parallel agents)
- Try smaller batch sizes or sequential spawning

## Future Enhancements

- [ ] Real-time vote tallying during debate
- [ ] Agent-to-agent direct responses (threading)
- [ ] Historical debate analytics
- [ ] ML-based consensus prediction
- [ ] Voice synthesis for agent personalities
- [ ] Web dashboard for live debate viewing
- [ ] Integration with trading execution system

## Examples

### Successful Debate Output

```
📊 SIGNAL: ASTS @ $4.20
⚡ CATALYST: FCC Approval Expected Q1 2026

🎭 18 AGENTS DEBATE RESULTS:

BUY: 8 votes (44%)
HOLD: 4 votes (22%)
SELL: 6 votes (33%)

CONSENSUS: BUY (44%)
AVG CONVICTION: 7.2/10

TOP BULL: Cathie Wood (BUY, 10/10)
TOP BEAR: Warren Buffett (SELL, 8/10)
```

## Credits

Built for Joselo's autonomous trading system.
Powered by OpenClaw multi-agent framework.

---

**The theater is ready. Let the legends debate.** 🎭
