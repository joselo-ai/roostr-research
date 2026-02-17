#!/usr/bin/env python3
"""
Package Assembler Agent
Monitors all content channels and creates final publish-ready packages
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
import discord_helper


def extract_story_url_from_post(content: str) -> Optional[str]:
    """Extract story URL from any post type."""
    lines = content.split('\n')
    for line in lines:
        if '🔗' in line or 'http' in line:
            # Extract URL
            url_match = re.search(r'https?://[^\s]+', line)
            if url_match:
                return url_match.group(0)
    return None


def extract_story_title_from_post(content: str) -> Optional[str]:
    """Extract story title from any post type."""
    lines = content.split('\n')
    
    # Try to find "Original Story:" line
    for line in lines:
        if '**Original Story:**' in line:
            return line.split('**Original Story:**')[1].strip()
    
    # Fallback: look for first bold heading with #
    for line in lines:
        if line.startswith('**#') and '-' in line:
            return line.split('-', 1)[1].strip(' *')
    
    return None


def fetch_content_for_story(story_url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Fetch script and thumbnail for a given story URL.
    
    Returns:
        (script_content, thumbnail_content, thumbnail_image_url)
    """
    # Fetch from scripts channel
    scripts = discord_helper.fetch_recent_messages('scripts', limit=20)
    script_content = None
    for msg in scripts:
        content = msg.get('content', '')
        if story_url in content:
            script_content = content
            break
    
    # Fetch from thumbnails channel
    thumbnails = discord_helper.fetch_recent_messages('thumbnails', limit=20)
    thumbnail_content = None
    thumbnail_image_url = None
    for msg in thumbnails:
        content = msg.get('content', '')
        if story_url in content:
            thumbnail_content = content
            # Extract image URL from attachments
            attachments = msg.get('attachments', [])
            if attachments:
                thumbnail_image_url = attachments[0].get('url')
            break
    
    return script_content, thumbnail_content, thumbnail_image_url


def extract_script_details(script_content: str) -> Dict:
    """Extract key details from script post."""
    details = {}
    
    lines = script_content.split('\n')
    
    # Extract format
    for line in lines:
        if '**Format:**' in line:
            details['format'] = line.split('**Format:**')[1].strip()
    
    # Extract duration
    for line in lines:
        if '**Duration:**' in line:
            duration_match = re.search(r'~(\d+) seconds', line)
            if duration_match:
                details['duration'] = int(duration_match.group(1))
    
    # Extract hook
    hook_started = False
    hook_lines = []
    for line in lines:
        if '**🎣 HOOK' in line:
            hook_started = True
            continue
        if hook_started:
            if line.startswith('**') or line.startswith('---'):
                break
            if line.strip():
                hook_lines.append(line.strip())
    details['hook'] = ' '.join(hook_lines)[:100] + '...' if hook_lines else ''
    
    return details


def extract_thumbnail_details(thumbnail_content: str) -> Dict:
    """Extract key details from thumbnail post."""
    details = {}
    
    lines = thumbnail_content.split('\n')
    
    # Extract title variations
    title_vars = []
    in_variations = False
    for line in lines:
        if '**📝 Suggested Title Variations:**' in line:
            in_variations = True
            continue
        if in_variations:
            if line.startswith('**') or line.startswith('---'):
                break
            if line.strip() and re.match(r'\d+\.', line.strip()):
                # Remove number prefix
                title_vars.append(re.sub(r'^\d+\.\s*', '', line.strip()))
    
    details['title_variations'] = title_vars[:3]  # Top 3
    
    return details


def create_publishing_checklist(story_title: str, format_type: str = 'educational') -> List[str]:
    """Generate publishing checklist."""
    checklist = [
        "☐ Review full script for accuracy and tone",
        "☐ Check thumbnail text is readable on mobile",
        "☐ Select best title variation (A/B test if possible)",
        "☐ Record video following script timing",
        "☐ Add suggested B-roll and visual overlays",
        "☐ Edit with music and sound effects",
        "☐ Add captions/subtitles for accessibility",
        "☐ Upload thumbnail and select publish time",
        "☐ Optimize video tags and description",
        "☐ Schedule for peak engagement time",
        "☐ Prepare social media promotion posts",
        "☐ Monitor first hour performance and engage with comments"
    ]
    
    # Add format-specific items
    if format_type == 'controversy':
        checklist.insert(3, "☐ Prepare response to potential criticism")
    elif format_type == 'educational':
        checklist.insert(3, "☐ Fact-check all claims and statistics")
    
    return checklist


def create_package(story_url: str, story_title: str, script_content: str, 
                   thumbnail_content: str, thumbnail_image_url: str) -> str:
    """Create final publish-ready package post."""
    
    script_details = extract_script_details(script_content)
    thumbnail_details = extract_thumbnail_details(thumbnail_content)
    
    format_type = script_details.get('format', 'general')
    duration = script_details.get('duration', 60)
    hook = script_details.get('hook', '')
    title_variations = thumbnail_details.get('title_variations', [story_title])
    
    checklist = create_publishing_checklist(story_title, format_type)
    checklist_text = '\n'.join(checklist)
    
    # Format title variations
    if title_variations:
        titles_text = '\n'.join([f"   {i+1}. {title}" for i, title in enumerate(title_variations)])
    else:
        titles_text = f"   1. {story_title}"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    package = f"""🚀 **READY TO PUBLISH - COMPLETE PACKAGE** 🚀

**Story:** {story_title}
**Format:** {format_type.title()} | **Duration:** ~{duration}s
**Generated:** {timestamp}

═══════════════════════════════════════

**📰 ORIGINAL STORY:**
{story_url}

**🎬 SCRIPT:**
View full script in #{discord_helper.CHANNELS.get('scripts', 'scripts')}
**Hook Preview:** "{hook}"

**🎨 THUMBNAIL:**
Image attached above ⬆️ (or check #{discord_helper.CHANNELS.get('thumbnails', 'thumbnails')})

**📝 TITLE OPTIONS (Pick One):**
{titles_text}

═══════════════════════════════════════

**✅ PUBLISHING CHECKLIST:**

{checklist_text}

═══════════════════════════════════════

**🎯 PERFORMANCE TARGETS:**
• First 24h: 10K+ views
• Engagement rate: >5%
• Watch time: >50% retention
• Comments: 100+ engaged viewers

**💡 PRO TIPS:**
• Post during peak hours (12 PM - 3 PM or 7 PM - 9 PM EST)
• Pin top comment with question to boost engagement
• Respond to first 20 comments within 1 hour
• Cross-post teaser to Instagram/TikTok/Twitter

═══════════════════════════════════════

**📁 ALL ASSETS AVAILABLE IN:**
• Script: #{discord_helper.CHANNELS.get('scripts', 'scripts')}
• Thumbnail: #{discord_helper.CHANNELS.get('thumbnails', 'thumbnails')}
• Trending Story: #{discord_helper.CHANNELS.get('trending-stories', 'trending-stories')}

🎬 **READY TO FILM AND PUBLISH!**
"""
    
    return package


def monitor_and_assemble(limit: int = 10):
    """
    Monitor all channels and create packages when script + thumbnail are ready.
    
    Args:
        limit: Number of recent messages to check per channel
    """
    print("📦 Package Assembler Agent: Monitoring all channels...")
    
    # Fetch recent trending stories
    trending_messages = discord_helper.fetch_recent_messages('trending-stories', limit=limit)
    
    if not trending_messages:
        print("   No trending stories found")
        return
    
    print(f"   Found {len(trending_messages)} trending story messages")
    
    # Extract story URLs
    stories_to_process = []
    for msg in trending_messages:
        content = msg.get('content', '')
        # Only process actual story posts (not headers/footers)
        if '**#' in content and '**Source:**' in content:
            url = extract_story_url_from_post(content)
            title = extract_story_title_from_post(content)
            if url and title:
                stories_to_process.append({'url': url, 'title': title})
    
    print(f"   Identified {len(stories_to_process)} stories to check")
    
    # Check each story for complete assets
    packages_created = 0
    for story in stories_to_process[:5]:  # Check top 5
        print(f"\n   Checking: {story['title'][:50]}...")
        
        script_content, thumbnail_content, thumbnail_image_url = fetch_content_for_story(story['url'])
        
        has_script = script_content is not None
        has_thumbnail = thumbnail_content is not None and thumbnail_image_url is not None
        
        print(f"      Script: {'✅' if has_script else '❌'}")
        print(f"      Thumbnail: {'✅' if has_thumbnail else '❌'}")
        
        if has_script and has_thumbnail:
            print(f"      🎉 Complete! Creating package...")
            
            package_post = create_package(
                story['url'],
                story['title'],
                script_content,
                thumbnail_content,
                thumbnail_image_url
            )
            
            # Post package with thumbnail image
            result = discord_helper.post_ready_to_publish(package_post)
            
            if result:
                packages_created += 1
                print(f"      ✅ Package posted to #ready-to-publish!")
        else:
            missing = []
            if not has_script:
                missing.append('script')
            if not has_thumbnail:
                missing.append('thumbnail')
            print(f"      ⏳ Waiting for: {', '.join(missing)}")
    
    print(f"\n✅ Package Assembler Agent complete! Created {packages_created} publish-ready packages.")


if __name__ == "__main__":
    # Standalone execution
    monitor_and_assemble(limit=15)
