#!/usr/bin/env python3
"""
Weekly Report Generator - Automated performance summary
Generates Friday EOD report with positions, P&L, lessons
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

def load_journal():
    """Load performance journal entries"""
    journal_path = Path(__file__).parent.parent / "performance-journal.jsonl"
    
    entries = []
    with open(journal_path) as f:
        for line in f:
            entries.append(json.loads(line))
    
    return entries

def calculate_weekly_stats(entries):
    """Calculate week-over-week statistics"""
    
    # Get this week's entries (last 7 days)
    week_entries = entries[-7:] if len(entries) >= 7 else entries
    
    if not week_entries:
        return None
    
    week_start = week_entries[0]
    week_end = week_entries[-1]
    
    # Calculate stats
    starting_value = week_start["portfolio_value"]
    ending_value = week_end["portfolio_value"]
    week_pnl = ending_value - starting_value
    week_pnl_pct = (week_pnl / starting_value) * 100
    
    # Best/worst days
    best_day = max(week_entries, key=lambda x: x["pnl_day"])
    worst_day = min(week_entries, key=lambda x: x["pnl_day"])
    
    # Position performance
    positions = week_end.get("positions", [])
    winners = [p for p in positions if p["pnl"] > 0]
    losers = [p for p in positions if p["pnl"] < 0]
    
    return {
        "period": f"{week_start['date']} to {week_end['date']}",
        "starting_value": starting_value,
        "ending_value": ending_value,
        "week_pnl": week_pnl,
        "week_pnl_pct": week_pnl_pct,
        "best_day": best_day,
        "worst_day": worst_day,
        "positions": positions,
        "winners": winners,
        "losers": losers,
        "win_rate": len(winners) / len(positions) * 100 if positions else 0
    }

def generate_lessons(stats):
    """Generate lessons learned from the week"""
    
    lessons = []
    
    if stats["week_pnl"] < 0:
        lessons.append("📉 Down week - tested stop discipline")
        lessons.append(f"   Worst day: {stats['worst_day']['date']} ({stats['worst_day']['pnl_day']:+,.0f})")
    else:
        lessons.append("📈 Green week - momentum building")
        lessons.append(f"   Best day: {stats['best_day']['date']} ({stats['best_day']['pnl_day']:+,.0f})")
    
    if stats["win_rate"] > 60:
        lessons.append(f"✅ High win rate ({stats['win_rate']:.0f}%) - selection process working")
    elif stats["win_rate"] < 40:
        lessons.append(f"⚠️  Low win rate ({stats['win_rate']:.0f}%) - need better entry timing")
    
    # Conviction lessons
    for pos in stats["losers"]:
        if pos["pnl_pct"] < -10:
            lessons.append(f"🔴 {pos['ticker']}: Down {pos['pnl_pct']:.1f}% - reassess thesis")
    
    for pos in stats["winners"]:
        if pos["pnl_pct"] > 10:
            lessons.append(f"🟢 {pos['ticker']}: Up {pos['pnl_pct']:.1f}% - conviction rewarded")
    
    return lessons

def generate_report():
    """Generate complete weekly report"""
    
    entries = load_journal()
    stats = calculate_weekly_stats(entries)
    
    if not stats:
        print("❌ Not enough data for weekly report")
        return
    
    lessons = generate_lessons(stats)
    
    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    report = f"""
🐓 Weekly Performance Report
{stats['period']}
Generated: {timestamp}

{'=' * 60}

📊 PORTFOLIO SUMMARY
{'=' * 60}

Starting Value: ${stats['starting_value']:,.0f}
Ending Value:   ${stats['ending_value']:,.0f}
Week P&L:       ${stats['week_pnl']:+,.0f} ({stats['week_pnl_pct']:+.2f}%)

Best Day:  {stats['best_day']['date']} (${stats['best_day']['pnl_day']:+,.0f})
Worst Day: {stats['worst_day']['date']} (${stats['worst_day']['pnl_day']:+,.0f})

{'=' * 60}

💼 POSITIONS ({len(stats['positions'])} active)
{'=' * 60}

"""
    
    for pos in stats["positions"]:
        status = "🟢" if pos["pnl"] > 0 else "🔴"
        report += f"{status} {pos['ticker']}: ${pos['current']:.2f} ({pos['pnl_pct']:+.1f}%) | ${pos['pnl']:+,.0f}\n"
    
    report += f"\nWin Rate: {stats['win_rate']:.0f}% ({len(stats['winners'])}/{len(stats['positions'])} positions)\n"
    
    report += f"\n{'=' * 60}\n\n"
    report += f"📚 LESSONS LEARNED\n"
    report += f"{'=' * 60}\n\n"
    
    for lesson in lessons:
        report += f"{lesson}\n"
    
    report += f"\n{'=' * 60}\n\n"
    report += "🎯 NEXT WEEK\n"
    report += f"{'=' * 60}\n\n"
    report += "• Review underperformers - exit or hold?\n"
    report += "• Deploy 1-2 new positions from priority list\n"
    report += "• Maintain stop discipline\n"
    report += "• Build in public - share wins AND losses\n"
    
    print(report)
    
    # Save to file
    output_file = Path(__file__).parent.parent / "weekly-report.txt"
    with open(output_file, "w") as f:
        f.write(report)
    
    print(f"\n✅ Report saved to {output_file}")
    
    return report

if __name__ == "__main__":
    generate_report()
