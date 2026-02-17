#!/usr/bin/env python3
"""
Script Writer Agent
Monitors #trending-stories and generates viral video scripts
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
import discord_helper


# Script templates for different formats
SCRIPT_TEMPLATES = {
    'educational': {
        'hook_style': 'question',
        'tone': 'informative but engaging',
        'cta': 'follow for more insights'
    },
    'entertaining': {
        'hook_style': 'shocking_statement',
        'tone': 'energetic and viral',
        'cta': 'smash that follow button'
    },
    'controversy': {
        'hook_style': 'hot_take',
        'tone': 'bold and opinionated',
        'cta': 'let me know your thoughts in comments'
    },
    'tutorial': {
        'hook_style': 'promise',
        'tone': 'helpful and actionable',
        'cta': 'try this and tag me with results'
    }
}


def extract_story_from_message(message_content: str) -> Optional[Dict]:
    """
    Parse a trending story message from Discord.
    
    Returns:
        Dict with title, source, url, score, angles
    """
    lines = message_content.split('\n')
    
    story = {}
    
    # Extract title (first line with **)
    for line in lines:
        if line.startswith('**#') and '-' in line:
            # Format: **#1 - Title**
            story['title'] = line.split('-', 1)[1].strip(' *')
            break
    
    # Extract source
    for line in lines:
        if '**Source:**' in line:
            story['source'] = line.split('**Source:**')[1].strip()
    
    # Extract URL
    for line in lines:
        if '**Link:**' in line:
            story['url'] = line.split('**Link:**')[1].strip()
    
    # Extract score
    for line in lines:
        if '**Overall Score:' in line:
            score_match = re.search(r'(\d+\.\d+)', line)
            if score_match:
                story['score'] = float(score_match.group(1))
    
    # Extract snippet
    snippet_started = False
    snippet_lines = []
    for line in lines:
        if '**Snippet:**' in line:
            snippet_started = True
            continue
        if snippet_started:
            if line.startswith('---') or line.startswith('═'):
                break
            if line.strip().startswith('_'):
                snippet_lines.append(line.strip('_ '))
    story['snippet'] = ' '.join(snippet_lines) if snippet_lines else ''
    
    return story if 'title' in story else None


def determine_script_format(story: Dict) -> str:
    """Determine best script format based on story content."""
    title = story.get('title', '').lower()
    snippet = story.get('snippet', '').lower()
    text = f"{title} {snippet}"
    
    # Check for educational signals
    if any(kw in text for kw in ['how', 'what', 'why', 'explains', 'understanding', 'learn']):
        return 'educational'
    
    # Check for controversy signals
    if any(kw in text for kw in ['controversy', 'debate', 'critics', 'slams', 'fires back']):
        return 'controversy'
    
    # Check for tutorial signals
    if any(kw in text for kw in ['how to', 'guide', 'tutorial', 'step', 'method']):
        return 'tutorial'
    
    # Default to entertaining for viral content
    return 'entertaining'


def generate_hook(story: Dict, hook_style: str) -> str:
    """Generate an attention-grabbing hook (first 3-5 seconds)."""
    title = story.get('title', '')
    
    if hook_style == 'question':
        return f"You know what everyone's talking about right now? {title}. Let me break it down."
    
    elif hook_style == 'shocking_statement':
        # Extract key shocking element
        if 'surges' in title.lower() or 'crashes' in title.lower():
            return f"Stop scrolling. {title}. This is massive."
        return f"This just happened and nobody's talking about it. {title}."
    
    elif hook_style == 'hot_take':
        return f"Hot take: {title}. And here's why everyone's getting it wrong."
    
    elif hook_style == 'promise':
        return f"By the end of this video, you'll understand exactly why {title.split('-')[0].strip()}. Let's go."
    
    else:
        return f"Listen up. {title}. Here's what you need to know."


def generate_body(story: Dict, tone: str, format_type: str) -> str:
    """Generate the main body of the script (45-60 seconds)."""
    title = story.get('title', '')
    snippet = story.get('snippet', '')
    
    if format_type == 'educational':
        return f"""First, the facts: {snippet}

Now here's why this matters to YOU. This isn't just another tech headline - this is going to change how we work, trade, and live.

Think about it: if this technology becomes mainstream, everyone who understands it NOW has a massive advantage.

The smart money is already positioning themselves. Are you?"""
    
    elif format_type == 'entertaining':
        return f"""So here's what went down: {snippet}

I know what you're thinking - "This is crazy!" And you're RIGHT.

This is the kind of thing that only happens once in a while, and when it does, it changes EVERYTHING.

The people who saw this coming are already winning. The people who ignored it? Well, they're still trying to figure out what happened.

Don't be that person."""
    
    elif format_type == 'controversy':
        return f"""Here's the situation: {snippet}

Now, I'm gonna say something that'll probably piss people off, but someone has to say it.

This is either GENIUS or complete INSANITY - and honestly? I think it's both.

Critics are already coming out of the woodwork, but here's what they're missing..."""
    
    elif format_type == 'tutorial':
        return f"""Here's what happened: {snippet}

Now let me show you exactly how to take advantage of this.

Step 1: Pay attention to what the experts are doing - not what they're saying.
Step 2: Position yourself BEFORE everyone else catches on.
Step 3: Stay consistent and trust the process.

It's that simple. Most people overcomplicate it."""
    
    else:
        return snippet[:200]


def generate_cta(cta_style: str, story_title: str) -> str:
    """Generate call-to-action closing."""
    ctas = {
        'follow for more insights': "If you want more analysis like this, hit that follow button. I break down trending stories daily so you never miss what matters.",
        
        'smash that follow button': "If this blew your mind, SMASH that follow button right now! More viral stories coming your way every single day.",
        
        'let me know your thoughts in comments': "Now I want to hear from YOU. What's your take on this? Drop a comment below. Let's debate!",
        
        'try this and tag me with results': "Go try this strategy and tag me with your results. I want to see if this works for you too. Let's get it!"
    }
    
    return ctas.get(cta_style, "Follow for daily trending insights!")


def generate_suggested_visuals(story: Dict, format_type: str) -> List[str]:
    """Generate suggestions for video visuals."""
    title = story.get('title', '').lower()
    
    visuals = [
        "📱 Opening: Face to camera with energetic expression",
    ]
    
    if 'ai' in title or 'tech' in title:
        visuals.append("💻 B-roll: Tech interfaces, code, futuristic graphics")
    
    if 'crypto' in title or 'trading' in title or 'bitcoin' in title:
        visuals.append("📈 Charts: Price charts, green candles, trading screens")
    
    if format_type == 'educational':
        visuals.append("📊 Graphics: Simple diagrams explaining the concept")
    
    if format_type == 'entertaining':
        visuals.append("🎬 B-roll: Fast cuts, dynamic transitions, trending memes")
    
    visuals.extend([
        "👁️ Mid-video: Zoom in for emphasis on key points",
        "🎯 Closing: Direct to camera with CTA"
    ])
    
    return visuals


def create_script(story: Dict) -> Dict:
    """
    Generate complete video script from story.
    
    Returns:
        Dict with script components
    """
    format_type = determine_script_format(story)
    template = SCRIPT_TEMPLATES[format_type]
    
    hook = generate_hook(story, template['hook_style'])
    body = generate_body(story, template['tone'], format_type)
    cta = generate_cta(template['cta'], story['title'])
    visuals = generate_suggested_visuals(story, format_type)
    
    # Calculate approximate duration (150 words per minute for spoken)
    total_words = len(f"{hook} {body} {cta}".split())
    duration_seconds = int((total_words / 150) * 60)
    
    return {
        'story_title': story['title'],
        'story_url': story['url'],
        'format': format_type,
        'hook': hook,
        'body': body,
        'cta': cta,
        'visuals': visuals,
        'duration_seconds': duration_seconds,
        'word_count': total_words
    }


def format_script_post(script: Dict) -> str:
    """Format script for Discord posting."""
    visuals_text = '\n'.join(script['visuals'])
    
    post = f"""🎬 **SCRIPT READY - {script['format'].upper()} FORMAT**

**Original Story:** {script['story_title']}
🔗 {script['story_url']}

⏱️ **Duration:** ~{script['duration_seconds']} seconds ({script['word_count']} words)
🎭 **Format:** {script['format'].title()}

---

**🎣 HOOK (0-5 sec):**
{script['hook']}

**📝 BODY (5-60 sec):**
{script['body']}

**🎯 CTA (60-70 sec):**
{script['cta']}

---

**🎥 SUGGESTED VISUALS:**
{visuals_text}

---

**💡 PRODUCTION NOTES:**
• Energy level: HIGH throughout
• Pacing: Fast cuts, no dead air
• Text overlays: Emphasize key numbers/phrases
• Music: Upbeat background, lower during speech
• Thumbnail: Should match hook intensity

✅ Ready for thumbnail generation!
"""
    
    return post


def monitor_and_generate(limit: int = 5):
    """
    Monitor #trending-stories channel and generate scripts.
    
    Args:
        limit: Number of recent messages to check
    """
    print("📝 Script Writer Agent: Monitoring #trending-stories...")
    
    # Fetch recent messages from trending-stories
    messages = discord_helper.fetch_recent_messages('trending-stories', limit=limit)
    
    if not messages:
        print("   No messages found in channel")
        return
    
    print(f"   Found {len(messages)} recent messages")
    
    # Filter for actual story posts (not headers/footers)
    story_messages = []
    for msg in messages:
        content = msg.get('content', '')
        if '**#' in content and '**Source:**' in content:  # Story format
            story_messages.append(content)
    
    print(f"   Identified {len(story_messages)} story posts")
    
    # Generate scripts for each story
    scripts_generated = 0
    for story_content in story_messages[:3]:  # Process top 3 stories
        story = extract_story_from_message(story_content)
        if story:
            print(f"\n   Generating script for: {story['title'][:50]}...")
            script = create_script(story)
            script_post = format_script_post(script)
            
            result = discord_helper.post_script(script_post)
            if result:
                scripts_generated += 1
                print(f"   ✅ Script posted!")
    
    print(f"\n✅ Script Writer Agent complete! Generated {scripts_generated} scripts.")


if __name__ == "__main__":
    # Standalone execution
    monitor_and_generate(limit=10)
