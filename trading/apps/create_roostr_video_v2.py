#!/usr/bin/env python3
"""
Create roostr Capital Video v2 - WITH AVATAR
"""

import requests
import json
import time
from pathlib import Path

API_KEY = (Path.home() / ".config/heygen/api_key").read_text().strip()
BASE_URL = "https://api.heygen.com/v2"

def create_video_with_avatar(script, title, avatar_id="Adrian_public_2_20240312"):
    """Create video with avatar + voice"""
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": script,
                "voice_id": "f38a635bee7a4d1f9b0a654a31d050d2"  # Chill Brian
            },
            "background": {
                "type": "color",
                "value": "#1a1a1a"  # Dark gray background
            }
        }],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": title
    }
    
    print(f"Creating video with avatar: {avatar_id}")
    
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
    
    print("🎬 Creating roostr Capital video WITH AVATAR...")
    print(f"📝 Script: {len(script)} chars, ~{len(script.split())} words")
    print()
    
    # Create video
    print("🚀 Submitting to HeyGen...")
    video_id = create_video_with_avatar(
        script, 
        "roostr Capital - TradingView Integration (WITH AVATAR)",
        avatar_id="Adrian_public_2_20240312"  # Professional in blue suit
    )
    
    print(f"✅ Video created: {video_id}")
    print(f"⏳ Processing (2-5 minutes)...")
    print()
    
    # Wait for completion
    for i in range(30):  # 5 minutes max
        time.sleep(10)
        status = check_status(video_id)
        
        if i % 6 == 0:  # Print every minute
            print(f"Status: {status['status']} ({i//6}min)")
        
        if status['status'] == 'completed':
            print(f"\n✅ VIDEO READY!")
            print(f"🎥 URL: {status['video_url']}")
            print(f"📸 Thumbnail: {status['thumbnail_url']}")
            
            # Download
            print("\n📥 Downloading...")
            import subprocess
            video_dir = Path(__file__).parent.parent / "videos"
            video_dir.mkdir(exist_ok=True)
            
            output_file = video_dir / "tradingview_integration_v2.mp4"
            subprocess.run([
                "curl", "-L", status['video_url'],
                "-o", str(output_file)
            ], check=True)
            
            print(f"✅ Saved: {output_file}")
            return str(output_file)
        
        elif status['status'] == 'failed':
            print(f"\n❌ Failed: {status.get('error')}")
            return None
    
    print(f"\n⏱️ Timeout - still processing: {video_id}")
    return None

if __name__ == "__main__":
    main()
