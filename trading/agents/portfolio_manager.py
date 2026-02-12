#!/usr/bin/env python3
"""
Portfolio Manager - Synthesizes All Agent Opinions
===================================================

Takes input from 12 Legendary Investors + 4 Quant Agents + Risk Manager (Joselo),
generates final conviction document and trading decision.

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

from typing import Dict, List
import json
from datetime import datetime
from legendary_investors import run_investor_debate, LEGENDARY_INVESTORS
from quant_agents import run_quant_analysis, QUANT_AGENTS

class PortfolioManager:
    """
    Synthesizes all 18 agent opinions into final trading decision.
    
    Workflow:
    1. Run 12 Legendary Investors → get avg conviction + consensus
    2. Run 4 Quant Agents → get avg score + consensus
    3. Combine → weighted final conviction
    4. Risk Manager validates → adjust conviction if needed
    5. Generate conviction document
    6. Make final decision: BUY/SELL/HOLD
    """
    
    def __init__(self, risk_manager=None):
        self.risk_manager = risk_manager
        self.legendary_weight = 0.6  # 60% weight to legendary investors
        self.quant_weight = 0.4      # 40% weight to quant agents
    
    def evaluate_signal(self, signal: Dict) -> Dict:
        """
        Full 18-agent evaluation pipeline.
        
        Args:
            signal: Dict with ticker, price, catalyst, source, etc.
            
        Returns:
            Complete conviction document with final decision
        """
        ticker = signal.get('ticker', 'Unknown')
        
        print(f"\n🐓 Evaluating {ticker} with 18-agent system...")
        print("=" * 60)
        
        # Step 1: Legendary Investors (12 agents)
        print("\n📊 Step 1: Legendary Investor Debate...")
        legendary_result = run_investor_debate(signal)
        legendary_conviction = legendary_result['avg_conviction']
        legendary_consensus = legendary_result['consensus']
        
        print(f"   Legendary Consensus: {legendary_consensus}")
        print(f"   Avg Conviction: {legendary_conviction}/10")
        print(f"   Votes: {legendary_result['votes']}")
        
        # Step 2: Quant Agents (4 agents)
        print("\n📈 Step 2: Quantitative Analysis...")
        quant_result = run_quant_analysis(signal)
        quant_score = quant_result['avg_score']
        quant_consensus = quant_result['consensus']
        
        print(f"   Quant Consensus: {quant_consensus}")
        print(f"   Avg Score: {quant_score}/10")
        print(f"   Votes: {quant_result['votes']}")
        
        # Step 3: Combine weighted conviction
        print("\n🎯 Step 3: Combining signals...")
        combined_conviction = (
            legendary_conviction * self.legendary_weight +
            quant_score * self.quant_weight
        )
        combined_conviction = round(combined_conviction, 2)
        
        print(f"   Combined Conviction: {combined_conviction}/10")
        print(f"   ({legendary_conviction} * {self.legendary_weight} + {quant_score} * {self.quant_weight})")
        
        # Step 4: Risk Manager validation
        print("\n⚠️  Step 4: Risk Manager Review...")
        risk_validated_conviction = combined_conviction
        risk_concerns = []
        
        if self.risk_manager:
            risk_result = self.risk_manager.validate(signal, combined_conviction)
            risk_validated_conviction = risk_result['adjusted_conviction']
            risk_concerns = risk_result['concerns']
            
            if risk_concerns:
                print(f"   Risk Concerns: {', '.join(risk_concerns)}")
                print(f"   Adjusted Conviction: {risk_validated_conviction}/10")
            else:
                print(f"   ✅ No risk concerns, conviction unchanged")
        else:
            print(f"   ⚠️  No Risk Manager configured")
        
        # Step 5: Final decision
        print("\n🎲 Step 5: Final Decision...")
        final_decision = self._make_decision(
            risk_validated_conviction,
            legendary_consensus,
            quant_consensus
        )
        
        print(f"   Final Decision: {final_decision}")
        print(f"   Final Conviction: {risk_validated_conviction}/10")
        
        # Step 6: Generate conviction document
        conviction_doc = self._generate_conviction_document(
            signal=signal,
            legendary_result=legendary_result,
            quant_result=quant_result,
            combined_conviction=combined_conviction,
            risk_validated_conviction=risk_validated_conviction,
            risk_concerns=risk_concerns,
            final_decision=final_decision
        )
        
        return conviction_doc
    
    def _make_decision(self, conviction: float, legendary_consensus: str, quant_consensus: str) -> str:
        """
        Make final BUY/SELL/HOLD decision based on conviction + consensus.
        
        Logic:
        - Conviction >= 7.5 + both consensus BUY → BUY
        - Conviction >= 7.0 + majority BUY → BUY
        - Conviction <= 3.5 + both consensus SELL → SELL
        - Conviction <= 4.0 + majority SELL → SELL
        - Otherwise → HOLD
        """
        both_buy = legendary_consensus == "BUY" and quant_consensus == "BUY"
        both_sell = legendary_consensus == "SELL" and quant_consensus == "SELL"
        majority_buy = (legendary_consensus == "BUY" or quant_consensus == "BUY")
        majority_sell = (legendary_consensus == "SELL" or quant_consensus == "SELL")
        
        if conviction >= 7.5 and both_buy:
            return "BUY"
        elif conviction >= 7.0 and majority_buy:
            return "BUY"
        elif conviction <= 3.5 and both_sell:
            return "SELL"
        elif conviction <= 4.0 and majority_sell:
            return "SELL"
        else:
            return "HOLD"
    
    def _generate_conviction_document(
        self,
        signal: Dict,
        legendary_result: Dict,
        quant_result: Dict,
        combined_conviction: float,
        risk_validated_conviction: float,
        risk_concerns: List[str],
        final_decision: str
    ) -> Dict:
        """
        Generate full conviction document for transparency.
        
        This document is published to GitHub + tweeted for full transparency.
        """
        ticker = signal.get('ticker', 'Unknown')
        
        doc = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "signal_source": signal.get('source', 'Unknown'),
            "catalyst": signal.get('catalyst', ''),
            "entry_price": signal.get('price', 0),
            
            # Agent opinions
            "legendary_investors": {
                "consensus": legendary_result['consensus'],
                "avg_conviction": legendary_result['avg_conviction'],
                "votes": legendary_result['votes'],
                "individual_opinions": legendary_result['opinions']
            },
            
            "quant_agents": {
                "consensus": quant_result['consensus'],
                "avg_score": quant_result['avg_score'],
                "votes": quant_result['votes'],
                "individual_opinions": quant_result['opinions']
            },
            
            # Combined analysis
            "combined_conviction": combined_conviction,
            "risk_validated_conviction": risk_validated_conviction,
            "risk_concerns": risk_concerns,
            
            # Final decision
            "final_decision": final_decision,
            "conviction_rating": self._get_conviction_rating(risk_validated_conviction),
            
            # Reasoning summary
            "reasoning": self._generate_reasoning_summary(
                legendary_result,
                quant_result,
                risk_validated_conviction,
                final_decision
            ),
            
            # Position sizing (if BUY)
            "position_sizing": self._calculate_position_sizing(
                signal,
                risk_validated_conviction,
                final_decision
            ) if final_decision == "BUY" else None
        }
        
        return doc
    
    def _get_conviction_rating(self, conviction: float) -> str:
        """Convert numerical conviction to rating"""
        if conviction >= 9:
            return "🟢 VERY HIGH"
        elif conviction >= 7:
            return "🟢 HIGH"
        elif conviction >= 5:
            return "🟡 MEDIUM"
        elif conviction >= 3:
            return "🟠 LOW"
        else:
            return "🔴 VERY LOW"
    
    def _generate_reasoning_summary(
        self,
        legendary_result: Dict,
        quant_result: Dict,
        conviction: float,
        decision: str
    ) -> str:
        """Generate human-readable reasoning summary"""
        
        # Count strong supporters
        strong_bulls = sum(1 for op in legendary_result['opinions'] if op['conviction'] >= 7)
        strong_bears = sum(1 for op in legendary_result['opinions'] if op['conviction'] <= 3)
        
        quant_bulls = sum(1 for op in quant_result['opinions'] if op['score'] >= 7)
        quant_bears = sum(1 for op in quant_result['opinions'] if op['score'] <= 3)
        
        summary = f"**Decision: {decision}** (Conviction: {conviction}/10)\n\n"
        
        summary += f"**Legendary Investors:** {strong_bulls}/12 bullish, {strong_bears}/12 bearish. "
        summary += f"Consensus: {legendary_result['consensus']}.\n\n"
        
        summary += f"**Quant Agents:** {quant_bulls}/4 bullish, {quant_bears}/4 bearish. "
        summary += f"Consensus: {quant_result['consensus']}.\n\n"
        
        if decision == "BUY":
            summary += "**Rationale:** Multi-agent consensus supports deployment. "
            summary += "Risk/reward favorable. Position sizing follows conviction.\n"
        elif decision == "SELL":
            summary += "**Rationale:** Multi-agent consensus advises against. "
            summary += "Risk/reward unfavorable or better opportunities exist.\n"
        else:
            summary += "**Rationale:** Mixed signals. Waiting for clearer setup. "
            summary += "Will reassess when conviction improves.\n"
        
        return summary
    
    def _calculate_position_sizing(
        self,
        signal: Dict,
        conviction: float,
        decision: str
    ) -> Dict:
        """
        Calculate position size based on conviction.
        
        Logic:
        - 10/10 conviction = 20% of portfolio
        - 9/10 = 15%
        - 7.5/10 = 10%
        - <7/10 = No deployment
        """
        if decision != "BUY" or conviction < 7.0:
            return None
        
        # Conviction-based allocation
        if conviction >= 9.5:
            pct_allocation = 0.20  # 20%
        elif conviction >= 9.0:
            pct_allocation = 0.15  # 15%
        elif conviction >= 7.5:
            pct_allocation = 0.10  # 10%
        else:
            pct_allocation = 0.05  # 5%
        
        # Calculate $ amounts (assuming $1M portfolio)
        portfolio_value = 1_000_000  # $1M paper trading
        position_size = portfolio_value * pct_allocation
        
        # Risk management
        stop_loss_pct = 0.10  # -10% stop
        risk_per_trade = position_size * stop_loss_pct
        
        return {
            "conviction": conviction,
            "pct_allocation": f"{pct_allocation * 100}%",
            "position_size": f"${position_size:,.0f}",
            "stop_loss": f"-{stop_loss_pct * 100}%",
            "max_risk": f"${risk_per_trade:,.0f}",
            "entry_price": signal.get('price', 0),
            "stop_price": round(signal.get('price', 0) * (1 - stop_loss_pct), 2)
        }


class RiskManager:
    """
    Risk Manager (Joselo 🐓) validates all decisions.
    
    Enforces stops, position sizing, portfolio risk limits.
    """
    
    def __init__(self, max_position_pct=0.20, max_portfolio_risk=0.038):
        self.max_position_pct = max_position_pct  # 20% max per position
        self.max_portfolio_risk = max_portfolio_risk  # 3.8% max portfolio loss
    
    def validate(self, signal: Dict, conviction: float) -> Dict:
        """
        Validate trade from risk perspective.
        
        Returns adjusted conviction + concerns.
        """
        concerns = []
        adjusted_conviction = conviction
        
        # Check 1: Is conviction high enough to deploy?
        if conviction < 7.0:
            concerns.append("Conviction <7.0, too low to deploy capital")
            adjusted_conviction = min(conviction, 5.0)
        
        # Check 2: Asset class risk
        asset_class = signal.get('asset_class', '')
        if asset_class == 'crypto' and conviction < 8.0:
            concerns.append("Crypto requires higher conviction (>=8.0)")
            adjusted_conviction -= 1.0
        
        # Check 3: Catalyst clarity
        catalyst = signal.get('catalyst', '')
        if not catalyst or len(catalyst) < 30:
            concerns.append("Weak catalyst, insufficient clarity")
            adjusted_conviction -= 0.5
        
        # Check 4: Stop loss defined?
        if 'stop' not in catalyst.lower():
            concerns.append("No stop loss mentioned")
        
        # Ensure conviction doesn't go negative
        adjusted_conviction = max(0, adjusted_conviction)
        
        return {
            "adjusted_conviction": round(adjusted_conviction, 2),
            "concerns": concerns,
            "approved": len(concerns) == 0
        }


if __name__ == "__main__":
    # Test full pipeline
    test_signal = {
        "ticker": "TAO",
        "price": 176.05,
        "catalyst": "AI + blockchain intersection, Yieldschool conviction 8.5/10, strong fundamentals, oversold RSI",
        "source": "Yieldschool",
        "asset_class": "crypto",
        "conviction": 8.5
    }
    
    # Initialize
    risk_manager = RiskManager()
    portfolio_manager = PortfolioManager(risk_manager=risk_manager)
    
    # Run full evaluation
    conviction_doc = portfolio_manager.evaluate_signal(test_signal)
    
    # Print results
    print("\n" + "=" * 60)
    print("🐓 FINAL CONVICTION DOCUMENT")
    print("=" * 60)
    print(json.dumps(conviction_doc, indent=2, default=str))
