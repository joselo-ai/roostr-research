#!/usr/bin/env python3
"""
Legendary Investor Agents - 12 Investment Philosophies
=======================================================

Each agent embodies a legendary investor's philosophy and evaluates trades
through that lens. They debate, score conviction, and generate reasoning.

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class InvestorOpinion:
    """Single investor's evaluation of a trade"""
    investor_name: str
    conviction: float  # 0-10 scale
    vote: str  # BUY, SELL, HOLD
    reasoning: str
    concerns: List[str]
    strengths: List[str]

class LegendaryInvestor:
    """Base class for legendary investor agents"""
    
    def __init__(self, name: str, philosophy: str, focus_areas: List[str]):
        self.name = name
        self.philosophy = philosophy
        self.focus_areas = focus_areas
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        """
        Evaluate a trade signal through this investor's lens.
        
        Args:
            signal: Dict with ticker, price, catalyst, fundamentals, etc.
            
        Returns:
            InvestorOpinion with conviction score, vote, reasoning
        """
        raise NotImplementedError("Each investor must implement evaluate()")
    
    def _calculate_conviction(self, strengths: List[str], concerns: List[str]) -> float:
        """Calculate conviction score based on strengths vs concerns"""
        # Recalibrated 2026-02-20: Start lower, wider range
        conviction = 3.0
        conviction += len(strengths) * 1.5  # More weight to strengths
        conviction -= len(concerns) * 1.2   # More penalty for concerns
        return max(0.0, min(10.0, conviction))


class WarrenBuffett(LegendaryInvestor):
    """Wonderful companies at fair prices"""
    
    def __init__(self):
        super().__init__(
            name="Warren Buffett",
            philosophy="Buy wonderful companies at fair prices. Long-term moat, strong management, consistent earnings.",
            focus_areas=["economic moat", "management quality", "consistent earnings", "reasonable valuation"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        price = signal.get('price', 0)
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        # Look for moat indicators
        if any(word in catalyst.lower() for word in ['brand', 'moat', 'competitive advantage', 'market leader']):
            strengths.append("Strong competitive moat")
        
        # Consistent earnings
        if 'consistent' in catalyst.lower() or 'steady' in catalyst.lower():
            strengths.append("Consistent earnings growth")
        
        # Management quality
        if 'management' in catalyst.lower() or 'ceo' in catalyst.lower():
            strengths.append("Quality management team")
        
        # Concerns
        if 'speculation' in catalyst.lower() or 'hype' in catalyst.lower():
            concerns.append("Appears speculative, not value-driven")
        
        if 'crypto' in ticker.lower() or signal.get('asset_class') == 'crypto':
            concerns.append("Cryptocurrency lacks intrinsic value")
        
        if not catalyst:
            concerns.append("No clear catalyst for investment")
        
        conviction = self._calculate_conviction(strengths, concerns)
        
        # Vote logic
        if conviction >= 5:
            vote = "BUY"
        elif conviction <= 3:
            vote = "SELL"
        else:
            vote = "HOLD"
        
        reasoning = f"Warren Buffett evaluates {ticker}: "
        if strengths:
            reasoning += f"Strengths include {', '.join(strengths)}. "
        if concerns:
            reasoning += f"However, concerns about {', '.join(concerns)}. "
        reasoning += f"Overall conviction: {conviction}/10."
        
        return InvestorOpinion(
            investor_name=self.name,
            conviction=conviction,
            vote=vote,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )


class CharlieMunger(LegendaryInvestor):
    """Wonderful businesses at fair prices, multidisciplinary thinking"""
    
    def __init__(self):
        super().__init__(
            name="Charlie Munger",
            philosophy="Seek wonderful businesses. Avoid stupidity more than seek brilliance. Multidisciplinary mental models.",
            focus_areas=["business quality", "mental models", "avoiding mistakes", "patience"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        # Business quality
        if any(word in catalyst.lower() for word in ['profitable', 'cash flow', 'sustainable']):
            strengths.append("Strong business fundamentals")
        
        # Avoiding stupidity
        if any(word in catalyst.lower() for word in ['fomo', 'pump', 'meme', 'moon']):
            concerns.append("Smells like crowd stupidity")
        
        # Patient capital
        if 'long-term' in catalyst.lower():
            strengths.append("Long-term value creation story")
        
        if 'quick' in catalyst.lower() or 'fast' in catalyst.lower():
            concerns.append("Seeking quick gains, not patient capital")
        
        conviction = self._calculate_conviction(strengths, concerns)
        
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Charlie Munger on {ticker}: Mental models suggest "
        reasoning += f"{'strong fundamentals' if len(strengths) > len(concerns) else 'red flags'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(
            investor_name=self.name,
            conviction=conviction,
            vote=vote,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )


class MichaelBurry(LegendaryInvestor):
    """Big Short contrarian, deep value, distressed situations"""
    
    def __init__(self):
        super().__init__(
            name="Michael Burry",
            philosophy="Big Short contrarian. Deep value in distressed situations. Go against the crowd when math supports it.",
            focus_areas=["contrarian opportunities", "distressed value", "market inefficiencies", "deep research"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        source = signal.get('source', '')
        
        strengths = []
        concerns = []
        
        # Contrarian indicators
        if any(word in catalyst.lower() for word in ['undervalued', 'oversold', 'contrarian', 'distressed']):
            strengths.append("Contrarian opportunity")
        
        # Deep research
        if 'fundamental' in catalyst.lower() or 'research' in catalyst.lower():
            strengths.append("Backed by deep research")
        
        # Market inefficiency
        if 'mispriced' in catalyst.lower() or 'overlooked' in catalyst.lower():
            strengths.append("Market inefficiency exploit")
        
        # Concerns
        if 'momentum' in catalyst.lower() or 'trending' in catalyst.lower():
            concerns.append("Following the herd, not contrarian")
        
        if 'reddit' in source.lower() and 'viral' in catalyst.lower():
            concerns.append("Social media hype, not deep value")
        
        conviction = self._calculate_conviction(strengths, concerns)
        
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Michael Burry on {ticker}: "
        reasoning += f"{'Contrarian setup with value' if conviction >= 6 else 'Not contrarian enough'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(
            investor_name=self.name,
            conviction=conviction,
            vote=vote,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )


class BenGraham(LegendaryInvestor):
    """Father of value investing, margin of safety, hidden gems"""
    
    def __init__(self):
        super().__init__(
            name="Ben Graham",
            philosophy="Margin of safety. Buy dollar for 50 cents. Quantitative value screens. Hidden gems.",
            focus_areas=["margin of safety", "quantitative value", "asset value", "price to book"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        # Margin of safety
        if any(word in catalyst.lower() for word in ['undervalued', 'cheap', 'discount', 'bargain']):
            strengths.append("Margin of safety present")
        
        # Asset value
        if any(word in catalyst.lower() for word in ['assets', 'book value', 'tangible']):
            strengths.append("Strong asset backing")
        
        # Concerns
        if 'growth' in catalyst.lower() and 'value' not in catalyst.lower():
            concerns.append("Growth story, not value play")
        
        if 'crypto' in ticker.lower():
            concerns.append("No tangible assets or book value")
        
        conviction = self._calculate_conviction(strengths, concerns)
        
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Ben Graham on {ticker}: "
        reasoning += f"{'Margin of safety exists' if conviction >= 6 else 'No safety margin'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(
            investor_name=self.name,
            conviction=conviction,
            vote=vote,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )


class MohnishPabrai(LegendaryInvestor):
    """Doubles at low risk, heads I win tails I don't lose much"""
    
    def __init__(self):
        super().__init__(
            name="Mohnish Pabrai",
            philosophy="Look for doubles at low risk. Heads I win, tails I don't lose much. Cloning great investors.",
            focus_areas=["asymmetric risk/reward", "downside protection", "cloning ideas", "patience"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        # Asymmetric risk/reward
        if any(word in catalyst.lower() for word in ['upside', 'asymmetric', 'limited downside']):
            strengths.append("Asymmetric risk/reward setup")
        
        # Downside protection
        if 'stop loss' in catalyst.lower() or 'protect' in catalyst.lower():
            strengths.append("Downside protection built-in")
        
        # Cloning
        if any(word in catalyst.lower() for word in ['buffett', 'munger', 'guru', 'follows']):
            strengths.append("Following proven investors")
        
        # Concerns
        if 'speculative' in catalyst.lower():
            concerns.append("Too speculative, high downside risk")
        
        conviction = self._calculate_conviction(strengths, concerns)
        
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Mohnish Pabrai on {ticker}: "
        reasoning += f"{'Heads I win, tails limited loss' if conviction >= 6 else 'Risk/reward not asymmetric'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(
            investor_name=self.name,
            conviction=conviction,
            vote=vote,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )


class CathieWood(LegendaryInvestor):
    """Innovation and disruption, 5-year horizon, exponential growth"""
    
    def __init__(self):
        super().__init__(
            name="Cathie Wood",
            philosophy="Innovation and disruption. 5-year horizon. Exponential growth in AI, genomics, fintech, blockchain.",
            focus_areas=["disruptive innovation", "exponential growth", "5-year thesis", "emerging tech"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        # Innovation
        if any(word in catalyst.lower() for word in ['innovation', 'disrupt', 'ai', 'blockchain', 'genomics', 'fintech']):
            strengths.append("Disruptive innovation play")
        
        # Exponential growth
        if any(word in catalyst.lower() for word in ['exponential', 'scaling', 'network effects']):
            strengths.append("Exponential growth potential")
        
        # 5-year thesis
        if 'long-term' in catalyst.lower() or '5-year' in catalyst.lower():
            strengths.append("Long-term transformation story")
        
        # Concerns
        if 'value' in catalyst.lower() and 'growth' not in catalyst.lower():
            concerns.append("Value play, not growth/innovation")
        
        if 'old economy' in catalyst.lower() or 'traditional' in catalyst.lower():
            concerns.append("Not disruptive enough")
        
        conviction = self._calculate_conviction(strengths, concerns)
        
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Cathie Wood on {ticker}: "
        reasoning += f"{'Disruptive innovation at scale' if conviction >= 6 else 'Not innovative enough'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(
            investor_name=self.name,
            conviction=conviction,
            vote=vote,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )


# Remaining 6 investors follow same pattern...
class PhilFisher(LegendaryInvestor):
    """Deep scuttlebutt research, talk to customers/employees"""
    
    def __init__(self):
        super().__init__(
            name="Phil Fisher",
            philosophy="Deep scuttlebutt research. Talk to customers, employees, competitors. Buy and hold great companies.",
            focus_areas=["scuttlebutt research", "competitive advantage", "management quality", "long-term hold"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        if 'research' in catalyst.lower() or 'due diligence' in catalyst.lower():
            strengths.append("Deep research conducted")
        
        if 'competitive' in catalyst.lower() or 'advantage' in catalyst.lower():
            strengths.append("Competitive advantage identified")
        
        if not catalyst or len(catalyst) < 50:
            concerns.append("Insufficient research depth")
        
        conviction = self._calculate_conviction(strengths, concerns)
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Phil Fisher on {ticker}: "
        reasoning += f"{'Thorough scuttlebutt research' if conviction >= 6 else 'Need deeper research'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(self.name, conviction, vote, reasoning, concerns, strengths)


class PeterLynch(LegendaryInvestor):
    """Ten-baggers in everyday businesses, buy what you know"""
    
    def __init__(self):
        super().__init__(
            name="Peter Lynch",
            philosophy="Ten-baggers in everyday businesses. Buy what you know. Look for growth at reasonable price.",
            focus_areas=["consumer businesses", "growth at reasonable price", "scalability", "market expansion"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        if any(word in catalyst.lower() for word in ['consumer', 'retail', 'brand', 'everyday']):
            strengths.append("Consumer-facing business")
        
        if 'growth' in catalyst.lower():
            strengths.append("Growth story")
        
        if 'complex' in catalyst.lower() or 'hard to understand' in catalyst.lower():
            concerns.append("Too complex, not everyday business")
        
        conviction = self._calculate_conviction(strengths, concerns)
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Peter Lynch on {ticker}: "
        reasoning += f"{'Ten-bagger potential in understandable business' if conviction >= 6 else 'Not everyday business'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(self.name, conviction, vote, reasoning, concerns, strengths)


class BillAckman(LegendaryInvestor):
    """Bold concentrated positions, activist catalyst"""
    
    def __init__(self):
        super().__init__(
            name="Bill Ackman",
            philosophy="Bold concentrated positions. Activist catalyst. High conviction, deep research, influence outcomes.",
            focus_areas=["activist opportunities", "concentration", "management change", "bold bets"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        conviction_score = signal.get('conviction', 5)
        
        strengths = []
        concerns = []
        
        if conviction_score >= 9:
            strengths.append("High conviction opportunity")
        
        if any(word in catalyst.lower() for word in ['catalyst', 'change', 'restructure', 'activist']):
            strengths.append("Catalyst for change present")
        
        if conviction_score < 7:
            concerns.append("Not high enough conviction for concentrated bet")
        
        conviction = self._calculate_conviction(strengths, concerns)
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Bill Ackman on {ticker}: "
        reasoning += f"{'Bold bet with catalyst' if conviction >= 7 else 'Not bold enough'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(self.name, conviction, vote, reasoning, concerns, strengths)


class StanleyDruckenmiller(LegendaryInvestor):
    """Asymmetric opportunities, macro trends, high conviction when right"""
    
    def __init__(self):
        super().__init__(
            name="Stanley Druckenmiller",
            philosophy="Asymmetric opportunities. Macro trends. Bet big when you're right. Cut losses fast when wrong.",
            focus_areas=["macro trends", "asymmetric bets", "timing", "position sizing"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        if any(word in catalyst.lower() for word in ['macro', 'trend', 'tailwind', 'secular']):
            strengths.append("Macro tailwind")
        
        if 'asymmetric' in catalyst.lower() or 'upside' in catalyst.lower():
            strengths.append("Asymmetric risk/reward")
        
        if 'stop loss' not in catalyst.lower():
            concerns.append("No exit strategy if wrong")
        
        conviction = self._calculate_conviction(strengths, concerns)
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Stanley Druckenmiller on {ticker}: "
        reasoning += f"{'Macro setup with asymmetry' if conviction >= 6 else 'No clear macro edge'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(self.name, conviction, vote, reasoning, concerns, strengths)


class AswathDamodaran(LegendaryInvestor):
    """Story, numbers, valuation - the Dean of Valuation"""
    
    def __init__(self):
        super().__init__(
            name="Aswath Damodaran",
            philosophy="Every investment is a story backed by numbers. Valuation bridges narrative and reality.",
            focus_areas=["valuation models", "DCF analysis", "story to numbers", "intrinsic value"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        price = signal.get('price', 0)
        
        strengths = []
        concerns = []
        
        if 'valuation' in catalyst.lower() or 'dcf' in catalyst.lower():
            strengths.append("Valuation-based thesis")
        
        if any(word in catalyst.lower() for word in ['cash flow', 'earnings', 'revenue']):
            strengths.append("Numbers back the story")
        
        if not any(word in catalyst.lower() for word in ['value', 'price', 'valuation', 'cheap', 'expensive']):
            concerns.append("No valuation framework")
        
        conviction = self._calculate_conviction(strengths, concerns)
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Aswath Damodaran on {ticker}: "
        reasoning += f"{'Story supported by numbers' if conviction >= 6 else 'Narrative without valuation'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(self.name, conviction, vote, reasoning, concerns, strengths)


class RakeshJhunjhunwala(LegendaryInvestor):
    """Big Bull of India, long-term growth, quality businesses"""
    
    def __init__(self):
        super().__init__(
            name="Rakesh Jhunjhunwala",
            philosophy="Big Bull of India. Long-term growth in quality businesses. Bet on India's future.",
            focus_areas=["emerging markets", "long-term growth", "quality businesses", "patience"]
        )
    
    def evaluate(self, signal: Dict) -> InvestorOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        strengths = []
        concerns = []
        
        if any(word in catalyst.lower() for word in ['growth', 'emerging', 'expansion']):
            strengths.append("Growth market opportunity")
        
        if 'long-term' in catalyst.lower():
            strengths.append("Long-term value creation")
        
        if 'short-term' in catalyst.lower() or 'quick' in catalyst.lower():
            concerns.append("Short-term thinking, not patient capital")
        
        conviction = self._calculate_conviction(strengths, concerns)
        vote = "BUY" if conviction >= 7 else "SELL" if conviction <= 3 else "HOLD"
        
        reasoning = f"Rakesh Jhunjhunwala on {ticker}: "
        reasoning += f"{'Long-term growth story' if conviction >= 6 else 'Not long-term enough'}. "
        reasoning += f"Conviction: {conviction}/10."
        
        return InvestorOpinion(self.name, conviction, vote, reasoning, concerns, strengths)


# Agent registry
LEGENDARY_INVESTORS = [
    WarrenBuffett(),
    CharlieMunger(),
    MichaelBurry(),
    BenGraham(),
    MohnishPabrai(),
    CathieWood(),
    PhilFisher(),
    PeterLynch(),
    BillAckman(),
    StanleyDruckenmiller(),
    AswathDamodaran(),
    RakeshJhunjhunwala()
]


def run_investor_debate(signal: Dict) -> Dict:
    """
    Run all 12 legendary investors on a signal.
    
    Returns aggregated opinions with consensus conviction.
    """
    opinions = []
    
    for investor in LEGENDARY_INVESTORS:
        opinion = investor.evaluate(signal)
        opinions.append(opinion)
    
    # Aggregate results
    buy_votes = sum(1 for op in opinions if op.vote == "BUY")
    sell_votes = sum(1 for op in opinions if op.vote == "SELL")
    hold_votes = sum(1 for op in opinions if op.vote == "HOLD")
    
    avg_conviction = sum(op.conviction for op in opinions) / len(opinions)
    
    # Consensus
    if buy_votes > sell_votes + hold_votes:
        consensus = "BUY"
    elif sell_votes > buy_votes + hold_votes:
        consensus = "SELL"
    else:
        consensus = "HOLD"
    
    return {
        "ticker": signal.get('ticker'),
        "consensus": consensus,
        "avg_conviction": round(avg_conviction, 2),
        "votes": {"BUY": buy_votes, "SELL": sell_votes, "HOLD": hold_votes},
        "opinions": [
            {
                "investor": op.investor_name,
                "conviction": op.conviction,
                "vote": op.vote,
                "reasoning": op.reasoning,
                "strengths": op.strengths,
                "concerns": op.concerns
            }
            for op in opinions
        ]
    }


if __name__ == "__main__":
    # Test with sample signal
    test_signal = {
        "ticker": "TAO",
        "price": 176.05,
        "catalyst": "AI + blockchain intersection, strong fundamentals, Yieldschool conviction 8.5/10",
        "conviction": 8.5,
        "source": "Yieldschool",
        "asset_class": "crypto"
    }
    
    result = run_investor_debate(test_signal)
    
    print(f"🐓 Legendary Investor Debate: {result['ticker']}")
    print(f"Consensus: {result['consensus']}")
    print(f"Avg Conviction: {result['avg_conviction']}/10")
    print(f"Votes: {result['votes']}")
    print("\nDetailed Opinions:")
    for op in result['opinions']:
        print(f"\n{op['investor']} ({op['conviction']}/10): {op['vote']}")
        print(f"  {op['reasoning']}")
