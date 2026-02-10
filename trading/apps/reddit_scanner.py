#!/usr/bin/env python3
"""
Reddit Scanner (WallStreetBets) - Social Arbitrage Signal Detection
Scans r/wallstreetbets for high-conviction stock mentions
Uses PRAW (Python Reddit API Wrapper) - free API
"""

import praw
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import os

# Reddit API credentials (free - need to register at reddit.com/prefs/apps)
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USER_AGENT = 'social-arbitrage-scanner/1.0'

OUTPUT_FILE = '/Users/agentjoselo/.openclaw/workspace/trading/reddit-signals.json'

class RedditScanner:
    """Scan Reddit for social arbitrage signals"""
    
    def __init__(self):
        self.reddit = None
        self.subreddits = ['wallstreetbets', 'stocks', 'investing']
        self.upvote_threshold = 500  # Min upvotes for signal
        self.hours_fresh = 48  # Only scan last 48h
        
    def connect(self):
        """Initialize Reddit API connection"""
        if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
            print("⚠️  Reddit API credentials not set")
            print("   1. Go to: https://www.reddit.com/prefs/apps")
            print("   2. Create app (script type)")
            print("   3. Set env vars: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET")
            return False
        
        try:
            self.reddit = praw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT
            )
            # Test connection
            self.reddit.user.me()
            print("✅ Connected to Reddit API")
            return True
        except Exception as e:
            print(f"❌ Reddit API connection failed: {e}")
            return False
    
    def scan_subreddit(self, subreddit_name, limit=100):
        """
        Scan a subreddit for ticker mentions
        
        Args:
            subreddit_name: Name of subreddit (e.g., 'wallstreetbets')
            limit: Number of posts to scan
            
        Returns:
            List of signal dictionaries
        """
        if not self.reddit:
            return []
        
        signals = []
        ticker_mentions = defaultdict(lambda: {
            'posts': [],
            'total_upvotes': 0,
            'total_comments': 0,
            'total_awards': 0,
            'conviction_score': 0
        })
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Scan hot posts (most active now)
            for post in subreddit.hot(limit=limit):
                # Skip if too old
                post_time = datetime.fromtimestamp(post.created_utc)
                if datetime.now() - post_time > timedelta(hours=self.hours_fresh):
                    continue
                
                # Extract tickers from title + body
                tickers = self._extract_tickers(post.title + ' ' + (post.selftext or ''))
                
                for ticker in tickers:
                    ticker_mentions[ticker]['posts'].append({
                        'title': post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'upvotes': post.score,
                        'comments': post.num_comments,
                        'awards': post.total_awards_received,
                        'created': post_time.isoformat(),
                        'subreddit': subreddit_name
                    })
                    ticker_mentions[ticker]['total_upvotes'] += post.score
                    ticker_mentions[ticker]['total_comments'] += post.num_comments
                    ticker_mentions[ticker]['total_awards'] += post.total_awards_received
            
            # Convert to signals
            for ticker, data in ticker_mentions.items():
                # Calculate conviction score
                conviction = self._calculate_conviction(
                    data['total_upvotes'],
                    data['total_comments'],
                    data['total_awards'],
                    len(data['posts'])
                )
                
                # Skip low conviction
                if data['total_upvotes'] < self.upvote_threshold:
                    continue
                
                signal = {
                    'ticker': ticker,
                    'source': f'Reddit-{subreddit_name}',
                    'date_found': datetime.now().strftime('%Y-%m-%d'),
                    'total_upvotes': data['total_upvotes'],
                    'total_comments': data['total_comments'],
                    'total_awards': data['total_awards'],
                    'post_count': len(data['posts']),
                    'conviction_score': conviction,
                    'status': self._get_status(conviction),
                    'top_posts': data['posts'][:3]  # Top 3 posts
                }
                
                signals.append(signal)
        
        except Exception as e:
            print(f"Error scanning r/{subreddit_name}: {e}")
        
        return signals
    
    def _extract_tickers(self, text):
        """Extract stock tickers from text"""
        # Pattern: $TICKER or TICKER: (1-5 uppercase letters)
        tickers = set()
        
        # $TICKER format
        tickers.update(re.findall(r'\$([A-Z]{1,5})\b', text))
        
        # Standalone tickers (more conservative for stocks)
        # Only if surrounded by financial keywords
        words = text.split()
        for i, word in enumerate(words):
            if word.isupper() and 1 <= len(word) <= 5:
                # Check context
                context = ' '.join(words[max(0,i-3):min(len(words),i+3)]).lower()
                if any(kw in context for kw in ['stock', 'share', 'trade', 'call', 'put', 'position']):
                    tickers.add(word)
        
        # Blacklist common words
        blacklist = {'I', 'A', 'THE', 'AND', 'FOR', 'WSB', 'DD', 'YOLO', 'CEO', 'IPO', 'FDA', 'SEC'}
        tickers = {t for t in tickers if t not in blacklist}
        
        return list(tickers)
    
    def _calculate_conviction(self, upvotes, comments, awards, posts):
        """
        Calculate conviction score 1-10
        
        Based on:
        - Upvotes (community agreement)
        - Comments (engagement)
        - Awards (strong conviction - costs money)
        - Post count (frequency of mentions)
        """
        score = 0
        
        # Upvotes (0-4 points)
        if upvotes >= 5000:
            score += 4
        elif upvotes >= 2000:
            score += 3
        elif upvotes >= 1000:
            score += 2
        elif upvotes >= 500:
            score += 1
        
        # Comments (0-3 points)
        if comments >= 500:
            score += 3
        elif comments >= 200:
            score += 2
        elif comments >= 100:
            score += 1
        
        # Awards (0-2 points)
        if awards >= 10:
            score += 2
        elif awards >= 5:
            score += 1
        
        # Post frequency (0-1 point)
        if posts >= 3:
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
    
    def run(self):
        """Main execution"""
        print(f"🔍 Reddit Scanner - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Connect to Reddit
        if not self.connect():
            return []
        
        # Scan all subreddits
        all_signals = []
        for subreddit in self.subreddits:
            print(f"Scanning r/{subreddit}...")
            signals = self.scan_subreddit(subreddit, limit=100)
            all_signals.extend(signals)
            print(f"   Found {len(signals)} signals")
        
        # Consolidate duplicate tickers
        consolidated = self._consolidate_signals(all_signals)
        
        # Sort by conviction
        consolidated.sort(key=lambda x: x['conviction_score'], reverse=True)
        
        # Save to file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(consolidated, f, indent=2)
        
        # Display top signals
        print(f"\n📊 Top 10 Reddit Signals:")
        for i, signal in enumerate(consolidated[:10], 1):
            status_emoji = '🟢' if signal['status'] == 'GREEN' else '🟡' if signal['status'] == 'YELLOW' else '🔴'
            print(f"{status_emoji} {i}. ${signal['ticker']} - "
                  f"{signal['total_upvotes']} upvotes, "
                  f"{signal['total_comments']} comments, "
                  f"{signal['total_awards']} awards, "
                  f"Conviction: {signal['conviction_score']}/10")
        
        print(f"\n💾 Saved {len(consolidated)} signals to {OUTPUT_FILE}")
        
        return consolidated
    
    def _consolidate_signals(self, signals):
        """Consolidate duplicate tickers across subreddits"""
        ticker_map = {}
        
        for signal in signals:
            ticker = signal['ticker']
            
            if ticker not in ticker_map:
                ticker_map[ticker] = signal
            else:
                # Merge data
                existing = ticker_map[ticker]
                existing['total_upvotes'] += signal['total_upvotes']
                existing['total_comments'] += signal['total_comments']
                existing['total_awards'] += signal['total_awards']
                existing['post_count'] += signal['post_count']
                existing['top_posts'].extend(signal['top_posts'])
                
                # Recalculate conviction
                existing['conviction_score'] = self._calculate_conviction(
                    existing['total_upvotes'],
                    existing['total_comments'],
                    existing['total_awards'],
                    existing['post_count']
                )
                existing['status'] = self._get_status(existing['conviction_score'])
                existing['source'] = 'Reddit-Multi'
        
        return list(ticker_map.values())


if __name__ == "__main__":
    scanner = RedditScanner()
    signals = scanner.run()
