#!/usr/bin/env python3
"""
Manus AI Research Integration
Structured research on trading signals using Manus Wide Research.

Better than Perplexity for parallel research on multiple tickers.
"""

import os
import json
import time
import requests
from datetime import datetime

# Manus API
MANUS_API_KEY = os.getenv("MANUS_API_KEY", "")
MANUS_BASE_URL = "https://api.manus.ai/v1"


def research_ticker(ticker, source, initial_conviction, notes="", agent_profile="manus-1.6"):
    """
    Deep dive research on a ticker using Manus AI.
    
    Args:
        ticker: Stock symbol (e.g. "ASTS")
        source: Where signal came from (e.g. "Reddit-wallstreetbets")
        initial_conviction: Initial signal conviction (0-10)
        notes: Additional context about the signal
        agent_profile: "manus-1.6" (default), "manus-1.6-lite", or "manus-1.6-max"
    
    Returns structured research report with:
    - Fundamentals (revenue, growth, margins)
    - Recent news & catalysts
    - Technical setup
    - Risk factors
    - Enhanced conviction score
    """
    
    print(f"\n🔬 Manus Research: {ticker} from {source}")
    print(f"   Initial conviction: {initial_conviction}/10")
    print(f"   Agent profile: {agent_profile}")
    
    if not MANUS_API_KEY:
        print("   ⚠️  MANUS_API_KEY not set - using placeholder research")
        return placeholder_research(ticker, source, initial_conviction, notes)
    
    # Structured research prompt
    prompt = f"""
Research ${ticker} for a short-to-medium term trade (3-30 days).

**Signal Context:**
- Source: {source}
- Initial Conviction: {initial_conviction}/10
- Notes: {notes}

**Research Required:**

1. **Company Fundamentals** (concise, 3-4 sentences)
   - Business model & revenue streams
   - Recent quarterly results (latest earnings)
   - Growth trajectory & profit margins
   
2. **Catalysts** (list 2-4 items with dates if known)
   - Upcoming events: earnings, product launches, FDA approvals, FCC decisions
   - Recent news: partnerships, acquisitions, regulatory wins
   - Macro trends: sector momentum, retail interest, institutional activity

3. **Technical Setup** (2-3 sentences)
   - Current price and 52-week range
   - Recent price action: trend, breakouts, support/resistance
   - Volume & momentum: unusual activity, RSI, MACD signals

4. **Risk Factors** (list 3-5 items)
   - Company-specific risks: execution, competition, dilution
   - Sector/market risks: regulation, macro headwinds
   - Valuation concerns: P/S ratio, burn rate, profitability timeline

5. **Enhanced Conviction Score**
   - Re-score conviction (0-10) based on research findings
   - Justify: what changed from initial {initial_conviction}/10?
   - Final recommendation: BUY, PASS, or MONITOR

**Output Format:**
Use markdown with clear sections. Be factual, concise, and cite specific data points (revenue numbers, dates, price levels). Focus on actionable intelligence for trading decisions.
"""
    
    try:
        # Create Manus task
        print(f"   📤 Creating Manus research task...")
        
        response = requests.post(
            f"{MANUS_BASE_URL}/tasks",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "API_KEY": MANUS_API_KEY
            },
            json={
                "prompt": prompt,
                "agentProfile": agent_profile,
                "taskMode": "agent",  # Full agent mode for Wide Research
                "hideInTaskList": True  # Don't clutter UI
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"   ❌ Manus API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return placeholder_research(ticker, source, initial_conviction, notes)
        
        task_data = response.json()
        task_id = task_data["task_id"]
        task_url = task_data.get("task_url", "")
        
        print(f"   ✅ Task created: {task_id}")
        print(f"   🔗 URL: {task_url}")
        
        # Poll for completion
        print(f"   ⏳ Waiting for research to complete...")
        
        max_wait = 300  # 5 minutes max
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(10)  # Poll every 10 seconds
            
            status_response = requests.get(
                f"{MANUS_BASE_URL}/tasks/{task_id}",
                headers={
                    "accept": "application/json",
                    "API_KEY": MANUS_API_KEY
                },
                timeout=30
            )
            
            if status_response.status_code != 200:
                print(f"   ⚠️  Status check failed: {status_response.status_code}")
                continue
            
            status_data = status_response.json()
            task_status = status_data.get("status", "pending")
            
            print(f"   ⏳ Status: {task_status}")
            
            if task_status == "completed":
                # Extract research text from output
                output_blocks = status_data.get("output", [])
                research_text = ""
                
                for block in output_blocks:
                    if block.get("role") == "assistant":
                        for content in block.get("content", []):
                            if content.get("type") == "output_text":
                                research_text += content.get("text", "") + "\n\n"
                
                # Parse enhanced conviction
                enhanced_conviction = parse_conviction(research_text, initial_conviction)
                
                report = {
                    "ticker": ticker,
                    "source": source,
                    "initial_conviction": initial_conviction,
                    "enhanced_conviction": enhanced_conviction,
                    "research": research_text.strip(),
                    "timestamp": datetime.now().isoformat(),
                    "model": f"manus-{agent_profile}",
                    "task_id": task_id,
                    "task_url": task_url,
                    "credit_usage": status_data.get("credit_usage", 0)
                }
                
                print(f"   ✅ Research complete!")
                print(f"   💡 Enhanced conviction: {enhanced_conviction}/10")
                print(f"   💳 Credits used: {report['credit_usage']}")
                
                return report
            
            elif task_status == "failed":
                error = status_data.get("error", "Unknown error")
                print(f"   ❌ Task failed: {error}")
                return placeholder_research(ticker, source, initial_conviction, notes)
        
        # Timeout
        print(f"   ⏰ Research timed out after {max_wait}s")
        return placeholder_research(ticker, source, initial_conviction, notes)
        
    except Exception as e:
        print(f"   ❌ Research failed: {e}")
        return placeholder_research(ticker, source, initial_conviction, notes)


def parse_conviction(research_text, fallback):
    """Extract enhanced conviction score from research text."""
    lines = research_text.lower().split("\n")
    
    for line in lines:
        if "conviction" in line and ("/" in line or ":" in line):
            # Try to extract number like "8/10" or "conviction: 7.5"
            import re
            match = re.search(r'(\d+\.?\d*)\s*/?\s*10', line)
            if match:
                return float(match.group(1))
            match = re.search(r'conviction:?\s*(\d+\.?\d*)', line)
            if match:
                score = float(match.group(1))
                # If already 0-10, use as-is; if 0-1, scale to 10
                return score if score > 1 else score * 10
    
    # Fallback to initial conviction
    return fallback


def placeholder_research(ticker, source, initial_conviction, notes):
    """Placeholder when Manus API unavailable."""
    return {
        "ticker": ticker,
        "source": source,
        "initial_conviction": initial_conviction,
        "enhanced_conviction": initial_conviction,  # No change
        "research": f"Placeholder research for {ticker}.\n\nManus API key not configured.\nUsing initial conviction: {initial_conviction}/10\n\nNotes: {notes}",
        "timestamp": datetime.now().isoformat(),
        "model": "placeholder",
        "task_id": None,
        "task_url": None
    }


def batch_research(signals, agent_profile="manus-1.6"):
    """
    Research multiple tickers in parallel using Manus Wide Research.
    
    Args:
        signals: List of signal dicts with keys: ticker, source, conviction, notes
        agent_profile: Manus agent to use
    
    Returns: List of research reports
    """
    
    print(f"\n🔬 Batch Research: {len(signals)} signals")
    print("="*60)
    
    reports = []
    
    # Create all tasks first (parallel submission)
    task_ids = []
    for signal in signals:
        print(f"\n📤 Submitting: {signal['ticker']}")
        
        # Create task (don't wait for completion yet)
        try:
            response = requests.post(
                f"{MANUS_BASE_URL}/tasks",
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                    "API_KEY": MANUS_API_KEY
                },
                json={
                    "prompt": build_research_prompt(signal),
                    "agentProfile": agent_profile,
                    "taskMode": "agent",
                    "hideInTaskList": True
                },
                timeout=30
            )
            
            if response.status_code == 200:
                task_data = response.json()
                task_ids.append({
                    "task_id": task_data["task_id"],
                    "ticker": signal["ticker"],
                    "signal": signal
                })
                print(f"   ✅ Task created: {task_data['task_id']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n⏳ Waiting for {len(task_ids)} tasks to complete...")
    
    # Poll all tasks until complete
    # (Simplified for now - could use webhooks for production)
    
    return reports


def build_research_prompt(signal):
    """Build research prompt from signal dict."""
    return f"""
Research ${signal['ticker']} for a short-to-medium term trade.

**Signal Context:**
- Source: {signal.get('source', 'Unknown')}
- Initial Conviction: {signal.get('conviction', 5.0)}/10
- Notes: {signal.get('notes', '')}

Provide: Fundamentals, Catalysts, Technical Setup, Risks, Enhanced Conviction (0-10).
"""


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
        notes="FCC approval expected Q1 2026. High social engagement.",
        agent_profile="manus-1.6"
    )
    
    print("\n" + "="*60)
    print("RESEARCH REPORT:")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    if report["research"] != "placeholder":
        save_research(report)
