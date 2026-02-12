#!/usr/bin/env python3
"""Quick test of 18-agent system without pandas dependency"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from portfolio_manager import PortfolioManager, RiskManager

# Test signal
test_signal = {
    "ticker": "TAO",
    "price": 176.05,
    "catalyst": "AI + blockchain intersection, Yieldschool conviction 8.5/10, strong fundamentals, oversold RSI, long-term growth potential",
    "source": "Yieldschool",
    "asset_class": "crypto",
    "conviction": 8.5
}

# Initialize
risk_manager = RiskManager()
portfolio_manager = PortfolioManager(risk_manager=risk_manager)

# Run
conviction_doc = portfolio_manager.evaluate_signal(test_signal)

# Print key results
print("\n" + "=" * 70)
print("🐓 18-AGENT SYSTEM TEST RESULTS")
print("=" * 70)
print(f"Ticker: {conviction_doc['ticker']}")
print(f"Decision: {conviction_doc['final_decision']}")
print(f"Conviction: {conviction_doc['risk_validated_conviction']}/10")
print(f"Legendary Consensus: {conviction_doc['legendary_investors']['consensus']}")
print(f"Quant Consensus: {conviction_doc['quant_agents']['consensus']}")

if conviction_doc['risk_concerns']:
    print(f"\nRisk Concerns:")
    for concern in conviction_doc['risk_concerns']:
        print(f"  - {concern}")

if conviction_doc.get('position_sizing'):
    sizing = conviction_doc['position_sizing']
    print(f"\nPosition Sizing:")
    print(f"  Allocation: {sizing['pct_allocation']}")
    print(f"  Size: {sizing['position_size']}")
    print(f"  Stop: ${sizing['stop_price']}")

print("\n✅ 18-Agent System Working!")
