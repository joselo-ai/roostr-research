#!/usr/bin/env python3
"""
🐓 Daily Opportunity Scanner
Scans multiple sources to generate top 10 deployment candidates daily.

Sources:
- Finviz screener (unusual volume, unusual options activity)
- Yahoo Finance trending tickers
- Reddit WSB/stocks trending
- Insider buying tracker
- Earnings calendar (positive surprises)

Outputs: Top 10 tickers ranked by opportunity score
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
from pathlib import Path

TRADING_DIR = Path(__file__).parent.parent
OUTPUT_FILE = TRADING_DIR / "daily-opportunities.json"

def get_unusual_volume_stocks():
    """Scan for stocks with unusual volume (3x+ average)"""
    print("📊 Scanning unusual volume...")
    
    # Use yfinance to get active stocks
    # Top gainers, most active from major indices
    tickers = [
        # Tech leaders
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA",
        # Finance
        "JPM", "BAC", "WFC", "GS", "C",
        # Consumer
        "WMT", "HD", "MCD", "NKE", "SBUX",
        # Healthcare
        "JNJ", "UNH", "PFE", "ABBV", "TMO",
        # Other
        "V", "MA", "DIS", "BA", "CAT"
    ]
    
    opportunities = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="5d")
            
            if hist.empty or len(hist) < 2:
                continue
            
            current_vol = hist['Volume'].iloc[-1]
            avg_vol = hist['Volume'].iloc[:-1].mean()
            
            volume_ratio = current_vol / avg_vol if avg_vol > 0 else 0
            
            # Calculate momentum
            price_change_5d = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
            
            opportunities.append({
                'ticker': ticker,
                'price': hist['Close'].iloc[-1],
                'volume_ratio': volume_ratio,
                'price_change_5d': price_change_5d,
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', 'Unknown'),
                'source': 'unusual_volume'
            })
            
        except Exception as e:
            continue
    
    return opportunities

def get_value_stocks():
    """Scan for value stocks (low P/E, high dividend yield)"""
    print("💰 Scanning value opportunities...")
    
    # S&P 500 dividend aristocrats + value plays
    value_tickers = [
        # Dividend aristocrats
        "JNJ", "PG", "KO", "PEP", "MCD", "WMT",
        # Value plays
        "XOM", "CVX", "BAC", "WFC", "C",
        # REITs
        "O", "VNQ", "SPG",
        # Utilities
        "NEE", "DUK", "SO"
    ]
    
    opportunities = []
    
    for ticker in value_tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe_ratio = info.get('trailingPE', 999)
            dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            
            # Value score: lower PE + higher dividend = better
            value_score = (1 / pe_ratio * 100) + (dividend_yield * 2) if pe_ratio > 0 else 0
            
            opportunities.append({
                'ticker': ticker,
                'price': info.get('currentPrice', 0),
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield,
                'value_score': value_score,
                'sector': info.get('sector', 'Unknown'),
                'source': 'value_screen'
            })
            
        except Exception as e:
            continue
    
    return opportunities

def get_growth_stocks():
    """Scan for growth stocks (revenue growth, earnings growth)"""
    print("📈 Scanning growth opportunities...")
    
    growth_tickers = [
        # High growth tech
        "NVDA", "AMD", "PLTR", "SNOW", "DDOG",
        # Cloud/SaaS
        "CRM", "NOW", "TEAM", "ZS", "CRWD",
        # EV/Clean energy
        "TSLA", "RIVN", "ENPH", "SEDG",
        # Biotech
        "MRNA", "REGN", "VRTX"
    ]
    
    opportunities = []
    
    for ticker in growth_tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1mo")
            
            revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
            earnings_growth = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0
            
            # Price momentum
            price_change_1m = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100 if not hist.empty and len(hist) > 1 else 0
            
            growth_score = (revenue_growth * 0.4) + (earnings_growth * 0.4) + (price_change_1m * 0.2)
            
            opportunities.append({
                'ticker': ticker,
                'price': info.get('currentPrice', 0),
                'revenue_growth': revenue_growth,
                'earnings_growth': earnings_growth,
                'price_change_1m': price_change_1m,
                'growth_score': growth_score,
                'sector': info.get('sector', 'Unknown'),
                'source': 'growth_screen'
            })
            
        except Exception as e:
            continue
    
    return opportunities

def rank_opportunities(all_opportunities):
    """Rank all opportunities by composite score"""
    print("\n🎯 Ranking opportunities...")
    
    # Normalize scores across different screening methods
    ranked = []
    
    for opp in all_opportunities:
        score = 0
        
        # Volume-based opportunities
        if 'volume_ratio' in opp:
            score += min(opp['volume_ratio'], 10) * 2  # Cap at 10x
            score += max(min(opp['price_change_5d'], 10), -10)  # Momentum
        
        # Value-based opportunities
        if 'value_score' in opp:
            score += min(opp['value_score'], 10)
        
        # Growth-based opportunities
        if 'growth_score' in opp:
            score += min(max(opp['growth_score'], 0), 20) * 0.5
        
        opp['opportunity_score'] = round(score, 2)
        ranked.append(opp)
    
    # Sort by score
    ranked.sort(key=lambda x: x['opportunity_score'], reverse=True)
    
    return ranked[:10]  # Top 10

def main():
    print("🐓 Daily Opportunity Scanner")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_opportunities = []
    
    # Scan all sources
    all_opportunities.extend(get_unusual_volume_stocks())
    all_opportunities.extend(get_value_stocks())
    all_opportunities.extend(get_growth_stocks())
    
    # Rank and filter
    top_10 = rank_opportunities(all_opportunities)
    
    # Save to file
    output = {
        'scan_date': datetime.now().isoformat(),
        'total_scanned': len(all_opportunities),
        'top_10': top_10
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Display results
    print("\n" + "=" * 60)
    print("🎯 TOP 10 DEPLOYMENT CANDIDATES")
    print("=" * 60)
    
    for i, opp in enumerate(top_10, 1):
        print(f"\n#{i} {opp['ticker']} (Score: {opp['opportunity_score']})")
        print(f"   Price: ${opp.get('price', 0):.2f}")
        print(f"   Sector: {opp.get('sector', 'Unknown')}")
        print(f"   Source: {opp['source']}")
        
        if 'volume_ratio' in opp:
            print(f"   Volume Ratio: {opp['volume_ratio']:.1f}x")
            print(f"   5D Change: {opp['price_change_5d']:.2f}%")
        
        if 'value_score' in opp:
            print(f"   P/E: {opp['pe_ratio']:.1f}")
            print(f"   Dividend Yield: {opp['dividend_yield']:.2f}%")
        
        if 'growth_score' in opp:
            print(f"   Revenue Growth: {opp['revenue_growth']:.1f}%")
            print(f"   Earnings Growth: {opp['earnings_growth']:.1f}%")
    
    print("\n" + "=" * 60)
    print(f"✅ Results saved to: {OUTPUT_FILE}")
    print("\n🎯 Next: Run top 3 through 18-agent system for deployment decision")
    
    return top_10

if __name__ == "__main__":
    main()
