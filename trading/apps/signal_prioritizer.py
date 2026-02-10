#!/usr/bin/env python3
"""
Signal Prioritizer - Ranks deployment candidates by conviction, catalyst, and entry clarity
Generates daily top 3 deployment targets
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

def calculate_priority_score(signal):
    """
    Priority Score = (Conviction × Catalyst × Entry Clarity) / 100
    
    Conviction: 0-10 from database
    Catalyst: 0-10 based on timing (earnings, news, events)
    Entry Clarity: 0-10 based on price action and setup
    """
    
    conviction = signal.get("conviction", 0)
    
    # Catalyst scoring (simplified - could be enhanced)
    notes = signal.get("notes", "").lower()
    catalyst_score = 5.0  # Default neutral
    
    if "earnings" in notes and ("days" in notes or "weeks" in notes):
        catalyst_score = 9.0  # Near-term earnings
    elif "catalyst" in notes or "fcc" in notes or "approval" in notes:
        catalyst_score = 8.0  # Binary event coming
    elif "pullback" in notes or "wait" in notes:
        catalyst_score = 3.0  # Waiting for entry
    
    # Entry clarity scoring
    entry_clarity = 5.0  # Default
    
    if signal.get("price_entry"):
        entry_clarity = 8.0  # Has specific entry price
    
    if "wait" in notes or "do not deploy" in notes:
        entry_clarity = 2.0  # Not ready
    elif "deploy now" in notes or "green" in signal.get("status", "").lower():
        entry_clarity = 9.0  # Ready to execute
    
    # Calculate composite score
    priority_score = (conviction * catalyst_score * entry_clarity) / 100
    
    return {
        "priority_score": round(priority_score, 2),
        "conviction": conviction,
        "catalyst": catalyst_score,
        "entry_clarity": entry_clarity
    }

def prioritize_signals():
    """Load signals, score them, return top 3"""
    
    signals_db = Path(__file__).parent.parent / "signals-database.csv"
    
    candidates = []
    
    with open(signals_db) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip already deployed
            if row["Deployed"] == "YES":
                continue
            
            # Skip RED signals
            if row["Status"] == "RED":
                continue
            
            signal = {
                "ticker": row["Ticker"],
                "source": row["Source"],
                "conviction": float(row["Conviction_Score"]) if row["Conviction_Score"] else 0,
                "status": row["Status"],
                "price_entry": row["Price_Entry"],
                "notes": row["Notes"]
            }
            
            scores = calculate_priority_score(signal)
            signal.update(scores)
            
            candidates.append(signal)
    
    # Sort by priority score (descending)
    candidates.sort(key=lambda x: x["priority_score"], reverse=True)
    
    # Return top 3
    return candidates[:3]

def generate_report():
    """Generate daily deployment priorities report"""
    
    top_3 = prioritize_signals()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    print(f"🎯 Signal Prioritizer ({timestamp})")
    print("=" * 60)
    print("\nTop 3 Deployment Candidates:\n")
    
    for i, signal in enumerate(top_3, 1):
        print(f"{i}. {signal['ticker']} - Priority Score: {signal['priority_score']:.2f}")
        print(f"   Source: {signal['source']}")
        print(f"   Conviction: {signal['conviction']}/10")
        print(f"   Catalyst: {signal['catalyst']}/10")
        print(f"   Entry Clarity: {signal['entry_clarity']}/10")
        print(f"   Status: {signal['status']}")
        if signal['price_entry']:
            print(f"   Entry: ${signal['price_entry']}")
        print(f"   Notes: {signal['notes'][:100]}...")
        print()
    
    # Save to file
    output_file = Path(__file__).parent.parent / "deployment-priorities.txt"
    with open(output_file, "w") as f:
        f.write(f"🎯 Daily Deployment Priorities - {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        
        for i, signal in enumerate(top_3, 1):
            f.write(f"{i}. {signal['ticker']} (Score: {signal['priority_score']:.2f})\n")
            f.write(f"   Conviction: {signal['conviction']}/10 | ")
            f.write(f"Catalyst: {signal['catalyst']}/10 | ")
            f.write(f"Entry: {signal['entry_clarity']}/10\n")
            f.write(f"   {signal['notes'][:150]}\n\n")
    
    print(f"✅ Saved to {output_file}")
    
    return top_3

if __name__ == "__main__":
    generate_report()
