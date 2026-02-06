#!/usr/bin/env python3
"""
Discord Message Fetcher - Automated message collection from multiple servers
Replaces manual message passing with real Discord API integration
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("⚠️  Discord.py not installed. Run: pip install discord.py")
    print("This is a skeleton - install dependencies before running")


class DiscordFetcher:
    """Fetch messages from Discord channels via bot"""
    
    def __init__(self, token: str = None, config_file: str = 'config/channel_ids.json'):
        """
        Initialize Discord fetcher
        
        Args:
            token: Discord bot token (or set DISCORD_BOT_TOKEN env var)
            config_file: Path to channel ID configuration
        """
        self.token = token or os.getenv('DISCORD_BOT_TOKEN')
        if not self.token:
            raise ValueError("Discord bot token required. Set DISCORD_BOT_TOKEN or pass token.")
        
        # Load channel configuration
        self.config_file = config_file
        self.channel_config = self._load_config()
        
        # Initialize Discord client
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.guilds = True
        
        self.client = discord.Client(intents=intents)
        
        # Storage for fetched messages
        self.fetched_messages = {}
    
    def _load_config(self) -> Dict[str, Any]:
        """Load channel ID configuration from JSON"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Config file not found: {self.config_file}")
            print("Creating default config...")
            
            default_config = {
                "servers": {
                    "yieldschool": {
                        "guild_id": "YOUR_GUILD_ID_HERE",
                        "channels": {
                            "yield_hub": "CHANNEL_ID_1",
                            "blue_chips": "CHANNEL_ID_2",
                            "mid_caps": "CHANNEL_ID_3"
                        }
                    },
                    "dumbmoney": {
                        "guild_id": "YOUR_GUILD_ID_HERE",
                        "channels": {
                            "main": "CHANNEL_ID_4"
                        }
                    },
                    "chart_fanatics": {
                        "guild_id": "YOUR_GUILD_ID_HERE",
                        "channels": {
                            "riz_eurusd": "CHANNEL_ID_5",
                            "general_setups": "CHANNEL_ID_6"
                        }
                    }
                }
            }
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            return default_config
    
    async def fetch_channel_messages(
        self, 
        channel_id: int, 
        hours_back: int = 24,
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Fetch messages from a single channel
        
        Args:
            channel_id: Discord channel ID (integer)
            hours_back: How many hours of history to fetch
            limit: Maximum number of messages (Discord limit: 100 per call)
        
        Returns:
            List of message dictionaries with metadata
        """
        messages = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        try:
            channel = await self.client.fetch_channel(channel_id)
            
            async for message in channel.history(limit=limit):
                # Stop if we've gone past the cutoff time
                if message.created_at.replace(tzinfo=None) < cutoff_time:
                    break
                
                # Extract reactions
                reactions = {}
                for reaction in message.reactions:
                    # Filter out bot reactions (optional)
                    users = [user async for user in reaction.users()]
                    human_count = sum(1 for user in users if not user.bot)
                    
                    if human_count > 0:
                        reactions[str(reaction.emoji)] = human_count
                
                # Build message object
                msg_data = {
                    'id': str(message.id),
                    'content': message.content,
                    'author': message.author.name,
                    'author_id': str(message.author.id),
                    'timestamp': message.created_at.isoformat(),
                    'reactions': reactions,
                    'channel_id': str(channel_id),
                    'channel_name': channel.name if hasattr(channel, 'name') else 'Unknown',
                    'embeds': len(message.embeds),
                    'attachments': len(message.attachments),
                    'has_thread': message.thread is not None
                }
                
                messages.append(msg_data)
            
            print(f"✅ Fetched {len(messages)} messages from {channel.name} (last {hours_back}h)")
            
        except discord.errors.Forbidden:
            print(f"❌ No access to channel {channel_id} (check bot permissions)")
        except discord.errors.NotFound:
            print(f"❌ Channel {channel_id} not found (check ID)")
        except Exception as e:
            print(f"❌ Error fetching from channel {channel_id}: {e}")
        
        return messages
    
    async def fetch_all_configured_channels(self, hours_back: int = 24) -> Dict[str, List[Dict]]:
        """
        Fetch messages from all channels in config
        
        Args:
            hours_back: How many hours of history to fetch
        
        Returns:
            Dictionary mapping server+channel names to message lists
        """
        all_messages = {}
        
        for server_name, server_config in self.channel_config.get('servers', {}).items():
            channels = server_config.get('channels', {})
            
            for channel_name, channel_id in channels.items():
                if channel_id == "YOUR_GUILD_ID_HERE" or channel_id.startswith("CHANNEL_ID"):
                    print(f"⚠️  Skipping {server_name}/{channel_name} (placeholder ID)")
                    continue
                
                print(f"Fetching {server_name}/{channel_name}...")
                
                messages = await self.fetch_channel_messages(
                    int(channel_id), 
                    hours_back=hours_back
                )
                
                key = f"{server_name}_{channel_name}"
                all_messages[key] = messages
                
                # Rate limit protection (Discord: 50 req/sec)
                await asyncio.sleep(0.5)
        
        return all_messages
    
    async def run_fetch(self, hours_back: int = 24, output_file: str = None):
        """
        Main execution: connect to Discord and fetch all messages
        
        Args:
            hours_back: How many hours of history
            output_file: Optional JSON file to save results
        """
        @self.client.event
        async def on_ready():
            print(f"✅ Discord bot connected as {self.client.user}")
            print(f"📊 Fetching messages from last {hours_back} hours...")
            
            # Fetch all configured channels
            messages = await self.fetch_all_configured_channels(hours_back)
            
            # Save to file if specified
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(messages, f, indent=2)
                print(f"💾 Saved {sum(len(msgs) for msgs in messages.values())} messages to {output_file}")
            
            # Store in memory
            self.fetched_messages = messages
            
            # Close client
            await self.client.close()
        
        # Connect and run
        try:
            await self.client.start(self.token)
        except discord.errors.LoginFailure:
            print("❌ Invalid Discord token. Check DISCORD_BOT_TOKEN.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def get_messages_for_scraper(
        self, 
        server_name: str, 
        channel_name: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get fetched messages formatted for scrapers
        
        Args:
            server_name: Server name from config (e.g., 'yieldschool')
            channel_name: Optional specific channel (e.g., 'yield_hub')
        
        Returns:
            List of messages ready for scraper input
        """
        if channel_name:
            key = f"{server_name}_{channel_name}"
            return self.fetched_messages.get(key, [])
        else:
            # Return all messages from this server
            server_messages = []
            for key, messages in self.fetched_messages.items():
                if key.startswith(f"{server_name}_"):
                    server_messages.extend(messages)
            return server_messages


# Standalone execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch Discord messages for signal scraping")
    parser.add_argument('--hours', type=int, default=24, help='Hours of history to fetch')
    parser.add_argument('--output', type=str, default='fetched_messages.json', help='Output JSON file')
    parser.add_argument('--config', type=str, default='config/channel_ids.json', help='Channel config file')
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║           Discord Message Fetcher v1.0                    ║
║        Automated Data Collection for Signal Scrapers      ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Check for token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ No Discord bot token found!")
        print("   Set environment variable: export DISCORD_BOT_TOKEN='your_token_here'")
        print("   Or create .env file with DISCORD_BOT_TOKEN=your_token")
        exit(1)
    
    # Initialize fetcher
    fetcher = DiscordFetcher(token=token, config_file=args.config)
    
    # Run async fetch
    asyncio.run(fetcher.run_fetch(hours_back=args.hours, output_file=args.output))
    
    print("\n✅ Fetch complete!")
    print(f"   Output: {args.output}")
    print(f"   Next: Run scrapers with this data (yieldschool_scraper.py, etc.)")
