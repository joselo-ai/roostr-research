#!/usr/bin/env python3
"""
Risk Alert Sender - Sends Telegram alerts for stop violations
Called by risk_monitor.py when violations detected
"""

import subprocess
import sys
from pathlib import Path

def send_alert():
    """Send Telegram alert using openclaw message tool"""
    
    alert_file = Path(__file__).parent.parent / "telegram-alert.txt"
    
    if not alert_file.exists():
        print("No alert file found")
        return
    
    with open(alert_file) as f:
        message = f.read()
    
    # Send via OpenClaw message tool (Telegram)
    # This will use the configured Telegram bot
    print(f"📱 Sending alert to Telegram...")
    print(message)
    
    # For now, just print - OpenClaw will handle actual sending
    # You'll call this via: message send --channel telegram --message "$(cat telegram-alert.txt)"
    
    return message

if __name__ == "__main__":
    send_alert()
