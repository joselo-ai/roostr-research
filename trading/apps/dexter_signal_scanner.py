#!/usr/bin/env python3
"""
Dexter Signal Scanner - Hunt signals using financial research agent

Uses Dexter to scan for high-conviction opportunities across:
- Trending stocks (Reddit, Twitter mentions)
- Unusual options activity
- Earnings beats
- Insider buying
"""

import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/trading/apps')

from dexter_research import DexterResearchEngine
import yfinance as yf
from datetime import datetime, timedelta
import json

def get_trending_tickers():
    """Get trending stock tickers to research"""
    
    # Start with watchlist + recent movers
    watchlist = [
        "ASTS",  # From our existing analysis
        "NVDA",  # AI momentum
        "PLTR",  # AI government contracts
        "TSLA",  # EV leader
        "META",  # AI ads
        "AMD",   # AI chips
        "COIN",  # Crypto exposure
        "SHOP",  # E-commerce
        "RBLX",  # Metaverse
        "U",     # Cloud growth
    ]
    
    return watchlist

def scan_for_signals():
    """Scan tickers using Dexter for high-conviction plays"""
    
    print("🐓 Dexter Signal Scanner - Starting hunt...\n")
    
    engine = DexterResearchEngine(timeout=120)
    tickers = get_trending_tickers()
    
    signals = []
    
    for ticker in tickers[:3]:  # Start with top 3 to test
        print(f"\n{'='*60}")
        print(f"Researching: {ticker}")
        print('='*60)
        
        try:
            # Run Dexter research
            research = engine.research_ticker(
                ticker=ticker,
                focus_areas=['fundamentals', 'valuation', 'catalysts']
            )
            
            # Extract signal data
            signal = {
                'ticker': ticker,
                'conviction': research.get('conviction', 5.0),
                'recommendation': research.get('recommendation', 'HOLD'),
                'summary': research.get('summary', ''),
                'catalysts': research.get('catalysts', []),
                'risks': research.get('risks', []),
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Dexter',
                'research_time': research.get('research_time', 0)
            }
            
            signals.append(signal)
            
            # Show results
            print(f"\n✅ {ticker}: {signal['recommendation']} ({signal['conviction']}/10)")
            print(f"📝 {signal['summary'][:200]}...")
            
            # Save research
            engine.save_research(research)
            
        except Exception as e:
            print(f"❌ Error researching {ticker}: {e}")
            continue
    
    # Filter for high conviction (≥7.0)
    high_conviction = [s for s in signals if s['conviction'] >= 7.0]
    
    print("\n" + "="*60)
    print(f"🎯 RESULTS: {len(high_conviction)}/{len(signals)} high-conviction signals (≥7.0)")
    print("="*60)
    
    for signal in high_conviction:
        print(f"\n🟢 {signal['ticker']}: {signal['conviction']}/10 ({signal['recommendation']})")
        print(f"   {signal['summary'][:150]}...")
    
    # Save signals
    output_file = '/Users/agentjoselo/.openclaw/workspace/trading/dexter-signals.json'
    with open(output_file, 'w') as f:
        json.dump(signals, f, indent=2)
    
    print(f"\n💾 Saved {len(signals)} signals to {output_file}")
    
    return high_conviction

if __name__ == "__main__":
    scan_for_signals()
