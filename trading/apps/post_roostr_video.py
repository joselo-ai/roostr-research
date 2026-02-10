#!/usr/bin/env python3
"""
Post roostr video to X, YouTube, TikTok
Once G sends the D-ID generated video
"""

from pathlib import Path
import subprocess

def post_to_platforms(video_path):
    """Post video to all platforms"""
    
    video = Path(video_path)
    if not video.exists():
        print(f"❌ Video not found: {video_path}")
        return
    
    # Caption for all platforms
    caption = """🐓 Real AI trading vs the scams

We're building roostr Capital in public. 
Real positions. Real P&L. Real infrastructure.

No moon promises. Just honest trading.

Follow the journey:
🔗 GitHub: github.com/joselo-ai/roostr-research
📊 Dashboard: Live updates every hour

#trading #AI #buildinpublic #crypto"""
    
    print(f"📹 Video ready: {video}")
    print(f"📝 Caption: {caption}")
    print()
    print("🚀 Ready to post to:")
    print("   - X/Twitter")
    print("   - YouTube")
    print("   - TikTok")
    print()
    print("⚠️  Manual posting for now (Twitter API setup needed)")
    print("   1. Upload video to each platform")
    print("   2. Use caption above")
    print("   3. Tag: #trading #AI #buildinpublic")
    
    # Save caption for easy copy-paste
    caption_file = video.parent / "video_caption.txt"
    with open(caption_file, 'w') as f:
        f.write(caption)
    
    print(f"\n✅ Caption saved: {caption_file}")
    
if __name__ == "__main__":
    print("Waiting for video from G...")
    print("Once received, run: python3 post_roostr_video.py /path/to/video.mp4")
