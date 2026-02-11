#!/usr/bin/env python3
"""
Social Arbitrage Agent - Reddit/Discord Stock Signal Scanner
============================================================

Scans social platforms for viral stock signals using engagement metrics.
Inspired by Camillo's 77% annual returns from social arbitrage.

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 11, 2026
"""

import os
import json
import pandas as pd
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from collections import defaultdict

class SocialArbitrageAgent:
    """
    Scans Reddit, Discord, Twitter for high-engagement stock signals.
    
    Logic:
    - High engagement (upvotes, 🔥 reactions) = crowd attention
    - Low market cap (<$5B) = room to run
    - Catalyst present = reason for move
    - Signal Score = engagement * catalyst_multiplier / market_cap_billions
    """
    
    def __init__(self, min_engagement=20, max_market_cap=5e9):
        self.min_engagement = min_engagement
        self.max_market_cap = max_market_cap
        self.signals = []
        
    def scan_reddit(self, subreddits=['wallstreetbets', 'stocks'], lookback_days=1) -> List[Dict]:
        """
        Scan Reddit for stock mentions with high engagement.
        
        Uses Pushshift API (Reddit archive) or Reddit API if available.
        """
        print(f"🐓 Scanning Reddit: {subreddits} (last {lookback_days} days)")
        
        signals = []
        
        # Check if Reddit API credentials available
        reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        reddit_secret = os.getenv('REDDIT_SECRET')
        
        if reddit_client_id and reddit_secret:
            signals = self._scan_reddit_api(subreddits, lookback_days)
        else:
            print("⚠️  Reddit API credentials not set. Using mock data for demo.")
            signals = self._scan_reddit_mock(subreddits, lookback_days)
        
        return signals
    
    def _scan_reddit_api(self, subreddits, lookback_days) -> List[Dict]:
        """Real Reddit API scanning (requires credentials)"""
        # TODO: Implement PRAW (Python Reddit API Wrapper)
        # This would use reddit.subreddit(name).hot(limit=100)
        # and extract tickers from titles/bodies
        pass
    
    def _scan_reddit_mock(self, subreddits, lookback_days) -> List[Dict]:
        """
        Mock Reddit data for testing.
        Returns example signals based on known Dumb Money patterns.
        """
        mock_posts = [
            {
                'ticker': 'ASTS',
                'title': 'AST SpaceMobile: FCC approval imminent 🚀',
                'upvotes': 342,
                'comments': 87,
                'fire_reactions': 34,
                'rocket_reactions': 16,
                'subreddit': 'wallstreetbets',
                'url': 'https://reddit.com/r/wallstreetbets/example',
                'posted_date': datetime.now() - timedelta(hours=12),
                'catalyst': 'FCC approval expected Q1 2026',
                'market_cap': 4.2e9  # $4.2B
            },
            {
                'ticker': 'ACGL',
                'title': 'Arch Capital (ACGL) - insurance play after natural disasters',
                'upvotes': 156,
                'comments': 42,
                'fire_reactions': 23,
                'rocket_reactions': 8,
                'subreddit': 'stocks',
                'url': 'https://reddit.com/r/stocks/example',
                'posted_date': datetime.now() - timedelta(days=1),
                'catalyst': 'Insurance sector strength post-hurricane season',
                'market_cap': 28e9  # $28B
            },
            {
                'ticker': 'PLTR',
                'title': 'Palantir government contracts expanding 🔥',
                'upvotes': 523,
                'comments': 134,
                'fire_reactions': 67,
                'rocket_reactions': 45,
                'subreddit': 'wallstreetbets',
                'url': 'https://reddit.com/r/wallstreetbets/example2',
                'posted_date': datetime.now() - timedelta(hours=6),
                'catalyst': 'New $500M Pentagon contract',
                'market_cap': 42e9  # $42B (too large)
            }
        ]
        
        signals = []
        for post in mock_posts:
            engagement_score = (
                post['upvotes'] + 
                post['comments'] * 2 + 
                post['fire_reactions'] * 3 + 
                post['rocket_reactions'] * 3
            )
            
            # Filter by engagement and market cap
            if engagement_score >= self.min_engagement and post['market_cap'] <= self.max_market_cap:
                signal = {
                    'ticker': post['ticker'],
                    'source': f"Reddit-{post['subreddit']}",
                    'engagement_score': engagement_score,
                    'upvotes': post['upvotes'],
                    'comments': post['comments'],
                    'fire_reactions': post['fire_reactions'],
                    'rocket_reactions': post['rocket_reactions'],
                    'catalyst': post['catalyst'],
                    'market_cap': post['market_cap'],
                    'url': post['url'],
                    'found_date': post['posted_date'].strftime('%Y-%m-%d'),
                    'title': post['title']
                }
                signals.append(signal)
        
        return signals
    
    def extract_tickers(self, text: str) -> List[str]:
        """
        Extract stock tickers from text.
        Format: $TICKER or TICKER (3-5 uppercase letters)
        """
        # Pattern 1: $TICKER format
        pattern1 = r'\$([A-Z]{1,5})\b'
        # Pattern 2: Standalone TICKER (3-5 caps, not part of word)
        pattern2 = r'\b([A-Z]{3,5})\b'
        
        tickers = []
        tickers.extend(re.findall(pattern1, text))
        tickers.extend(re.findall(pattern2, text))
        
        # Filter out common false positives
        blacklist = {'CEO', 'USA', 'SEC', 'ETF', 'IPO', 'DD', 'YOLO', 'WSB', 'IMO', 'FOMO'}
        tickers = [t for t in tickers if t not in blacklist]
        
        return list(set(tickers))  # Remove duplicates
    
    def get_market_cap(self, ticker: str) -> Optional[float]:
        """
        Get market cap for ticker using yfinance.
        Returns None if data unavailable.
        """
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            return info.get('marketCap', None)
        except Exception as e:
            print(f"⚠️  Could not fetch market cap for {ticker}: {e}")
            return None
    
    def calculate_conviction_score(self, signal: Dict) -> float:
        """
        Calculate conviction score (0-10) based on:
        - Engagement (higher = better)
        - Market cap (lower = more room to run)
        - Catalyst presence (yes = 2x multiplier)
        
        Formula: score = (engagement / 100) * catalyst_mult * (5B / market_cap_B)
        Capped at 10.
        """
        engagement = signal['engagement_score']
        market_cap_b = signal['market_cap'] / 1e9
        catalyst_mult = 2.0 if signal.get('catalyst') else 1.0
        
        # Base score from engagement
        base_score = (engagement / 100)
        
        # Market cap bonus (smaller = better)
        # $1B cap = 5x bonus, $5B cap = 1x bonus
        cap_bonus = min(5.0, 5.0 / market_cap_b)
        
        # Final score
        score = base_score * catalyst_mult * cap_bonus
        
        # Cap at 10
        return min(10.0, score)
    
    def score_signals(self, signals: List[Dict]) -> List[Dict]:
        """Add conviction scores to all signals"""
        for signal in signals:
            signal['conviction_score'] = self.calculate_conviction_score(signal)
        
        # Sort by conviction (highest first)
        signals.sort(key=lambda x: x['conviction_score'], reverse=True)
        
        return signals
    
    def filter_signals(self, signals: List[Dict], min_conviction=5.0) -> List[Dict]:
        """Filter signals by minimum conviction score"""
        return [s for s in signals if s['conviction_score'] >= min_conviction]
    
    def generate_report(self, signals: List[Dict]) -> str:
        """Generate human-readable report"""
        report = []
        report.append("=" * 80)
        report.append("🐓 SOCIAL ARBITRAGE AGENT REPORT")
        report.append("=" * 80)
        report.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M EST')}")
        report.append(f"Signals Found: {len(signals)}")
        report.append("")
        
        if not signals:
            report.append("❌ No signals found meeting criteria.")
            return "\n".join(report)
        
        for i, signal in enumerate(signals, 1):
            report.append(f"\n📊 SIGNAL #{i}: {signal['ticker']}")
            report.append(f"   Conviction: {signal['conviction_score']:.1f}/10")
            report.append(f"   Source: {signal['source']}")
            report.append(f"   Engagement: {signal['engagement_score']} points")
            report.append(f"      ├─ Upvotes: {signal['upvotes']}")
            report.append(f"      ├─ Comments: {signal['comments']}")
            report.append(f"      ├─ 🔥 Reactions: {signal['fire_reactions']}")
            report.append(f"      └─ 🚀 Reactions: {signal['rocket_reactions']}")
            report.append(f"   Market Cap: ${signal['market_cap']/1e9:.2f}B")
            report.append(f"   Catalyst: {signal.get('catalyst', 'None identified')}")
            report.append(f"   Title: {signal['title'][:80]}")
            report.append(f"   URL: {signal['url']}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def save_to_database(self, signals: List[Dict], db_path='signals-database.csv'):
        """Append signals to signals database"""
        if not signals:
            print("⚠️  No signals to save.")
            return
        
        # Convert to DataFrame
        df_new = pd.DataFrame(signals)
        
        # Rename columns to match existing database schema
        df_new = df_new.rename(columns={
            'ticker': 'Ticker',
            'conviction_score': 'Conviction_Score',
            'source': 'Source',
            'found_date': 'Date_Found',
            'catalyst': 'Notes'
        })
        
        # Add missing columns
        df_new['Status'] = 'Monitoring'
        df_new['Price_Entry'] = None
        df_new['Date_Entry'] = None
        
        # Select only columns that exist in database
        cols = ['Ticker', 'Source', 'Date_Found', 'Conviction_Score', 'Status', 
                'Price_Entry', 'Date_Entry', 'Notes']
        df_new = df_new[cols]
        
        # Load existing database
        if os.path.exists(db_path):
            df_existing = pd.read_csv(db_path)
            
            # Avoid duplicates (same ticker + date)
            df_new = df_new[~df_new[['Ticker', 'Date_Found']].apply(tuple, axis=1).isin(
                df_existing[['Ticker', 'Date_Found']].apply(tuple, axis=1)
            )]
            
            if df_new.empty:
                print("✅ All signals already in database.")
                return
            
            # Append new signals
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        
        # Save
        df_combined.to_csv(db_path, index=False)
        print(f"✅ Saved {len(df_new)} new signals to {db_path}")
    
    def run_scan(self, save=True, min_conviction=5.0) -> List[Dict]:
        """
        Main entry point: Run full scan pipeline.
        
        Returns: List of high-conviction signals
        """
        print("\n" + "=" * 80)
        print("🐓 SOCIAL ARBITRAGE AGENT - Daily Scan")
        print("=" * 80)
        
        # Step 1: Scan Reddit
        signals = self.scan_reddit(['wallstreetbets', 'stocks'], lookback_days=1)
        print(f"✅ Found {len(signals)} raw signals")
        
        # Step 2: Score signals
        signals = self.score_signals(signals)
        print(f"✅ Scored all signals (conviction range: {min([s['conviction_score'] for s in signals]):.1f}-{max([s['conviction_score'] for s in signals]):.1f})")
        
        # Step 3: Filter by conviction
        high_conviction = self.filter_signals(signals, min_conviction=min_conviction)
        print(f"✅ Filtered to {len(high_conviction)} signals with conviction ≥{min_conviction}/10")
        
        # Step 4: Generate report
        report = self.generate_report(high_conviction)
        print("\n" + report)
        
        # Step 5: Save to database
        if save and high_conviction:
            self.save_to_database(high_conviction)
        
        return high_conviction


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Arbitrage Agent - Scan Reddit/Discord for stock signals')
    parser.add_argument('--min-engagement', type=int, default=20, help='Minimum engagement score')
    parser.add_argument('--max-market-cap', type=float, default=5e9, help='Maximum market cap ($)')
    parser.add_argument('--min-conviction', type=float, default=5.0, help='Minimum conviction score (0-10)')
    parser.add_argument('--no-save', action='store_true', help='Do not save to database')
    parser.add_argument('--test', action='store_true', help='Test mode (use mock data)')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = SocialArbitrageAgent(
        min_engagement=args.min_engagement,
        max_market_cap=args.max_market_cap
    )
    
    # Run scan
    signals = agent.run_scan(
        save=not args.no_save,
        min_conviction=args.min_conviction
    )
    
    print(f"\n✅ Scan complete. Found {len(signals)} high-conviction signals.")
    

if __name__ == '__main__':
    main()
