#!/usr/bin/env python3
"""
HeyGen API Client - AI Video Generation
Create talking-head videos from scripts
"""

import requests
import json
from pathlib import Path
from datetime import datetime

API_KEY_PATH = Path.home() / ".config/heygen/api_key"
BASE_URL = "https://api.heygen.com/v1"

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

def list_avatars():
    """List available avatars"""
    url = f"{BASE_URL}/avatars"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def list_voices():
    """List available voices"""
    url = f"{BASE_URL}/voices"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def create_video(script, title="Untitled", avatar_id=None, voice_id=None):
    """
    Create a video from a script
    
    Args:
        script: Text script for the video
        title: Video title
        avatar_id: Avatar ID (if None, uses default)
        voice_id: Voice ID (if None, uses default)
    
    Returns:
        Video generation job ID
    """
    url = f"{BASE_URL}/video/generate"
    
    payload = {
        "title": title,
        "test": False,  # Set to True for test mode (no credit charge)
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id or "default",  # Use default avatar if not specified
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": script,
                    "voice_id": voice_id or "1bd001e7e50f421d891986aad5158bc8"  # Default voice
                },
                "background": {
                    "type": "color",
                    "value": "#000000"
                }
            }
        ]
    }
    
    response = requests.post(url, headers=get_headers(), json=payload)
    response.raise_for_status()
    result = response.json()
    
    return result.get("data", {}).get("video_id")

def get_video_status(video_id):
    """Check video generation status"""
    url = f"{BASE_URL}/video/{video_id}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def test_connection():
    """Test API connection"""
    try:
        print("🔐 Testing HeyGen API connection...")
        
        # Test with list_avatars (lightweight call)
        url = f"{BASE_URL}/avatars"
        response = requests.get(url, headers=get_headers())
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            data = response.json()
            avatars = data.get("data", {}).get("avatars", [])
            print(f"   Available avatars: {len(avatars)}")
            if avatars:
                print(f"   Example avatar: {avatars[0].get('avatar_name', 'Unknown')}")
            return True
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    if test_connection():
        print("\n✅ HeyGen integration ready!")
        print("   Use create_video() to generate videos")
    else:
        print("\n❌ HeyGen integration failed")
