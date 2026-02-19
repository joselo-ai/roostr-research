#!/usr/bin/env python3
"""
Discord Signal Forwarder - Automated Signal Aggregation & Distribution
Monitors external Discord servers, scores signals, posts to our #trading-signals

Runs: Every 30 minutes via cron (or as daemon)
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent / 'scrapers'))

try:
    import discord
    from discord import Webhook
except ImportError:
    print("❌ discord.py not installed")
    exit(1)

from dumbmoney_scraper import DumbMoneyScanner

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config" / "discord_sources.json"
TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / ".discord-bot-token"
STATE_FILE = BASE_DIR / "logs" / "last_discord_scan.json"

# Our server channel IDs (where we post signals)
OUR_GUILD_ID = 1469019919671885915
TRADING_SIGNALS_CHANNEL = 1472685997182685466
AGENTS_DEBATE_CHANNEL = 1472692185106481417
RESEARCH_CHANNEL = 1472686030204178534

class DiscordSignalForwarder:
    """Automatically monitor external servers and forward high-conviction signals"""
    
    def __init__(self):
        self.token = self._load_token()
        self.config = self._load_config()
        self.state = self._load_state()
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.guilds = True
        
        self.client = discord.Client(intents=intents)
        self.signals_found = []
    
    def _load_token(self) -> str:
        """Load Discord bot token"""
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    
    def _load_config(self) -> dict:
        """Load Discord sources configuration"""
        if not CONFIG_FILE.exists():
            return {"dumbmoney": {"enabled": False}, "yieldschool": {"enabled": False}, "chart_fanatics": {"enabled": False}}
        
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    def _load_state(self) -> dict:
        """Load last scan state (timestamps, processed message IDs)"""
        if not STATE_FILE.exists():
            return {
                "last_scan": None,
                "processed_messages": []
            }
        
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    
    def _save_state(self):
        """Save scan state"""
        STATE_FILE.parent.mkdir(exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    async def scan_dumb_money(self) -> list:
        """Scan Dumb Money for social arbitrage signals"""
        config = self.config.get('dumbmoney', {})
        
        if not config.get('enabled', False):
            print("⏭️  Dumb Money scanning disabled in config")
            return []
        
        channels = config.get('channels', {})
        channel_ids = [int(cid) for cid in channels.values() if cid != "CHANNEL_ID_HERE"]
        
        if not channel_ids:
            print("⚠️  No Dumb Money channels configured")
            return []
        
        print(f"📊 Scanning Dumb Money ({len(channel_ids)} channels)...")
        
        scanner = DumbMoneyScanner(token=self.token)
        
        # Scan last 30 minutes (since last run)
        raw_signals = []
        for channel_id in channel_ids:
            signals = await scanner.scan_channel(
                channel_id,
                hours_back=1,  # Last hour (overlap OK)
                min_reactions=config.get('min_reactions', 10)
            )
            raw_signals.extend(signals)
        
        # Aggregate and filter
        aggregated = scanner.aggregate_signals(raw_signals)
        
        # Filter by conviction threshold
        threshold = config.get('conviction_threshold', 7.0)
        high_conviction = [s for s in aggregated if s['avg_conviction'] >= threshold]
        
        print(f"   Found {len(high_conviction)} high-conviction signals (≥{threshold}/10)")
        
        return high_conviction
    
    async def scan_yieldschool(self) -> list:
        """Scan Yieldschool for crypto signals"""
        config = self.config.get('yieldschool', {})
        
        if not config.get('enabled', False):
            print("⏭️  Yieldschool scanning disabled")
            return []
        
        print("📊 Scanning Yieldschool...")
        
        # TODO: Implement Yieldschool scraper
        # Look for Dan's posts, crypto tickers, fundamental analysis
        
        return []
    
    async def scan_chart_fanatics(self) -> list:
        """Scan Chart Fanatics for forex signals"""
        config = self.config.get('chart_fanatics', {})
        
        if not config.get('enabled', False):
            print("⏭️  Chart Fanatics scanning disabled")
            return []
        
        print("📊 Scanning Chart Fanatics...")
        
        # TODO: Implement Chart Fanatics scraper
        # Look for Riz's posts, EURUSD setups, R-multiple results
        
        return []
    
    async def post_signal_to_channel(self, channel_id: int, signal: dict):
        """Post signal to our Discord channel"""
        try:
            channel = await self.client.fetch_channel(channel_id)
            
            # Format signal message
            msg = f"""🚨 **NEW SIGNAL DETECTED**

**Ticker:** ${signal['ticker']}
**Source:** {signal['source']}
**Conviction:** {signal['avg_conviction']}/10
**Total Reactions:** {signal['total_reactions']}
**Mentions:** {signal['mention_count']}

**Top Emojis:**
{self._format_emojis(signal['top_emojis'])}

**Sample Messages:**
"""
            
            for i, message in enumerate(signal['messages'][:2], 1):
                msg += f"{i}. @{message['author']}: {message['content'][:100]}...\n"
                msg += f"   {message['url']}\n"
            
            msg += f"\n🤖 **Triggering 18-agent deliberation...**"
            
            await channel.send(msg)
            print(f"   ✅ Posted {signal['ticker']} to #{channel.name}")
            
        except Exception as e:
            print(f"   ❌ Error posting signal: {e}")
    
    def _format_emojis(self, emojis: dict) -> str:
        """Format emoji counts"""
        sorted_emojis = sorted(emojis.items(), key=lambda x: x[1], reverse=True)
        return " ".join([f"{emoji}×{count}" for emoji, count in sorted_emojis[:5]])
    
    async def trigger_18_agent_deliberation(self, ticker: str):
        """Trigger 18-agent system for a ticker"""
        try:
            # Run agent deliberation script
            import subprocess
            
            venv_python = BASE_DIR / "venv" / "bin" / "python3"
            agents_script = BASE_DIR / "agents" / "legendary_investors_v2.py"
            
            result = subprocess.run(
                [str(venv_python), str(agents_script), ticker],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(BASE_DIR / "agents")
            )
            
            if result.returncode == 0:
                # Parse consensus from output
                output = result.stdout
                
                # Post to agents debate channel
                channel = await self.client.fetch_channel(AGENTS_DEBATE_CHANNEL)
                
                # Extract consensus line
                consensus_line = [line for line in output.split('\n') if 'CONSENSUS:' in line]
                conviction_line = [line for line in output.split('\n') if 'AVG CONVICTION:' in line]
                
                summary = f"**18-Agent Deliberation: ${ticker}**\n\n"
                if consensus_line:
                    summary += consensus_line[0] + "\n"
                if conviction_line:
                    summary += conviction_line[0] + "\n"
                
                summary += f"\nFull report: `deliberations/{ticker.lower()}_*.txt`"
                
                await channel.send(summary)
                
                print(f"   ✅ 18-agent deliberation complete for {ticker}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  Agent deliberation timed out for {ticker}")
        except Exception as e:
            print(f"   ❌ Error in deliberation: {e}")
    
    async def run_scan_cycle(self):
        """Main scan cycle - runs every 30 minutes"""
        
        @self.client.event
        async def on_ready():
            print(f"\n✅ Connected as {self.client.user}")
            print(f"⏰ Starting scan cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            # Scan all enabled sources
            all_signals = []
            
            dumbmoney_signals = await self.scan_dumb_money()
            all_signals.extend(dumbmoney_signals)
            
            yieldschool_signals = await self.scan_yieldschool()
            all_signals.extend(yieldschool_signals)
            
            chartfanatics_signals = await self.scan_chart_fanatics()
            all_signals.extend(chartfanatics_signals)
            
            print("="*60)
            print(f"📊 TOTAL: {len(all_signals)} high-conviction signals found")
            
            # Process each signal
            for signal in all_signals:
                ticker = signal['ticker']
                
                # Check if already processed
                if ticker in self.state.get('processed_messages', []):
                    print(f"   ⏭️  {ticker} already processed")
                    continue
                
                # Post to our trading signals channel
                await self.post_signal_to_channel(TRADING_SIGNALS_CHANNEL, signal)
                
                # Trigger 18-agent deliberation
                await self.trigger_18_agent_deliberation(ticker)
                
                # Mark as processed
                if 'processed_messages' not in self.state:
                    self.state['processed_messages'] = []
                self.state['processed_messages'].append(ticker)
                
                # Rate limit
                await asyncio.sleep(2)
            
            # Update state
            self.state['last_scan'] = datetime.now().isoformat()
            self._save_state()
            
            print(f"\n✅ Scan cycle complete")
            print(f"   Signals processed: {len(all_signals)}")
            print(f"   Next scan: 30 minutes\n")
            
            await self.client.close()
        
        try:
            await self.client.start(self.token)
        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    """CLI entry point"""
    print("🐓 Discord Signal Forwarder - Automated Signal Aggregation")
    print("="*60)
    
    forwarder = DiscordSignalForwarder()
    await forwarder.run_scan_cycle()


if __name__ == "__main__":
    asyncio.run(main())
