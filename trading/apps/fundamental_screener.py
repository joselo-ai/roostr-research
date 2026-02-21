#!/usr/bin/env python3
"""
Fundamental Screener - Quick value/quality scan using yfinance

Screens for:
- Low P/E (< 15)
- High ROE (> 15%)
- Strong margins
- Revenue growth
- Low debt
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

def screen_stocks():
    """Screen stocks for value/quality"""
    
    print("🐓 Fundamental Screener - Starting scan...\n")
    
    # Watchlist to screen
    watchlist = [
        # Insurance (our bucket)
        "ALL", "PGR", "TRV", "CB", "AIG",
        
        # Value candidates
        "INTC", "BAC", "WFC", "JPM", "XOM", "CVX",
        
        # Growth at reasonable price
        "GOOGL", "META", "MSFT", "NVDA", "AMD",
        
        # Small/mid caps
        "KTB", "ASTS", "RKLB", "PLTR"
    ]
    
    signals = []
    
    for ticker in watchlist:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key metrics
            pe = info.get('trailingPE', None)
            roe = info.get('returnOnEquity', None)
            profit_margin = info.get('profitMargins', None)
            debt_to_equity = info.get('debtToEquity', None)
            revenue_growth = info.get('revenueGrowth', None)
            price = info.get('currentPrice', 0)
            
            # Skip if missing critical data
            if not pe or not price:
                continue
            
            # Calculate conviction score
            conviction = 5.0  # Baseline
            
            # P/E scoring
            if pe < 10:
                conviction += 2.0
            elif pe < 15:
                conviction += 1.0
            elif pe > 30:
                conviction -= 1.0
            
            # ROE scoring
            if roe and roe > 0.20:  # >20%
                conviction += 1.5
            elif roe and roe > 0.15:  # >15%
                conviction += 0.5
            
            # Margin scoring
            if profit_margin and profit_margin > 0.15:
                conviction += 1.0
            
            # Growth scoring
            if revenue_growth and revenue_growth > 0.10:
                conviction += 1.0
            
            # Debt penalty
            if debt_to_equity and debt_to_equity > 1.5:
                conviction -= 1.0
            
            # Cap at 10
            conviction = min(conviction, 10.0)
            
            signal = {
                'ticker': ticker,
                'price': price,
                'pe': pe,
                'roe': roe * 100 if roe else None,
                'profit_margin': profit_margin * 100 if profit_margin else None,
                'debt_to_equity': debt_to_equity,
                'revenue_growth': revenue_growth * 100 if revenue_growth else None,
                'conviction': round(conviction, 1),
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Fundamental Screener'
            }
            
            signals.append(signal)
            
            # Print results
            status = "🟢" if conviction >= 7.0 else "🟡" if conviction >= 5.0 else "🔴"
            print(f"{status} {ticker}: {conviction}/10 | P/E: {pe:.1f} | ROE: {roe*100 if roe else 'N/A':.1f}%")
            
        except Exception as e:
            print(f"❌ {ticker}: Error - {e}")
            continue
    
    # Sort by conviction
    signals.sort(key=lambda x: x['conviction'], reverse=True)
    
    # Filter high conviction
    high_conviction = [s for s in signals if s['conviction'] >= 7.0]
    
    print(f"\n{'='*60}")
    print(f"🎯 RESULTS: {len(high_conviction)}/{len(signals)} high-conviction (≥7.0)")
    print('='*60)
    
    for signal in high_conviction:
        print(f"\n🟢 {signal['ticker']}: {signal['conviction']}/10")
        print(f"   Price: ${signal['price']:.2f} | P/E: {signal['pe']:.1f}")
        print(f"   ROE: {signal['roe']:.1f}% | Margin: {signal['profit_margin']:.1f}%")
        print(f"   Revenue Growth: {signal['revenue_growth']:.1f}%")
    
    # Save results
    import json
    output_file = '/Users/agentjoselo/.openclaw/workspace/trading/fundamental-signals.json'
    with open(output_file, 'w') as f:
        json.dump(signals, f, indent=2)
    
    print(f"\n💾 Saved {len(signals)} signals to {output_file}")
    
    return high_conviction

if __name__ == "__main__":
    screen_stocks()
