#!/usr/bin/env python3
"""Test 18-agent system on value stock candidate"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from portfolio_manager import PortfolioManager, RiskManager

# Test value stock: Progressive (PGR)
test_signal = {
    "ticker": "PGR",
    "price": 245.50,
    "catalyst": "Progressive Insurance - Strong competitive moat in auto insurance. Consistent earnings growth for 10+ years. P/E 15.2 (below industry avg 18.5). ROE 24.3%. Undervalued relative to peers. Quality management team. Steady cash flow generation. Long-term value investment with margin of safety.",
    "source": "Value Screener",
    "asset_class": "stock",
    "conviction": 8.5
}

# Initialize
risk_manager = RiskManager()
portfolio_manager = PortfolioManager(risk_manager=risk_manager)

# Run
conviction_doc = portfolio_manager.evaluate_signal(test_signal)

# Print results
print("\n" + "=" * 70)
print("🐓 VALUE STOCK EVALUATION")
print("=" * 70)
print(f"Ticker: {conviction_doc['ticker']}")
print(f"Decision: {conviction_doc['final_decision']}")
print(f"Conviction: {conviction_doc['risk_validated_conviction']}/10")
print(f"Rating: {conviction_doc['conviction_rating']}")

print(f"\nLegendary Investors:")
print(f"  Consensus: {conviction_doc['legendary_investors']['consensus']}")
print(f"  Conviction: {conviction_doc['legendary_investors']['avg_conviction']}/10")
print(f"  Votes: {conviction_doc['legendary_investors']['votes']}")

print(f"\nQuant Agents:")
print(f"  Consensus: {conviction_doc['quant_agents']['consensus']}")
print(f"  Score: {conviction_doc['quant_agents']['avg_score']}/10")
print(f"  Votes: {conviction_doc['quant_agents']['votes']}")

if conviction_doc['risk_concerns']:
    print(f"\nRisk Concerns:")
    for concern in conviction_doc['risk_concerns']:
        print(f"  - {concern}")

if conviction_doc.get('position_sizing'):
    sizing = conviction_doc['position_sizing']
    print(f"\n💰 POSITION SIZING (APPROVED FOR DEPLOYMENT):")
    print(f"  Allocation: {sizing['pct_allocation']} = {sizing['position_size']}")
    print(f"  Entry: ${sizing['entry_price']}")
    print(f"  Stop: ${sizing['stop_price']} ({sizing['stop_loss']})")
    print(f"  Max Risk: {sizing['max_risk']}")
else:
    print(f"\n❌ NOT APPROVED FOR DEPLOYMENT")

print("=" * 70)
