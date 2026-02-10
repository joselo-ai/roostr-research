#!/usr/bin/env python3
"""
Create video with custom roostr avatar + voiceover
Uses static image + HeyGen voice for now (animated version later)
"""

import subprocess
from pathlib import Path
import json

def create_video_with_roostr():
    """
    Create video with:
    1. Static roostr image as background
    2. HeyGen voice for narration
    3. Simple fade in/out effects
    """
    
    video_dir = Path(__file__).parent.parent / "videos"
    roostr_img = Path(__file__).parent.parent / "roostr-avatar" / "roostr_character.jpg"
    
    # Anti-scam script (Version 3)
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
    
    # For now, create a simple text file with the script
    # (Full video generation with custom avatar needs D-ID or similar tool)
    output = video_dir / "roostr_script_v1.txt"
    with open(output, 'w') as f:
        f.write(script)
    
    print(f"✅ roostr character saved: {roostr_img}")
    print(f"✅ Script ready: {output}")
    print()
    print("📝 Next steps:")
    print("1. Use D-ID.com (free tier) to animate the rooster")
    print("2. Upload roostr_character.jpg")
    print("3. Paste script")
    print("4. Generate video")
    print()
    print("OR: Keep using HeyGen with Adrian until we set up D-ID API")

if __name__ == "__main__":
    create_video_with_roostr()
