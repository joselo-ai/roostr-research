#!/usr/bin/env python3
"""
Perplexity Deep Research Integration
Structured research on trading signals before agent deliberation.
"""

import os
import json
import requests
from datetime import datetime

# Perplexity API (requires PERPLEXITY_API_KEY env var)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


def research_ticker(ticker, source, initial_conviction, notes=""):
    """
    Deep dive research on a ticker using Perplexity.
    
    Returns structured research report with:
    - Fundamentals (revenue, growth, margins)
    - Recent news & catalysts
    - Technical setup
    - Risk factors
    - Enhanced conviction score
    """
    
    print(f"\n🔬 Researching {ticker} from {source}...")
    print(f"   Initial conviction: {initial_conviction}/10")
    print(f"   Notes: {notes[:100]}")
    
    if not PERPLEXITY_API_KEY:
        print("   ⚠️  PERPLEXITY_API_KEY not set - using placeholder research")
        return placeholder_research(ticker, source, initial_conviction, notes)
    
    # Structured research prompt
    prompt = f"""
You are a professional equity research analyst. Provide a concise, structured analysis of ${ticker}.

**Signal Context:**
- Source: {source}
- Initial Conviction: {initial_conviction}/10
- Notes: {notes}

**Research Required:**

1. **Fundamentals** (3-4 sentences)
   - Business model & revenue streams
   - Recent quarterly results
   - Growth trajectory & margins
   
2. **Catalysts** (2-3 items)
   - Upcoming events, earnings, product launches
   - Regulatory decisions, partnerships
   - Macro trends favoring the company

3. **Technical Setup** (2-3 sentences)
   - Current price action & trend
   - Key support/resistance levels
   - Volume & momentum indicators

4. **Risk Factors** (3-4 items)
   - Company-specific risks
   - Sector/market risks
   - Valuation concerns

5. **Enhanced Conviction** (1-10 scale)
   - Adjust initial conviction based on research
   - Justify the change (if any)

Keep it factual, concise, and action-oriented. Focus on information that would inform a 3-30 day trade.
"""
    
    try:
        response = requests.post(
            PERPLEXITY_URL,
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-sonar-large-128k-online",
                "messages": [
                    {"role": "system", "content": "You are a professional equity research analyst providing concise, structured analysis for short-to-medium term trades."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500,
                "temperature": 0.2
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            research_text = data["choices"][0]["message"]["content"]
            
            # Parse enhanced conviction from response
            enhanced_conviction = parse_conviction(research_text, initial_conviction)
            
            report = {
                "ticker": ticker,
                "source": source,
                "initial_conviction": initial_conviction,
                "enhanced_conviction": enhanced_conviction,
                "research": research_text,
                "timestamp": datetime.now().isoformat(),
                "model": "perplexity-sonar-large"
            }
            
            print(f"   ✅ Research complete")
            print(f"   Enhanced conviction: {enhanced_conviction}/10")
            
            return report
            
        else:
            print(f"   ❌ Perplexity API error: {response.status_code}")
            return placeholder_research(ticker, source, initial_conviction, notes)
            
    except Exception as e:
        print(f"   ❌ Research failed: {e}")
        return placeholder_research(ticker, source, initial_conviction, notes)


def parse_conviction(research_text, fallback):
    """Extract enhanced conviction score from research text."""
    lines = research_text.lower().split("\n")
    for line in lines:
        if "conviction" in line and "/" in line:
            # Try to extract number like "8/10" or "conviction: 7.5"
            import re
            match = re.search(r'(\d+\.?\d*)\s*/?\s*10', line)
            if match:
                return float(match.group(1))
            match = re.search(r'conviction:?\s*(\d+\.?\d*)', line)
            if match:
                return float(match.group(1))
    
    # Fallback to initial conviction
    return fallback


def placeholder_research(ticker, source, initial_conviction, notes):
    """Placeholder when Perplexity API unavailable."""
    return {
        "ticker": ticker,
        "source": source,
        "initial_conviction": initial_conviction,
        "enhanced_conviction": initial_conviction,  # No change
        "research": f"Placeholder research for {ticker}. Perplexity API key not configured. Using initial conviction: {initial_conviction}/10",
        "timestamp": datetime.now().isoformat(),
        "model": "placeholder"
    }


def save_research(report, output_dir="research"):
    """Save research report to file."""
    from pathlib import Path
    
    research_dir = Path(__file__).parent.parent / output_dir
    research_dir.mkdir(exist_ok=True)
    
    filename = f"{report['ticker']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = research_dir / filename
    
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"   💾 Saved to {filepath}")
    
    return filepath


if __name__ == "__main__":
    # Test with ASTS signal
    report = research_ticker(
        ticker="ASTS",
        source="Reddit-wallstreetbets",
        initial_conviction=10.0,
        notes="FCC approval expected Q1 2026..."
    )
    
    print("\n" + "="*60)
    print("RESEARCH REPORT:")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    save_research(report)
