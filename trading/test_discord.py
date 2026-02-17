#!/usr/bin/env python3
"""Quick Discord test post"""

import requests
import os

# Read bot token
with open('/Users/agentjoselo/.openclaw/workspace/.discord-bot-token', 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNEL_ID = "1469019921592619154"  # #general

def test_post():
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    message = """🐓 **Joselo Monitor - System Test**

Discord integration verified.

**Current Status:**
✅ Risk monitoring active (hourly)
✅ Price updates running (hourly)
✅ Autonomous pipeline configured
✅ GitHub auto-commit operational

**Active Positions:**
- TAO: $182.46 (SELL signal, RSI 39.3)
- SOL: $85.40 (SELL signal, RSI 34.5)
- Net P&L: $268

All systems operational."""
    
    payload = {"content": message}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("✅ Test message sent to Discord successfully")
        print(f"   Message ID: {response.json()['id']}")
        return True
    else:
        print(f"❌ Failed to send: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

if __name__ == "__main__":
    test_post()
