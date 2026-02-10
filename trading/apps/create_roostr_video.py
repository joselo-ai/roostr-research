#!/usr/bin/env python3
"""
Create roostr Capital Video - TradingView Integration Story
"""

import requests
import json
import time
from pathlib import Path

API_KEY = (Path.home() / ".config/heygen/api_key").read_text().strip()
BASE_URL = "https://api.heygen.com/v2"

def create_video(script, title):
    """Create video with HeyGen"""
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "video_inputs": [{
            "voice": {
                "type": "text",
                "input_text": script,
                "voice_id": "f38a635bee7a4d1f9b0a654a31d050d2"  # Chill Brian
            }
        }],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": title
    }
    
    response = requests.post(
        f"{BASE_URL}/video/generate",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()['data']['video_id']

def check_status(video_id):
    """Check video status"""
    headers = {"X-Api-Key": API_KEY}
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def main():
    # TradingView integration script
    script = """Hey everyone, I want to show you what we just built in the last hour.

We integrated TradingView into our trading infrastructure.

Before, we were scraping prices from CoinGecko, dealing with rate limits, getting delayed data. Not ideal.

Now, we're pulling real-time prices, RSI indicators, and trading signals directly from TradingView. No rate limits. No delays.

We also built a webhook system. When TradingView fires an alert, like if TAO crosses above 160 dollars, it hits our server and sends a Telegram notification instantly.

This took 20 minutes to build. And it's already running.

Our risk monitor now has RSI context. Our price updates show technical signals. And we can set up custom alerts for any condition we want.

This is the kind of infrastructure that hedge funds spend months building. We did it in 20 minutes because we automated the right things.

Next up, we're adding more alerts, backtesting capabilities, and multi-asset tracking.

Building in public. Full transparency. No BS.

That's it for today."""
    
    print("🎬 Creating roostr Capital video...")
    print(f"📝 Script: {len(script)} chars, ~{len(script.split())} words")
    print()
    
    # Create video
    print("🚀 Submitting to HeyGen...")
    video_id = create_video(script, "roostr Capital - TradingView Integration")
    
    print(f"✅ Video created: {video_id}")
    print(f"⏳ Processing (usually 2-5 minutes)...")
    print()
    
    # Save video ID
    video_log = Path(__file__).parent.parent / "videos.log"
    with open(video_log, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {video_id} | TradingView Integration\n")
    
    # Check status a few times
    for i in range(3):
        time.sleep(10)
        status = check_status(video_id)
        
        print(f"Status check {i+1}: {status['status']}")
        
        if status['status'] == 'completed':
            print(f"\n✅ VIDEO READY!")
            print(f"🎥 URL: {status['video_url']}")
            print(f"📸 Thumbnail: {status['thumbnail_url']}")
            
            # Save URL
            with open(video_log, "a") as f:
                f.write(f"  → {status['video_url']}\n")
            
            return status['video_url']
        elif status['status'] == 'failed':
            print(f"\n❌ Video generation failed: {status.get('error')}")
            return None
    
    print(f"\n⏳ Still processing... Check later:")
    print(f"   video_id: {video_id}")
    print(f"   Check: python3 -c \"from heygen_client_v2 import check_status; print(check_status('{video_id}'))\"")
    
    return video_id

if __name__ == "__main__":
    main()
