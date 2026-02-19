#!/usr/bin/env python3
"""
Mark a tweet as posted in the queue
Usage: python3 mark_posted.py <tweet_id> <posted_url>
"""

import json
import sys
from pathlib import Path
from datetime import datetime

QUEUE_FILE = Path(__file__).parent / "content-queue.json"
LOG_FILE = Path(__file__).parent / "posted-log.json"

def load_queue():
    with open(QUEUE_FILE) as f:
        data = json.load(f)
        return data.get("posts", data)

def save_queue(posts):
    with open(QUEUE_FILE, 'w') as f:
        json.dump({"posts": posts}, f, indent=2)

def load_log():
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 mark_posted.py <tweet_id> <posted_url>")
        print("Example: python3 mark_posted.py w3-2 https://x.com/roostrcapital/status/123456789")
        return 1
    
    tweet_id = sys.argv[1]
    posted_url = sys.argv[2]
    
    # Extract tweet ID from URL
    if "/status/" in posted_url:
        posted_id = posted_url.split("/status/")[1].split("?")[0]
    else:
        print("❌ Invalid URL format")
        return 1
    
    # Load queue
    posts = load_queue()
    
    # Find and update tweet
    found = False
    for post in posts:
        if post.get("id") == tweet_id:
            post["posted"] = True
            post["posted_at"] = datetime.now().isoformat()
            post["posted_url"] = posted_url
            post["posted_id"] = posted_id
            found = True
            
            print(f"✅ Marked {tweet_id} as posted")
            print(f"   URL: {posted_url}")
            print(f"   Time: {post['posted_at']}")
            
            # Save updated queue
            save_queue(posts)
            
            # Add to log
            log = load_log()
            log.append({
                "id": posted_id,
                "url": posted_url,
                "text": post.get('content') or post.get('text', ''),
                "timestamp": post['posted_at'],
                "tweet_id": tweet_id
            })
            save_log(log)
            
            break
    
    if not found:
        print(f"❌ Tweet {tweet_id} not found in queue")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
