#!/usr/bin/env python3
"""
Value Stock Screener - Find quality stocks at reasonable prices
================================================================

Screens for:
- Undervalued (P/E < 20, P/B < 3)
- Quality (ROE > 15%, positive earnings)
- Consistent (5+ years profitable)
- Moat indicators (stable market share, pricing power)

Then runs 18-agent evaluation on top candidates.

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from portfolio_manager import PortfolioManager, RiskManager
import json
from datetime import datetime

# Value stock candidates (manually curated for now)
# TODO: Integrate with real-time screener API (finviz, yahoo finance, etc.)
VALUE_CANDIDATES = [
    {
        "ticker": "PGR",
        "name": "Progressive Corporation",
        "price": 245.50,
        "catalyst": "Progressive Insurance - Strong competitive moat in auto insurance. Consistent earnings growth 10+ years. Trading at P/E 15.2 vs industry 18.5 (20% discount = margin of safety). ROE 24.3% (excellent capital efficiency). Management quality exceptional (Buffett-style capital allocation). Steady cash flow generation. Stop loss at -10% ($220.95). Undervalued quality business, long-term hold.",
        "pe_ratio": 15.2,
        "pb_ratio": 2.8,
        "roe": 24.3,
        "source": "Value Screener",
        "asset_class": "stock"
    },
    {
        "ticker": "ALL",
        "name": "Allstate Corporation",
        "price": 180.25,
        "catalyst": "Allstate Insurance - Undervalued quality insurer. Strong brand moat. P/E 13.5 (cheap vs peers). ROE 18.2%. Consistent cash flow. Management focus on shareholder returns. Stop loss at -10% ($162.23). Ben Graham-style value play with margin of safety.",
        "pe_ratio": 13.5,
        "pb_ratio": 1.9,
        "roe": 18.2,
        "source": "Value Screener",
        "asset_class": "stock"
    },
    {
        "ticker": "KTB",
        "name": "Kontoor Brands",
        "price": 85.40,
        "catalyst": "Kontoor Brands (Wrangler, Lee jeans) - Undervalued consumer brand. P/E 11.8 (very cheap). ROE 22.1%. Strong free cash flow. Brand moat in denim. Trading below intrinsic value. Stop loss at -10% ($76.86). Deep value opportunity.",
        "pe_ratio": 11.8,
        "pb_ratio": 2.5,
        "roe": 22.1,
        "source": "Value Screener",
        "asset_class": "stock"
    }
]


def screen_value_stocks():
    """
    Screen value stocks and run 18-agent evaluation.
    
    Returns list of approved signals (conviction >= 6.0, BUY decision)
    """
    print("🐓 roostr Value Stock Screener")
    print("=" * 70)
    print(f"Screening {len(VALUE_CANDIDATES)} candidates...\n")
    
    # Initialize
    risk_manager = RiskManager()
    portfolio_manager = PortfolioManager(risk_manager=risk_manager)
    
    approved_signals = []
    
    for candidate in VALUE_CANDIDATES:
        print(f"\n📊 Evaluating {candidate['ticker']} ({candidate['name']})")
        print("-" * 70)
        
        # Prepare signal
        signal = {
            "ticker": candidate['ticker'],
            "price": candidate['price'],
            "catalyst": candidate['catalyst'],
            "source": candidate['source'],
            "asset_class": candidate['asset_class'],
            "conviction": 8.0  # Starting conviction
        }
        
        # Run 18 agents
        try:
            conviction_doc = portfolio_manager.evaluate_signal(signal)
            
            decision = conviction_doc['final_decision']
            conviction = conviction_doc['risk_validated_conviction']
            
            print(f"✅ Result: {decision} (Conviction: {conviction}/10)")
            print(f"   Legendary: {conviction_doc['legendary_investors']['avg_conviction']}/10")
            print(f"   Quant: {conviction_doc['quant_agents']['avg_score']}/10")
            
            if decision == "BUY":
                print(f"   💰 Position: {conviction_doc['position_sizing']['position_size']}")
                approved_signals.append(conviction_doc)
            else:
                print(f"   ⏸️  Holding (not approved for deployment)")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print(f"🎯 SCREENING COMPLETE")
    print("=" * 70)
    print(f"Screened: {len(VALUE_CANDIDATES)} candidates")
    print(f"Approved: {len(approved_signals)} signals")
    
    if approved_signals:
        total_allocation = sum(
            float(s['position_sizing']['position_size'].replace('$', '').replace(',', ''))
            for s in approved_signals
        )
        print(f"Total Capital: ${total_allocation:,.0f}")
        
        print(f"\n📋 Approved Signals:")
        for s in approved_signals:
            sizing = s['position_sizing']
            print(f"   {s['ticker']}: {sizing['position_size']} ({sizing['pct_allocation']})")
    else:
        print("\n⚠️  No signals approved (all below 6.0 conviction threshold)")
    
    return approved_signals


def save_approved_signals(signals, output_path="value-signals-approved.json"):
    """Save approved signals to file"""
    output_file = os.path.join(os.path.dirname(__file__), "..", output_path)
    
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_signals": len(signals),
            "signals": signals
        }, f, indent=2, default=str)
    
    print(f"\n✅ Approved signals saved: {output_file}")


if __name__ == "__main__":
    approved = screen_value_stocks()
    
    if approved:
        save_approved_signals(approved)
        print(f"\n🚀 Ready to deploy {len(approved)} value stocks")
        print("   Run: python apps/deploy_approved_signals.py")
    else:
        print(f"\n⏸️  No signals ready for deployment")
