#!/usr/bin/env python3
"""
D-ID API Client - Animate roostr character
API docs: https://docs.d-id.com/reference/talks-api
"""

import requests
import json
import time
from pathlib import Path
import base64

API_KEY_PATH = Path.home() / ".config/did/api_key"
BASE_URL = "https://api.d-id.com"

def load_api_key():
    """Load D-ID API key"""
    if not API_KEY_PATH.exists():
        print(f"❌ D-ID API key not found: {API_KEY_PATH}")
        print("   Get your API key from: https://studio.d-id.com/account-settings")
        print("   Then save it: mkdir -p ~/.config/did && echo 'YOUR_KEY' > ~/.config/did/api_key")
        return None
    with open(API_KEY_PATH) as f:
        return f.read().strip()

def get_headers(api_key):
    """Get authorization headers"""
    return {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }

def create_talk(image_path, script, voice="en-US-ChristopherNeural"):
    """
    Create talking video from image + script
    
    Args:
        image_path: Path to roostr image
        script: Text script
        voice: Voice ID (default: professional male)
    
    Returns:
        Talk ID for status checking
    """
    api_key = load_api_key()
    if not api_key:
        return None
    
    # Upload image and get URL (or use base64)
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()
    
    payload = {
        "source_url": f"data:image/jpeg;base64,{image_data}",
        "script": {
            "type": "text",
            "input": script,
            "provider": {
                "type": "microsoft",
                "voice_id": voice
            }
        },
        "config": {
            "stitch": True
        }
    }
    
    print(f"🚀 Creating D-ID talk...")
    
    response = requests.post(
        f"{BASE_URL}/talks",
        headers=get_headers(api_key),
        json=payload
    )
    
    if response.status_code == 201:
        result = response.json()
        talk_id = result['id']
        print(f"✅ Talk created: {talk_id}")
        return talk_id
    else:
        print(f"❌ D-ID API error: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def check_status(talk_id):
    """Check talk generation status"""
    api_key = load_api_key()
    if not api_key:
        return None
    
    response = requests.get(
        f"{BASE_URL}/talks/{talk_id}",
        headers=get_headers(api_key)
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Status check failed: {response.status_code}")
        return None

def wait_for_video(talk_id, max_wait_minutes=5):
    """Wait for video to complete"""
    print(f"⏳ Waiting for video to generate...")
    
    for i in range(max_wait_minutes * 6):  # Check every 10 seconds
        status = check_status(talk_id)
        
        if not status:
            return None
        
        state = status.get('status')
        
        if state == 'done':
            video_url = status.get('result_url')
            print(f"✅ Video ready!")
            return video_url
        elif state == 'error':
            print(f"❌ Generation failed: {status.get('error')}")
            return None
        
        if i % 6 == 0:  # Print every minute
            print(f"   Status: {state} ({i//6}min)")
        
        time.sleep(10)
    
    print(f"⏱️ Timeout after {max_wait_minutes} minutes")
    return None

def download_video(url, output_path):
    """Download generated video"""
    print(f"📥 Downloading video...")
    response = requests.get(url, stream=True)
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✅ Saved: {output_path}")

def create_roostr_video():
    """Main flow: Create roostr video"""
    
    # Paths
    roostr_img = Path(__file__).parent.parent / "roostr-avatar" / "roostr_character.jpg"
    video_dir = Path(__file__).parent.parent / "videos"
    video_dir.mkdir(exist_ok=True)
    
    # Script (anti-scam version)
    script = """Ever see those AI trading bot ads? Turn one hundred dollars into ten thousand overnight! Yeah. Those are scams.

Here's what real AI-powered trading looks like. Real-time data infrastructure. Not promises. Risk management that actually protects you. Not dreams. Conviction scoring based on multiple sources. Not hope.

We integrated TradingView this morning. Full automation. Live RSI. Instant alerts. Took 20 minutes.

Meanwhile, other people are paying thousands for trading bots that use ChatGPT to analyze tweets.

We're building the boring stuff that matters. Stop-loss protection. Signal validation. Multi-source confirmation.

And we're doing it in public. You can watch. All of it.

Currently down on TAO. Up slightly on SOL. Overall negative seven percent for the week.

No hiding. No cherry-picked wins. Just real positions. Real P&L.

This is roostr Capital.

If you want moon promises, go somewhere else. If you want to see how a real hedge fund gets built, stick around."""
    
    # Create talk
    talk_id = create_talk(str(roostr_img), script)
    
    if not talk_id:
        print("\n⚠️  D-ID API key needed!")
        print("1. Go to: https://studio.d-id.com/account-settings")
        print("2. Copy your API key")
        print("3. Save it: mkdir -p ~/.config/did && echo 'YOUR_KEY' > ~/.config/did/api_key")
        print("4. Run this script again")
        return None
    
    # Wait for completion
    video_url = wait_for_video(talk_id)
    
    if video_url:
        output = video_dir / "roostr_talking_v1.mp4"
        download_video(video_url, output)
        return str(output)
    
    return None

if __name__ == "__main__":
    video = create_roostr_video()
    if video:
        print(f"\n🎉 roostr video ready: {video}")
        print("   Ready to post to X, YouTube, TikTok!")
