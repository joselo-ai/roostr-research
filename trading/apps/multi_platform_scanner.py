#!/usr/bin/env python3
"""
Multi-Platform Social Scanner - Camillo's Edge Replicated
Combines Discord + Reddit + Twitter + Google Trends
Only signals validated across 3+ platforms = GREEN

This is how Camillo achieved 77% annual returns:
- Information arbitrage (early detection before Wall Street)
- Multi-source validation (reduces false positives)
- Velocity tracking (momentum building)
"""

import json
from datetime import datetime
import os
import sys

# Import individual scanners
sys.path.append('/Users/agentjoselo/.openclaw/workspace/trading/apps')

try:
    from reddit_scanner import RedditScanner
    REDDIT_AVAILABLE = True
except:
    REDDIT_AVAILABLE = False

try:
    from twitter_scanner import TwitterScanner
    TWITTER_AVAILABLE = True
except:
    TWITTER_AVAILABLE = False

try:
    from google_trends_validator import GoogleTrendsValidator
    TRENDS_AVAILABLE = True
except:
    TRENDS_AVAILABLE = False

try:
    from dumbmoney_scraper import DumbMoneyScraper
    DISCORD_AVAILABLE = True
except:
    DISCORD_AVAILABLE = False

OUTPUT_FILE = '/Users/agentjoselo/.openclaw/workspace/trading/multi-platform-signals.json'
SIGNALS_DB = '/Users/agentjoselo/.openclaw/workspace/trading/signals-database.csv'

class MultiPlatformScanner:
    """Combine all social platforms for maximum signal quality"""
    
    def __init__(self):
        self.platforms = {
            'reddit': None,
            'twitter': None,
            'trends': None,
            'discord': None
        }
        
        # Multi-platform thresholds for GREEN
        self.min_platforms = 3  # Must appear on 3+ platforms
        self.min_conviction = 7  # Average conviction >= 7/10
        
    def initialize(self):
        """Initialize all available scanners"""
        print("🚀 Initializing Multi-Platform Scanner\n")
        
        if REDDIT_AVAILABLE:
            self.platforms['reddit'] = RedditScanner()
            print("✅ Reddit scanner loaded")
        else:
            print("⚠️  Reddit scanner not available (install praw: pip install praw)")
        
        if TWITTER_AVAILABLE:
            self.platforms['twitter'] = TwitterScanner()
            print("✅ Twitter scanner loaded")
        else:
            print("⚠️  Twitter scanner not available (need TWITTER_BEARER_TOKEN)")
        
        if TRENDS_AVAILABLE:
            self.platforms['trends'] = GoogleTrendsValidator()
            print("✅ Google Trends validator loaded")
        else:
            print("⚠️  Google Trends validator not available (install pytrends: pip install pytrends)")
        
        if DISCORD_AVAILABLE:
            self.platforms['discord'] = DumbMoneyScraper()
            print("✅ Discord scanner loaded")
        else:
            print("⚠️  Discord scanner not available")
        
        print()
    
    def scan_all_platforms(self):
        """
        Run all platform scanners and collect signals
        
        Returns:
            Dictionary of signals by platform
        """
        all_signals = {
            'reddit': [],
            'twitter': [],
            'discord': [],
            'trends': []
        }
        
        # Reddit
        if self.platforms['reddit']:
            print("📊 Scanning Reddit (WSB, r/stocks, r/investing)...")
            try:
                all_signals['reddit'] = self.platforms['reddit'].run()
            except Exception as e:
                print(f"   ❌ Reddit scan failed: {e}")
        
        # Twitter
        if self.platforms['twitter']:
            print("\n📊 Scanning Twitter (top trending tickers)...")
            try:
                all_signals['twitter'] = self.platforms['twitter'].run()
            except Exception as e:
                print(f"   ❌ Twitter scan failed: {e}")
        
        # Discord (Dumb Money)
        if self.platforms['discord']:
            print("\n📊 Scanning Discord (Dumb Money community)...")
            try:
                # Load recent Discord messages (if available)
                # For now, skip unless we have message data
                print("   ⚠️  Discord message data not available (run discord scraper first)")
            except Exception as e:
                print(f"   ❌ Discord scan failed: {e}")
        
        return all_signals
    
    def cross_validate(self, platform_signals):
        """
        Cross-validate signals across platforms
        
        A ticker is GREEN only if:
        1. Appears on 3+ platforms
        2. Average conviction >= 7/10
        3. Google Trends shows RISING
        
        Returns:
            List of validated multi-platform signals
        """
        # Build ticker map
        ticker_map = {}
        
        for platform, signals in platform_signals.items():
            if platform == 'trends':
                continue  # Trends is validation layer, not signal source
            
            for signal in signals:
                ticker = signal.get('ticker', '')
                if not ticker:
                    continue
                
                if ticker not in ticker_map:
                    ticker_map[ticker] = {
                        'ticker': ticker,
                        'platforms': [],
                        'platform_data': {},
                        'total_conviction': 0,
                        'conviction_count': 0
                    }
                
                ticker_map[ticker]['platforms'].append(platform)
                ticker_map[ticker]['platform_data'][platform] = signal
                
                # Add conviction score
                conviction = signal.get('conviction_score', 0)
                ticker_map[ticker]['total_conviction'] += conviction
                ticker_map[ticker]['conviction_count'] += 1
        
        # Validate with Google Trends
        if self.platforms['trends']:
            print(f"\n🔍 Validating {len(ticker_map)} tickers with Google Trends...")
            
            tickers_to_validate = list(ticker_map.keys())
            validations = self.platforms['trends'].validate_signals(tickers_to_validate)
            
            for validation in validations:
                ticker = validation['ticker']
                if ticker in ticker_map:
                    ticker_map[ticker]['google_trends'] = validation
                    ticker_map[ticker]['trends_rising'] = validation.get('trend') == 'RISING'
        
        # Filter to multi-platform signals
        validated_signals = []
        
        for ticker, data in ticker_map.items():
            platform_count = len(data['platforms'])
            avg_conviction = data['total_conviction'] / max(data['conviction_count'], 1)
            trends_rising = data.get('trends_rising', False)
            
            # Calculate final status
            status = 'RED'
            
            if platform_count >= self.min_platforms and avg_conviction >= self.min_conviction and trends_rising:
                status = 'GREEN'
            elif platform_count >= 2 and avg_conviction >= 5:
                status = 'YELLOW'
            
            signal = {
                'ticker': ticker,
                'status': status,
                'platform_count': platform_count,
                'platforms': data['platforms'],
                'avg_conviction': round(avg_conviction, 1),
                'google_trends': data.get('google_trends', {}),
                'platform_data': data['platform_data'],
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Multi-Platform'
            }
            
            validated_signals.append(signal)
        
        # Sort by conviction
        validated_signals.sort(key=lambda x: (
            x['platform_count'],
            x['avg_conviction']
        ), reverse=True)
        
        return validated_signals
    
    def display_results(self, signals):
        """Display final results"""
        print("\n" + "="*80)
        print("🎯 MULTI-PLATFORM SOCIAL ARBITRAGE SIGNALS")
        print("="*80 + "\n")
        
        green = [s for s in signals if s['status'] == 'GREEN']
        yellow = [s for s in signals if s['status'] == 'YELLOW']
        
        print(f"🟢 GREEN SIGNALS ({len(green)}) - Deploy capital")
        print("-" * 80)
        for signal in green:
            trends = signal['google_trends']
            print(f"\n${signal['ticker']}")
            print(f"   Platforms: {', '.join(signal['platforms'])} ({signal['platform_count']})")
            print(f"   Avg Conviction: {signal['avg_conviction']}/10")
            print(f"   Google Trends: {trends.get('trend', 'N/A')} "
                  f"({trends.get('change_percent', 0):+.1f}%)")
            
            # Show platform details
            for platform, data in signal['platform_data'].items():
                if platform == 'reddit':
                    print(f"   Reddit: {data['total_upvotes']} upvotes, "
                          f"{data['total_comments']} comments")
                elif platform == 'twitter':
                    print(f"   Twitter: {data['mentions']} mentions, "
                          f"{data['total_likes']} likes")
                elif platform == 'discord':
                    print(f"   Discord: {data['total_reactions']} reactions")
        
        print(f"\n🟡 YELLOW SIGNALS ({len(yellow)}) - Watch list")
        print("-" * 80)
        for signal in yellow[:5]:  # Top 5 only
            print(f"${signal['ticker']}: {', '.join(signal['platforms'])} "
                  f"({signal['avg_conviction']}/10)")
        
        print(f"\n💾 Total signals: {len(signals)}")
        print(f"   GREEN (deploy): {len(green)}")
        print(f"   YELLOW (watch): {len(yellow)}")
        print(f"\n✅ Saved to: {OUTPUT_FILE}")
    
    def save_results(self, signals):
        """Save results to JSON"""
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(signals, f, indent=2)
    
    def run(self):
        """Main execution"""
        print(f"\n🐓 Multi-Platform Social Scanner - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print("Replicating Chris Camillo's 77% annual return methodology:")
        print("• Multi-source validation (Discord + Reddit + Twitter + Trends)")
        print("• Information arbitrage (early detection before Wall Street)")
        print("• Velocity tracking (momentum building)")
        print("="*80 + "\n")
        
        # Initialize
        self.initialize()
        
        # Scan all platforms
        platform_signals = self.scan_all_platforms()
        
        # Cross-validate
        print("\n" + "="*80)
        print("🔍 CROSS-PLATFORM VALIDATION")
        print("="*80)
        validated_signals = self.cross_validate(platform_signals)
        
        # Display results
        self.display_results(validated_signals)
        
        # Save
        self.save_results(validated_signals)
        
        return validated_signals


if __name__ == "__main__":
    scanner = MultiPlatformScanner()
    signals = scanner.run()
