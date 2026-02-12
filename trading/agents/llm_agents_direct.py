#!/usr/bin/env python3
"""
LLM-Powered Agents (Direct OpenAI API)
======================================
No LangChain dependency - direct API calls.

Author: Joselo 🐓
Date: Feb 12, 2026
"""

import os
import json
from typing import Dict
import openai

# Set API key
openai.api_key = os.getenv('OPENAI_API_KEY')


class LLMAgent:
    """LLM-powered agent using direct OpenAI API"""
    
    def __init__(self, name: str, philosophy: str, model="gpt-4o-mini"):
        self.name = name
        self.philosophy = philosophy
        self.model = model
    
    def evaluate(self, signal: Dict) -> Dict:
        """Evaluate signal with LLM reasoning"""
        
        prompt = f"""You are {self.name}, a legendary investor.

Your philosophy: {self.philosophy}

Evaluate this investment signal:

Ticker: {signal.get('ticker')}
Price: ${signal.get('price')}
Catalyst: {signal.get('catalyst')}
Source: {signal.get('source')}
Asset Class: {signal.get('asset_class')}

Provide your analysis in JSON format:
{{
    "conviction": 7.5,  // 0-10 scale
    "vote": "BUY",      // BUY, SELL, or HOLD
    "reasoning": "Brief 2-3 sentence explanation",
    "strengths": ["strength 1", "strength 2"],
    "concerns": ["concern 1", "concern 2"]
}}

Be critical but fair. Consider your investment philosophy."""
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are {self.name}. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON (sometimes wrapped in ```json```)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            result = json.loads(content)
            
            return {
                'investor': self.name,
                'conviction': result.get('conviction', 5.0),
                'vote': result.get('vote', 'HOLD'),
                'reasoning': result.get('reasoning', ''),
                'strengths': result.get('strengths', []),
                'concerns': result.get('concerns', [])
            }
        
        except Exception as e:
            print(f"⚠️  LLM error for {self.name}: {e}")
            return None


# Legendary investor agents
LEGENDARY_LLM_AGENTS = [
    LLMAgent("Warren Buffett", "Buy wonderful companies at fair prices. Long-term moat, strong management, consistent earnings."),
    LLMAgent("Charlie Munger", "Seek wonderful businesses. Avoid stupidity. Multidisciplinary mental models."),
    LLMAgent("Michael Burry", "Big Short contrarian. Deep value in distressed situations."),
    LLMAgent("Ben Graham", "Margin of safety. Buy dollar for 50 cents. Quantitative value screens."),
    LLMAgent("Mohnish Pabrai", "Doubles at low risk. Heads I win, tails I don't lose much."),
    LLMAgent("Cathie Wood", "Innovation and disruption. 5-year horizon. Exponential growth in AI, genomics, fintech."),
    LLMAgent("Phil Fisher", "Deep scuttlebutt research. Talk to customers, employees, competitors."),
    LLMAgent("Peter Lynch", "Ten-baggers in everyday businesses. Buy what you know."),
    LLMAgent("Bill Ackman", "Bold concentrated positions. Activist catalyst."),
    LLMAgent("Stanley Druckenmiller", "Asymmetric opportunities. Macro trends. Bet big when right."),
    LLMAgent("Aswath Damodaran", "Every investment is story backed by numbers. Valuation bridges narrative and reality."),
    LLMAgent("Rakesh Jhunjhunwala", "Big Bull of India. Long-term growth in quality businesses.")
]


def run_llm_debate(signal: Dict) -> Dict:
    """Run all 12 LLM agents on signal"""
    print(f"🤖 Running LLM agents on {signal.get('ticker')}...")
    
    opinions = []
    
    for agent in LEGENDARY_LLM_AGENTS:
        print(f"   {agent.name}...", end=' ')
        result = agent.evaluate(signal)
        
        if result:
            opinions.append(result)
            print(f"{result['conviction']}/10 {result['vote']}")
        else:
            print("FAILED")
    
    # Aggregate
    if not opinions:
        return None
    
    buy_votes = sum(1 for op in opinions if op['vote'] == 'BUY')
    sell_votes = sum(1 for op in opinions if op['vote'] == 'SELL')
    hold_votes = sum(1 for op in opinions if op['vote'] == 'HOLD')
    
    avg_conviction = sum(op['conviction'] for op in opinions) / len(opinions)
    
    consensus = "HOLD"
    if buy_votes > sell_votes + hold_votes:
        consensus = "BUY"
    elif sell_votes > buy_votes + hold_votes:
        consensus = "SELL"
    
    return {
        'consensus': consensus,
        'avg_conviction': round(avg_conviction, 2),
        'votes': {'BUY': buy_votes, 'SELL': sell_votes, 'HOLD': hold_votes},
        'opinions': opinions
    }


if __name__ == "__main__":
    # Test
    test_signal = {
        'ticker': 'PGR',
        'price': 245.50,
        'catalyst': 'Progressive Insurance - Strong moat, P/E 15.2, ROE 24.3%, consistent earnings growth 10+ years',
        'source': 'Value Screener',
        'asset_class': 'stock'
    }
    
    result = run_llm_debate(test_signal)
    
    if result:
        print(f"\n✅ LLM Debate Complete")
        print(f"   Consensus: {result['consensus']}")
        print(f"   Avg Conviction: {result['avg_conviction']}/10")
        print(f"   Votes: {result['votes']}")
    else:
        print("\n❌ LLM debate failed")
