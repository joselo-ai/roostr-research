#!/usr/bin/env python3
"""
Dumb Money Browser Scraper - Uses browser automation to scrape Discord web
No bot permissions needed - works with any server you have access to

Usage:
    python3 dumbmoney_browser_scraper.py --channel-url "https://discord.com/channels/..." --hours 24
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Conviction emoji weights (same as bot scraper)
CONVICTION_EMOJIS = {
    '🚀': 3.0,
    '🔥': 2.5,
    '💎': 2.0,
    '💯': 1.5,
    '👀': 1.0,
    '📈': 1.5,
    '🤑': 1.0,
    '⚡': 1.0,
}

def extract_tickers(text):
    """Extract stock tickers from message text"""
    if not text:
        return []
    
    tickers = []
    
    # Match $TICKER format
    dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
    tickers.extend(dollar_tickers)
    
    # Match standalone tickers (2-5 chars)
    excluded = {'THIS', 'THAT', 'MAKE', 'JUST', 'OVER', 'MORE', 'SOME', 'VERY', 'ONLY', 'LIKE', 'BEEN', 'WHEN', 'WILL', 'CALL', 'PUTS', 'SAME', 'FROM', 'WITH'}
    standalone = re.findall(r'\b([A-Z]{2,5})\b', text)
    tickers.extend([t for t in standalone if t not in excluded])
    
    # Remove duplicates
    seen = set()
    unique = []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    
    return unique

def calculate_conviction(reactions):
    """Calculate conviction score from emoji reactions"""
    total = 0.0
    for emoji, count in reactions.items():
        weight = CONVICTION_EMOJIS.get(emoji, 0.1)
        total += weight * count
    
    # Scale to 0-10 (20+ weighted reactions = 10/10)
    normalized = min(10.0, (total / 20.0) * 10.0)
    return round(normalized, 1)

def parse_discord_messages(messages_json):
    """
    Parse messages scraped from Discord browser
    
    Args:
        messages_json: JSON array of messages with format:
            [
                {
                    "author": "UserName",
                    "content": "message text",
                    "timestamp": "2h ago",
                    "reactions": {"🚀": 23, "🔥": 18}
                }
            ]
    """
    signals = {}
    
    for msg in messages_json:
        author = msg.get('author', 'Unknown')
        content = msg.get('content', '')
        reactions = msg.get('reactions', {})
        timestamp = msg.get('timestamp', '')
        
        # Extract tickers
        tickers = extract_tickers(content)
        if not tickers:
            continue
        
        # Count total reactions
        total_reactions = sum(reactions.values())
        if total_reactions < 5:  # Minimum threshold
            continue
        
        # Calculate conviction
        conviction = calculate_conviction(reactions)
        
        # Aggregate by ticker
        for ticker in tickers:
            if ticker not in signals:
                signals[ticker] = {
                    'ticker': ticker,
                    'source': 'dumbmoney-browser',
                    'total_reactions': 0,
                    'total_conviction': 0.0,
                    'mention_count': 0,
                    'messages': [],
                    'top_emojis': {}
                }
            
            signals[ticker]['total_reactions'] += total_reactions
            signals[ticker]['total_conviction'] += conviction
            signals[ticker]['mention_count'] += 1
            signals[ticker]['messages'].append({
                'author': author,
                'content': content[:150],
                'timestamp': timestamp
            })
            
            # Aggregate emojis
            for emoji, count in reactions.items():
                if emoji not in signals[ticker]['top_emojis']:
                    signals[ticker]['top_emojis'][emoji] = 0
                signals[ticker]['top_emojis'][emoji] += count
    
    # Calculate average conviction
    aggregated = []
    for ticker, data in signals.items():
        data['avg_conviction'] = round(
            data['total_conviction'] / data['mention_count'],
            1
        )
        aggregated.append(data)
    
    # Sort by conviction
    aggregated.sort(key=lambda x: x['avg_conviction'], reverse=True)
    
    return aggregated

def save_signals(signals, output_file):
    """Save signals to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(signals, f, indent=2)
    
    print(f"\n💾 Saved {len(signals)} signals to {output_file}")

def print_report(signals):
    """Print signal report"""
    print(f"\n{'='*60}")
    print(f"📊 DUMB MONEY SIGNALS REPORT")
    print(f"{'='*60}\n")
    
    if not signals:
        print("No signals found.")
        return
    
    print(f"Found {len(signals)} unique tickers\n")
    
    for sig in signals[:10]:  # Top 10
        print(f"🎯 {sig['ticker']:6} | Conviction: {sig['avg_conviction']}/10")
        print(f"   Reactions: {sig['total_reactions']} | Mentions: {sig['mention_count']}")
        
        # Top 3 emojis
        top_emojis = sorted(sig['top_emojis'].items(), key=lambda x: x[1], reverse=True)[:3]
        emoji_str = " ".join([f"{e}×{c}" for e, c in top_emojis])
        print(f"   {emoji_str}")
        
        # Sample message
        if sig['messages']:
            msg = sig['messages'][0]
            print(f"   @{msg['author']}: {msg['content'][:80]}...")
        print()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Browser-based Dumb Money Discord scraper")
    parser.add_argument('--messages-file', type=str, help='JSON file with scraped messages')
    parser.add_argument('--output', type=str, default='dumbmoney-signals.json', help='Output file')
    
    args = parser.parse_args()
    
    print("🐓 Dumb Money Browser Scraper")
    print("="*60)
    
    # For now, expect messages to be provided via file
    # Browser scraping will be done by a separate OpenClaw command
    
    if args.messages_file:
        with open(args.messages_file, 'r') as f:
            messages = json.load(f)
        
        signals = parse_discord_messages(messages)
        print_report(signals)
        save_signals(signals, args.output)
    else:
        print("\n⚠️  No messages file provided.")
        print("Usage:")
        print("  1. First, scrape Discord using browser automation")
        print("  2. Save messages to JSON file")
        print("  3. Run this script with --messages-file")
        print("\nExample messages format:")
        print("""
[
  {
    "author": "TraderJoe",
    "content": "$NVDA breaking out 🚀🚀🚀",
    "timestamp": "2h ago",
    "reactions": {"🚀": 23, "🔥": 18, "💎": 12}
  }
]
""")

if __name__ == "__main__":
    main()
