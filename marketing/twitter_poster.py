#!/usr/bin/env python3
"""
Twitter Auto-Poster for roostr Capital
Posts tweets from content queue using Twitter API v1.1 (OAuth 1.0a)
"""

import tweepy
import json
from pathlib import Path
from datetime import datetime

# Paths
CREDS_FILE = Path(__file__).parent / ".twitter-credentials.json"
QUEUE_FILE = Path(__file__).parent / "content-queue.json"
LOG_FILE = Path(__file__).parent / "posted-log.json"

def load_credentials():
    """Load Twitter API credentials"""
    with open(CREDS_FILE) as f:
        return json.load(f)

def get_twitter_client():
    """Create authenticated Twitter API client"""
    creds = load_credentials()
    
    auth = tweepy.OAuth1UserHandler(
        creds["consumer_key"],
        creds["consumer_secret"],
        creds["access_token"],
        creds["access_token_secret"]
    )
    
    return tweepy.API(auth)

def load_queue():
    """Load content queue"""
    with open(QUEUE_FILE) as f:
        data = json.load(f)
        return data.get("posts", data)  # Handle both structures

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

def post_tweet(client, text, reply_to=None):
    """
    Post a tweet, optionally as a reply
    
    Args:
        client: Tweepy API client
        text: Tweet text
        reply_to: Tweet ID to reply to (optional)
    
    Returns:
        Tweet object with id, url
    """
    if reply_to:
        tweet = client.update_status(
            status=text,
            in_reply_to_status_id=reply_to,
            auto_populate_reply_metadata=True
        )
    else:
        tweet = client.update_status(status=text)
    
    return {
        "id": str(tweet.id),
        "url": f"https://x.com/roostrcapital/status/{tweet.id}",
        "text": text,
        "timestamp": datetime.now().isoformat()
    }

def main():
    """Main execution"""
    print("🐓 Twitter Auto-Poster")
    print("=" * 60)
    
    # Load data
    queue = load_queue()
    log = load_log()
    client = get_twitter_client()
    
    # Find next unposted tweet for current slot
    now = datetime.now()
    current_hour = now.hour
    
    # Determine slot based on time
    if 9 <= current_hour < 12:
        slot = "morning"
    elif 12 <= current_hour < 16:
        slot = "midday"
    elif 16 <= current_hour < 19:
        slot = "afternoon"
    elif 19 <= current_hour < 23:
        slot = "evening"
    else:
        print("❌ Outside posting hours (9 AM - 11 PM)")
        return 1
    
    print(f"📅 Current slot: {slot} ({current_hour}:00)")
    
    # Find next unposted item for this slot
    next_tweet = None
    for item in queue:
        if item.get("slot") == slot and not item.get("posted"):
            next_tweet = item
            break
    
    if not next_tweet:
        print(f"ℹ️  No unposted {slot} tweets in queue")
        return 0
    
    print(f"📝 Found tweet: {next_tweet['id']}")
    print(f"   Reply to: {next_tweet.get('reply_to', 'None')}")
    tweet_text = next_tweet.get('content') or next_tweet.get('text', '')
    print(f"   Text: {tweet_text[:50]}...")
    
    # Extract reply_to ID if it's a URL
    reply_to_id = None
    if next_tweet.get("reply_to"):
        reply_url = next_tweet["reply_to"]
        if "/status/" in reply_url:
            reply_to_id = reply_url.split("/status/")[1].split("?")[0]
    
    # Post tweet
    try:
        tweet_text = next_tweet.get('content') or next_tweet.get('text', '')
        result = post_tweet(client, tweet_text, reply_to=reply_to_id)
        print(f"✅ Posted: {result['url']}")
        
        # Update queue
        next_tweet["posted"] = True
        next_tweet["posted_at"] = result["timestamp"]
        next_tweet["posted_url"] = result["url"]
        next_tweet["posted_id"] = result["id"]
        save_queue(queue)
        
        # Add to log
        log.append(result)
        save_log(log)
        
        print(f"📊 Total tweets posted: {len(log)}")
        return 0
        
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
