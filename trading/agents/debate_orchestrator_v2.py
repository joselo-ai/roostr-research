#!/usr/bin/env python3
"""
Enhanced Multi-Agent Debate Orchestrator with Dexter Integration

Flow:
1. Signal arrives → Trigger Dexter research (2-3 min deep dive)
2. Post Dexter summary to #research channel
3. Spawn 18 agents WITH Dexter's institutional-grade data
4. Agents debate, citing Dexter's findings
5. Final conviction doc includes Dexter research link
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add trading/apps to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "apps"))

from dexter_research import DexterResearchEngine

# Configuration
DISCORD_CHANNEL_ID = "1472692185106481417"  # #18-agents-debate
RESEARCH_CHANNEL_ID = "1469016715421175919"  # #research
DNA_CARDS_DIR = Path(__file__).parent / "investors"

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


class EnhancedDebateOrchestrator:
    """
    Orchestrates multi-agent debate with Dexter research integration.
    
    Dexter provides institutional-grade financial data that all agents
    can reference in their analysis.
    """
    
    def __init__(self, signal_data: Dict[str, Any], use_dexter: bool = True):
        self.signal = signal_data
        self.use_dexter = use_dexter
        self.agents = self.load_agent_dna()
        self.debate_messages = []
        self.agent_votes = {}
        self.debate_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.dexter_research = None
        self.dexter_engine = DexterResearchEngine() if use_dexter else None
        
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
    
    def run_dexter_research(self) -> Optional[Dict[str, Any]]:
        """
        Phase 1: Run Dexter deep research on the signal.
        
        Returns comprehensive financial analysis that agents will reference.
        """
        if not self.use_dexter:
            print("⚠️  Dexter research disabled")
            return None
        
        print("\n" + "="*60)
        print("🔬 PHASE 1: DEXTER DEEP RESEARCH")
        print("="*60)
        
        ticker = self.signal['ticker']
        catalyst = self.signal.get('catalyst', '')
        
        # Build focused research query based on catalyst
        focus_areas = ['fundamentals', 'valuation', 'risks', 'catalysts']
        
        # Add specific focus based on catalyst keywords
        if 'fcc' in catalyst.lower() or 'approval' in catalyst.lower():
            focus_areas.append('regulatory')
        if 'earnings' in catalyst.lower():
            focus_areas.append('earnings_quality')
        if 'acquisition' in catalyst.lower() or 'merger' in catalyst.lower():
            focus_areas.append('M&A')
        
        # Custom query
        query = f"""Analyze {ticker}: {catalyst}

Provide institutional-grade analysis:
1. **Fundamentals**: Revenue/earnings growth (5yr), margins, ROIC, FCF
2. **Financial Health**: Balance sheet (debt/equity), cash position
3. **Valuation**: P/E, P/FCF vs peers and historical; DCF if possible
4. **Competitive Moat**: Sustainable advantages vs competitors
5. **Catalyst Analysis**: How significant is this catalyst? Historical precedents?
6. **Risks**: What could derail this thesis?
7. **Investment Recommendation**: BUY/HOLD/SELL with conviction (0-10)

Be data-driven. Cite specific financial metrics.
"""
        
        try:
            research = self.dexter_engine.research_ticker(
                ticker=ticker,
                question=query
            )
            
            # Save research to file
            research_file = self.dexter_engine.save_research(research)
            research['research_file'] = str(research_file)
            
            self.dexter_research = research
            
            print(f"\n✅ Dexter research complete!")
            print(f"   Recommendation: {research['recommendation']}")
            print(f"   Conviction: {research['conviction']}/10")
            print(f"   Research saved: {research_file.name}")
            
            return research
            
        except Exception as e:
            print(f"⚠️  Dexter research failed: {e}")
            print("   Continuing without Dexter data...")
            return None
    
    def post_dexter_summary(self):
        """
        Phase 2: Post Dexter research summary to #research channel.
        
        This gives visibility into the institutional-grade data
        that agents will reference.
        """
        if not self.dexter_research:
            return
        
        print("\n📢 Posting Dexter research to #research...")
        
        research = self.dexter_research
        
        # Build summary message
        summary = f"""🔬 **DEXTER RESEARCH: {research['ticker']}**

**Recommendation:** {research['recommendation']}
**Conviction:** {research['conviction']}/10
**Research Time:** {research.get('research_time', 0):.1f}s

**Summary:**
{research['summary'][:500]}...

**Key Financials:**
{self._format_financials(research.get('financials', {}))}

**Valuation:**
{self._format_valuation(research.get('valuation', {}))}

**Identified Risks:**
{self._format_list(research.get('risks', []))}

**Upcoming Catalysts:**
{self._format_list(research.get('catalysts', []))}

---
📊 **Full Report:** `{research.get('research_file', 'N/A')}`
⏰ **Generated:** {research.get('timestamp', 'N/A')}

*This data will be provided to the 18-agent ensemble for debate.*
"""
        
        # Post to Discord
        self._post_to_discord(RESEARCH_CHANNEL_ID, summary)
        
        time.sleep(2)
    
    def _format_financials(self, financials: Dict) -> str:
        """Format financial data for Discord"""
        if not financials:
            return "• (Processing financial data...)"
        
        lines = []
        for key, value in financials.items():
            lines.append(f"• {key}: {value}")
        
        return "\n".join(lines) if lines else "• (Data being analyzed)"
    
    def _format_valuation(self, valuation: Dict) -> str:
        """Format valuation data for Discord"""
        if not valuation:
            return "• (Processing valuation data...)"
        
        lines = []
        for key, value in valuation.items():
            lines.append(f"• {key}: {value}")
        
        return "\n".join(lines) if lines else "• (Data being analyzed)"
    
    def _format_list(self, items: List) -> str:
        """Format a list for Discord"""
        if not items:
            return "• None identified"
        
        return "\n".join(f"• {item}" for item in items[:5])  # Max 5 items
    
    def build_agent_prompt_with_dexter(
        self, 
        agent_id: str, 
        round_num: int,
        previous_posts: List[str] = None
    ) -> str:
        """
        Build agent prompt WITH Dexter's institutional-grade data.
        
        This is the key integration: agents now have access to real
        financial data, not just the catalyst text.
        """
        agent = self.agents[agent_id]
        
        # Base prompt
        prompt = f"""You are {agent['display_name']} {agent['emoji']}

**Your Investment Philosophy:**
{json.dumps(agent.get('investment_philosophy', {}), indent=2)}

**Your Analysis Framework:**
{json.dumps(agent.get('analysis_framework', {}), indent=2)}

---

**TRADING SIGNAL TO ANALYZE:**
Ticker: {self.signal['ticker']}
Price: ${self.signal['price']}
Catalyst: {self.signal.get('catalyst', 'General analysis')}

**Signal Description:**
{self.signal.get('description', '')}

"""

        # ADD DEXTER'S INSTITUTIONAL-GRADE DATA
        if self.dexter_research:
            prompt += f"""
---

**🔬 DEXTER RESEARCH DATA (Institutional-Grade)**

**Dexter's Recommendation:** {self.dexter_research['recommendation']}
**Dexter's Conviction:** {self.dexter_research['conviction']}/10

**Executive Summary:**
{self.dexter_research['summary'][:800]}

**Key Financials:**
{json.dumps(self.dexter_research.get('financials', {}), indent=2)}

**Valuation Analysis:**
{json.dumps(self.dexter_research.get('valuation', {}), indent=2)}

**Identified Risks:**
{json.dumps(self.dexter_research.get('risks', []), indent=2)}

**Upcoming Catalysts:**
{json.dumps(self.dexter_research.get('catalysts', []), indent=2)}

**Full Research Notes:**
{self.dexter_research.get('research_notes', '')[:1500]}

---

**IMPORTANT:** You now have access to REAL financial data (income statements, 
balance sheets, valuations). Use this institutional-grade data in your analysis.
Cite specific metrics when making your case.

If Dexter's data contradicts your initial impression, explain why.
"""

        # Task instructions
        prompt += f"""
---

**YOUR TASK:**
Analyze this signal through YOUR unique investment lens, using Dexter's data.

**Post Format (Discord #18-agents-debate):**

{agent['emoji']} **{agent['display_name']}**

[Your 3-5 sentence analysis in your distinctive voice/style]

**Key Data Points I'm Using:**
• [Cite specific financial metrics from Dexter]
• [Cite valuation data]

**Vote:** BUY / HOLD / SELL
**Conviction:** X/10
**Risk:** Low / Medium / High

---

**Instructions:**
1. Analyze using BOTH your philosophy AND Dexter's real data
2. Cite specific financial metrics (revenue growth, margins, P/E, etc.)
3. If you disagree with Dexter, explain why
4. Post to Discord #18-agents-debate

Use the message tool:
- action: send
- target: {DISCORD_CHANNEL_ID}
- message: [your formatted analysis]
"""

        # Add previous posts for later rounds
        if round_num > 1 and previous_posts:
            prompt += f"\n\n**Previous Debate Posts:**\n"
            prompt += "\n---\n".join(previous_posts[-10:])
            prompt += "\n\nAddress contrarian views or add new insights."
        
        return prompt
    
    def spawn_agent_with_dexter_data(
        self, 
        agent_id: str, 
        round_num: int,
        previous_posts: List[str] = None
    ) -> str:
        """Spawn agent with Dexter data included in prompt"""
        
        prompt = self.build_agent_prompt_with_dexter(
            agent_id, 
            round_num, 
            previous_posts
        )
        
        # Escape quotes for shell
        escaped_prompt = prompt.replace('"', '\\"').replace('\n', '\\n')
        
        # Build spawn command
        cmd = f'''openclaw sessions_spawn \\
            --label "{agent_id}_r{round_num}_{self.debate_id}" \\
            --task "{escaped_prompt}" \\
            --background'''
        
        print(f"🚀 Spawning {agent_id} (Round {round_num}) with Dexter data...")
        os.system(cmd)
        
        return f"spawned_{agent_id}_r{round_num}"
    
    def post_signal_overview(self):
        """Post the signal overview to Discord with Dexter integration note"""
        
        dexter_note = ""
        if self.dexter_research:
            dexter_note = f"""
**🔬 Dexter Research Complete:**
• Recommendation: {self.dexter_research['recommendation']}
• Conviction: {self.dexter_research['conviction']}/10
• Full report posted to #research
"""
        
        overview = f"""🎭 **18 AGENTS DEBATE: {self.signal['ticker']}**

**Signal Details:**
• Ticker: {self.signal['ticker']}
• Price: ${self.signal['price']}
• Catalyst: {self.signal.get('catalyst', 'N/A')}

**Description:**
{self.signal.get('description', '')}

{dexter_note}

---

**The 18 Legendary Investors will now debate this signal...**
*Each agent has access to Dexter's institutional-grade financial data.*

**Round 1: Initial Analysis** (18 agents posting)
⏳ Stand by for agent analyses...
"""
        
        self._post_to_discord(DISCORD_CHANNEL_ID, overview)
        time.sleep(2)
    
    def _post_to_discord(self, channel_id: str, message: str):
        """Post message to Discord channel"""
        import subprocess
        
        cmd = [
            'openclaw', 'message',
            '--action', 'send',
            '--target', channel_id,
            '--message', message
        ]
        
        subprocess.run(cmd)
    
    def run_debate_round(self, round_num: int, previous_posts: List[str] = None):
        """Run a debate round with Dexter data"""
        
        print(f"\n{'='*60}")
        print(f"🎭 ROUND {round_num}: {'Initial Analysis' if round_num == 1 else 'Response Round'}")
        print(f"{'='*60}\n")
        
        # Spawn all agents with Dexter data
        spawned = []
        for agent_id in AGENT_ORDER:
            if agent_id not in self.agents:
                continue
            
            spawn_id = self.spawn_agent_with_dexter_data(
                agent_id, 
                round_num, 
                previous_posts
            )
            spawned.append(spawn_id)
            time.sleep(0.5)
        
        print(f"\n✅ Spawned {len(spawned)} agents for Round {round_num}")
        print(f"⏳ Waiting 60 seconds for agents to analyze and post...")
        
        time.sleep(60)
        
        print(f"✅ Round {round_num} complete!")
    
    def run_full_debate_with_dexter(self, rounds: int = 2):
        """
        Run complete debate flow with Dexter integration:
        
        1. Run Dexter research (2-3 min)
        2. Post Dexter summary to #research
        3. Post signal overview to #18-agents-debate
        4. Spawn 18 agents WITH Dexter data
        5. Agents debate, citing Dexter's findings
        6. Generate final conviction report with Dexter link
        """
        
        print(f"\n{'='*60}")
        print(f"🔬 DEXTER-ENHANCED 18-AGENT DEBATE: {self.signal['ticker']}")
        print(f"{'='*60}\n")
        
        # PHASE 1: Dexter Research
        self.run_dexter_research()
        
        # PHASE 2: Post Dexter Summary
        if self.dexter_research:
            self.post_dexter_summary()
        
        # PHASE 3: Post Signal Overview
        self.post_signal_overview()
        time.sleep(3)
        
        # PHASE 4: Run Multi-Round Debate
        previous_posts = []
        for round_num in range(1, rounds + 1):
            self.run_debate_round(round_num, previous_posts)
            
            if round_num < rounds:
                print("\n⏳ Waiting for next round...")
                time.sleep(10)
        
        # PHASE 5: Final Report
        print("\n⏳ Waiting 30 seconds for final posts...")
        time.sleep(30)
        
        print(f"\n{'='*60}")
        print(f"✅ DEXTER-ENHANCED DEBATE COMPLETE!")
        print(f"{'='*60}\n")
        
        if self.dexter_research:
            print(f"📊 Dexter Research: {self.dexter_research.get('research_file')}")
        print(f"💬 Debate Channel: #18-agents-debate")
        print(f"📈 Research Channel: #research")
        

def main():
    """Main entry point - Test with ASTS"""
    
    # ASTS Signal (as specified in the task)
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

**Key Question:** Is FCC approval underpriced by the market?

**Competitive Analysis Needed:**
- ASTS vs SpaceX Starlink (direct-to-phone)
- Technology moat assessment
- Capital requirements vs runway"""
    }
    
    # Run Dexter-enhanced debate
    orchestrator = EnhancedDebateOrchestrator(signal, use_dexter=True)
    orchestrator.run_full_debate_with_dexter(rounds=2)
    
    print("\n✅ Integration test complete!")
    print("\n📋 Next Steps:")
    print("1. Check #research for Dexter's analysis")
    print("2. Check #18-agents-debate for agent deliberation")
    print("3. Review conviction docs for final recommendation")


if __name__ == "__main__":
    main()
