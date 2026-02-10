#!/usr/bin/env python3
"""
Research Scraper - Use Smooth.sh to pull fundamental data
"""

import sys
from smooth_client import SmoothClient

def research_stock(ticker):
    """Scrape Yahoo Finance for stock fundamentals"""
    
    client = SmoothClient()
    
    task = f"""
    Go to Yahoo Finance and research {ticker}. 
    Extract and return:
    - Current price
    - P/E ratio
    - Revenue (TTM)
    - Revenue growth YoY
    - Earnings per share (EPS)
    - Market cap
    - 52-week high/low
    - Analyst consensus (Strong Buy/Buy/Hold/Sell/Strong Sell)
    - Price target (median analyst estimate)
    
    Format as clean bullet points.
    """
    
    print(f"🔍 Researching {ticker} on Yahoo Finance...")
    result = client.run_task(task, wait_for_result=True, timeout=90)
    
    if result["status"] == "completed":
        print(f"\n📊 {ticker} Fundamentals:")
        print("=" * 60)
        print(result["result"])
        print("=" * 60)
        
        # Save to file
        output_file = f"../research/{ticker}-fundamentals.txt"
        with open(output_file, "w") as f:
            f.write(f"{ticker} Fundamentals (Smooth.sh scrape)\n")
            f.write("=" * 60 + "\n\n")
            f.write(result["result"])
        
        print(f"\n✅ Saved to {output_file}")
    else:
        print(f"❌ Task failed: {result.get('error', 'Unknown error')}")
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 research_scraper.py TICKER")
        print("Example: python3 research_scraper.py PLTR")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    research_stock(ticker)
