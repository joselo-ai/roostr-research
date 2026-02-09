#!/usr/bin/env python3
"""
Daily Summary Generator - roostr Trading Operations
Captures EOD snapshot for journal and summary reporting
"""

import json
from datetime import datetime
from pathlib import Path

def generate_summary():
    """Generate daily summary from current state"""
    
    # Read current prices
    price_cache = Path(__file__).parent.parent / ".price_cache.json"
    with open(price_cache) as f:
        prices = json.loads(f.read())
    
    # Read signals database to get positions
    signals_db = Path(__file__).parent.parent / "signals-database.csv"
    deployed_positions = []
    
    with open(signals_db) as f:
        for line in f:
            if line.startswith("Ticker"):
                continue  # Skip header
            parts = line.split(",")
            ticker = parts[0]
            deployed = parts[6]
            if deployed == "YES":
                entry = float(parts[3])
                current = prices.get(ticker, {}).get("price", 0)
                qty_text = [p for p in parts if "Qty:" in p]
                if qty_text:
                    qty = float(qty_text[0].split("Qty: ")[1].split(" ")[0])
                else:
                    qty = 0
                
                pnl = (current - entry) * qty
                pnl_pct = ((current - entry) / entry) * 100
                
                deployed_positions.append({
                    "ticker": ticker,
                    "entry": entry,
                    "current": current,
                    "qty": qty,
                    "pnl": round(pnl, 2),
                    "pnl_pct": round(pnl_pct, 2)
                })
    
    # Calculate portfolio
    total_pnl = sum(p["pnl"] for p in deployed_positions)
    portfolio_value = 100000 + total_pnl  # Starting capital + P&L
    
    # Generate summary
    today = datetime.now().strftime("%Y-%m-%d")
    
    summary = {
        "date": today,
        "portfolio_value": round(portfolio_value, 2),
        "pnl_day": round(total_pnl, 2),  # Simplified - would need yesterday's snapshot for true daily
        "pnl_total": round(total_pnl, 2),
        "positions": deployed_positions,
        "notes": f"Auto-generated EOD snapshot. {len(deployed_positions)} positions."
    }
    
    print("🐓 Daily Summary")
    print("=" * 60)
    print(f"📅 Date: {today}")
    print(f"💰 Portfolio: ${portfolio_value:,.0f}")
    print(f"📊 P&L: ${total_pnl:+,.0f}")
    print(f"\n📦 Positions ({len(deployed_positions)}):")
    for pos in deployed_positions:
        status = "🟢" if pos["pnl"] > 0 else "🔴"
        print(f"   {status} {pos['ticker']}: ${pos['current']:.2f} ({pos['pnl_pct']:+.1f}%) | ${pos['pnl']:+,.0f}")
    print("=" * 60)
    
    # Append to journal
    journal_path = Path(__file__).parent.parent / "performance-journal.jsonl"
    with open(journal_path, "a") as f:
        f.write(json.dumps(summary) + "\n")
    
    print(f"\n✅ Appended to {journal_path.name}")
    
    return summary

if __name__ == "__main__":
    generate_summary()
