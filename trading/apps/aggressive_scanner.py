#!/usr/bin/env python3
"""
Aggressive Market Scanner - Cast wider net, show ALL opportunities

Find ANY stock with edge - then let 18 agents filter
"""

import yfinance as yf
from datetime import datetime
import json

def scan_everything():
    """Scan with looser criteria - find anything interesting"""
    
    print("🐓 Aggressive Scanner - Finding ANY edge\n")
    
    # Expanded universe
    universe = [
        # Value plays
        "ALL", "PGR", "TRV", "CB", "AFL", "MET", "PRU", "AIG",
        "BAC", "WFC", "C", "JPM", "GS", "MS", "BK", "STT",
        "INTC", "IBM", "HPQ", "CSCO", "ORCL",
        
        # Growth
        "NVDA", "AMD", "AVGO", "QCOM", "AMAT", "LRCX",
        "PLTR", "SNOW", "DDOG", "CRWD", "ZS", "NET", "S",
        
        # Consumer
        "NKE", "LULU", "DECK", "CROX", "DKS", "FL",
        
        # Aerospace/Defense  
        "ASTS", "RKLB", "LMT", "RTX", "BA", "GD", "NOC",
        
        # Beaten down / Turnaround
        "DIS", "PYPL", "SQ", "COIN", "HOOD", "SOFI",
        "F", "GM", "RIVN", "LCID",
        
        # Commodity
        "XOM", "CVX", "COP", "SLB", "HAL",
        "FCX", "NEM", "GOLD"
    ]
    
    signals = []
    
    for ticker in universe:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            price = info.get('currentPrice', 0)
            pe = info.get('trailingPE')
            roe = info.get('returnOnEquity')
            margin = info.get('profitMargins')
            growth = info.get('revenueGrowth')
            debt_eq = info.get('debtToEquity', 0)
            
            if not price or price == 0:
                continue
            
            # Score each stock
            score = 5.0  # Baseline
            reasons = []
            
            # P/E scoring
            if pe:
                if pe < 10:
                    score += 2.0
                    reasons.append(f"P/E {pe:.1f} (cheap)")
                elif pe < 15:
                    score += 1.0
                    reasons.append(f"P/E {pe:.1f} (reasonable)")
                elif pe > 40:
                    score -= 1.0
                    reasons.append(f"P/E {pe:.1f} (expensive)")
            
            # ROE scoring
            if roe:
                if roe > 0.30:
                    score += 2.0
                    reasons.append(f"ROE {roe*100:.0f}% (exceptional)")
                elif roe > 0.20:
                    score += 1.5
                    reasons.append(f"ROE {roe*100:.0f}% (strong)")
                elif roe > 0.15:
                    score += 0.5
                    reasons.append(f"ROE {roe*100:.0f}% (good)")
            
            # Margin scoring
            if margin:
                if margin > 0.20:
                    score += 1.0
                    reasons.append(f"Margin {margin*100:.0f}% (high)")
            
            # Growth scoring
            if growth:
                if growth > 0.15:
                    score += 1.5
                    reasons.append(f"Growth +{growth*100:.0f}% (strong)")
                elif growth > 0.10:
                    score += 0.5
                    reasons.append(f"Growth +{growth*100:.0f}% (decent)")
            
            # Debt penalty
            if debt_eq and debt_eq > 2.0:
                score -= 1.0
                reasons.append(f"Debt/Eq {debt_eq:.1f} (high)")
            
            score = min(score, 10.0)
            
            if score >= 5.5:  # Show anything above mediocre
                signals.append({
                    'ticker': ticker,
                    'score': round(score, 1),
                    'price': price,
                    'pe': pe,
                    'roe': roe * 100 if roe else None,
                    'margin': margin * 100 if margin else None,
                    'growth': growth * 100 if growth else None,
                    'reasons': ', '.join(reasons) if reasons else 'Basic quality'
                })
        except Exception as e:
            continue
    
    # Sort by score
    signals.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"{'='*70}")
    print(f"🎯 FOUND {len(signals)} OPPORTUNITIES (score ≥5.5)")
    print(f"{'='*70}\n")
    
    # Show top 20
    for i, s in enumerate(signals[:20], 1):
        emoji = "🟢" if s['score'] >= 7.0 else "🟡"
        print(f"{i}. {emoji} {s['ticker']}: {s['score']}/10 @ ${s['price']:.2f}")
        print(f"   {s['reasons']}")
        print()
    
    # Save all
    output = '/Users/agentjoselo/.openclaw/workspace/trading/aggressive-scan-results.json'
    with open(output, 'w') as f:
        json.dump(signals, f, indent=2)
    
    print(f"💾 Saved {len(signals)} signals to {output}")
    
    # Top candidates for 18-agent review
    top_candidates = [s for s in signals if s['score'] >= 7.0]
    print(f"\n🎯 {len(top_candidates)} candidates ≥7.0 ready for 18-agent deliberation:")
    for s in top_candidates[:5]:
        print(f"   - {s['ticker']} ({s['score']}/10)")
    
    return signals

if __name__ == "__main__":
    scan_everything()
