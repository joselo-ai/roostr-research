#!/usr/bin/env python3
"""
Quick script to discover what Discord servers the bot has access to
"""

import discord
import asyncio

DISCORD_TOKEN_FILE = "/Users/agentjoselo/.openclaw/workspace/.discord-bot-token"

async def discover():
    with open(DISCORD_TOKEN_FILE) as f:
        token = f.read().strip()
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'\n🐓 Bot: {client.user}')
        print(f'📊 Connected to {len(client.guilds)} servers:\n')
        
        for guild in client.guilds:
            print(f'Server: {guild.name}')
            print(f'  ID: {guild.id}')
            print(f'  Channels: {len(guild.channels)}')
            
            # List text channels
            text_channels = [c for c in guild.channels if isinstance(c, discord.TextChannel)]
            if text_channels:
                print(f'  Text Channels ({len(text_channels)}):')
                for channel in text_channels[:10]:  # Show first 10
                    print(f'    - {channel.name} (ID: {channel.id})')
            print()
        
        await client.close()
    
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(discover())
