#!/usr/bin/env python3
"""
Performance Analyzer - roostr Trading Journal Analysis
Reads performance-journal.jsonl and generates insights
"""

import json
from datetime import datetime
from pathlib import Path

def analyze_journal():
    journal_path = Path(__file__).parent.parent / "performance-journal.jsonl"
    
    if not journal_path.exists():
        print("❌ No journal found")
        return
    
    entries = []
    with open(journal_path) as f:
        for line in f:
            entries.append(json.loads(line))
    
    if not entries:
        print("❌ Journal empty")
        return
    
    print(f"🐓 Performance Analysis ({len(entries)} days)")
    print("=" * 60)
    
    # Overall stats
    start_value = entries[0]["portfolio_value"]
    current_value = entries[-1]["portfolio_value"]
    total_return = current_value - start_value
    total_return_pct = (total_return / start_value) * 100
    
    print(f"\n📊 Portfolio Summary:")
    print(f"   Start:   ${start_value:,.0f}")
    print(f"   Current: ${current_value:,.0f}")
    print(f"   P&L:     ${total_return:+,.0f} ({total_return_pct:+.2f}%)")
    
    # Best/worst days
    best_day = max(entries, key=lambda x: x["pnl_day"])
    worst_day = min(entries, key=lambda x: x["pnl_day"])
    
    print(f"\n📈 Best Day:  {best_day['date']} ({best_day['pnl_day']:+,.0f})")
    print(f"📉 Worst Day: {worst_day['date']} ({worst_day['pnl_day']:+,.0f})")
    
    # Position performance
    print(f"\n💼 Current Positions:")
    for pos in entries[-1]["positions"]:
        status = "🟢" if pos["pnl"] > 0 else "🔴"
        print(f"   {status} {pos['ticker']}: ${pos['current']:.2f} ({pos['pnl_pct']:+.1f}%) | P&L: ${pos['pnl']:+,.0f}")
    
    # Daily P&L trend
    print(f"\n📅 Daily P&L:")
    for entry in entries:
        trend = "🟢" if entry["pnl_day"] >= 0 else "🔴"
        print(f"   {trend} {entry['date']}: ${entry['pnl_day']:+,.0f}")
    
    # Notes
    print(f"\n📝 Recent Note:")
    print(f"   {entries[-1]['notes']}")
    
    print("=" * 60)

if __name__ == "__main__":
    analyze_journal()
