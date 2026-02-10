#!/usr/bin/env python3
"""
Telegram Alert Sender
Monitors telegram-queue.txt and sends alerts via OpenClaw message tool
Run via cron every minute to check for new alerts
"""

from pathlib import Path
import subprocess
import sys

TELEGRAM_QUEUE = Path(__file__).parent.parent / "telegram-queue.txt"
SENT_MARKER = Path(__file__).parent.parent / ".telegram_last_sent"

def send_alert():
    """Check for new alerts and send via Telegram"""
    
    if not TELEGRAM_QUEUE.exists():
        return False
    
    # Read the queued message
    with open(TELEGRAM_QUEUE, 'r') as f:
        message = f.read().strip()
    
    if not message:
        return False
    
    # Check if already sent (by comparing to marker)
    if SENT_MARKER.exists():
        with open(SENT_MARKER, 'r') as f:
            last_sent = f.read().strip()
        if last_sent == message:
            return False  # Already sent
    
    # Send via OpenClaw (NOTE: This should be called by OpenClaw, not directly)
    print(f"📱 New TradingView alert to send:")
    print(message)
    print("\n✅ Use: message action=send channel=telegram message=\"{content}\"")
    
    # Mark as sent
    with open(SENT_MARKER, 'w') as f:
        f.write(message)
    
    return True

if __name__ == "__main__":
    if send_alert():
        print("\n📤 Alert queued for Telegram delivery")
    else:
        print("✅ No new alerts")
