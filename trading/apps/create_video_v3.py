#!/usr/bin/env python3
"""
Create roostr Video v3 - Better Script (Anti-Scam Angle)
"""

import requests
import json
import time
from pathlib import Path

API_KEY = (Path.home() / ".config/heygen/api_key").read_text().strip()
BASE_URL = "https://api.heygen.com/v2"

def create_video(script, title, avatar_id="Adrian_public_2_20240312"):
    """Create video"""
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
                "value": "#0a0a0a"  # Very dark background
            }
        }],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": title
    }
    
    response = requests.post(f"{BASE_URL}/video/generate", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['data']['video_id']

def check_status(video_id):
    headers = {"X-Api-Key": API_KEY}
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def main():
    # Version 3: Anti-scam, trust-building
    script = """Ever see those AI trading bot ads?

Turn one hundred dollars into ten thousand overnight!

Yeah. Those are scams.

Here's what real AI-powered trading looks like.

Real-time data infrastructure. Not promises.
Risk management that actually protects you. Not dreams.
Conviction scoring based on multiple sources. Not hope.

We integrated TradingView this morning. Full automation. Live RSI. Instant alerts.

Took 20 minutes.

Meanwhile, other people are paying thousands for trading bots that use ChatGPT to analyze tweets.

We're building the boring stuff that matters. Stop-loss protection. Signal validation. Multi-source confirmation.

And we're doing it in public. You can watch. All of it.

Currently down on TAO. Up slightly on SOL. Overall negative seven percent for the week.

No hiding. No cherry-picked wins. Just real positions. Real P&L.

This is roostr Capital.

If you want moon promises, go somewhere else.

If you want to see how a real hedge fund gets built, stick around."""
    
    print("🎬 Creating roostr v3 - BETTER SCRIPT")
    print(f"📝 {len(script.split())} words")
    print()
    
    video_id = create_video(script, "roostr Capital - Real Trading vs Scams")
    print(f"✅ Video ID: {video_id}")
    print("⏳ Processing (2-5 min)...")
    
    # Wait for completion
    for i in range(30):
        time.sleep(10)
        status = check_status(video_id)
        
        if i % 6 == 0:
            print(f"Status: {status['status']} ({i//6}min)")
        
        if status['status'] == 'completed':
            print(f"\n✅ READY!")
            print(f"🎥 {status['video_url']}")
            
            # Download
            import subprocess
            video_dir = Path(__file__).parent.parent / "videos"
            output = video_dir / "roostr_v3_anti_scam.mp4"
            
            subprocess.run(["curl", "-L", status['video_url'], "-o", str(output)], check=True, capture_output=True)
            print(f"📥 Saved: {output}")
            return str(output)
        
        elif status['status'] == 'failed':
            print(f"\n❌ Failed: {status.get('error')}")
            return None
    
    print(f"\n⏱️ Timeout: {video_id}")
    return None

if __name__ == "__main__":
    main()
