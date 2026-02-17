#!/usr/bin/env python3
"""
Thumbnail Generator Agent
Monitors #scripts and generates eye-catching thumbnails using OpenAI image generation
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
import discord_helper

# Output directory for generated thumbnails
OUTPUT_DIR = Path(__file__).parent / 'generated_thumbnails'
OUTPUT_DIR.mkdir(exist_ok=True)

# OpenAI image gen script path
IMAGE_GEN_SCRIPT = Path('/opt/homebrew/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py')


def extract_script_from_message(message_content: str) -> Optional[Dict]:
    """
    Parse a script message from Discord.
    
    Returns:
        Dict with story_title, story_url, format, hook, body
    """
    lines = message_content.split('\n')
    
    script = {}
    
    # Extract story title
    for line in lines:
        if line.startswith('**Original Story:**'):
            script['story_title'] = line.split('**Original Story:**')[1].strip()
    
    # Extract URL
    for i, line in enumerate(lines):
        if '🔗' in line and i > 0:
            script['story_url'] = line.replace('🔗', '').strip()
    
    # Extract format
    for line in lines:
        if '**Format:**' in line:
            script['format'] = line.split('**Format:**')[1].strip()
    
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
    script['hook'] = ' '.join(hook_lines) if hook_lines else ''
    
    # Extract body (first part for context)
    body_started = False
    body_lines = []
    for line in lines:
        if '**📝 BODY' in line:
            body_started = True
            continue
        if body_started:
            if line.startswith('**') or line.startswith('---'):
                break
            if line.strip():
                body_lines.append(line.strip())
                if len(body_lines) >= 3:  # Just need first few lines
                    break
    script['body'] = ' '.join(body_lines) if body_lines else ''
    
    return script if 'story_title' in script else None


def generate_thumbnail_prompts(script: Dict) -> List[str]:
    """
    Generate multiple thumbnail prompt variations.
    
    Returns:
        List of image generation prompts
    """
    title = script.get('story_title', '')
    hook = script.get('hook', '')
    format_type = script.get('format', '').lower()
    
    # Extract key subject
    subject = title.split('-')[0].strip() if '-' in title else title.split(':')[0].strip()
    
    prompts = []
    
    # Style 1: Bold text with dramatic imagery
    if 'ai' in title.lower() or 'tech' in title.lower():
        prompts.append(
            f"YouTube thumbnail style: Bold red text '{subject[:30]}' overlaid on dramatic "
            f"futuristic tech background with circuit boards, glowing blue lights, AI neural "
            f"network patterns, high contrast, eye-catching, professional design, 16:9 aspect ratio"
        )
    
    # Style 2: Shocked face reaction (if controversy or shocking)
    if format_type == 'controversy' or any(word in title.lower() for word in ['shocking', 'surges', 'crashes']):
        prompts.append(
            f"YouTube thumbnail: Shocked surprised face expression, mouth open, pointing gesture, "
            f"large yellow text '{subject[:25]}', red arrows, bright background, clickbait style "
            f"but professional quality, trending viral aesthetic, 16:9"
        )
    
    # Style 3: Clean minimal with bold typography
    if 'crypto' in title.lower() or 'trading' in title.lower():
        prompts.append(
            f"Modern YouTube thumbnail: Large bold white text '{subject[:30]}' on gradient "
            f"background (dark blue to purple), Bitcoin logo or candlestick charts, gold accents, "
            f"premium luxury feel, clean minimalist design, 16:9 ratio"
        )
    
    # Style 4: Before/after split screen
    prompts.append(
        f"YouTube thumbnail split screen design: Left side labeled 'BEFORE' darker, right side "
        f"'AFTER' brighter and better, large bold text '{subject[:25]}' across center, "
        f"transformation theme, high energy, professional, 16:9"
    )
    
    # Style 5: Question mark intrigue
    if format_type == 'educational' or '?' in title:
        prompts.append(
            f"YouTube thumbnail: Giant glowing question mark, text '{subject[:30]}' in bold white "
            f"font, mysterious dark background with spotlight effect, curiosity-driven design, "
            f"clean professional look, 16:9 aspect ratio"
        )
    
    # Return top 3 most relevant
    return prompts[:3]


def generate_title_variations(script: Dict) -> List[str]:
    """Generate clickable title variations for the thumbnail."""
    title = script.get('story_title', '')
    
    # Extract main subject
    if '-' in title:
        subject = title.split('-')[0].strip()
    elif ':' in title:
        subject = title.split(':')[0].strip()
    else:
        subject = title[:50]
    
    variations = [
        # Original style
        title[:60],
        
        # Question format
        f"What {subject}? The Truth Revealed",
        
        # Shocking format
        f"SHOCKING: {subject}",
        
        # Timeline format
        f"{subject} (What Happens Next Will Shock You)",
        
        # Simple bold
        f"{subject.upper()}",
        
        # Number format
        f"Why {subject} Changes Everything",
    ]
    
    return variations[:4]


def generate_thumbnail_image(prompt: str, output_filename: str) -> Optional[str]:
    """
    Generate thumbnail using OpenAI image generation skill.
    
    Args:
        prompt: Image generation prompt
        output_filename: Output file name (without extension)
    
    Returns:
        Path to generated image or None
    """
    try:
        output_path = OUTPUT_DIR / f"{output_filename}.png"
        
        # Run OpenAI image gen script
        cmd = [
            'python3',
            str(IMAGE_GEN_SCRIPT),
            '--prompt', prompt,
            '--count', '1',
            '--model', 'dall-e-3',
            '--size', '1792x1024',  # Landscape for YouTube
            '--quality', 'hd',
            '--style', 'vivid',
            '--out-dir', str(OUTPUT_DIR)
        ]
        
        print(f"      Running: {' '.join(cmd[:4])}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # Find the generated image (dall-e-3 generates with timestamp)
            generated_files = sorted(OUTPUT_DIR.glob('*.png'), key=lambda x: x.stat().st_mtime, reverse=True)
            if generated_files:
                latest_file = generated_files[0]
                # Rename to our desired filename
                latest_file.rename(output_path)
                print(f"      ✅ Image generated: {output_path.name}")
                return str(output_path)
            else:
                print(f"      ❌ No image file found after generation")
                return None
        else:
            print(f"      ❌ Image generation failed: {result.stderr}")
            return None
    
    except subprocess.TimeoutExpired:
        print(f"      ❌ Image generation timed out")
        return None
    except Exception as e:
        print(f"      ❌ Error generating image: {e}")
        return None


def create_thumbnail(script: Dict, style_index: int = 0) -> Optional[Dict]:
    """
    Generate thumbnail for a script.
    
    Args:
        script: Script dict
        style_index: Which style prompt to use (0-2)
    
    Returns:
        Dict with thumbnail info
    """
    prompts = generate_thumbnail_prompts(script)
    
    if style_index >= len(prompts):
        style_index = 0
    
    prompt = prompts[style_index]
    
    # Generate safe filename
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', script['story_title'][:40])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"thumb_{safe_title}_{timestamp}"
    
    print(f"   Generating thumbnail with style #{style_index + 1}...")
    print(f"      Prompt: {prompt[:100]}...")
    
    image_path = generate_thumbnail_image(prompt, filename)
    
    if not image_path:
        return None
    
    title_variations = generate_title_variations(script)
    
    return {
        'story_title': script['story_title'],
        'story_url': script['story_url'],
        'image_path': image_path,
        'prompt_used': prompt,
        'title_variations': title_variations,
        'style': style_index + 1
    }


def format_thumbnail_post(thumbnail: Dict) -> str:
    """Format thumbnail post for Discord."""
    title_vars = '\n'.join([f"{i+1}. {title}" for i, title in enumerate(thumbnail['title_variations'])])
    
    post = f"""🎨 **THUMBNAIL GENERATED**

**Original Story:** {thumbnail['story_title']}
🔗 {thumbnail['story_url']}

**🎨 Style Used:** #{thumbnail['style']} (DALL-E 3, HD quality, 16:9 landscape)

**📝 Suggested Title Variations:**
{title_vars}

**💡 Thumbnail Tips:**
• Use variation #1-2 for max clicks
• A/B test different titles
• Ensure text is readable on mobile
• High contrast = better CTR

**🎯 Prompt Used:**
_{thumbnail['prompt_used'][:200]}..._

---

✅ Thumbnail ready! Check image above ⬆️
"""
    
    return post


def monitor_and_generate(limit: int = 5):
    """
    Monitor #scripts channel and generate thumbnails.
    
    Args:
        limit: Number of recent messages to check
    """
    print("🎨 Thumbnail Generator Agent: Monitoring #scripts...")
    
    # Fetch recent messages from scripts channel
    messages = discord_helper.fetch_recent_messages('scripts', limit=limit)
    
    if not messages:
        print("   No messages found in channel")
        return
    
    print(f"   Found {len(messages)} recent messages")
    
    # Filter for actual script posts
    script_messages = []
    for msg in messages:
        content = msg.get('content', '')
        if '**SCRIPT READY' in content and '**Original Story:**' in content:
            script_messages.append(content)
    
    print(f"   Identified {len(script_messages)} script posts")
    
    # Generate thumbnails for each script
    thumbnails_generated = 0
    for script_content in script_messages[:2]:  # Process top 2 scripts
        script = extract_script_from_message(script_content)
        if script:
            print(f"\n   Processing: {script['story_title'][:50]}...")
            
            # Try generating thumbnail (style 0 = most relevant)
            thumbnail = create_thumbnail(script, style_index=0)
            
            if thumbnail:
                thumbnail_post = format_thumbnail_post(thumbnail)
                
                # Post to Discord with image attachment
                result = discord_helper.post_thumbnail(
                    content=thumbnail_post,
                    file_path=thumbnail['image_path']
                )
                
                if result:
                    thumbnails_generated += 1
                    print(f"   ✅ Thumbnail posted!")
            else:
                print(f"   ⚠️ Thumbnail generation failed, skipping...")
    
    print(f"\n✅ Thumbnail Generator Agent complete! Generated {thumbnails_generated} thumbnails.")


if __name__ == "__main__":
    # Standalone execution
    monitor_and_generate(limit=10)
