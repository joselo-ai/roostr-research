#!/usr/bin/env python3
"""
Morning Brief Generator
Generates daily morning briefing for Discord #morning-brief channel
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Add workspace to path for imports
WORKSPACE = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE))

DISCORD_TOKEN_PATH = WORKSPACE / ".discord-bot-token"
CHANNEL_ID = "1472688401558933578"  # #morning-brief
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")

def read_discord_token():
    """Read Discord bot token"""
    with open(DISCORD_TOKEN_PATH) as f:
        return f.read().strip()

def get_web_news(query, count=3):
    """Fetch news using Brave Search API"""
    if not BRAVE_API_KEY:
        return []
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {
        "q": query,
        "count": count,
        "freshness": "pd"  # Past day
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("web", {}).get("results", [])[:count]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", "")
            })
        return results
    except Exception as e:
        print(f"Error fetching news for '{query}': {e}")
        return []

def generate_business_ideas():
    """Generate 2-3 creative business ideas based on current trends"""
    # This would ideally use web_search results, but for now we'll generate contextual ideas
    ideas = [
        {
            "title": "AI-Powered Market Newsletter",
            "description": "Automated daily market analysis using 18-agent consensus model. Subscription model ($99/mo) targeting retail traders seeking edge.",
            "edge": "Full transparency + algorithmic decision-making (roostr model)"
        },
        {
            "title": "Social Arbitrage SaaS",
            "description": "Reddit/Twitter sentiment scanner that detects viral stocks 2-4 hours before mainstream. API access for hedge funds.",
            "edge": "Real-time social graph analysis + conviction scoring (proven with Dumb Money strategy)"
        },
        {
            "title": "Simmer Weather Trading Course",
            "description": "Teach NOAA forecast arbitrage on Polymarket. Course ($299) + Discord community ($49/mo).",
            "edge": "First-mover in weather prediction markets + proven strategy"
        }
    ]
    return ideas[:2]  # Return 2 ideas

def extract_tasks():
    """Extract tasks from MEMORY.md, today's memory file, and HEARTBEAT.md"""
    tasks = []
    
    # Check HEARTBEAT.md
    heartbeat_path = WORKSPACE / "HEARTBEAT.md"
    if heartbeat_path.exists():
        with open(heartbeat_path) as f:
            content = f.read()
            if "Social Arbitrage Agent" in content:
                tasks.append("🤖 Run social arb scan (9 AM daily)")
            if "Simmer Weather Trading" in content:
                tasks.append("🌤️ Check Simmer weather opportunities (9 AM, 1 PM, 7 PM)")
    
    # Check today's memory file
    today = datetime.now().strftime("%Y-%m-%d")
    memory_path = WORKSPACE / "memory" / f"{today}.md"
    if memory_path.exists():
        with open(memory_path) as f:
            content = f.read()
            # Look for TODO markers
            for line in content.split("\n"):
                if "TODO" in line or "[ ]" in line:
                    tasks.append(line.strip("- ").strip())
    
    # Check MEMORY.md for active projects
    memory_main = WORKSPACE / "MEMORY.md"
    if memory_main.exists():
        with open(memory_main) as f:
            content = f.read()
            if "Harvard OPM" in content:
                tasks.append("📚 Harvard OPM case studies (starting Feb 2026)")
            if "Phase 1: $1M Paper" in content:
                tasks.append("💰 Monitor Phase 1 paper trading (target: >20% returns, <15% drawdown)")
    
    return tasks

def get_recommendations():
    """Generate recommendations for tasks to do together"""
    recommendations = [
        "Review 18-agent deliberation logs for last 24h (trading/logs/)",
        "Analyze yesterday's trading performance vs conviction scores",
        "Update roostr social media with latest signal (if GREEN ≥8.0/10)",
        "Review Yieldschool + Dumb Money for new opportunities"
    ]
    return recommendations

def get_oura_stats():
    """Get Oura ring stats (placeholder for now)"""
    # Check for API key
    oura_key_path = WORKSPACE / ".oura-api-key"
    if oura_key_path.exists():
        # TODO: Implement Oura API integration
        return {
            "status": "configured",
            "readiness": "85%",
            "sleep_score": "82",
            "note": "API integration pending"
        }
    else:
        return {
            "status": "not_configured",
            "note": "Set up Oura API key in .oura-api-key"
        }

def format_news_section(news_items):
    """Format news section for Discord"""
    if not news_items:
        return "_No recent news found_"
    
    lines = []
    for item in news_items:
        title = item["title"][:100]  # Truncate long titles
        url = item["url"]
        # Wrap URLs in <> to suppress embeds
        lines.append(f"• **{title}**\n  <{url}>")
    
    return "\n".join(lines)

def generate_morning_brief():
    """Generate the complete morning brief"""
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    
    # Gather all sections
    print("Fetching news...")
    trading_news = get_web_news("stock market trading news", 2)
    ai_news = get_web_news("artificial intelligence AI news", 2)
    markets_news = get_web_news("financial markets economic news", 2)
    
    print("Generating business ideas...")
    business_ideas = generate_business_ideas()
    
    print("Extracting tasks...")
    tasks = extract_tasks()
    
    print("Getting recommendations...")
    recommendations = get_recommendations()
    
    print("Fetching Oura stats...")
    oura_stats = get_oura_stats()
    
    # Build the brief
    brief = f"""**🌅 Morning Brief — {date_str}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📰 News & Markets**

*Trading & Markets:*
{format_news_section(trading_news)}

*AI & Technology:*
{format_news_section(ai_news)}

*Economic News:*
{format_news_section(markets_news)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**💡 Business Ideas**

"""
    
    for i, idea in enumerate(business_ideas, 1):
        brief += f"**{i}. {idea['title']}**\n"
        brief += f"{idea['description']}\n"
        brief += f"_Edge:_ {idea['edge']}\n\n"
    
    brief += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**✅ Tasks for Today**

"""
    
    if tasks:
        for task in tasks[:8]:  # Limit to 8 tasks
            brief += f"• {task}\n"
    else:
        brief += "_No specific tasks scheduled_\n"
    
    brief += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**🎯 Recommendations**

"""
    
    for rec in recommendations:
        brief += f"• {rec}\n"
    
    brief += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**💪 Oura Stats**

"""
    
    if oura_stats["status"] == "configured":
        brief += f"• Readiness: {oura_stats['readiness']}\n"
        brief += f"• Sleep Score: {oura_stats['sleep_score']}\n"
        brief += f"• _{oura_stats['note']}_\n"
    else:
        brief += f"_{oura_stats['note']}_\n"
    
    brief += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_Generated by Joselo at {now.strftime("%I:%M %p EST")}_
"""
    
    return brief

def post_to_discord(message):
    """Post message to Discord channel"""
    token = read_discord_token()
    
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()

def main():
    """Main execution"""
    print(f"🌅 Generating morning brief for {datetime.now().strftime('%Y-%m-%d')}")
    
    try:
        brief = generate_morning_brief()
        
        # Save to file for debugging
        output_dir = WORKSPACE / "morning-brief" / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(output_file, "w") as f:
            f.write(brief)
        
        print(f"\n✅ Brief saved to: {output_file}")
        
        # Post to Discord
        print("\n📤 Posting to Discord...")
        result = post_to_discord(brief)
        
        print(f"✅ Posted successfully! Message ID: {result['id']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
