#!/usr/bin/env python3
"""
Discord Channel Router
Routes messages to appropriate Discord channels based on content type.
"""

import requests
import json
import os
from pathlib import Path

# Load channel mapping
CHANNELS_FILE = Path(__file__).parent.parent / '.discord-channels.json'
with open(CHANNELS_FILE, 'r') as f:
    DISCORD_CONFIG = json.load(f)

# Load bot token
TOKEN_FILE = Path.home() / '.openclaw/workspace/.discord-bot-token'
with open(TOKEN_FILE, 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNELS = DISCORD_CONFIG['channels']
GUILD_ID = DISCORD_CONFIG['guild_id']

def post_to_channel(channel_name: str, message: str) -> bool:
    """Post message to specified Discord channel."""
    if channel_name not in CHANNELS:
        print(f"❌ Unknown channel: {channel_name}")
        return False
    
    channel_id = CHANNELS[channel_name]
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {"content": message}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        msg_id = response.json()['id']
        print(f"✅ Posted to #{channel_name} (ID: {msg_id})")
        return True
    else:
        print(f"❌ Failed to post to #{channel_name}: {response.status_code}")
        print(f"   {response.text}")
        return False

# Convenience functions
def signal(message: str) -> bool:
    """Post to #trading-signals"""
    return post_to_channel('trading-signals', message)

def update(message: str) -> bool:
    """Post to #trading-updates"""
    return post_to_channel('trading-updates', message)

def research(message: str) -> bool:
    """Post to #research"""
    return post_to_channel('research', message)

def chat(message: str) -> bool:
    """Post to #agent-chat"""
    return post_to_channel('agent-chat', message)

def log(message: str) -> bool:
    """Post to #logs"""
    return post_to_channel('logs', message)

def dexter(message: str) -> bool:
    """Post to #dexter-research"""
    return post_to_channel('dexter-research', message)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: discord_helper.py <channel> <message>")
        print(f"Channels: {', '.join(CHANNELS.keys())}")
        sys.exit(1)
    
    channel = sys.argv[1]
    message = ' '.join(sys.argv[2:])
    post_to_channel(channel, message)
