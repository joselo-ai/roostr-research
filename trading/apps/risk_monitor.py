#!/usr/bin/env python3
"""
Risk Monitor v2 - Real-time stop-loss violation alerts (TradingView)
Checks every 5min, alerts via Telegram if positions breach stops
Now includes RSI context and real-time TradingView data
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from tradingview_ta import TA_Handler, Interval

# Position configs (matches price_updater.py)
POSITIONS = {
    "TAO": {
        "symbol": "TAOUSD",
        "exchange": "BINANCE",
        "entry": 176.05,
        "quantity": 56.8,
        "stop": 140.84
    }
}

def fetch_live_data(ticker):
    """Fetch current price + RSI from TradingView"""
    if ticker not in POSITIONS:
        return None
    
    try:
        pos = POSITIONS[ticker]
        handler = TA_Handler(
            symbol=pos["symbol"],
            exchange=pos["exchange"],
            screener='crypto',
            interval=Interval.INTERVAL_1_HOUR
        )
        analysis = handler.get_analysis()
        
        return {
            "price": analysis.indicators["close"],
            "rsi": analysis.indicators.get("RSI", 0),
            "recommendation": analysis.summary["RECOMMENDATION"]
        }
    except Exception as e:
        print(f"⚠️  {ticker}: Error fetching live data - {e}")
        return None

def check_stops():
    """Check if any positions have violated their stop losses"""
    
    violations = []
    warnings = []
    
    for ticker, pos in POSITIONS.items():
        data = fetch_live_data(ticker)
        
        if not data:
            print(f"⚠️  {ticker}: No live data available")
            continue
        
        current_price = data["price"]
        stop_price = pos["stop"]
        entry_price = pos["entry"]
        rsi = data["rsi"]
        signal = data["recommendation"]
        
        # Calculate distances
        distance_to_stop = ((current_price - stop_price) / current_price) * 100
        pnl_pct = ((current_price - entry_price) / entry_price) * 100
        
        # Check if stop violated
        if current_price <= stop_price:
            violations.append({
                "ticker": ticker,
                "current": current_price,
                "stop": stop_price,
                "entry": entry_price,
                "breach_pct": abs(distance_to_stop),
                "pnl_pct": pnl_pct,
                "rsi": rsi,
                "signal": signal
            })
        # Warn if approaching stop (within 5%)
        elif distance_to_stop <= 5.0:
            warnings.append({
                "ticker": ticker,
                "current": current_price,
                "stop": stop_price,
                "distance_pct": distance_to_stop,
                "rsi": rsi,
                "signal": signal
            })
    
    # Report status
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Show warnings first
    if warnings:
        print(f"\n⚠️  APPROACHING STOP ({timestamp})")
        for w in warnings:
            print(f"   {w['ticker']}: ${w['current']:.2f} (stop: ${w['stop']:.2f}) | {w['distance_pct']:.1f}% away | RSI {w['rsi']:.1f}")
    
    # Then violations
    if violations:
        print(f"\n🚨 STOP LOSS VIOLATIONS DETECTED ({timestamp})")
        print("=" * 60)
        
        for v in violations:
            print(f"\n🔴 {v['ticker']}")
            print(f"   Entry:   ${v['entry']:.2f}")
            print(f"   Current: ${v['current']:.2f} ({v['pnl_pct']:+.1f}%)")
            print(f"   Stop:    ${v['stop']:.2f}")
            print(f"   ⚠️  BREACHED BY {v['breach_pct']:.1f}%")
            print(f"   RSI: {v['rsi']:.1f} | Signal: {v['signal']}")
        
        print("\n" + "=" * 60)
        print("🚨 ACTION REQUIRED: Exit positions immediately!")
        
        # Save alert to file
        alert_file = Path(__file__).parent.parent / "risk-alerts.log"
        with open(alert_file, "a") as f:
            f.write(f"\n[{timestamp}] STOP LOSS VIOLATION\n")
            for v in violations:
                f.write(f"  {v['ticker']}: ${v['current']:.2f} <= ${v['stop']:.2f} (RSI {v['rsi']:.1f})\n")
        
        return violations
    else:
        if not warnings:
            print(f"✅ Risk Monitor ({timestamp}): All positions within stops")
        return []

def send_telegram_alert(violations):
    """Send Telegram alert for stop violations"""
    
    if not violations:
        return
    
    message = "🚨 STOP LOSS VIOLATION 🚨\n\n"
    
    for v in violations:
        message += f"**{v['ticker']}:** ${v['current']:.2f}\n"
        message += f"Stop: ${v['stop']:.2f} | Breached by {v['breach_pct']:.1f}%\n"
        message += f"Loss: {v['pnl_pct']:.1f}%\n"
        message += f"RSI: {v['rsi']:.1f} | {v['signal']}\n\n"
    
    message += "**ACTION: Exit positions NOW!**"
    
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
