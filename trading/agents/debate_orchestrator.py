#!/usr/bin/env python3
"""
Multi-Agent Debate Orchestrator

Spawns 18 legendary investor sub-agents to debate trading signals in Discord.
Each agent is a separate OpenClaw sub-agent that posts, reads, and responds.
"""

import json
import os
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Configuration
DISCORD_CHANNEL_ID = "1472692185106481417"  # #18-agents-debate
RESEARCH_CHANNEL_ID = "1469016715421175919"  # #research
DNA_CARDS_DIR = Path(__file__).parent / "investors"
BOT_TOKEN_FILE = Path(__file__).parent.parent.parent / ".discord-bot-token"

# The 18 Agents (in debate order)
AGENT_ORDER = [
    # Legendary Investors (12)
    "warren_buffett",
    "charlie_munger",
    "michael_burry",
    "benjamin_graham",
    "mohnish_pabrai",
    "cathie_wood",
    "phil_fisher",
    "peter_lynch",
    "bill_ackman",
    "stan_druckenmiller",
    "aswath_damodaran",
    "rakesh_jhunjhunwala",
    
    # Quant Agents (4)
    "valuation_agent",
    "sentiment_agent",
    "fundamentals_agent",
    "technicals_agent",
    
    # Special Agents (2)
    "risk_manager",
    "portfolio_manager"
]


class DebateOrchestrator:
    """Orchestrates multi-agent debate in Discord"""
    
    def __init__(self, signal_data: Dict[str, Any]):
        self.signal = signal_data
        self.agents = self.load_agent_dna()
        self.debate_messages = []
        self.agent_votes = {}
        self.debate_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_agent_dna(self) -> Dict[str, Dict]:
        """Load all agent DNA cards"""
        agents = {}
        for agent_id in AGENT_ORDER:
            dna_file = DNA_CARDS_DIR / f"{agent_id}.json"
            if not dna_file.exists():
                print(f"⚠️  Warning: DNA card not found for {agent_id}")
                continue
            
            with open(dna_file, 'r') as f:
                agents[agent_id] = json.load(f)
                
        print(f"✅ Loaded {len(agents)} agent DNA cards")
        return agents
    
    def build_agent_prompt(self, agent_id: str, round_num: int, previous_posts: List[str] = None) -> str:
        """Build the prompt for a specific agent"""
        agent = self.agents[agent_id]
        
        # Base prompt with signal information
        prompt = f"""You are {agent['display_name']} {agent['emoji']}

**Your Investment Philosophy:**
{json.dumps(agent.get('investment_philosophy', {}), indent=2)}

**Your Analysis Framework:**
{json.dumps(agent.get('analysis_framework', {}), indent=2)}

**Trading Signal to Analyze:**
Ticker: {self.signal['ticker']}
Price: ${self.signal['price']}
Catalyst: {self.signal.get('catalyst', 'General analysis')}

**Signal Details:**
{self.signal.get('description', '')}

---

**YOUR TASK:**
Post your analysis to Discord channel #18-agents-debate.

**Format your Discord post EXACTLY like this:**

{agent['emoji']} **{agent['display_name']}**

[Your 3-5 sentence analysis in your distinctive voice/style]

**Vote:** BUY / HOLD / SELL
**Conviction:** X/10
**Risk:** Low / Medium / High

---

**Instructions:**
1. Analyze the signal through YOUR unique investment lens
2. Be true to your philosophy and style
3. Post your analysis to Discord using the message tool:
   - action: send
   - target: {DISCORD_CHANNEL_ID}
   - message: [your formatted analysis]

"""

        # Add previous posts for later rounds
        if round_num > 1 and previous_posts:
            prompt += f"\n\n**Previous Posts (Read before responding):**\n"
            prompt += "\n---\n".join(previous_posts[-10:])  # Last 10 posts
            prompt += "\n\nYou may address contrarian views or add new insights."
        
        return prompt
    
    def spawn_agent(self, agent_id: str, round_num: int, previous_posts: List[str] = None) -> str:
        """Spawn a sub-agent using OpenClaw sessions_spawn"""
        prompt = self.build_agent_prompt(agent_id, round_num, previous_posts)
        
        # Build the sessions_spawn command
        cmd = f'''openclaw sessions_spawn \\
            --label "{agent_id}_round{round_num}" \\
            --task "{prompt.replace('"', '\\"')}" \\
            --background'''
        
        print(f"🚀 Spawning {agent_id} (Round {round_num})...")
        os.system(cmd)
        
        return f"spawned_{agent_id}_r{round_num}"
    
    def post_signal_overview(self):
        """Post the trading signal overview to Discord"""
        overview = f"""🎭 **18 AGENTS DEBATE: {self.signal['ticker']}**

**Signal Details:**
• Ticker: {self.signal['ticker']}
• Price: ${self.signal['price']}
• Catalyst: {self.signal.get('catalyst', 'N/A')}

**Description:**
{self.signal.get('description', '')}

---

**The 18 Legendary Investors will now debate this signal...**

**Round 1: Initial Analysis** (18 agents posting)
⏳ Stand by for agent analyses...
"""
        
        # Post to Discord using message tool
        import subprocess
        cmd = [
            'openclaw', 'message',
            '--action', 'send',
            '--target', DISCORD_CHANNEL_ID,
            '--message', overview
        ]
        
        print("📢 Posting signal overview to Discord...")
        subprocess.run(cmd)
        time.sleep(2)
    
    def fetch_recent_discord_messages(self, limit: int = 50) -> List[Dict]:
        """Fetch recent messages from the debate channel"""
        import subprocess
        
        cmd = [
            'openclaw', 'message',
            '--action', 'search',
            '--channel-id', DISCORD_CHANNEL_ID,
            '--limit', str(limit)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Parse the output (this is simplified - real implementation would parse JSON)
        # For now, return empty list - agents will use message search directly
        return []
    
    def run_debate_round(self, round_num: int, previous_posts: List[str] = None):
        """Run a single round of debate"""
        print(f"\n{'='*60}")
        print(f"🎭 ROUND {round_num}: {'Initial Analysis' if round_num == 1 else 'Response Round'}")
        print(f"{'='*60}\n")
        
        # Spawn all agents in parallel
        spawned = []
        for agent_id in AGENT_ORDER:
            if agent_id not in self.agents:
                continue
            
            spawn_id = self.spawn_agent(agent_id, round_num, previous_posts)
            spawned.append(spawn_id)
            time.sleep(0.5)  # Small delay between spawns
        
        print(f"\n✅ Spawned {len(spawned)} agents for Round {round_num}")
        print(f"⏳ Waiting 60 seconds for agents to post...")
        
        # Wait for agents to complete
        time.sleep(60)
        
        print(f"✅ Round {round_num} complete!")
    
    def tally_votes(self) -> Dict[str, Any]:
        """Tally the final votes from Discord messages"""
        print("\n📊 Tallying votes...")
        
        # This is a simplified version - real implementation would parse Discord messages
        # For now, return a template
        tally = {
            "buy_votes": 0,
            "hold_votes": 0,
            "sell_votes": 0,
            "avg_conviction": 0.0,
            "consensus": "TBD",
            "agent_votes": {}
        }
        
        print("⚠️  Vote tallying requires parsing Discord messages (TODO)")
        
        return tally
    
    def generate_conviction_report(self, tally: Dict) -> str:
        """Generate the final conviction report"""
        report = f"""# Investment Conviction Report: {self.signal['ticker']}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Debate ID:** {self.debate_id}

## Signal Overview
- **Ticker:** {self.signal['ticker']}
- **Price:** ${self.signal['price']}
- **Catalyst:** {self.signal.get('catalyst', 'N/A')}

## Vote Tally
- **BUY:** {tally['buy_votes']} votes
- **HOLD:** {tally['hold_votes']} votes
- **SELL:** {tally['sell_votes']} votes

## Consensus
**Decision:** {tally['consensus']}
**Average Conviction:** {tally['avg_conviction']}/10

## Agent Breakdown
"""
        
        for agent_id, vote_data in tally.get('agent_votes', {}).items():
            agent = self.agents.get(agent_id, {})
            report += f"\n### {agent.get('display_name', agent_id)} {agent.get('emoji', '')}\n"
            report += f"- **Vote:** {vote_data.get('vote', 'N/A')}\n"
            report += f"- **Conviction:** {vote_data.get('conviction', 'N/A')}/10\n"
            report += f"- **Risk:** {vote_data.get('risk', 'N/A')}\n"
        
        report += f"\n\n---\n**Full debate:** <discord://channels/1469016615718924349/{DISCORD_CHANNEL_ID}>\n"
        
        return report
    
    def post_final_report(self, report: str):
        """Post the final conviction report to #research"""
        import subprocess
        
        # Post to #research channel
        cmd = [
            'openclaw', 'message',
            '--action', 'send',
            '--target', RESEARCH_CHANNEL_ID,
            '--message', f"```markdown\n{report}\n```"
        ]
        
        print("📢 Posting final report to #research...")
        subprocess.run(cmd)
    
    def run_full_debate(self, rounds: int = 2):
        """Run the complete multi-round debate"""
        print(f"\n{'='*60}")
        print(f"🎭 STARTING 18-AGENT DEBATE: {self.signal['ticker']}")
        print(f"{'='*60}\n")
        
        # Step 1: Post signal overview
        self.post_signal_overview()
        time.sleep(3)
        
        # Step 2: Run debate rounds
        previous_posts = []
        for round_num in range(1, rounds + 1):
            self.run_debate_round(round_num, previous_posts)
            
            # Fetch messages for next round
            if round_num < rounds:
                print("\n⏳ Fetching messages for next round...")
                time.sleep(5)
                # previous_posts = self.fetch_recent_discord_messages()
        
        # Step 3: Wait for final posts
        print("\n⏳ Waiting 30 seconds for final posts...")
        time.sleep(30)
        
        # Step 4: Tally votes
        tally = self.tally_votes()
        
        # Step 5: Generate and post report
        report = self.generate_conviction_report(tally)
        self.post_final_report(report)
        
        print(f"\n{'='*60}")
        print(f"✅ DEBATE COMPLETE!")
        print(f"{'='*60}\n")
        
        return tally


def main():
    """Main entry point"""
    
    # Example signal: ASTS
    signal = {
        "ticker": "ASTS",
        "price": 4.20,
        "catalyst": "FCC Approval Expected Q1 2026",
        "description": """AST SpaceMobile - Space-based cellular broadband network.

**Bull Case:**
- Direct-to-device satellite connectivity (massive TAM)
- Strategic partnerships: AT&T, Vodafone, Rakuten (~2.8B subscribers)
- Technology proven with BlueBird test satellite
- FCC approval is binary catalyst

**Bear Case:**
- Pre-revenue, cash-burning
- FCC approval binary risk
- SpaceX competition (better capitalized)
- Execution risk on global constellation buildout

**Key Question:** Is FCC approval underpriced by the market?"""
    }
    
    # Create orchestrator and run debate
    orchestrator = DebateOrchestrator(signal)
    orchestrator.run_full_debate(rounds=2)


if __name__ == "__main__":
    main()
