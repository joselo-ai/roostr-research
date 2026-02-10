#!/usr/bin/env python3
"""
Discord Message Listener - Real-time signal collection from Chart Fanatics
Runs as background service, saves messages to JSON for signal_scraper.py
"""

import discord
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
DISCORD_TOKEN_FILE = "/Users/agentjoselo/.openclaw/workspace/.discord-bot-token"
OUTPUT_FILE = "/Users/agentjoselo/.openclaw/workspace/trading/discord-messages.json"
CONFIG_FILE = "/Users/agentjoselo/.openclaw/workspace/trading/config/discord_channels.json"

class SignalListener(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []
        
        # Load config
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                self.config = json.load(f)
        else:
            self.config = {"chart_fanatics": {"watch_traders": []}}
        
        # Load existing messages
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE) as f:
                self.messages = json.load(f)
    
    async def on_ready(self):
        print(f'🐓 Discord listener active: {self.user}')
        print(f'📊 Monitoring {len(self.guilds)} servers')
        for guild in self.guilds:
            print(f'   - {guild.name} ({len(guild.channels)} channels)')
    
    async def on_message(self, message):
        # Ignore bot's own messages
        if message.author == self.user:
            return
        
        # Ignore DMs
        if not message.guild:
            return
        
        # Check if author is in watch list
        watch_traders = self.config.get('chart_fanatics', {}).get('watch_traders', [])
        if watch_traders and message.author.display_name not in watch_traders:
            return
        
        # Extract message data
        msg_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "server": message.guild.name,
            "channel": message.channel.name,
            "author": message.author.display_name,
            "content": message.content,
            "message_id": str(message.id),
            "reactions": len(message.reactions) if message.reactions else 0
        }
        
        # Add to collection
        self.messages.append(msg_data)
        
        # Keep only last 1000 messages
        if len(self.messages) > 1000:
            self.messages = self.messages[-1000:]
        
        # Save to file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(self.messages, f, indent=2)
        
        # Log to console
        print(f"💬 [{message.guild.name}/{message.channel.name}] {message.author.display_name}: {message.content[:50]}...")


def main():
    """Run Discord listener"""
    
    # Load bot token
    if not os.path.exists(DISCORD_TOKEN_FILE):
        print(f"❌ Discord token not found at {DISCORD_TOKEN_FILE}")
        return
    
    with open(DISCORD_TOKEN_FILE) as f:
        token = f.read().strip()
    
    # Initialize client
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.reactions = True
    
    client = SignalListener(intents=intents)
    
    # Run bot
    print("🐓 Starting Discord listener...")
    client.run(token)


if __name__ == '__main__':
    main()
