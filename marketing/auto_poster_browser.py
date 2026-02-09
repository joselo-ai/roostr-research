#!/usr/bin/env python3
"""
roostr Auto-Poster (Browser Automation)
Posts to X/Instagram via browser automation - no API needed.
Runs on cron schedule: 9 AM, 12 PM, 4 PM, 7 PM EST daily.
"""

import json
import os
from datetime import datetime
import subprocess
import sys

WORKSPACE = "/Users/agentjoselo/.openclaw/workspace"
CONTENT_QUEUE = f"{WORKSPACE}/marketing/content-queue.json"
POSTED_LOG = f"{WORKSPACE}/marketing/posted-log.json"

def load_content_queue():
    """Load content from queue file."""
    if not os.path.exists(CONTENT_QUEUE):
        return {"posts": []}
    
    with open(CONTENT_QUEUE, 'r') as f:
        return json.load(f)

def save_content_queue(data):
    """Save updated queue."""
    with open(CONTENT_QUEUE, 'w') as f:
        json.dump(data, f, indent=2)

def log_posted_content(post):
    """Archive posted content."""
    if not os.path.exists(POSTED_LOG):
        log_data = {"posted": []}
    else:
        with open(POSTED_LOG, 'r') as f:
            log_data = json.load(f)
    
    post["posted_at"] = datetime.now().isoformat()
    log_data["posted"].append(post)
    
    with open(POSTED_LOG, 'w') as f:
        json.dump(log_data, f, indent=2)

def post_to_twitter(text):
    """Post to X via OpenClaw browser automation."""
    # Use OpenClaw's message tool to post
    cmd = [
        "openclaw", "msg", 
        "--channel", "twitter",
        "--message", text
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ Posted to X: {text[:50]}...")
            return True
        else:
            print(f"❌ Failed to post to X: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error posting to X: {e}")
        return False

def post_to_instagram(text, image=None):
    """Post to Instagram via browser automation."""
    # Instagram requires image - skip if text-only
    if not image:
        print("⚠️ Instagram requires image, skipping text-only post")
        return False
    
    cmd = [
        "openclaw", "msg",
        "--channel", "instagram",
        "--message", text,
        "--media", image
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ Posted to Instagram: {text[:50]}...")
            return True
        else:
            print(f"❌ Failed to post to Instagram: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error posting to Instagram: {e}")
        return False

def run_posting(slot):
    """Run posting for a specific time slot."""
    print(f"\n🐓 roostr Auto-Poster - {slot} slot ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
    
    # Load queue
    data = load_content_queue()
    posts = data.get("posts", [])
    
    if not posts:
        print("⚠️ Content queue empty - no posts to send")
        print("💡 Refill queue by adding to marketing/content-queue.json")
        return
    
    # Get next post for this slot
    slot_posts = [p for p in posts if p.get("slot") == slot and not p.get("posted")]
    
    if not slot_posts:
        print(f"⚠️ No posts scheduled for {slot} slot")
        return
    
    post = slot_posts[0]
    
    # Post to platforms
    success = False
    
    if "twitter" in post.get("platforms", []):
        success = post_to_twitter(post["content"])
    
    if "instagram" in post.get("platforms", []):
        post_to_instagram(post["content"], post.get("image"))
    
    # Mark as posted and archive
    if success:
        post["posted"] = True
        log_posted_content(post)
        
        # Remove from queue
        data["posts"] = [p for p in posts if p != post]
        save_content_queue(data)
        
        print(f"\n✅ Successfully posted and logged")
    else:
        print(f"\n❌ Posting failed, keeping in queue for retry")
    
    # Check if queue is low
    remaining = len([p for p in data["posts"] if not p.get("posted")])
    if remaining < 5:
        print(f"\n⚠️ Queue low ({remaining} posts remaining)")
        print("💡 Generate more content soon")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: auto_poster_browser.py [morning|midday|afternoon|evening]")
        sys.exit(1)
    
    slot = sys.argv[1]
    valid_slots = ["morning", "midday", "afternoon", "evening"]
    
    if slot not in valid_slots:
        print(f"Invalid slot: {slot}. Must be one of: {', '.join(valid_slots)}")
        sys.exit(1)
    
    run_posting(slot)
