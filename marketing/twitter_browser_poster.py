#!/usr/bin/env python3
"""
Twitter Browser Auto-Poster for roostr Capital
Posts tweets via browser automation (no API tier required)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Paths
QUEUE_FILE = Path(__file__).parent / "content-queue.json"
LOG_FILE = Path(__file__).parent / "posted-log.json"

def load_queue():
    """Load content queue"""
    with open(QUEUE_FILE) as f:
        data = json.load(f)
        return data.get("posts", data)

def save_queue(posts):
    """Save content queue"""
    with open(QUEUE_FILE, 'w') as f:
        json.dump({"posts": posts}, f, indent=2)

def load_log():
    """Load posted tweets log"""
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return []

def save_log(log):
    """Save posted tweets log"""
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def get_current_slot():
    """Determine current posting slot"""
    now = datetime.now()
    hour = now.hour
    
    if 9 <= hour < 12:
        return "morning"
    elif 12 <= hour < 16:
        return "midday"
    elif 16 <= hour < 19:
        return "afternoon"
    elif 19 <= hour < 23:
        return "evening"
    else:
        return None

def find_next_tweet(posts, slot):
    """Find next unposted tweet for current slot"""
    for post in posts:
        if post.get("slot") == slot and not post.get("posted"):
            return post
    return None

def extract_tweet_id_from_url(url):
    """Extract tweet ID from X URL"""
    if not url or "/status/" not in url:
        return None
    return url.split("/status/")[1].split("?")[0]

def main():
    """Main execution"""
    print("🐓 Twitter Browser Auto-Poster")
    print("=" * 60)
    
    # Load data
    queue = load_queue()
    slot = get_current_slot()
    
    if not slot:
        print("❌ Outside posting hours (9 AM - 11 PM)")
        return 1
    
    print(f"📅 Current slot: {slot} ({datetime.now().hour}:00)")
    
    # Find next tweet
    next_tweet = find_next_tweet(queue, slot)
    
    if not next_tweet:
        print(f"ℹ️  No unposted {slot} tweets in queue")
        return 0
    
    print(f"\n📝 Tweet to post:")
    print(f"   ID: {next_tweet['id']}")
    print(f"   Date: {next_tweet.get('date', 'N/A')}")
    
    # Get tweet text
    tweet_text = next_tweet.get('content') or next_tweet.get('text', '')
    print(f"\n💬 Text ({len(tweet_text)} chars):")
    print("-" * 60)
    print(tweet_text)
    print("-" * 60)
    
    # Reply-to handling
    reply_to_url = next_tweet.get('reply_to')
    reply_to_id = extract_tweet_id_from_url(reply_to_url) if reply_to_url else None
    
    if reply_to_id:
        print(f"\n🔗 Reply to: {reply_to_url}")
        print(f"   Tweet ID: {reply_to_id}")
    else:
        print(f"\n📌 Standalone tweet (no reply)")
    
    # Output JSON for OpenClaw browser tool
    browser_command = {
        "action": "navigate_and_post",
        "tweet_text": tweet_text,
        "reply_to_id": reply_to_id,
        "post_id": next_tweet['id']
    }
    
    print(f"\n🌐 Browser automation payload:")
    print(json.dumps(browser_command, indent=2))
    
    # Mark as ready for posting
    print(f"\n⚠️  Manual step required:")
    print(f"   This script prepared the tweet data.")
    print(f"   Use OpenClaw browser tool or post manually to X.")
    print(f"\n   After posting, run:")
    print(f"   python3 mark_posted.py {next_tweet['id']} <tweet_url>")
    
    return 0

if __name__ == "__main__":
    exit(main())
