#!/usr/bin/env python3
"""
roostr Marketing Automation - Social Media Poster
Reads from content queue and posts to X/Instagram at scheduled times.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
WORKSPACE = Path.home() / ".openclaw" / "workspace" / "marketing-agent"
QUEUE_FILE = WORKSPACE / "automation" / "content_queue.json"
LOG_FILE = WORKSPACE / "automation" / "posting_log.json"
CONFIG_FILE = WORKSPACE / "automation" / "config.json"

def load_config():
    """Load API credentials and configuration"""
    if not CONFIG_FILE.exists():
        return {
            "x_api_key": os.getenv("X_API_KEY", ""),
            "x_api_secret": os.getenv("X_API_SECRET", ""),
            "x_access_token": os.getenv("X_ACCESS_TOKEN", ""),
            "x_access_secret": os.getenv("X_ACCESS_SECRET", ""),
            "instagram_username": os.getenv("INSTAGRAM_USERNAME", "roostrcapital"),
            "instagram_password": os.getenv("INSTAGRAM_PASSWORD", ""),
            "dry_run": True  # Safety: start in dry-run mode
        }
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def load_queue():
    """Load content queue"""
    if not QUEUE_FILE.exists():
        return {"posts": []}
    
    with open(QUEUE_FILE, 'r') as f:
        return json.load(f)

def save_queue(queue):
    """Save content queue"""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

def log_post(platform, content, status, error=None):
    """Log posted content"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing log
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            log = json.load(f)
    else:
        log = {"posts": []}
    
    # Add new entry
    log["posts"].append({
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "content": content[:100] + "..." if len(content) > 100 else content,
        "status": status,
        "error": error
    })
    
    # Keep last 1000 entries
    log["posts"] = log["posts"][-1000:]
    
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def post_to_x(content, config):
    """Post to X (Twitter)"""
    if config.get("dry_run", True):
        print(f"[DRY RUN] Would post to X: {content}")
        return True
    
    try:
        # TODO: Implement actual X API posting
        # Using tweepy or requests to Twitter API v2
        # For now, return placeholder
        import tweepy
        
        client = tweepy.Client(
            consumer_key=config["x_api_key"],
            consumer_secret=config["x_api_secret"],
            access_token=config["x_access_token"],
            access_token_secret=config["x_access_secret"]
        )
        
        response = client.create_tweet(text=content)
        print(f"✅ Posted to X: {response.data['id']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to post to X: {e}")
        log_post("x", content, "failed", str(e))
        return False

def post_to_instagram(content, image_path=None, config=None):
    """Post to Instagram"""
    if config.get("dry_run", True):
        print(f"[DRY RUN] Would post to Instagram: {content}")
        return True
    
    try:
        # TODO: Implement Instagram posting via instagrapi or similar
        # For now, return placeholder
        print(f"⚠️  Instagram posting not yet implemented")
        print(f"Content: {content}")
        if image_path:
            print(f"Image: {image_path}")
        return False
        
    except Exception as e:
        print(f"❌ Failed to post to Instagram: {e}")
        log_post("instagram", content, "failed", str(e))
        return False

def get_next_scheduled_post(queue):
    """Get the next post scheduled for now"""
    now = datetime.now()
    current_hour = now.hour
    
    for post in queue["posts"]:
        if post.get("posted", False):
            continue
            
        scheduled_time = post.get("scheduled_time", "")
        if not scheduled_time:
            continue
            
        # Parse scheduled time (format: "HH:MM")
        try:
            scheduled_hour = int(scheduled_time.split(":")[0])
            
            # If we're within 15 minutes of scheduled time, post it
            if abs(current_hour - scheduled_hour) <= 0 or \
               (current_hour == scheduled_hour and now.minute <= 15):
                return post
        except:
            continue
    
    return None

def mark_as_posted(queue, post):
    """Mark a post as posted"""
    for p in queue["posts"]:
        if p["id"] == post["id"]:
            p["posted"] = True
            p["posted_at"] = datetime.now().isoformat()
    save_queue(queue)

def main():
    config = load_config()
    queue = load_queue()
    
    print(f"🐓 roostr Marketing Automation")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'DRY RUN' if config.get('dry_run', True) else 'LIVE'}")
    print(f"Queue size: {len([p for p in queue.get('posts', []) if not p.get('posted', False)])} pending posts")
    print()
    
    # Get next scheduled post
    post = get_next_scheduled_post(queue)
    
    if not post:
        print("📭 No posts scheduled for this time")
        return
    
    print(f"📝 Found scheduled post: {post.get('title', 'Untitled')}")
    print(f"Platforms: {', '.join(post.get('platforms', []))}")
    print()
    
    # Post to each platform
    success = True
    for platform in post.get("platforms", []):
        content = post.get("content", "")
        
        if platform == "x":
            if post_to_x(content, config):
                log_post("x", content, "success")
            else:
                success = False
                
        elif platform == "instagram":
            image_path = post.get("image_path")
            if post_to_instagram(content, image_path, config):
                log_post("instagram", content, "success")
            else:
                success = False
    
    # Mark as posted if successful
    if success:
        mark_as_posted(queue, post)
        print("✅ Post completed and marked as posted")
    else:
        print("⚠️  Some platforms failed, not marking as posted")

if __name__ == "__main__":
    main()
