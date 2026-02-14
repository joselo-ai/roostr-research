#!/usr/bin/env python3
"""
🐓 Agent Deliberation Engine
Runs all agents on a signal, produces consensus recommendation with full rationales.
"""

import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

# Paths
AGENTS_DIR = Path(__file__).parent
SIGNALS_DB = AGENTS_DIR.parent / "signals-database.csv"

@dataclass
class AgentVote:
    """Single agent's vote on a signal"""
    agent_id: str
    display_name: str
    conviction: float  # 0-10
    vote: str  # BUY, SELL, HOLD, PASS
    rationale: str  # First-person explanation
    key_factors: Dict[str, Any]
    concerns: List[str]

@dataclass
class RiskAssessment:
    """Risk Manager's evaluation"""
    approved: bool
    position_limit: float
    stop_loss_pct: float
    concerns: List[str]
    conditions: List[str]
    rationale: str

@dataclass
class Deliberation:
    """Complete multi-agent deliberation on a signal"""
    signal_id: str
    ticker: str
    timestamp: str
    agent_votes: List[AgentVote]
    risk_assessment: RiskAssessment
    ensemble_conviction: float
    recommendation: str  # BUY, SELL, HOLD, PASS
    position_size: float
    stop_loss: float
    premortem: str
    summary: str

class AgentPersonality:
    """Loads and represents an agent's personality"""
    
    def __init__(self, card_path: Path):
        with open(card_path) as f:
            self.card = json.load(f)
        self.agent_id = self.card['agent_id']
        self.display_name = self.card['display_name']
        self.cluster = self.card['cluster']
        self.doctrine = self.card['doctrine']
        self.rules = self.card['decision_rules']
        self.disqualifiers = self.card['disqualifiers']
        
    def evaluate(self, signal: Dict[str, Any], market_data: Optional[Dict] = None) -> AgentVote:
        """
        Evaluate a signal through this agent's lens.
        For Phase 1, this is a rule-based heuristic.
        Phase 2 will use LLM with agent personality as system prompt.
        """
        ticker = signal.get('Ticker', '')
        notes = signal.get('Notes', '')
        price = float(signal.get('Price_Entry', 0))
        
        # Phase 1: Rule-based heuristic per agent archetype
        conviction, vote, rationale, factors, concerns = self._apply_rules(
            ticker, notes, price, market_data
        )
        
        return AgentVote(
            agent_id=self.agent_id,
            display_name=self.display_name,
            conviction=conviction,
            vote=vote,
            rationale=rationale,
            key_factors=factors,
            concerns=concerns
        )
    
    def _apply_rules(self, ticker: str, notes: str, price: float, market_data: Optional[Dict]) -> tuple:
        """
        Apply agent-specific rules (Phase 1 heuristics).
        Returns: (conviction, vote, rationale, factors, concerns)
        """
        # Base template - each agent would have custom logic
        conviction = 5.0  # neutral default
        vote = "HOLD"
        factors = {}
        concerns = []
        
        # Agent-specific logic based on personality
        if self.agent_id == "buffett_quality":
            # Buffett: Look for moat indicators in notes
            moat_keywords = ["moat", "pricing power", "brand", "network effect", "switching cost"]
            moat_score = sum(1 for kw in moat_keywords if kw.lower() in notes.lower())
            
            # Check for disqualifiers
            if any(d.lower() in notes.lower() for d in ["can't explain", "complex", "leverage"]):
                conviction = 2.0
                vote = "PASS"
                rationale = "I don't understand this business well enough to invest with confidence."
                concerns.append("Business model complexity or leverage concerns")
            elif moat_score >= 2:
                conviction = 7.5
                vote = "BUY"
                rationale = f"I see evidence of a durable competitive advantage. {notes[:200]}"
                factors['moat_indicators'] = moat_score
            else:
                conviction = 4.0
                vote = "PASS"
                rationale = "I need clearer evidence of a moat before committing capital."
                concerns.append("Moat evidence insufficient")
                
        elif self.agent_id == "burry_contrarian":
            # Burry: Look for contrarian setups, downside protection
            contrarian_keywords = ["hated", "pessimism", "forced selling", "mispriced", "overlooked"]
            downside_keywords = ["asset", "cash flow", "balance sheet", "coverage"]
            
            contrarian_score = sum(1 for kw in contrarian_keywords if kw.lower() in notes.lower())
            downside_score = sum(1 for kw in downside_keywords if kw.lower() in notes.lower())
            
            if contrarian_score >= 1 and downside_score >= 1:
                conviction = 8.0
                vote = "BUY"
                rationale = f"I see asymmetric opportunity: downside protected by fundamentals, upside from mean reversion. {notes[:200]}"
                factors['contrarian_setup'] = contrarian_score
                factors['downside_protection'] = downside_score
            elif downside_score == 0:
                conviction = 2.0
                vote = "PASS"
                rationale = "I can't define my downside clearly enough. Pass."
                concerns.append("Downside not quantifiable")
            else:
                conviction = 5.0
                vote = "HOLD"
                rationale = "Setup is interesting but not asymmetric enough yet."
                
        elif self.agent_id == "risk_manager":
            # Risk Manager: Check for risk flags
            risk_flags = ["binary", "catalyst", "volatile", "illiquid", "concentrated"]
            risk_count = sum(1 for flag in risk_flags if flag.lower() in notes.lower())
            
            if risk_count >= 3:
                conviction = 0.0
                vote = "REJECT"
                rationale = "Too many risk flags. This violates risk management principles."
                concerns = ["High risk concentration", "Binary outcomes", "Volatility"]
            elif risk_count >= 1:
                conviction = 5.0
                vote = "APPROVED_WITH_CONDITIONS"
                rationale = "Approved but with reduced position sizing due to risk factors."
                concerns = [f"{risk_count} risk flags identified"]
                factors['risk_flags'] = risk_count
            else:
                conviction = 8.0
                vote = "APPROVED"
                rationale = "Risk parameters acceptable. Standard sizing approved."
        
        # Default for agents not yet implemented
        else:
            conviction = 5.0
            vote = "ABSTAIN"
            rationale = f"[{self.display_name}] Agent evaluation logic pending implementation."
            concerns.append("Agent not fully implemented yet")
        
        return conviction, vote, rationale, factors, concerns

class DeliberationEngine:
    """Runs multi-agent deliberation"""
    
    def __init__(self, agents_dir: Path = AGENTS_DIR):
        self.agents_dir = agents_dir
        self.agents: List[AgentPersonality] = []
        self.load_agents()
        
    def load_agents(self):
        """Load all agent personality cards"""
        agent_files = sorted(self.agents_dir.glob("*.json"))
        for card_path in agent_files:
            try:
                agent = AgentPersonality(card_path)
                self.agents.append(agent)
                print(f"✅ Loaded: {agent.display_name}")
            except Exception as e:
                print(f"⚠️  Failed to load {card_path.name}: {e}")
        
        print(f"\n🐓 {len(self.agents)} agents ready for deliberation\n")
    
    def deliberate(self, signal: Dict[str, Any], market_data: Optional[Dict] = None) -> Deliberation:
        """Run all agents on a signal and produce consensus"""
        
        ticker = signal.get('Ticker', 'UNKNOWN')
        print(f"🎯 Deliberating on {ticker}...")
        print("=" * 60)
        
        # Collect votes from all agents
        agent_votes = []
        for agent in self.agents:
            if agent.agent_id == 'risk_manager':
                continue  # Risk manager evaluates after others
            
            vote = agent.evaluate(signal, market_data)
            agent_votes.append(vote)
            print(f"{agent.display_name}: {vote.vote} ({vote.conviction}/10)")
        
        # Risk Manager evaluates the consensus
        risk_vote = next((a for a in self.agents if a.agent_id == 'risk_manager'), None)
        if risk_vote:
            risk_assessment_vote = risk_vote.evaluate(signal, market_data)
            risk_assessment = RiskAssessment(
                approved=(risk_assessment_vote.vote in ["APPROVED", "APPROVED_WITH_CONDITIONS"]),
                position_limit=10000.0,  # Phase 1 default
                stop_loss_pct=0.15,
                concerns=risk_assessment_vote.concerns,
                conditions=[] if risk_assessment_vote.vote == "APPROVED" else ["Reduced position size"],
                rationale=risk_assessment_vote.rationale
            )
        else:
            # Default if no risk manager
            risk_assessment = RiskAssessment(
                approved=True,
                position_limit=10000.0,
                stop_loss_pct=0.15,
                concerns=[],
                conditions=[],
                rationale="Default approval (no risk manager loaded)"
            )
        
        # Calculate ensemble conviction (weighted average of non-PASS votes)
        active_votes = [v for v in agent_votes if v.vote != "PASS"]
        if active_votes:
            ensemble_conviction = sum(v.conviction for v in active_votes) / len(active_votes)
        else:
            ensemble_conviction = 0.0
        
        # Determine recommendation
        buy_count = sum(1 for v in agent_votes if v.vote == "BUY")
        sell_count = sum(1 for v in agent_votes if v.vote == "SELL")
        
        if not risk_assessment.approved:
            recommendation = "PASS"
            position_size = 0.0
        elif buy_count > len(agent_votes) * 0.5:
            recommendation = "BUY"
            # Scale position size by conviction (8.0 = $5k, 10.0 = $10k)
            position_size = min(
                5000 + (ensemble_conviction - 8.0) * 2500,
                risk_assessment.position_limit
            )
        elif sell_count > len(agent_votes) * 0.5:
            recommendation = "SELL"
            position_size = 0.0
        else:
            recommendation = "HOLD"
            position_size = 0.0
        
        # Generate pre-mortem
        all_concerns = []
        for vote in agent_votes:
            all_concerns.extend(vote.concerns)
        premortem = " | ".join(set(all_concerns)) if all_concerns else "No major concerns identified"
        
        # Summary
        summary = f"{ticker}: {recommendation} | Conviction: {ensemble_conviction:.1f}/10 | Size: ${position_size:,.0f}"
        
        print(f"\n{'='*60}")
        print(f"📊 RESULT: {summary}")
        print(f"🚨 Pre-mortem: {premortem}")
        print(f"{'='*60}\n")
        
        return Deliberation(
            signal_id=signal.get('Ticker', 'UNKNOWN'),
            ticker=ticker,
            timestamp=datetime.now().isoformat(),
            agent_votes=agent_votes,
            risk_assessment=risk_assessment,
            ensemble_conviction=ensemble_conviction,
            recommendation=recommendation,
            position_size=position_size,
            stop_loss=float(signal.get('Price_Entry', 0)) * (1 - risk_assessment.stop_loss_pct),
            premortem=premortem,
            summary=summary
        )
    
    def format_for_telegram(self, delib: Deliberation) -> str:
        """Format deliberation for Telegram delivery"""
        lines = [
            f"🐓 **Agent Deliberation: {delib.ticker}**",
            f"",
            f"**Recommendation:** {delib.recommendation}",
            f"**Ensemble Conviction:** {delib.ensemble_conviction:.1f}/10",
            f"**Position Size:** ${delib.position_size:,.0f}",
            f"**Stop Loss:** ${delib.stop_loss:.2f} ({delib.risk_assessment.stop_loss_pct:.0%})",
            f"",
            f"**🎭 Agent Votes:**"
        ]
        
        for vote in delib.agent_votes:
            emoji = "✅" if vote.vote == "BUY" else "🚫" if vote.vote == "SELL" else "⏸️"
            lines.append(f"{emoji} **{vote.display_name}:** {vote.vote} ({vote.conviction:.1f}/10)")
            lines.append(f"   _{vote.rationale[:150]}..._")
            lines.append("")
        
        lines.append(f"**⚠️ Pre-mortem:** {delib.premortem}")
        lines.append("")
        lines.append(f"**Risk Manager:** {'✅ APPROVED' if delib.risk_assessment.approved else '🚫 REJECTED'}")
        if delib.risk_assessment.concerns:
            lines.append(f"   Concerns: {', '.join(delib.risk_assessment.concerns)}")
        
        return "\n".join(lines)

def main():
    """Test deliberation on existing signals"""
    import csv
    
    engine = DeliberationEngine()
    
    # Load GREEN signals
    signals = []
    with open(SIGNALS_DB) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Status') == 'GREEN':
                signals.append(row)
    
    print(f"Found {len(signals)} GREEN signals\n")
    
    # Deliberate on first signal as test
    if signals:
        test_signal = signals[0]
        delib = engine.deliberate(test_signal)
        
        print("\n📱 TELEGRAM FORMAT:")
        print(engine.format_for_telegram(delib))

if __name__ == "__main__":
    main()
