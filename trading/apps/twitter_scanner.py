#!/usr/bin/env python3
"""
Twitter/X Scanner - Social Arbitrage Signal Detection
Tracks $TICKER mentions, sentiment, and velocity
Uses Twitter API v2 (Essential tier - free)
"""

import tweepy
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import os

# Twitter API credentials (free Essential tier)
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')

OUTPUT_FILE = '/Users/agentjoselo/.openclaw/workspace/trading/twitter-signals.json'

class TwitterScanner:
    """Scan Twitter for stock ticker mentions and sentiment"""
    
    def __init__(self):
        self.client = None
        self.mention_threshold = 50  # Min mentions for signal
        self.hours_lookback = 24  # Scan last 24h
        
    def connect(self):
        """Initialize Twitter API connection"""
        if not TWITTER_BEARER_TOKEN:
            print("⚠️  Twitter API credentials not set")
            print("   1. Go to: https://developer.twitter.com/en/portal/dashboard")
            print("   2. Create app (Essential tier - free)")
            print("   3. Set env var: TWITTER_BEARER_TOKEN")
            return False
        
        try:
            self.client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
            print("✅ Connected to Twitter API")
            return True
        except Exception as e:
            print(f"❌ Twitter API connection failed: {e}")
            return False
    
    def search_ticker(self, ticker, max_results=100):
        """
        Search Twitter for ticker mentions
        
        Args:
            ticker: Stock symbol (e.g., 'ASTS')
            max_results: Number of tweets to fetch
            
        Returns:
            Signal data dictionary
        """
        if not self.client:
            return None
        
        try:
            # Build query
            query = f"${ticker} -is:retweet lang:en"
            
            # Search tweets (last 7 days max for free tier)
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'verified']
            )
            
            if not tweets.data:
                return None
            
            # Analyze tweets
            total_likes = 0
            total_retweets = 0
            total_replies = 0
            mentions = 0
            verified_mentions = 0
            sample_tweets = []
            
            # Get users data
            users = {user.id: user for user in tweets.includes.get('users', [])}
            
            for tweet in tweets.data:
                metrics = tweet.public_metrics
                total_likes += metrics['like_count']
                total_retweets += metrics['retweet_count']
                total_replies += metrics['reply_count']
                mentions += 1
                
                # Check if author verified
                author = users.get(tweet.author_id)
                if author and author.verified:
                    verified_mentions += 1
                
                # Save sample tweets
                if len(sample_tweets) < 5:
                    sample_tweets.append({
                        'text': tweet.text,
                        'likes': metrics['like_count'],
                        'retweets': metrics['retweet_count'],
                        'created': tweet.created_at.isoformat(),
                        'author': author.username if author else 'unknown',
                        'verified': author.verified if author else False
                    })
            
            # Calculate conviction
            conviction = self._calculate_conviction(
                mentions, total_likes, total_retweets, verified_mentions
            )
            
            signal = {
                'ticker': ticker,
                'source': 'Twitter',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'mentions': mentions,
                'total_likes': total_likes,
                'total_retweets': total_retweets,
                'total_replies': total_replies,
                'verified_mentions': verified_mentions,
                'conviction_score': conviction,
                'status': self._get_status(conviction),
                'sample_tweets': sample_tweets
            }
            
            return signal
        
        except Exception as e:
            print(f"Error searching ${ticker}: {e}")
            return None
    
    def scan_trending_tickers(self, ticker_list):
        """
        Scan a list of tickers for Twitter activity
        
        Args:
            ticker_list: List of stock symbols
            
        Returns:
            List of signal dictionaries
        """
        signals = []
        
        for ticker in ticker_list:
            print(f"   Searching ${ticker}...")
            signal = self.search_ticker(ticker)
            
            if signal and signal['mentions'] >= self.mention_threshold:
                signals.append(signal)
        
        return signals
    
    def _calculate_conviction(self, mentions, likes, retweets, verified):
        """
        Calculate conviction score 1-10
        
        Based on:
        - Mentions (volume)
        - Likes (sentiment)
        - Retweets (virality)
        - Verified accounts (credibility)
        """
        score = 0
        
        # Mentions (0-3 points)
        if mentions >= 500:
            score += 3
        elif mentions >= 200:
            score += 2
        elif mentions >= 50:
            score += 1
        
        # Likes (0-3 points)
        if likes >= 5000:
            score += 3
        elif likes >= 2000:
            score += 2
        elif likes >= 500:
            score += 1
        
        # Retweets (0-2 points)
        if retweets >= 2000:
            score += 2
        elif retweets >= 500:
            score += 1
        
        # Verified mentions (0-2 points)
        if verified >= 5:
            score += 2
        elif verified >= 2:
            score += 1
        
        return min(score, 10)
    
    def _get_status(self, conviction):
        """Convert conviction score to status"""
        if conviction >= 7:
            return 'GREEN'
        elif conviction >= 5:
            return 'YELLOW'
        else:
            return 'RED'
    
    def run(self, ticker_list=None):
        """Main execution"""
        print(f"🔍 Twitter Scanner - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Connect to Twitter
        if not self.connect():
            return []
        
        # Default ticker list (top social arb candidates)
        if not ticker_list:
            ticker_list = [
                'ASTS', 'PLTR', 'NVDA', 'TSLA', 'AMD', 'GOOG', 'META',
                'COIN', 'HOOD', 'RKLB', 'SOFI', 'GME', 'AMC'
            ]
        
        # Scan tickers
        print(f"Scanning {len(ticker_list)} tickers...")
        signals = self.scan_trending_tickers(ticker_list)
        
        # Sort by conviction
        signals.sort(key=lambda x: x['conviction_score'], reverse=True)
        
        # Save to file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(signals, f, indent=2)
        
        # Display results
        print(f"\n📊 Top 10 Twitter Signals:")
        for i, signal in enumerate(signals[:10], 1):
            status_emoji = '🟢' if signal['status'] == 'GREEN' else '🟡' if signal['status'] == 'YELLOW' else '🔴'
            print(f"{status_emoji} {i}. ${signal['ticker']} - "
                  f"{signal['mentions']} mentions, "
                  f"{signal['total_likes']} likes, "
                  f"{signal['verified_mentions']} verified, "
                  f"Conviction: {signal['conviction_score']}/10")
        
        print(f"\n💾 Saved {len(signals)} signals to {OUTPUT_FILE}")
        
        return signals


if __name__ == "__main__":
    scanner = TwitterScanner()
    signals = scanner.run()
