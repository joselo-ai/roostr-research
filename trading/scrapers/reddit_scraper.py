#!/usr/bin/env python3
"""
Reddit Social Sentiment Scraper
Monitors r/wallstreetbets, r/stocks, r/investing, r/stockmarket
Tracks ticker mentions, sentiment, conviction signals for social arbitrage
"""

import re
import json
import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import defaultdict, Counter

try:
    import praw
    from praw.models import Submission, Comment
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    Submission = None  # Type hint placeholder
    Comment = None
    print("⚠️  PRAW not installed. Run: pip install praw")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("⚠️  TextBlob not installed. Run: pip install textblob")


class RedditScraper:
    """Extract social sentiment signals from Reddit"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize Reddit scraper
        
        Args:
            config_path: Path to reddit_config.json (defaults to ../config/reddit_config.json)
        """
        self.subreddits = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']
        self.output_file = '../signals-database.csv'
        self.cache_file = '../.reddit_cache.json'
        
        # Thresholds for conviction scoring
        self.min_upvotes = 50  # Minimum post upvotes for consideration
        self.high_upvotes = 500  # High conviction threshold
        self.min_comments = 10  # Minimum comments for engagement
        self.high_comments = 100  # High engagement threshold
        
        # Load config
        if config_path is None:
            config_path = '../config/reddit_config.json'
        
        self.config = self._load_config(config_path)
        
        # Initialize Reddit API
        if PRAW_AVAILABLE and self.config:
            try:
                self.reddit = praw.Reddit(
                    client_id=self.config.get('client_id'),
                    client_secret=self.config.get('client_secret'),
                    user_agent=self.config.get('user_agent', 'OpenClaw Trading Signal Bot v1.0')
                )
                self.reddit.read_only = True
                print("✅ Reddit API initialized")
            except Exception as e:
                print(f"❌ Reddit API init failed: {e}")
                self.reddit = None
        else:
            self.reddit = None
    
    def _load_config(self, config_path: str) -> Dict[str, str]:
        """Load Reddit API credentials from config file"""
        if not os.path.exists(config_path):
            print(f"⚠️  Config not found: {config_path}")
            print("   Create config with Reddit API credentials")
            return {}
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Config load error: {e}")
            return {}
    
    def extract_tickers(self, text: str) -> List[str]:
        """
        Extract stock tickers from text
        
        Matches:
        - $TICKER format (most common on Reddit)
        - Standalone TICKER in financial context
        
        Args:
            text: Post/comment text
            
        Returns:
            List of unique ticker symbols
        """
        tickers = set()
        
        # Pattern 1: $TICKER (primary Reddit format)
        dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
        tickers.update(dollar_tickers)
        
        # Pattern 2: TICKER surrounded by spaces or punctuation
        # Only if text contains financial keywords
        financial_keywords = ['stock', 'share', 'buy', 'sell', 'calls', 'puts', 
                              'price', 'target', 'earnings', 'revenue', 'DD', 'YOLO']
        
        text_lower = text.lower()
        has_financial_context = any(kw in text_lower for kw in financial_keywords)
        
        if has_financial_context:
            standalone_tickers = re.findall(r'\b([A-Z]{2,5})\b', text)
            tickers.update(standalone_tickers)
        
        # Blacklist common false positives
        blacklist = {
            'I', 'A', 'THE', 'AND', 'FOR', 'ARE', 'CAN', 'CEO', 'CFO', 'USA', 
            'NYSE', 'NASDAQ', 'IMO', 'OP', 'DD', 'YOLO', 'WSB', 'ATH', 'ATL',
            'AM', 'PM', 'EST', 'PST', 'UTC', 'IPO', 'ETF', 'SP', 'US', 'UK',
            'RE', 'IT', 'AI', 'TO', 'OR', 'SO', 'GO', 'NO', 'ON', 'AT', 'BY',
            'UP', 'ALL', 'NEW', 'OUT', 'NOW', 'EOD', 'AH', 'PM'
        }
        
        tickers = {t for t in tickers if t not in blacklist}
        
        return list(tickers)
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text using TextBlob
        
        Args:
            text: Post/comment content
            
        Returns:
            Tuple of (sentiment_label, confidence_score)
            sentiment_label: 'positive', 'negative', or 'neutral'
            confidence_score: -1.0 to 1.0
        """
        if not TEXTBLOB_AVAILABLE:
            return 'neutral', 0.0
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return sentiment, polarity
        
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 'neutral', 0.0
    
    def calculate_conviction_score(self, submission, 
                                   sentiment: str, 
                                   comment_count: int) -> int:
        """
        Calculate conviction score 1-10 based on engagement and sentiment
        
        High conviction = high upvotes + high comments + positive sentiment
        
        Args:
            submission: Reddit submission object
            sentiment: Sentiment label
            comment_count: Number of comments
            
        Returns:
            Conviction score 1-10
        """
        score = 5  # Base score
        
        # Upvote factor
        upvotes = submission.score
        if upvotes >= 5000:
            score += 3
        elif upvotes >= 1000:
            score += 2
        elif upvotes >= 500:
            score += 1
        elif upvotes < 50:
            score -= 1
        
        # Comment engagement factor
        if comment_count >= 500:
            score += 2
        elif comment_count >= 100:
            score += 1
        elif comment_count < 10:
            score -= 1
        
        # Sentiment factor
        if sentiment == 'positive':
            score += 1
        elif sentiment == 'negative':
            score -= 2
        
        # Award factor (gilded posts show strong community support)
        if submission.gilded > 0:
            score += 1
        
        # Upvote ratio (controversial posts get lower score)
        if hasattr(submission, 'upvote_ratio') and submission.upvote_ratio < 0.7:
            score -= 1
        
        # Cap between 1-10
        return max(1, min(10, score))
    
    def scrape_subreddit(self, subreddit_name: str, 
                         time_filter: str = 'day',
                         limit: int = 100) -> List[Dict[str, Any]]:
        """
        Scrape a single subreddit for ticker mentions
        
        Args:
            subreddit_name: Name of subreddit (e.g., 'wallstreetbets')
            time_filter: Time range ('hour', 'day', 'week', 'month')
            limit: Max posts to scrape
            
        Returns:
            List of signal dictionaries
        """
        if not self.reddit:
            print(f"❌ Reddit API not available")
            return []
        
        signals = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get hot posts (most engaging right now)
            for submission in subreddit.hot(limit=limit):
                # Skip stickied/pinned posts
                if submission.stickied:
                    continue
                
                # Check minimum engagement
                if submission.score < self.min_upvotes:
                    continue
                
                # Extract tickers from title and selftext
                text = f"{submission.title} {submission.selftext}"
                tickers = self.extract_tickers(text)
                
                if not tickers:
                    continue
                
                # Analyze sentiment
                sentiment, polarity = self.analyze_sentiment(text)
                
                # Get comment count
                comment_count = submission.num_comments
                
                # Calculate conviction
                conviction = self.calculate_conviction_score(
                    submission, sentiment, comment_count
                )
                
                # Create signal for each ticker mentioned
                for ticker in tickers:
                    signal = {
                        'ticker': ticker,
                        'source': f'Reddit-{subreddit_name}',
                        'subreddit': subreddit_name,
                        'post_id': submission.id,
                        'post_title': submission.title[:150],
                        'post_url': f"https://reddit.com{submission.permalink}",
                        'upvotes': submission.score,
                        'comments': comment_count,
                        'upvote_ratio': getattr(submission, 'upvote_ratio', 0),
                        'gilded': submission.gilded,
                        'sentiment': sentiment,
                        'sentiment_score': round(polarity, 2),
                        'conviction_score': conviction,
                        'timestamp': datetime.fromtimestamp(submission.created_utc).isoformat(),
                        'text_snippet': text[:300]
                    }
                    
                    signals.append(signal)
            
            print(f"✅ {subreddit_name}: Found {len(signals)} ticker mentions")
        
        except Exception as e:
            print(f"❌ Error scraping r/{subreddit_name}: {e}")
        
        return signals
    
    def scrape_all_subreddits(self, time_filter: str = 'day', 
                               limit_per_sub: int = 100) -> List[Dict[str, Any]]:
        """
        Scrape all configured subreddits
        
        Args:
            time_filter: Time range for posts
            limit_per_sub: Max posts per subreddit
            
        Returns:
            Combined list of all signals
        """
        all_signals = []
        
        print(f"🔍 Scraping {len(self.subreddits)} subreddits...")
        
        for subreddit in self.subreddits:
            signals = self.scrape_subreddit(subreddit, time_filter, limit_per_sub)
            all_signals.extend(signals)
        
        print(f"\n📊 Total signals extracted: {len(all_signals)}")
        return all_signals
    
    def aggregate_ticker_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aggregate multiple mentions of same ticker
        
        Combines:
        - Total mentions across subreddits
        - Average sentiment
        - Max conviction score
        - Sum of upvotes/comments
        
        Args:
            signals: Raw signal list
            
        Returns:
            Aggregated signals (one per ticker)
        """
        ticker_data = defaultdict(lambda: {
            'mentions': 0,
            'upvotes': 0,
            'comments': 0,
            'sentiment_scores': [],
            'conviction_scores': [],
            'subreddits': set(),
            'posts': []
        })
        
        # Aggregate data
        for signal in signals:
            ticker = signal['ticker']
            data = ticker_data[ticker]
            
            data['mentions'] += 1
            data['upvotes'] += signal['upvotes']
            data['comments'] += signal['comments']
            data['sentiment_scores'].append(signal['sentiment_score'])
            data['conviction_scores'].append(signal['conviction_score'])
            data['subreddits'].add(signal['subreddit'])
            data['posts'].append({
                'title': signal['post_title'],
                'url': signal['post_url'],
                'upvotes': signal['upvotes']
            })
        
        # Create aggregated signals
        aggregated = []
        
        for ticker, data in ticker_data.items():
            # Calculate averages
            avg_sentiment = sum(data['sentiment_scores']) / len(data['sentiment_scores'])
            max_conviction = max(data['conviction_scores'])
            
            # Determine overall sentiment
            if avg_sentiment > 0.1:
                sentiment = 'positive'
            elif avg_sentiment < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Get top post (highest upvotes)
            top_post = max(data['posts'], key=lambda p: p['upvotes'])
            
            aggregated.append({
                'ticker': ticker,
                'mentions': data['mentions'],
                'subreddits': ', '.join(sorted(data['subreddits'])),
                'total_upvotes': data['upvotes'],
                'total_comments': data['comments'],
                'sentiment': sentiment,
                'avg_sentiment_score': round(avg_sentiment, 2),
                'max_conviction': max_conviction,
                'top_post_title': top_post['title'],
                'top_post_url': top_post['url'],
                'top_post_upvotes': top_post['upvotes']
            })
        
        # Sort by total engagement (upvotes + comments)
        aggregated.sort(
            key=lambda x: x['total_upvotes'] + x['total_comments'], 
            reverse=True
        )
        
        return aggregated
    
    def detect_unusual_volume(self, current_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Flag tickers with unusual mention volume
        
        Compares current mentions to historical baseline from cache
        
        Args:
            current_signals: Current aggregated signals
            
        Returns:
            Signals with unusual_volume flag added
        """
        # Load historical data
        baseline = self._load_cache()
        
        for signal in current_signals:
            ticker = signal['ticker']
            current_mentions = signal['mentions']
            
            # Get historical average
            if ticker in baseline:
                hist_mentions = baseline[ticker].get('avg_mentions', 0)
                
                # Flag if current > 3x historical average
                if hist_mentions > 0 and current_mentions > hist_mentions * 3:
                    signal['unusual_volume'] = True
                    signal['volume_multiplier'] = round(current_mentions / hist_mentions, 1)
                else:
                    signal['unusual_volume'] = False
            else:
                # New ticker, flag if high mentions
                signal['unusual_volume'] = current_mentions >= 5
        
        # Update cache
        self._update_cache(current_signals)
        
        return current_signals
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load historical mention data from cache"""
        if not os.path.exists(self.cache_file):
            return {}
        
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _update_cache(self, signals: List[Dict[str, Any]]):
        """Update cache with current mention data"""
        cache = self._load_cache()
        
        timestamp = datetime.now().isoformat()
        
        for signal in signals:
            ticker = signal['ticker']
            
            if ticker not in cache:
                cache[ticker] = {
                    'history': [],
                    'avg_mentions': 0
                }
            
            # Add to history (keep last 30 days)
            cache[ticker]['history'].append({
                'timestamp': timestamp,
                'mentions': signal['mentions']
            })
            
            # Keep only last 30 entries
            cache[ticker]['history'] = cache[ticker]['history'][-30:]
            
            # Recalculate average
            mention_counts = [h['mentions'] for h in cache[ticker]['history']]
            cache[ticker]['avg_mentions'] = sum(mention_counts) / len(mention_counts)
        
        # Save cache
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"⚠️  Cache save error: {e}")
    
    def assign_status(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assign GREEN/YELLOW/RED status based on conviction + sentiment
        
        GREEN: High conviction (8+) + positive sentiment + high engagement
        YELLOW: Medium conviction (5-7) or mixed signals
        RED: Negative sentiment or low conviction (<5)
        
        Args:
            signals: Aggregated signals
            
        Returns:
            Signals with status field added
        """
        for signal in signals:
            conviction = signal['max_conviction']
            sentiment = signal['sentiment']
            upvotes = signal['total_upvotes']
            
            # GREEN criteria
            if (conviction >= 8 and 
                sentiment == 'positive' and 
                upvotes >= 500):
                status = 'GREEN'
            
            # RED criteria
            elif (sentiment == 'negative' or 
                  conviction < 5):
                status = 'RED'
            
            # Default YELLOW
            else:
                status = 'YELLOW'
            
            signal['status'] = status
        
        return signals
    
    def export_to_csv(self, signals: List[Dict[str, Any]], 
                      output_path: str = None):
        """
        Export signals to CSV (matches signals-database.csv format)
        
        Args:
            signals: Aggregated and scored signals
            output_path: Output CSV path (defaults to signals-database.csv)
        """
        if output_path is None:
            output_path = self.output_file
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        # Append to existing CSV
        with open(output_path, 'a', newline='') as f:
            writer = csv.writer(f)
            
            for signal in signals:
                # Format notes field
                notes = (
                    f"Reddit mentions: {signal['mentions']} "
                    f"(r/{signal['subreddits']}) | "
                    f"Sentiment: {signal['sentiment']} ({signal['avg_sentiment_score']}) | "
                    f"Engagement: {signal['total_upvotes']}↑ {signal['total_comments']}💬 | "
                    f"Top post: {signal['top_post_title'][:50]}..."
                )
                
                if signal.get('unusual_volume'):
                    notes = f"🚨 UNUSUAL VOLUME {signal.get('volume_multiplier', '?')}x | " + notes
                
                writer.writerow([
                    signal['ticker'],
                    'Reddit',  # Source
                    timestamp,  # Date found
                    '',  # Price entry (filled later)
                    signal['max_conviction'],  # Conviction score
                    signal['status'],  # Status
                    'NO',  # Deployed
                    '',  # Position size
                    '',  # Stop loss
                    '',  # Target 1
                    '',  # Target 2
                    '',  # Current price
                    '',  # PnL dollars
                    '',  # PnL percent
                    notes
                ])
        
        print(f"✅ Exported {len(signals)} signals to {output_path}")
    
    def generate_report(self, signals: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable report
        
        Args:
            signals: Aggregated signals
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 70)
        report.append("🔥 REDDIT SOCIAL SENTIMENT REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
        report.append("=" * 70)
        report.append("")
        
        # Summary stats
        total = len(signals)
        green = len([s for s in signals if s['status'] == 'GREEN'])
        yellow = len([s for s in signals if s['status'] == 'YELLOW'])
        red = len([s for s in signals if s['status'] == 'RED'])
        unusual = len([s for s in signals if s.get('unusual_volume')])
        
        report.append(f"📊 SUMMARY:")
        report.append(f"   Total tickers: {total}")
        report.append(f"   🟢 GREEN (High conviction): {green}")
        report.append(f"   🟡 YELLOW (Watch): {yellow}")
        report.append(f"   🔴 RED (Avoid): {red}")
        report.append(f"   🚨 Unusual volume: {unusual}")
        report.append("")
        
        # Top signals by status
        for status, emoji in [('GREEN', '🟢'), ('YELLOW', '🟡'), ('RED', '🔴')]:
            status_signals = [s for s in signals if s['status'] == status]
            
            if not status_signals:
                continue
            
            report.append(f"{emoji} {status} SIGNALS ({len(status_signals)}):")
            report.append("-" * 70)
            
            for i, sig in enumerate(status_signals[:10], 1):  # Top 10
                unusual = " 🚨" if sig.get('unusual_volume') else ""
                report.append(f"{i}. ${sig['ticker']}{unusual}")
                report.append(f"   Mentions: {sig['mentions']} | "
                            f"Conviction: {sig['max_conviction']}/10 | "
                            f"Sentiment: {sig['sentiment']} ({sig['avg_sentiment_score']})")
                report.append(f"   Engagement: {sig['total_upvotes']:,}↑ {sig['total_comments']:,}💬")
                report.append(f"   Subreddits: r/{sig['subreddits']}")
                report.append(f"   Top post: {sig['top_post_title'][:60]}...")
                report.append(f"   URL: {sig['top_post_url']}")
                report.append("")
            
            if len(status_signals) > 10:
                report.append(f"   ... and {len(status_signals) - 10} more\n")
        
        report.append("=" * 70)
        report.append("💡 Next steps:")
        report.append("   1. Review GREEN signals for entry opportunities")
        report.append("   2. Research tickers with unusual volume")
        report.append("   3. Cross-reference with other sources (Yieldschool, DumbMoney)")
        report.append("   4. Check fundamentals before deployment")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def run(self, time_filter: str = 'day', 
            limit_per_sub: int = 100) -> Dict[str, Any]:
        """
        Main execution: Scrape Reddit, analyze, and export
        
        Args:
            time_filter: Time range for posts ('day', 'week')
            limit_per_sub: Max posts per subreddit
            
        Returns:
            Dictionary with signals and stats
        """
        print("🐓 Reddit Social Sentiment Scraper")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
        print("=" * 70)
        
        # 1. Scrape all subreddits
        raw_signals = self.scrape_all_subreddits(time_filter, limit_per_sub)
        
        if not raw_signals:
            print("⚠️  No signals found")
            return {'signals': [], 'stats': {}}
        
        # 2. Aggregate by ticker
        print("\n📊 Aggregating ticker mentions...")
        aggregated = self.aggregate_ticker_signals(raw_signals)
        print(f"   Unique tickers: {len(aggregated)}")
        
        # 3. Detect unusual volume
        print("\n🚨 Detecting unusual volume...")
        signals_with_volume = self.detect_unusual_volume(aggregated)
        unusual_count = len([s for s in signals_with_volume if s.get('unusual_volume')])
        print(f"   Unusual volume tickers: {unusual_count}")
        
        # 4. Assign status
        print("\n🎯 Assigning conviction status...")
        final_signals = self.assign_status(signals_with_volume)
        
        # 5. Export to CSV
        print("\n💾 Exporting to signals database...")
        self.export_to_csv(final_signals)
        
        # 6. Generate report
        report = self.generate_report(final_signals)
        print("\n" + report)
        
        # Save report to file
        report_path = '../reddit-sentiment-report.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\n📄 Report saved to {report_path}")
        
        return {
            'signals': final_signals,
            'stats': {
                'total': len(final_signals),
                'green': len([s for s in final_signals if s['status'] == 'GREEN']),
                'yellow': len([s for s in final_signals if s['status'] == 'YELLOW']),
                'red': len([s for s in final_signals if s['status'] == 'RED']),
                'unusual_volume': unusual_count
            }
        }


# CLI usage
if __name__ == "__main__":
    import sys
    
    # Check dependencies
    if not PRAW_AVAILABLE:
        print("❌ PRAW not installed. Install with: pip install praw")
        sys.exit(1)
    
    if not TEXTBLOB_AVAILABLE:
        print("⚠️  TextBlob not installed. Sentiment analysis disabled.")
        print("   Install with: pip install textblob")
    
    # Initialize and run
    scraper = RedditScraper()
    
    if not scraper.reddit:
        print("\n❌ Reddit API not configured")
        print("\n📝 Setup instructions:")
        print("   1. Create Reddit app: https://www.reddit.com/prefs/apps")
        print("   2. Create config/reddit_config.json with:")
        print('      {')
        print('        "client_id": "your_client_id",')
        print('        "client_secret": "your_client_secret",')
        print('        "user_agent": "OpenClaw Trading Bot v1.0"')
        print('      }')
        sys.exit(1)
    
    # Run scraper
    results = scraper.run(time_filter='day', limit_per_sub=100)
    
    print(f"\n✅ Complete! Found {results['stats']['total']} signals")
    print(f"   🟢 GREEN: {results['stats']['green']}")
    print(f"   🟡 YELLOW: {results['stats']['yellow']}")
    print(f"   🔴 RED: {results['stats']['red']}")
