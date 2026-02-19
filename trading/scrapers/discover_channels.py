#!/usr/bin/env python3
"""
Discover Discord Channels - Show all servers and channels the bot can access
"""

import asyncio
import discord
from pathlib import Path

TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / ".discord-bot-token"

async def discover():
    """Discover all accessible servers and channels"""
    
    # Load token
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"\n✅ Connected as {client.user}\n")
        print("="*80)
        print("ACCESSIBLE DISCORD SERVERS & CHANNELS")
        print("="*80)
        
        if len(client.guilds) == 0:
            print("\n❌ Bot is not in any servers!")
            print("   Invite bot using: https://discord.com/api/oauth2/authorize?client_id=1469016616711884913&permissions=67584&scope=bot")
        
        for guild in client.guilds:
            print(f"\n🏢 SERVER: {guild.name}")
            print(f"   Guild ID: {guild.id}")
            print(f"   Members: {guild.member_count}")
            print(f"\n   📁 CHANNELS:")
            
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    print(f"      #{channel.name:30} → {channel.id}")
        
        print("\n" + "="*80)
        print("Copy these IDs into: trading/config/discord_sources.json")
        print("="*80 + "\n")
        
        await client.close()
    
    await client.start(token)

if __name__ == "__main__":
    asyncio.run(discover())
