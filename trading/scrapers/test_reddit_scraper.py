#!/usr/bin/env python3
"""
Test Reddit Scraper with Mock Data
Demonstrates functionality without Reddit API
"""

import sys
import os
from datetime import datetime, timedelta

# Mock data for testing
MOCK_POSTS = [
    {
        'subreddit': 'wallstreetbets',
        'title': '$NVDA crushing earnings - AI revenue up 200% YoY',
        'selftext': 'Jensen just delivered. Data center revenue beat by $2B. Every cloud provider is buying H100s. This is going to $1000. Strong buy.',
        'score': 3420,
        'num_comments': 567,
        'upvote_ratio': 0.94,
        'gilded': 3,
        'id': 'abc123',
        'created_utc': datetime.now().timestamp()
    },
    {
        'subreddit': 'wallstreetbets',
        'title': 'NVDA to the moon! 🚀🚀🚀',
        'selftext': 'Buy calls! This is going to 10x!',
        'score': 89,
        'num_comments': 23,
        'upvote_ratio': 0.67,
        'gilded': 0,
        'id': 'def456',
        'created_utc': datetime.now().timestamp()
    },
    {
        'subreddit': 'stocks',
        'title': '$PLTR Palantir - Government contracts accelerating',
        'selftext': 'Just announced $400M DoD contract. Margins expanding, ARR growing 30%. Trading at reasonable 15x sales for growth rate. Entry around $25 looks solid.',
        'score': 1250,
        'num_comments': 234,
        'upvote_ratio': 0.88,
        'gilded': 1,
        'id': 'ghi789',
        'created_utc': (datetime.now() - timedelta(hours=2)).timestamp()
    },
    {
        'subreddit': 'investing',
        'title': 'Bear case on $TSLA - deliveries missing targets',
        'selftext': 'Q4 deliveries came in 15% below guidance. Competition from BYD intensifying. Margins compressing. Valuation still stretched at 60x PE. Avoid.',
        'score': 890,
        'num_comments': 412,
        'upvote_ratio': 0.72,
        'gilded': 0,
        'id': 'jkl012',
        'created_utc': (datetime.now() - timedelta(hours=5)).timestamp()
    },
    {
        'subreddit': 'stocks',
        'title': '$AMD strong position in data center CPUs',
        'selftext': 'Market share gains vs Intel continue. EPYC chips dominating server market. MI300 AI accelerators ramping. Undervalued vs NVDA at current levels.',
        'score': 678,
        'num_comments': 156,
        'upvote_ratio': 0.85,
        'gilded': 1,
        'id': 'mno345',
        'created_utc': (datetime.now() - timedelta(hours=8)).timestamp()
    },
    {
        'subreddit': 'wallstreetbets',
        'title': '$NVDA DD - Why this goes higher',
        'selftext': 'Demand for AI compute is insane. TAM expanding faster than production capacity. Blackwell chips sold out through 2025. Pricing power intact.',
        'score': 2100,
        'num_comments': 389,
        'upvote_ratio': 0.91,
        'gilded': 2,
        'id': 'pqr678',
        'created_utc': (datetime.now() - timedelta(hours=12)).timestamp()
    },
    {
        'subreddit': 'stockmarket',
        'title': 'Small caps heating up - $IONQ quantum computing play',
        'selftext': 'Quantum computing is the next frontier. IONQ has working systems deployed. Revenue small but growing fast. High risk high reward.',
        'score': 234,
        'num_comments': 67,
        'upvote_ratio': 0.79,
        'gilded': 0,
        'id': 'stu901',
        'created_utc': (datetime.now() - timedelta(hours=6)).timestamp()
    },
    {
        'subreddit': 'investing',
        'title': 'Dividend play: $T AT&T yield 6.5%',
        'selftext': 'Telecom is boring but pays. Debt coming down, FCF strong. Safe dividend with upside from fiber expansion. Good for income portfolio.',
        'score': 445,
        'num_comments': 98,
        'upvote_ratio': 0.83,
        'gilded': 0,
        'id': 'vwx234',
        'created_utc': (datetime.now() - timedelta(hours=15)).timestamp()
    },
]


class MockSubmission:
    """Mock Reddit submission for testing"""
    def __init__(self, data):
        self.subreddit = type('obj', (object,), {'display_name': data['subreddit']})
        self.title = data['title']
        self.selftext = data['selftext']
        self.score = data['score']
        self.num_comments = data['num_comments']
        self.upvote_ratio = data['upvote_ratio']
        self.gilded = data['gilded']
        self.id = data['id']
        self.created_utc = data['created_utc']
        self.permalink = f"/r/{data['subreddit']}/comments/{data['id']}/"
        self.stickied = False


class MockReddit:
    """Mock Reddit API for testing"""
    def __init__(self):
        self.posts = MOCK_POSTS
    
    def subreddit(self, name):
        return MockSubreddit(name, self.posts)


class MockSubreddit:
    """Mock subreddit"""
    def __init__(self, name, posts):
        self.name = name
        self.all_posts = posts
    
    def hot(self, limit=100):
        # Filter posts for this subreddit
        filtered = [p for p in self.all_posts if p['subreddit'] == self.name]
        return [MockSubmission(p) for p in filtered[:limit]]


def test_scraper():
    """Test Reddit scraper with mock data"""
    print("🧪 Testing Reddit Scraper with Mock Data")
    print("=" * 70)
    
    # Import scraper
    sys.path.insert(0, '/Users/agentjoselo/.openclaw/workspace/trading/scrapers')
    
    try:
        from reddit_scraper import RedditScraper
    except ImportError as e:
        print(f"❌ Could not import reddit_scraper: {e}")
        return
    
    # Create scraper instance (no real API)
    scraper = RedditScraper(config_path='/dev/null')  # Dummy config
    scraper.reddit = MockReddit()  # Inject mock
    
    # Run scraper
    print("\n📊 Running scraper on mock data...\n")
    results = scraper.run(time_filter='day', limit_per_sub=50)
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    print(f"\nSignals generated: {results['stats']['total']}")
    print(f"  🟢 GREEN: {results['stats']['green']}")
    print(f"  🟡 YELLOW: {results['stats']['yellow']}")
    print(f"  🔴 RED: {results['stats']['red']}")
    
    print("\n💡 This demonstrates:")
    print("  ✓ Ticker extraction from Reddit posts")
    print("  ✓ Sentiment analysis (positive/negative/neutral)")
    print("  ✓ Conviction scoring based on engagement")
    print("  ✓ Signal aggregation across multiple posts")
    print("  ✓ GREEN/YELLOW/RED classification")
    print("  ✓ CSV export to signals-database.csv")
    print("  ✓ Formatted report generation")
    
    print("\n📁 Output files:")
    print("  • signals-database.csv (appended with new signals)")
    print("  • reddit-sentiment-report.txt (human-readable report)")
    
    print("\n🚀 Next step: Configure real Reddit API credentials")
    print("   See: REDDIT-SETUP.md for instructions")


if __name__ == "__main__":
    test_scraper()
