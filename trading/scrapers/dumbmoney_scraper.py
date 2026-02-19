#!/usr/bin/env python3
"""
Dumb Money Discord Scraper - Social Arbitrage Signal Hunter
Scans Discord for high-engagement stock picks before Wall Street notices

Usage:
    python3 dumbmoney_scraper.py --hours 24 --min-reactions 20
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import os

try:
    import discord
except ImportError:
    print("❌ discord.py not installed. Run: pip install discord.py")
    exit(1)

BASE_DIR = Path(__file__).parent.parent
TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / ".discord-bot-token"

# Social arbitrage emoji indicators (high conviction)
CONVICTION_EMOJIS = {
    '🚀': 3.0,  # Rocket = strong buy signal
    '🔥': 2.5,  # Fire = trending/hot
    '💎': 2.0,  # Diamond hands = hold conviction
    '💯': 1.5,  # 100 = strong agreement
    '👀': 1.0,  # Eyes = watching/interested
    '📈': 1.5,  # Chart up = bullish
    '🤑': 1.0,  # Money face = profit potential
    '⚡': 1.0,  # Lightning = quick move expected
}

class DumbMoneyScanner:
    """Scan Dumb Money Discord for social arbitrage signals"""
    
    def __init__(self, token: str = None):
        """Initialize scanner with Discord bot token"""
        self.token = token or self._load_token()
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.guilds = True
        
        self.client = discord.Client(intents=intents)
        self.signals = []
    
    def _load_token(self) -> str:
        """Load Discord bot token from file"""
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'r') as f:
                return f.read().strip()
        
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            raise ValueError(
                "Discord token not found. Set DISCORD_BOT_TOKEN env var or "
                f"create {TOKEN_FILE}"
            )
        return token
    
    def extract_tickers(self, text: str) -> List[str]:
        """
        Extract stock tickers from message text
        Matches: $TICKER, TICKER (all caps), or common formats
        """
        if not text:
            return []
        
        tickers = []
        
        # Match $TICKER format (most common in trading Discord)
        dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
        tickers.extend(dollar_tickers)
        
        # Match standalone ALL CAPS tickers (2-5 chars, common stock symbols)
        # But exclude common words like "THIS", "MAKE", "JUST", etc.
        excluded_words = {'THIS', 'THAT', 'MAKE', 'JUST', 'OVER', 'MORE', 'SOME', 'VERY', 'ONLY', 'LIKE', 'BEEN', 'WHEN', 'WILL', 'CALL', 'PUTS', 'SAME'}
        standalone = re.findall(r'\b([A-Z]{2,5})\b', text)
        tickers.extend([t for t in standalone if t not in excluded_words])
        
        # Remove duplicates, preserve order
        seen = set()
        unique_tickers = []
        for ticker in tickers:
            if ticker not in seen:
                seen.add(ticker)
                unique_tickers.append(ticker)
        
        return unique_tickers
    
    def calculate_conviction_score(self, reactions: Dict[str, int]) -> float:
        """
        Calculate conviction score from emoji reactions
        
        Formula: Σ(emoji_weight × count) 
        Returns: 0-10 scale
        """
        total_score = 0.0
        
        for emoji, count in reactions.items():
            weight = CONVICTION_EMOJIS.get(emoji, 0.1)  # Default 0.1 for other emojis
            total_score += weight * count
        
        # Scale to 0-10 (20+ weighted reactions = 10/10)
        normalized = min(10.0, (total_score / 20.0) * 10.0)
        return round(normalized, 1)
    
    async def scan_channel(
        self, 
        channel_id: int, 
        hours_back: int = 24,
        min_reactions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Scan a Discord channel for social arbitrage signals
        
        Args:
            channel_id: Discord channel ID
            hours_back: Hours of history to scan
            min_reactions: Minimum total reactions to qualify
        
        Returns:
            List of signal dictionaries
        """
        signals = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        try:
            channel = await self.client.fetch_channel(channel_id)
            print(f"📊 Scanning #{channel.name} (last {hours_back}h)...")
            
            message_count = 0
            async for message in channel.history(limit=1000):
                message_count += 1
                
                # Stop if past cutoff
                if message.created_at.replace(tzinfo=None) < cutoff_time:
                    break
                
                # Extract tickers from message
                tickers = self.extract_tickers(message.content)
                if not tickers:
                    continue
                
                # Count reactions
                reactions = {}
                total_reaction_count = 0
                
                for reaction in message.reactions:
                    emoji = str(reaction.emoji)
                    count = reaction.count
                    reactions[emoji] = count
                    total_reaction_count += count
                
                # Filter: minimum reactions required
                if total_reaction_count < min_reactions:
                    continue
                
                # Calculate conviction score
                conviction = self.calculate_conviction_score(reactions)
                
                # Build signal for each ticker mentioned
                for ticker in tickers:
                    signal = {
                        'ticker': ticker,
                        'source': 'dumbmoney-discord',
                        'channel': channel.name,
                        'message_id': str(message.id),
                        'author': message.author.name,
                        'content': message.content[:200],  # Truncate
                        'timestamp': message.created_at.isoformat(),
                        'reactions': reactions,
                        'total_reactions': total_reaction_count,
                        'conviction_score': conviction,
                        'url': message.jump_url
                    }
                    
                    signals.append(signal)
            
            print(f"   Scanned {message_count} messages, found {len(signals)} signals")
            
        except discord.errors.Forbidden:
            print(f"❌ No access to channel {channel_id}")
        except discord.errors.NotFound:
            print(f"❌ Channel {channel_id} not found")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return signals
    
    async def scan_server(
        self,
        guild_id: int,
        channel_ids: List[int],
        hours_back: int = 24,
        min_reactions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Scan multiple channels in a Discord server
        
        Args:
            guild_id: Discord server (guild) ID
            channel_ids: List of channel IDs to scan
            hours_back: Hours of history
            min_reactions: Minimum reaction threshold
        
        Returns:
            Combined list of all signals found
        """
        all_signals = []
        
        for channel_id in channel_ids:
            channel_signals = await self.scan_channel(
                channel_id, 
                hours_back=hours_back,
                min_reactions=min_reactions
            )
            all_signals.extend(channel_signals)
            
            # Rate limit protection
            await asyncio.sleep(0.5)
        
        return all_signals
    
    def aggregate_signals(self, signals: List[Dict]) -> List[Dict]:
        """
        Aggregate multiple mentions of same ticker
        Combines reactions across messages
        """
        ticker_data = {}
        
        for signal in signals:
            ticker = signal['ticker']
            
            if ticker not in ticker_data:
                ticker_data[ticker] = {
                    'ticker': ticker,
                    'source': 'dumbmoney-discord',
                    'total_reactions': 0,
                    'total_conviction': 0.0,
                    'mention_count': 0,
                    'messages': [],
                    'top_emojis': {}
                }
            
            # Aggregate
            ticker_data[ticker]['total_reactions'] += signal['total_reactions']
            ticker_data[ticker]['total_conviction'] += signal['conviction_score']
            ticker_data[ticker]['mention_count'] += 1
            ticker_data[ticker]['messages'].append({
                'author': signal['author'],
                'content': signal['content'],
                'url': signal['url'],
                'timestamp': signal['timestamp']
            })
            
            # Aggregate emoji counts
            for emoji, count in signal['reactions'].items():
                if emoji not in ticker_data[ticker]['top_emojis']:
                    ticker_data[ticker]['top_emojis'][emoji] = 0
                ticker_data[ticker]['top_emojis'][emoji] += count
        
        # Calculate average conviction
        aggregated = []
        for ticker, data in ticker_data.items():
            data['avg_conviction'] = round(
                data['total_conviction'] / data['mention_count'], 
                1
            )
            aggregated.append(data)
        
        # Sort by average conviction (descending)
        aggregated.sort(key=lambda x: x['avg_conviction'], reverse=True)
        
        return aggregated
    
    async def run_scan(
        self,
        channel_ids: List[int],
        hours_back: int = 24,
        min_reactions: int = 5,
        output_file: str = None
    ) -> List[Dict]:
        """
        Main scan execution
        
        Args:
            channel_ids: List of Discord channel IDs to scan
            hours_back: Hours of history
            min_reactions: Minimum reaction count
            output_file: Optional JSON output file
        
        Returns:
            List of aggregated signals
        """
        @self.client.event
        async def on_ready():
            print(f"✅ Connected as {self.client.user}")
            print(f"🔍 Scanning {len(channel_ids)} channel(s)...")
            
            # Scan all channels
            raw_signals = []
            for channel_id in channel_ids:
                signals = await self.scan_channel(
                    channel_id,
                    hours_back=hours_back,
                    min_reactions=min_reactions
                )
                raw_signals.extend(signals)
            
            # Aggregate by ticker
            aggregated = self.aggregate_signals(raw_signals)
            
            self.signals = aggregated
            
            # Save to file
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(aggregated, f, indent=2)
                print(f"💾 Saved {len(aggregated)} signals to {output_file}")
            
            # Print summary
            print(f"\n📊 FOUND {len(aggregated)} UNIQUE TICKERS\n")
            for sig in aggregated[:10]:  # Top 10
                print(f"  {sig['ticker']:6} | Conviction: {sig['avg_conviction']}/10 | "
                      f"Reactions: {sig['total_reactions']} | "
                      f"Mentions: {sig['mention_count']}")
            
            await self.client.close()
        
        # Run
        try:
            await self.client.start(self.token)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return self.signals


async def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dumb Money Discord social arbitrage scanner")
    parser.add_argument('--channels', type=str, help='Comma-separated channel IDs')
    parser.add_argument('--hours', type=int, default=24, help='Hours of history')
    parser.add_argument('--min-reactions', type=int, default=5, help='Minimum reactions')
    parser.add_argument('--output', type=str, default='dumbmoney-signals.json', help='Output file')
    
    args = parser.parse_args()
    
    print("🐓 Dumb Money Social Arbitrage Scanner")
    print("="*60)
    
    # Parse channel IDs
    if args.channels:
        channel_ids = [int(c.strip()) for c in args.channels.split(',')]
    else:
        print("❌ No channels specified. Use --channels CHANNEL_ID1,CHANNEL_ID2")
        print("\nTo find channel IDs:")
        print("  1. Enable Discord Developer Mode (Settings > Advanced)")
        print("  2. Right-click channel → Copy ID")
        return
    
    # Run scanner
    scanner = DumbMoneyScanner()
    signals = await scanner.run_scan(
        channel_ids=channel_ids,
        hours_back=args.hours,
        min_reactions=args.min_reactions,
        output_file=args.output
    )
    
    print(f"\n✅ Scan complete: {len(signals)} signals found")
    print(f"   Output: {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
