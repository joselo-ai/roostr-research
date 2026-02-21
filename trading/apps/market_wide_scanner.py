#!/usr/bin/env python3
"""
Market-Wide Scanner - Hunt across entire universe for edge

Strategies:
1. Deep Value: Low P/E + High ROE + Hidden quality
2. Insider Buying: Recent insider purchases + good fundamentals  
3. Earnings Momentum: Recent earnings beat + revenue acceleration
4. Short Squeeze Candidates: High short interest + improving fundamentals
5. Turnaround Plays: Beaten down stocks showing recovery signs
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json

def get_sp500_tickers():
    """Get S&P 500 tickers"""
    # Using a common list - in production, fetch from Wikipedia or API
    return [
        # Top 100 S&P 500 by market cap (sample - can expand)
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
        "LLY", "V", "UNH", "XOM", "JPM", "JNJ", "WMT", "MA", "PG", "AVGO",
        "HD", "CVX", "MRK", "ABBV", "COST", "KO", "PEP", "BAC", "ORCL",
        "CSCO", "MCD", "TMO", "ACN", "ADBE", "CRM", "NFLX", "ABT", "AMD",
        "CMCSA", "DHR", "VZ", "INTC", "TXN", "WFC", "DIS", "NKE", "INTU",
        "UPS", "PM", "QCOM", "HON", "RTX", "LOW", "AMGN", "IBM", "SPGI",
        "COP", "CAT", "GE", "NEE", "SBUX", "BA", "GS", "AXP", "MMM", "DE",
        "BLK", "MDT", "LMT", "SYK", "BMY", "GILD", "PLD", "ADI", "MDLZ",
        "SCHW", "ISRG", "AMT", "VRTX", "CI", "C", "PNC", "MO", "REGN",
        "ZTS", "CB", "BKNG", "TJX", "USB", "DUK", "SO", "PYPL", "BDX",
        "MS", "PGR", "EOG", "TMUS", "CME", "EQIX", "ETN", "NOC", "SLB"
    ]

def get_russell_midcaps():
    """Get Russell mid-cap stocks"""
    return [
        # Sample mid-caps
        "ASTS", "RKLB", "PLTR", "COIN", "HOOD", "SOFI", "AFRM", "UPST",
        "OPEN", "RDFN", "KTB", "CROX", "DECK", "LULU", "CHWY", "ETSY"
    ]

def screen_deep_value(tickers):
    """Screen for deep value plays"""
    print("\n🔍 Strategy 1: Deep Value Screening...")
    signals = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe = info.get('trailingPE')
            roe = info.get('returnOnEquity')
            pb = info.get('priceToBook')
            debt_eq = info.get('debtToEquity', 999)
            price = info.get('currentPrice', 0)
            
            # Deep value criteria
            if not pe or not roe or not pb or not price:
                continue
            
            # Looking for: P/E < 10, ROE > 15%, P/B < 2, Low debt
            if pe < 10 and roe > 0.15 and pb < 2 and debt_eq < 1.0:
                conviction = 7.0 + (10 - pe) * 0.2 + (roe - 0.15) * 10
                conviction = min(conviction, 10.0)
                
                signals.append({
                    'ticker': ticker,
                    'strategy': 'Deep Value',
                    'price': price,
                    'pe': pe,
                    'roe': roe * 100,
                    'pb': pb,
                    'conviction': round(conviction, 1),
                    'catalyst': f"Hidden value: P/E {pe:.1f}, ROE {roe*100:.1f}%, P/B {pb:.1f}"
                })
                
                print(f"  🟢 {ticker}: P/E {pe:.1f}, ROE {roe*100:.1f}%, P/B {pb:.1f} - Conviction {conviction:.1f}/10")
        except:
            continue
    
    return signals

def screen_high_growth():
    """Screen for high-growth stocks at reasonable prices"""
    print("\n🔍 Strategy 2: Growth at Reasonable Price...")
    
    tickers = ["NVDA", "AMD", "PLTR", "SNOW", "NET", "DDOG", "CRWD", "ZS"]
    signals = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            revenue_growth = info.get('revenueGrowth')
            earnings_growth = info.get('earningsGrowth')
            peg = info.get('pegRatio')
            price = info.get('currentPrice', 0)
            
            if not revenue_growth or not price:
                continue
            
            # Looking for: Revenue growth > 20%, PEG < 2
            if revenue_growth > 0.20:
                conviction = 6.0 + revenue_growth * 10
                if peg and peg < 2:
                    conviction += 1.0
                
                conviction = min(conviction, 10.0)
                
                signals.append({
                    'ticker': ticker,
                    'strategy': 'High Growth',
                    'price': price,
                    'revenue_growth': revenue_growth * 100,
                    'peg': peg,
                    'conviction': round(conviction, 1),
                    'catalyst': f"Growth: Revenue +{revenue_growth*100:.1f}%, PEG {peg:.1f if peg else 'N/A'}"
                })
                
                print(f"  🟢 {ticker}: Revenue +{revenue_growth*100:.1f}% - Conviction {conviction:.1f}/10")
        except:
            continue
    
    return signals

def screen_turnarounds():
    """Screen for potential turnarounds"""
    print("\n🔍 Strategy 3: Turnaround Candidates...")
    
    # Stocks that were beaten down but showing recovery
    tickers = ["INTC", "PYPL", "DIS", "BA", "F", "GM", "WBD", "PARA"]
    signals = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="6mo")
            
            price = info.get('currentPrice', 0)
            pe = info.get('trailingPE')
            
            if not price or len(hist) < 20:
                continue
            
            # Check if down from highs
            high_6m = hist['High'].max()
            pct_from_high = ((price - high_6m) / high_6m) * 100
            
            # Recent momentum
            price_20d_ago = hist['Close'].iloc[-20] if len(hist) >= 20 else price
            recent_gain = ((price - price_20d_ago) / price_20d_ago) * 100 if price_20d_ago > 0 else 0
            
            # Looking for: Down 30%+ from highs but up 10%+ recently
            if pct_from_high < -30 and recent_gain > 10:
                conviction = 6.0 + (recent_gain / 10) * 0.5
                conviction = min(conviction, 10.0)
                
                signals.append({
                    'ticker': ticker,
                    'strategy': 'Turnaround',
                    'price': price,
                    'pct_from_high': pct_from_high,
                    'recent_gain': recent_gain,
                    'pe': pe,
                    'conviction': round(conviction, 1),
                    'catalyst': f"Recovery: {pct_from_high:.0f}% from high, +{recent_gain:.1f}% recent"
                })
                
                print(f"  🟢 {ticker}: {pct_from_high:.0f}% from high, +{recent_gain:.1f}% bounce - Conviction {conviction:.1f}/10")
        except:
            continue
    
    return signals

def screen_insider_buying():
    """Screen for insider buying (simplified - would need real data)"""
    print("\n🔍 Strategy 4: Insider Buying...")
    print("  ⚠️  Need insider data API - placeholder for now")
    return []

def main():
    print("🐓 Market-Wide Scanner - Hunting 7+ Conviction Signals")
    print("="*60)
    
    # Get universe
    sp500 = get_sp500_tickers()
    midcaps = get_russell_midcaps()
    
    all_signals = []
    
    # Run all strategies
    all_signals.extend(screen_deep_value(sp500))
    all_signals.extend(screen_high_growth())
    all_signals.extend(screen_turnarounds())
    
    # Sort by conviction
    all_signals.sort(key=lambda x: x['conviction'], reverse=True)
    
    # Filter high conviction (≥7.0)
    high_conviction = [s for s in all_signals if s['conviction'] >= 7.0]
    
    print("\n" + "="*60)
    print(f"🎯 RESULTS: {len(high_conviction)} high-conviction signals (≥7.0)")
    print("="*60)
    
    for signal in high_conviction[:10]:  # Top 10
        print(f"\n🟢 {signal['ticker']}: {signal['conviction']}/10 ({signal['strategy']})")
        print(f"   {signal['catalyst']}")
        print(f"   Price: ${signal['price']:.2f}")
    
    # Save results
    output_file = '/Users/agentjoselo/.openclaw/workspace/trading/market-wide-signals.json'
    with open(output_file, 'w') as f:
        json.dump(all_signals, f, indent=2)
    
    print(f"\n💾 Saved {len(all_signals)} signals to {output_file}")
    print(f"\n🎯 Top {min(5, len(high_conviction))} candidates ready for 18-agent deliberation")
    
    return high_conviction

if __name__ == "__main__":
    main()
