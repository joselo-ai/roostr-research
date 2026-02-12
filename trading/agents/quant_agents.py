#!/usr/bin/env python3
"""
Quantitative Analysis Agents - 4 Data-Driven Evaluators
========================================================

Valuation, Sentiment, Fundamentals, Technicals agents
provide quantitative scoring to complement legendary investor opinions.

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

from typing import Dict, Optional
from dataclasses import dataclass
import re

@dataclass
class QuantOpinion:
    """Quantitative agent's evaluation"""
    agent_name: str
    score: float  # 0-10 scale
    metrics: Dict
    recommendation: str  # BUY, SELL, HOLD
    reasoning: str


class ValuationAgent:
    """Evaluates price vs intrinsic value"""
    
    def __init__(self):
        self.name = "Valuation Agent"
    
    def evaluate(self, signal: Dict) -> QuantOpinion:
        ticker = signal.get('ticker', 'Unknown')
        price = signal.get('price', 0)
        catalyst = signal.get('catalyst', '')
        
        # Extract valuation keywords
        undervalued = any(word in catalyst.lower() for word in ['undervalued', 'cheap', 'discount', 'bargain'])
        overvalued = any(word in catalyst.lower() for word in ['overvalued', 'expensive', 'rich', 'stretched'])
        fair_value = 'fair value' in catalyst.lower()
        
        # Scoring
        if undervalued:
            score = 8.0
            recommendation = "BUY"
            reasoning = f"{ticker} appears undervalued relative to intrinsic value"
        elif overvalued:
            score = 3.0
            recommendation = "SELL"
            reasoning = f"{ticker} appears overvalued"
        elif fair_value:
            score = 5.5
            recommendation = "HOLD"
            reasoning = f"{ticker} trading near fair value"
        else:
            score = 5.0
            recommendation = "HOLD"
            reasoning = f"{ticker} no clear valuation signal"
        
        metrics = {
            "undervalued_signal": undervalued,
            "overvalued_signal": overvalued,
            "fair_value_signal": fair_value
        }
        
        return QuantOpinion(
            agent_name=self.name,
            score=score,
            metrics=metrics,
            recommendation=recommendation,
            reasoning=reasoning
        )


class SentimentAgent:
    """Evaluates market sentiment and social signals"""
    
    def __init__(self):
        self.name = "Sentiment Agent"
    
    def evaluate(self, signal: Dict) -> QuantOpinion:
        ticker = signal.get('ticker', 'Unknown')
        source = signal.get('source', '')
        catalyst = signal.get('catalyst', '')
        
        # Social sentiment indicators
        reddit_score = 0
        if 'reddit' in source.lower():
            if any(word in catalyst.lower() for word in ['🚀', 'moon', 'apes', 'yolo']):
                reddit_score = 7  # High engagement
            else:
                reddit_score = 5
        
        # Discord/Community sentiment
        discord_score = 0
        if 'discord' in source.lower() or 'yieldschool' in source.lower():
            if 'conviction' in catalyst.lower():
                discord_score = 7
            else:
                discord_score = 5
        
        # Aggregate sentiment
        sentiment_score = max(reddit_score, discord_score, 5)
        
        if sentiment_score >= 7:
            recommendation = "BUY"
            reasoning = f"{ticker} strong positive sentiment from {source}"
        elif sentiment_score <= 3:
            recommendation = "SELL"
            reasoning = f"{ticker} weak or negative sentiment"
        else:
            recommendation = "HOLD"
            reasoning = f"{ticker} neutral sentiment"
        
        metrics = {
            "reddit_score": reddit_score,
            "discord_score": discord_score,
            "overall_sentiment": sentiment_score
        }
        
        return QuantOpinion(
            agent_name=self.name,
            score=sentiment_score,
            metrics=metrics,
            recommendation=recommendation,
            reasoning=reasoning
        )


class FundamentalsAgent:
    """Evaluates business fundamentals"""
    
    def __init__(self):
        self.name = "Fundamentals Agent"
    
    def evaluate(self, signal: Dict) -> QuantOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        # Fundamental strength indicators
        strong_fundamentals = any(word in catalyst.lower() for word in [
            'profitable', 'cash flow', 'revenue growth', 'earnings', 'margin'
        ])
        
        weak_fundamentals = any(word in catalyst.lower() for word in [
            'unprofitable', 'burning cash', 'losses', 'declining revenue'
        ])
        
        catalyst_present = any(word in catalyst.lower() for word in [
            'product launch', 'partnership', 'contract', 'approval', 'expansion'
        ])
        
        # Scoring
        score = 5.0
        if strong_fundamentals:
            score += 2
        if weak_fundamentals:
            score -= 2
        if catalyst_present:
            score += 1
        
        score = max(0, min(10, score))
        
        if score >= 7:
            recommendation = "BUY"
            reasoning = f"{ticker} strong fundamentals with catalyst"
        elif score <= 3:
            recommendation = "SELL"
            reasoning = f"{ticker} weak fundamentals"
        else:
            recommendation = "HOLD"
            reasoning = f"{ticker} mixed fundamental signals"
        
        metrics = {
            "strong_fundamentals": strong_fundamentals,
            "weak_fundamentals": weak_fundamentals,
            "catalyst_present": catalyst_present
        }
        
        return QuantOpinion(
            agent_name=self.name,
            score=score,
            metrics=metrics,
            recommendation=recommendation,
            reasoning=reasoning
        )


class TechnicalsAgent:
    """Evaluates technical indicators and chart patterns"""
    
    def __init__(self):
        self.name = "Technicals Agent"
    
    def evaluate(self, signal: Dict) -> QuantOpinion:
        ticker = signal.get('ticker', 'Unknown')
        catalyst = signal.get('catalyst', '')
        
        # Technical indicators
        bullish_technicals = any(word in catalyst.lower() for word in [
            'breakout', 'golden cross', 'support', 'oversold', 'bounce'
        ])
        
        bearish_technicals = any(word in catalyst.lower() for word in [
            'breakdown', 'death cross', 'resistance', 'overbought'
        ])
        
        # Momentum
        momentum = 'momentum' in catalyst.lower() or 'trending' in catalyst.lower()
        
        # Scoring
        score = 5.0
        if bullish_technicals:
            score += 2
        if bearish_technicals:
            score -= 2
        if momentum:
            score += 1
        
        score = max(0, min(10, score))
        
        if score >= 7:
            recommendation = "BUY"
            reasoning = f"{ticker} bullish technical setup"
        elif score <= 3:
            recommendation = "SELL"
            reasoning = f"{ticker} bearish technicals"
        else:
            recommendation = "HOLD"
            reasoning = f"{ticker} neutral technical picture"
        
        metrics = {
            "bullish_technicals": bullish_technicals,
            "bearish_technicals": bearish_technicals,
            "momentum": momentum
        }
        
        return QuantOpinion(
            agent_name=self.name,
            score=score,
            metrics=metrics,
            recommendation=recommendation,
            reasoning=reasoning
        )


# Agent registry
QUANT_AGENTS = [
    ValuationAgent(),
    SentimentAgent(),
    FundamentalsAgent(),
    TechnicalsAgent()
]


def run_quant_analysis(signal: Dict) -> Dict:
    """
    Run all 4 quantitative agents on a signal.
    
    Returns aggregated quant scores.
    """
    opinions = []
    
    for agent in QUANT_AGENTS:
        opinion = agent.evaluate(signal)
        opinions.append(opinion)
    
    # Aggregate
    buy_votes = sum(1 for op in opinions if op.recommendation == "BUY")
    sell_votes = sum(1 for op in opinions if op.recommendation == "SELL")
    hold_votes = sum(1 for op in opinions if op.recommendation == "HOLD")
    
    avg_score = sum(op.score for op in opinions) / len(opinions)
    
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
        "avg_score": round(avg_score, 2),
        "votes": {"BUY": buy_votes, "SELL": sell_votes, "HOLD": hold_votes},
        "opinions": [
            {
                "agent": op.agent_name,
                "score": op.score,
                "recommendation": op.recommendation,
                "reasoning": op.reasoning,
                "metrics": op.metrics
            }
            for op in opinions
        ]
    }


if __name__ == "__main__":
    # Test
    test_signal = {
        "ticker": "TAO",
        "price": 176.05,
        "catalyst": "Strong fundamentals, AI narrative, oversold RSI, bullish breakout setup",
        "source": "Yieldschool"
    }
    
    result = run_quant_analysis(test_signal)
    
    print(f"🐓 Quant Analysis: {result['ticker']}")
    print(f"Consensus: {result['consensus']}")
    print(f"Avg Score: {result['avg_score']}/10")
    print(f"Votes: {result['votes']}")
    print("\nDetailed Opinions:")
    for op in result['opinions']:
        print(f"\n{op['agent']} ({op['score']}/10): {op['recommendation']}")
        print(f"  {op['reasoning']}")
