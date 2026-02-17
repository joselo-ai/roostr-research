#!/usr/bin/env python3
"""
Test Script - Verify Content Factory Setup
Checks all dependencies and posts a test message
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    try:
        import discord_helper
        import agent_research
        import agent_script_writer
        import agent_thumbnail
        import agent_assembler
        import run_pipeline
        print("   ✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False


def test_discord_config():
    """Test Discord configuration."""
    print("\n🧪 Testing Discord configuration...")
    
    # Check bot token
    token_file = Path.home() / '.openclaw/workspace/.discord-bot-token'
    if not token_file.exists():
        print(f"   ❌ Bot token not found: {token_file}")
        return False
    print(f"   ✅ Bot token exists")
    
    # Check channels config
    channels_file = Path.home() / '.openclaw/workspace/.discord-channels.json'
    if not channels_file.exists():
        print(f"   ❌ Channels config not found: {channels_file}")
        return False
    print(f"   ✅ Channels config exists")
    
    # Verify Content Factory channels
    import json
    with open(channels_file) as f:
        config = json.load(f)
    
    required_channels = ['trending-stories', 'scripts', 'thumbnails', 'ready-to-publish']
    for channel in required_channels:
        if channel in config.get('channels', {}):
            print(f"   ✅ Channel #{channel} configured")
        else:
            print(f"   ❌ Channel #{channel} missing")
            return False
    
    return True


def test_openai_skill():
    """Test OpenAI image gen skill."""
    print("\n🧪 Testing OpenAI image generation skill...")
    
    skill_path = Path('/opt/homebrew/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py')
    if not skill_path.exists():
        print(f"   ❌ Image gen skill not found: {skill_path}")
        return False
    print(f"   ✅ Image gen skill exists")
    
    # Check OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("   ⚠️  OPENAI_API_KEY not set (thumbnails will fail)")
        return False
    print("   ✅ OPENAI_API_KEY is set")
    
    return True


def test_output_directory():
    """Test output directory creation."""
    print("\n🧪 Testing output directory...")
    
    output_dir = Path(__file__).parent / 'generated_thumbnails'
    output_dir.mkdir(exist_ok=True)
    
    if output_dir.exists():
        print(f"   ✅ Output directory exists: {output_dir}")
        return True
    else:
        print(f"   ❌ Failed to create output directory")
        return False


def test_discord_post():
    """Test posting to Discord."""
    print("\n🧪 Testing Discord posting...")
    
    try:
        import discord_helper
        
        test_message = """🧪 **Content Factory Test Message**

This is a test post from the Content Factory setup script.

✅ If you see this, the Discord integration is working!

Components tested:
• Discord API connection
• Channel routing
• Message formatting

Ready to generate content! 🚀"""
        
        result = discord_helper.post_trending_story(test_message)
        
        if result:
            print(f"   ✅ Test message posted to #trending-stories")
            print(f"      Message ID: {result.get('id')}")
            return True
        else:
            print(f"   ❌ Failed to post test message")
            return False
    
    except Exception as e:
        print(f"   ❌ Discord post failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("🏭 CONTENT FACTORY - SETUP TEST")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Discord Config", test_discord_config),
        ("OpenAI Skill", test_openai_skill),
        ("Output Directory", test_output_directory),
        ("Discord Posting", test_discord_post)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Content Factory is ready to run.")
        print("\nNext steps:")
        print("  1. Run research agent: python3 agent_research.py")
        print("  2. Run full pipeline: python3 run_pipeline.py")
        print("  3. Check Discord channels for output")
    else:
        print("\n⚠️  Some tests failed. Please fix issues before running pipeline.")
    
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
