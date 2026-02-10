#!/usr/bin/env python3
"""
Create test video - TradingView Integration Story
"""

from heygen_client import create_video, get_video_status
from video_script_generator import generate_tradingview_integration_script
import time

def create_tradingview_video():
    """Create video about TradingView integration"""
    
    print("🎬 Creating TradingView Integration video...")
    print()
    
    # Generate script
    script = generate_tradingview_integration_script()
    print("📝 Script:")
    print("-" * 60)
    print(script)
    print("-" * 60)
    print()
    
    # Create video
    print("🚀 Submitting to HeyGen...")
    video_id = create_video(
        script=script,
        title="TradingView Integration - AI Hedge Fund Build",
        avatar_id=None,  # Use default avatar
        voice_id=None    # Use default voice
    )
    
    if video_id:
        print(f"✅ Video job created: {video_id}")
        print(f"   Check status: python3 -c \"from heygen_client import get_video_status; print(get_video_status('{video_id}'))\"")
        print()
        print("⏳ Video generation takes 2-5 minutes...")
        print("   Will notify when ready")
        
        return video_id
    else:
        print("❌ Failed to create video")
        return None

if __name__ == "__main__":
    video_id = create_tradingview_video()
    
    if video_id:
        print(f"\n📹 Video ID: {video_id}")
        print("   Save this ID to check status later")
