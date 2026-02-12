#!/usr/bin/env python3
"""
LLM-Powered Agent Layer
=======================
Enhances rule-based agents with LLM reasoning.

Uses LangChain + GPT-4o-mini for 16 agents, Claude for Portfolio Manager.

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

import os
from typing import Dict, List
from dataclasses import dataclass

try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    print("⚠️  LangChain not available, using rule-based agents only")


@dataclass
class LLMConfig:
    """LLM configuration"""
    model: str = "gpt-4o-mini"  # Cheap for 16 agents
    temperature: float = 0.3  # Low for consistency
    max_tokens: int = 300  # Short responses


class LLMAgent:
    """
    Base LLM-powered agent.
    
    Wraps existing rule-based agents with LLM reasoning.
    Falls back to rules if LLM unavailable.
    """
    
    def __init__(self, name: str, philosophy: str, config: LLMConfig = None):
        self.name = name
        self.philosophy = philosophy
        self.config = config or LLMConfig()
        self.llm = None
        
        if HAS_LANGCHAIN and os.getenv('OPENAI_API_KEY'):
            try:
                self.llm = ChatOpenAI(
                    model=self.config.model,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
            except Exception as e:
                print(f"⚠️  Could not initialize LLM for {name}: {e}")
    
    def evaluate_with_llm(self, signal: Dict) -> Dict:
        """Evaluate signal using LLM reasoning"""
        if not self.llm:
            return None
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are {self.name}, a legendary investor.

Your philosophy: {self.philosophy}

Evaluate the following investment signal and provide:
1. Conviction score (0-10, where 10 = highest conviction)
2. Vote (BUY, SELL, or HOLD)
3. Brief reasoning (2-3 sentences)
4. Key strengths (bullet points)
5. Key concerns (bullet points)

Be critical but fair. Consider your investment philosophy."""),
            ("human", """Signal Details:
Ticker: {ticker}
Price: ${price}
Catalyst: {catalyst}
Source: {source}
Asset Class: {asset_class}

Provide your analysis in this exact format:
CONVICTION: [0-10]
VOTE: [BUY/SELL/HOLD]
REASONING: [2-3 sentences]
STRENGTHS:
- [strength 1]
- [strength 2]
CONCERNS:
- [concern 1]
- [concern 2]""")
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "ticker": signal.get('ticker', 'Unknown'),
                "price": signal.get('price', 0),
                "catalyst": signal.get('catalyst', 'No catalyst provided'),
                "source": signal.get('source', 'Unknown'),
                "asset_class": signal.get('asset_class', 'unknown')
            })
            
            # Parse response
            content = response.content
            return self._parse_llm_response(content)
        
        except Exception as e:
            print(f"⚠️  LLM evaluation failed for {self.name}: {e}")
            return None
    
    def _parse_llm_response(self, content: str) -> Dict:
        """Parse LLM response into structured format"""
        lines = content.strip().split('\n')
        
        result = {
            'conviction': 5.0,
            'vote': 'HOLD',
            'reasoning': '',
            'strengths': [],
            'concerns': []
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('CONVICTION:'):
                try:
                    result['conviction'] = float(line.split(':')[1].strip())
                except:
                    pass
            
            elif line.startswith('VOTE:'):
                vote = line.split(':')[1].strip().upper()
                if vote in ['BUY', 'SELL', 'HOLD']:
                    result['vote'] = vote
            
            elif line.startswith('REASONING:'):
                result['reasoning'] = line.split(':', 1)[1].strip()
                current_section = 'reasoning'
            
            elif line.startswith('STRENGTHS:'):
                current_section = 'strengths'
            
            elif line.startswith('CONCERNS:'):
                current_section = 'concerns'
            
            elif line.startswith('-') and current_section in ['strengths', 'concerns']:
                item = line.lstrip('- ').strip()
                if item:
                    result[current_section].append(item)
            
            elif current_section == 'reasoning' and line:
                result['reasoning'] += ' ' + line
        
        return result


# Create LLM-enhanced versions of legendary investors
def create_llm_buffett():
    """Warren Buffett with LLM reasoning"""
    return LLMAgent(
        name="Warren Buffett",
        philosophy="Buy wonderful companies at fair prices. Long-term moat, strong management, consistent earnings."
    )


def create_llm_munger():
    """Charlie Munger with LLM reasoning"""
    return LLMAgent(
        name="Charlie Munger",
        philosophy="Seek wonderful businesses. Avoid stupidity more than seek brilliance. Multidisciplinary mental models."
    )


def create_llm_burry():
    """Michael Burry with LLM reasoning"""
    return LLMAgent(
        name="Michael Burry",
        philosophy="Big Short contrarian. Deep value in distressed situations. Go against the crowd when math supports it."
    )


# Test LLM agent
if __name__ == "__main__":
    print("🤖 Testing LLM Agent System")
    
    if not HAS_LANGCHAIN:
        print("❌ LangChain not available")
        exit(1)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not set")
        exit(1)
    
    # Test signal
    test_signal = {
        'ticker': 'PGR',
        'price': 245.50,
        'catalyst': 'Progressive Insurance - Strong moat, P/E 15.2, ROE 24.3%, consistent earnings',
        'source': 'Value Screener',
        'asset_class': 'stock'
    }
    
    # Test Buffett
    buffett = create_llm_buffett()
    print(f"\n📊 Testing {buffett.name}...")
    
    result = buffett.evaluate_with_llm(test_signal)
    
    if result:
        print(f"   Conviction: {result['conviction']}/10")
        print(f"   Vote: {result['vote']}")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Strengths: {result['strengths']}")
        print(f"   Concerns: {result['concerns']}")
        print(f"\n✅ LLM agents working!")
    else:
        print(f"❌ LLM evaluation failed")
