#!/usr/bin/env python3
"""
HeyGen API Client v2 - CORRECTED endpoints
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime

API_KEY_PATH = Path.home() / ".config/heygen/api_key"
BASE_URL = "https://api.heygen.com/v2"

def load_api_key():
    """Load HeyGen API key"""
    with open(API_KEY_PATH) as f:
        return f.read().strip()

def get_headers():
    """Get authorization headers"""
    api_key = load_api_key()
    return {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }

def list_voices():
    """List available voices"""
    url = f"{BASE_URL}/voices"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def create_video(script, title="Untitled", voice_id=None):
    """
    Create a video from a script using template
    
    Args:
        script: Text script for the video
        title: Video title
        voice_id: Voice ID (if None, uses default)
    
    Returns:
        Video generation result
    """
    url = f"{BASE_URL}/video/generate"
    
    # Simplified payload - using HeyGen's template approach
    payload = {
        "video_inputs": [{
            "voice": {
                "type": "text",
                "input_text": script,
                "voice_id": voice_id or "f38a635bee7a4d1f9b0a654a31d050d2"  # Chill Brian
            }
        }],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": title
    }
    
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, headers=get_headers(), json=payload)
    print(f"Response status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def check_status(video_id):
    """Check video generation status"""
    headers = {"X-Api-Key": load_api_key()}
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def wait_for_video(video_id, max_wait_minutes=10):
    """
    Wait for video to complete
    
    Returns:
        dict with video_url if successful, None if failed/timeout
    """
    print(f"⏳ Waiting for video {video_id}...")
    
    max_checks = max_wait_minutes * 6  # Check every 10 seconds
    for i in range(max_checks):
        status_data = check_status(video_id)
        status = status_data['status']
        
        if status == 'completed':
            print(f"✅ Video ready!")
            return status_data
        elif status == 'failed':
            print(f"❌ Video generation failed: {status_data.get('error')}")
            return None
        
        if i % 6 == 0:  # Print every minute
            print(f"   Status: {status} ({i//6}min)")
        
        time.sleep(10)
    
    print(f"⏱️ Timeout after {max_wait_minutes} minutes")
    return None

def test_simple():
    """Test with minimal script"""
    print("🎬 Testing HeyGen video generation...")
    
    script = "Hello, this is a test from roostr Capital. We're building an AI hedge fund in public."
    
    try:
        result = create_video(script, "Test Video")
        print(f"✅ Success: {result}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_simple()
