#!/usr/bin/env python3
"""
Post midday tweet (w2-6) via Smooth.sh
"""

import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/trading/apps')

from smooth_client import SmoothClient

def main():
    client = SmoothClient()
    
    # Tweet content from w2-6
    tweet_content = """How we validate signals:

1️⃣ Social: Dumb Money Discord reactions (18+ = strong)
2️⃣ Fundamental: Screener (P/E, ROE, debt)
3️⃣ Technical: Chart structure + volume
4️⃣ Catalyst: Earnings, news, insider activity
5️⃣ Analyst: Consensus + recent upgrades

Multi-source or no trade."""
    
    task = f"""
    Go to x.com and log in as @roostrcapital (if not already logged in).
    
    Then compose a new tweet with this exact content:
    
    {tweet_content}
    
    Post the tweet.
    
    After posting, get the tweet URL from the browser and report it back.
    """
    
    print("🐓 Posting midday tweet (w2-6) via Smooth.sh...")
    print("="*60)
    print(f"Content:\n{tweet_content}\n")
    print("="*60)
    
    result = client.run_task(task, wait_for_result=True, timeout=180)
    
    print("\n" + "="*60)
    print("Result:")
    print(f"  Status: {result['status']}")
    if result['status'] == 'completed':
        print(f"  ✅ Tweet posted!")
        print(f"  Result: {result.get('result', 'N/A')}")
        return result.get('result', '')
    else:
        print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
        return None

if __name__ == "__main__":
    main()
