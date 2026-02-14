# 18-Agent Investment Ensemble

## Overview

18 AI agents with distinct investment philosophies deliberate on every signal:
- 12 Legendary Investors (Buffett, Munger, Burry, Graham, Pabrai, Cathie Wood, Fisher, Lynch, Ackman, Druckenmiller, Damodaran, Jhunjhunwala)
- 4 Quant Agents (Valuation, Sentiment, Fundamentals, Technicals)
- 1 Risk Manager (gatekeeper)
- 1 Portfolio Synthesizer (final decision)

## How It Works

1. **Signal appears** (ASTS, TAO, etc.)
2. **All agents analyze** using their frameworks
3. **Each votes** with conviction (0-10) + first-person rationale
4. **Risk Manager** challenges assumptions, flags risks
5. **Synthesizer** produces weighted recommendation
6. **Output:** Trade proposal with full deliberation for human review

## Agent Files

Each agent has:
- `{agent_id}.json` - Personality card (doctrine, rules, triggers, disqualifiers)
- First-person voice
- Distinct decision framework
- Falsification conditions

## Deliberation Engine

`deliberate.py` - Runs all agents on a signal, produces consensus recommendation

## Output Format

```json
{
  "signal": "ASTS",
  "ensemble_conviction": 7.8,
  "recommendation": "BUY",
  "position_size": "$8,500",
  "agent_votes": [
    {
      "agent": "buffett_quality",
      "conviction": 3.0,
      "vote": "PASS",
      "rationale": "I don't understand satellite-to-cell economics well enough..."
    },
    {
      "agent": "burry_contrarian",
      "conviction": 8.5,
      "vote": "BUY",
      "rationale": "Market is underpricing FCC approval catalyst..."
    }
  ],
  "risk_manager_assessment": {
    "approved": true,
    "concerns": ["Binary catalyst risk", "High volatility"],
    "position_limit": "$10,000"
  },
  "premortem": "If FCC denies approval or delays indefinitely, thesis breaks completely."
}
```

## Status

- [ ] Agent personality cards (18)
- [ ] Deliberation engine
- [ ] Data feed integration
- [ ] Output formatter
- [ ] Test on existing signals
