#!/usr/bin/env python3
"""
Risk Monitor - Real-time stop-loss violation alerts
Checks every 5min, alerts via Telegram if positions breach stops
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def check_stops():
    """Check if any positions have violated their stop losses"""
    
    # Read current prices
    price_cache = Path(__file__).parent.parent / ".price_cache.json"
    with open(price_cache) as f:
        prices = json.loads(f.read())
    
    # Read positions from signals database
    signals_db = Path(__file__).parent.parent / "signals-database.csv"
    violations = []
    
    with open(signals_db) as f:
        for line in f:
            if line.startswith("Ticker"):
                continue  # Skip header
            
            parts = line.split(",")
            ticker = parts[0]
            deployed = parts[6]
            
            if deployed != "YES":
                continue
            
            # Extract stop loss from notes
            notes = ",".join(parts[13:])
            if "Stop:" not in notes:
                continue
            
            try:
                stop_str = notes.split("Stop: $")[1].split(" ")[0]
                stop_price = float(stop_str)
                entry_price = float(parts[3])
                current_price = prices.get(ticker, {}).get("price", 0)
                
                if current_price == 0:
                    print(f"⚠️  {ticker}: No price data available")
                    continue
                
                # Check if stop violated
                distance_to_stop = ((current_price - stop_price) / current_price) * 100
                
                if current_price <= stop_price:
                    violations.append({
                        "ticker": ticker,
                        "current": current_price,
                        "stop": stop_price,
                        "entry": entry_price,
                        "breach_pct": abs(distance_to_stop)
                    })
                
                # Also warn if approaching stop (within 5%)
                elif distance_to_stop <= 5.0:
                    print(f"⚠️  {ticker}: Approaching stop (${current_price:.2f} vs ${stop_price:.2f}, {distance_to_stop:.1f}% away)")
            
            except (IndexError, ValueError) as e:
                print(f"❌ Error parsing {ticker}: {e}")
                continue
    
    # Report status
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if violations:
        print(f"\n🚨 STOP LOSS VIOLATIONS DETECTED ({timestamp})")
        print("=" * 60)
        
        for v in violations:
            loss_pct = ((v["current"] - v["entry"]) / v["entry"]) * 100
            print(f"\n🔴 {v['ticker']}")
            print(f"   Entry:   ${v['entry']:.2f}")
            print(f"   Current: ${v['current']:.2f} ({loss_pct:+.1f}%)")
            print(f"   Stop:    ${v['stop']:.2f}")
            print(f"   ⚠️  BREACHED BY {v['breach_pct']:.1f}%")
        
        print("\n" + "=" * 60)
        print("🚨 ACTION REQUIRED: Exit positions immediately!")
        
        # Save alert to file
        alert_file = Path(__file__).parent.parent / "risk-alerts.log"
        with open(alert_file, "a") as f:
            f.write(f"\n[{timestamp}] STOP LOSS VIOLATION\n")
            for v in violations:
                f.write(f"  {v['ticker']}: ${v['current']:.2f} <= ${v['stop']:.2f}\n")
        
        return violations
    else:
        print(f"✅ Risk Monitor ({timestamp}): All positions within stops")
        return []

def send_telegram_alert(violations):
    """Send Telegram alert for stop violations"""
    
    if not violations:
        return
    
    message = "🚨 STOP LOSS VIOLATION 🚨\n\n"
    
    for v in violations:
        loss_pct = ((v["current"] - v["entry"]) / v["entry"]) * 100
        message += f"{v['ticker']}: ${v['current']:.2f} (stop: ${v['stop']:.2f})\n"
        message += f"Loss: {loss_pct:.1f}% | BREACHED BY {v['breach_pct']:.1f}%\n\n"
    
    message += "ACTION: Exit positions NOW!"
    
    # Save alert message
    alert_msg_file = Path(__file__).parent.parent / "telegram-alert.txt"
    with open(alert_msg_file, "w") as f:
        f.write(message)
    
    print(f"\n📱 Telegram alert ready: {alert_msg_file}")
    print("(Use `message` tool to send to Telegram)")

if __name__ == "__main__":
    violations = check_stops()
    
    if violations:
        send_telegram_alert(violations)
        sys.exit(1)  # Exit with error code to trigger alerts
    else:
        sys.exit(0)
