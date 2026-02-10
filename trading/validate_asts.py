#!/usr/bin/env python3
"""
Quick validator for $ASTS using Google Trends
No API credentials needed - runs immediately
"""

import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/trading/apps')

from google_trends_validator import GoogleTrendsValidator

def main():
    print("🔍 Validating $ASTS Social Sentiment...\n")
    
    validator = GoogleTrendsValidator()
    
    # Check 1-month trend
    result_1m = validator.check_ticker_trend('ASTS', timeframe='today 1-m')
    
    # Check 3-month trend
    result_3m = validator.check_ticker_trend('ASTS', timeframe='today 3-m')
    
    print("=" * 60)
    print("$ASTS GOOGLE TRENDS ANALYSIS")
    print("=" * 60)
    
    print("\n📊 1-Month Trend:")
    print(f"   Status: {result_1m.get('trend', 'N/A')}")
    print(f"   Change: {result_1m.get('change_percent', 0):+.1f}%")
    print(f"   Current Interest: {result_1m.get('current_interest', 0)}/100")
    print(f"   Average Interest: {result_1m.get('avg_interest', 0)}/100")
    print(f"   Validated: {'✅ YES' if result_1m.get('validated') else '❌ NO'}")
    
    print("\n📊 3-Month Trend:")
    print(f"   Status: {result_3m.get('trend', 'N/A')}")
    print(f"   Change: {result_3m.get('change_percent', 0):+.1f}%")
    print(f"   Current Interest: {result_3m.get('current_interest', 0)}/100")
    print(f"   Average Interest: {result_3m.get('avg_interest', 0)}/100")
    print(f"   Validated: {'✅ YES' if result_3m.get('validated') else '❌ NO'}")
    
    # Decision logic
    print("\n🎯 DEPLOYMENT DECISION:")
    
    if result_1m.get('trend') == 'RISING' and result_1m.get('validated'):
        print("   ✅ GREEN - Deploy capital")
        print("   Reason: 1-month trend RISING, above average interest")
    elif result_1m.get('trend') == 'STABLE':
        print("   🟡 YELLOW - Wait for pullback or catalyst")
        print("   Reason: Interest stable, not building momentum yet")
    elif result_1m.get('trend') == 'FALLING':
        print("   🔴 RED - Pass for now")
        print("   Reason: Interest declining, may be late to party")
    else:
        print("   ⚪ UNKNOWN - Need more data")
    
    print("\n" + "=" * 60)
    print("📝 NOTES:")
    print("   • RISING + validated = early stage (good entry)")
    print("   • STABLE = no momentum (wait for catalyst)")
    print("   • FALLING = late stage (already peaked)")
    print("   • Check again after FCC news or partnership announcement")
    print("=" * 60)

if __name__ == "__main__":
    main()
