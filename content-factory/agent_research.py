#!/usr/bin/env python3
"""
Research Agent - Trending Stories Scanner
Scans web for trending topics and posts to #trending-stories
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
import discord_helper

# Scoring weights
WEIGHTS = {
    'virality': 0.3,
    'relevance': 0.4,
    'freshness': 0.2,
    'engagement_potential': 0.1
}

# Relevance keywords for our audience
RELEVANT_KEYWORDS = [
    'ai', 'artificial intelligence', 'chatgpt', 'openai', 'llm', 'machine learning',
    'trading', 'stocks', 'crypto', 'bitcoin', 'ethereum', 'market', 'finance',
    'tech', 'startup', 'business', 'entrepreneur', 'innovation',
    'automation', 'productivity', 'saas', 'software'
]


def search_trending_topics(openclaw_search_fn=None) -> List[Dict]:
    """
    Search for trending topics using web_search.
    In OpenClaw context, this gets called with web_search injected.
    For standalone testing, returns mock data.
    
    Returns:
        List of trending story dicts with: title, source, url, snippet, score
    """
    if openclaw_search_fn:
        # Real search via OpenClaw
        queries = [
            "trending AI news today",
            "trending cryptocurrency trading news",
            "viral tech stories today",
            "trending startup business news"
        ]
        
        all_results = []
        for query in queries:
            results = openclaw_search_fn(query, count=5)
            for r in results:
                all_results.append({
                    'title': r.get('title', 'Untitled'),
                    'url': r.get('url', ''),
                    'snippet': r.get('description', ''),
                    'source': r.get('url', '').split('/')[2] if r.get('url') else 'Unknown'
                })
        
        return all_results
    else:
        # Mock data for testing
        return [
            {
                'title': 'OpenAI Announces GPT-5 with Revolutionary Reasoning',
                'source': 'techcrunch.com',
                'url': 'https://techcrunch.com/mock-article-1',
                'snippet': 'OpenAI unveils GPT-5 with unprecedented reasoning capabilities...'
            },
            {
                'title': 'Bitcoin Surges Past $100K as ETF Inflows Hit Record',
                'source': 'bloomberg.com',
                'url': 'https://bloomberg.com/mock-article-2',
                'snippet': 'Bitcoin reaches new all-time high amid massive institutional demand...'
            }
        ]


def score_story(story: Dict) -> Tuple[float, Dict]:
    """
    Score a story based on virality, relevance, freshness, engagement potential.
    
    Returns:
        (total_score, score_breakdown)
    """
    scores = {}
    
    # Virality (based on source authority and title excitement)
    high_authority_sources = ['techcrunch', 'bloomberg', 'wsj', 'reuters', 'cnbc']
    source = story.get('source', '').lower()
    virality_score = 0.7 if any(s in source for s in high_authority_sources) else 0.4
    
    # Boost for viral keywords
    viral_keywords = ['breaking', 'surges', 'crashes', 'revolutionary', 'announces', 'unveils']
    title_lower = story.get('title', '').lower()
    if any(kw in title_lower for kw in viral_keywords):
        virality_score += 0.3
    scores['virality'] = min(virality_score, 1.0)
    
    # Relevance (keyword matching)
    text_to_check = f"{story.get('title', '')} {story.get('snippet', '')}".lower()
    keyword_matches = sum(1 for kw in RELEVANT_KEYWORDS if kw in text_to_check)
    relevance_score = min(keyword_matches / 3.0, 1.0)  # 3+ matches = perfect score
    scores['relevance'] = relevance_score
    
    # Freshness (assume all search results are recent for now)
    scores['freshness'] = 0.9
    
    # Engagement potential (length, numbers, questions)
    engagement_score = 0.5
    if any(char.isdigit() for char in story.get('title', '')):
        engagement_score += 0.2  # Numbers attract attention
    if '?' in story.get('title', ''):
        engagement_score += 0.3  # Questions engage
    scores['engagement_potential'] = min(engagement_score, 1.0)
    
    # Calculate weighted total
    total_score = sum(scores[key] * WEIGHTS[key] for key in WEIGHTS)
    
    return total_score, scores


def generate_content_angles(story: Dict) -> List[str]:
    """Generate content angle ideas for a story."""
    title = story.get('title', '')
    
    angles = []
    
    if 'ai' in title.lower() or 'gpt' in title.lower():
        angles.append("🎓 Educational: How this AI advancement affects everyday users")
        angles.append("💼 Business: Investment opportunities in AI sector")
        angles.append("⚡ Quick Take: 60-second explanation for beginners")
    
    if 'crypto' in title.lower() or 'bitcoin' in title.lower():
        angles.append("📈 Trading: Technical analysis and price targets")
        angles.append("🎯 Strategy: How traders should position themselves")
        angles.append("🚀 Hype: Why this could trigger the next bull run")
    
    if 'startup' in title.lower() or 'business' in title.lower():
        angles.append("💡 Lessons: What entrepreneurs can learn from this")
        angles.append("🎬 Story: The dramatic rise/fall narrative")
    
    # Default angles if no specific match
    if not angles:
        angles.append("🔥 Hot Take: Controversial opinion on this topic")
        angles.append("📊 Deep Dive: Full breakdown and analysis")
        angles.append("⚡ Quickfire: Fast-paced summary for busy viewers")
    
    return angles[:3]  # Return top 3


def format_story_post(story: Dict, rank: int, score: float, score_breakdown: Dict) -> str:
    """Format a story for Discord posting."""
    angles = generate_content_angles(story)
    angles_text = '\n'.join(angles)
    
    # Calculate engagement estimate (mock)
    engagement_est = int(score * 10000)  # Mock engagement number
    
    post = f"""**#{rank} - {story['title']}**

📰 **Source:** {story['source']}
🔗 **Link:** {story['url']}

📊 **Why It's Trending:**
• Virality: {score_breakdown['virality']:.0%} (source authority + viral keywords)
• Relevance: {score_breakdown['relevance']:.0%} (audience interest match)
• Freshness: {score_breakdown['freshness']:.0%} (recency)
• Engagement: {score_breakdown['engagement_potential']:.0%} (click potential)
• **Overall Score: {score:.2f}/1.00**

💬 **Estimated Engagement:** ~{engagement_est:,} views potential

🎬 **Content Angle Ideas:**
{angles_text}

📝 **Snippet:**
_{story['snippet'][:200]}{'...' if len(story['snippet']) > 200 else ''}_

---"""
    
    return post


def run_research_agent(openclaw_search_fn=None, top_n: int = 7) -> List[Dict]:
    """
    Main research agent function.
    
    Args:
        openclaw_search_fn: Optional web_search function injected by OpenClaw
        top_n: Number of top stories to post
    
    Returns:
        List of selected stories with scores
    """
    print("🔍 Research Agent: Scanning trending topics...")
    
    # Search for stories
    raw_stories = search_trending_topics(openclaw_search_fn)
    print(f"   Found {len(raw_stories)} potential stories")
    
    # Score and rank stories
    scored_stories = []
    for story in raw_stories:
        score, breakdown = score_story(story)
        story['score'] = score
        story['score_breakdown'] = breakdown
        scored_stories.append(story)
    
    # Sort by score and take top N
    top_stories = sorted(scored_stories, key=lambda x: x['score'], reverse=True)[:top_n]
    
    print(f"   Selected top {len(top_stories)} stories")
    print(f"   Score range: {top_stories[0]['score']:.2f} - {top_stories[-1]['score']:.2f}")
    
    return top_stories


def post_to_discord(stories: List[Dict]):
    """Post trending stories to Discord #trending-stories channel."""
    print("\n📤 Posting to Discord #trending-stories...")
    
    # Header message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    header = f"""🔥 **TRENDING STORIES REPORT** 🔥
Generated: {timestamp}

Top {len(stories)} stories ranked by virality, relevance, and engagement potential.
Ready for script writing! 👇

═══════════════════════════════════════"""
    
    discord_helper.post_trending_story(header)
    
    # Post each story
    for i, story in enumerate(stories, 1):
        post_content = format_story_post(
            story, 
            rank=i, 
            score=story['score'], 
            score_breakdown=story['score_breakdown']
        )
        result = discord_helper.post_trending_story(post_content)
        if result:
            print(f"   ✅ Posted story #{i}: {story['title'][:50]}...")
    
    # Footer
    footer = f"""═══════════════════════════════════════

✅ **Research complete!** {len(stories)} trending stories posted.

🤖 Next: Script Writer Agent will monitor this channel and generate scripts.
"""
    discord_helper.post_trending_story(footer)
    
    print(f"\n✅ Research Agent complete! Posted {len(stories)} stories to Discord.")


if __name__ == "__main__":
    # Standalone execution (uses mock data)
    stories = run_research_agent(openclaw_search_fn=None, top_n=7)
    post_to_discord(stories)
