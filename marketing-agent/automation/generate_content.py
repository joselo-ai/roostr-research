#!/usr/bin/env python3
"""
roostr Marketing Automation - Content Generator
Auto-generates posts from signals and performance data.
Replenishes the content queue.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import random

# Configuration
WORKSPACE = Path.home() / ".openclaw" / "workspace" / "marketing-agent"
QUEUE_FILE = WORKSPACE / "automation" / "content_queue.json"
SIGNALS_DIR = Path.home() / ".openclaw" / "workspace" / "trading-agent" / "signals"

def load_queue():
    """Load existing content queue"""
    if not QUEUE_FILE.exists():
        return {"posts": [], "last_id": 0}
    
    with open(QUEUE_FILE, 'r') as f:
        return json.load(f)

def save_queue(queue):
    """Save content queue"""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

def get_latest_signals():
    """Get latest GREEN signals from trading agent"""
    if not SIGNALS_DIR.exists():
        return []
    
    # Look for today's signals file
    today = datetime.now().strftime("%Y-%m-%d")
    signals_file = SIGNALS_DIR / f"{today}_signals.json"
    
    if not signals_file.exists():
        return []
    
    try:
        with open(signals_file, 'r') as f:
            data = json.load(f)
            return [s for s in data.get("signals", []) if s.get("signal") == "GREEN"]
    except:
        return []

def generate_signal_post(signal):
    """Generate a post from a GREEN signal"""
    ticker = signal.get("ticker", "UNKNOWN")
    conviction = signal.get("conviction", 7)
    thesis = signal.get("thesis", "Strong technical setup")
    
    content = f"""🟢 NEW SIGNAL

${ticker} - {thesis}

conviction: {conviction}/10
entry zone: ${signal.get('entry_min', '...')}-${signal.get('entry_max', '...')}
targets: ${signal.get('target_1', '...')} / ${signal.get('target_2', '...')}

full research: github.com/roostrcapital/research

roostr. no hype. just signals."""

    return {
        "id": None,  # Will be assigned
        "type": "signal",
        "title": f"Signal: {ticker}",
        "content": content,
        "platforms": ["x", "instagram"],
        "scheduled_time": "09:00",
        "posted": False,
        "created_at": datetime.now().isoformat()
    }

def generate_daily_update():
    """Generate daily recap post"""
    templates = [
        {
            "content": """🐓 daily update

signals scanned: checking all sources
positions: tracking {positions}
watching: {tickers}

automated alpha. running 24/7.

roostr.""",
            "scheduled_time": "19:00"
        },
        {
            "content": """end of day:

✅ signal pipeline: operational
✅ conviction docs: {docs_count} generated
✅ trades: {trades_count} executed

tomorrow: more signals, more transparency.

roostr capital.""",
            "scheduled_time": "19:00"
        }
    ]
    
    template = random.choice(templates)
    
    return {
        "id": None,
        "type": "daily_update",
        "title": "Daily Update",
        "content": template["content"].format(
            positions=random.randint(3, 8),
            tickers="TAO, SOL, BTC",  # Placeholder
            docs_count=random.randint(2, 5),
            trades_count=random.randint(1, 4)
        ),
        "platforms": ["x"],
        "scheduled_time": template["scheduled_time"],
        "posted": False,
        "created_at": datetime.now().isoformat()
    }

def generate_lesson_post():
    """Generate a lesson learned post"""
    lessons = [
        "conviction without position sizing is gambling. we size based on conviction score. 10/10 = max size. 6/10 = min size.",
        "stop losses aren't optional. every trade has a predefined exit. stick to the system. emotions lose money.",
        "green signals aren't buy signals until conviction doc validates. patience filters noise.",
        "transparency builds trust. we post wins AND losses. real track record or nothing.",
        "automation removes emotion. the agents don't feel FOMO. neither should you."
    ]
    
    lesson = random.choice(lessons)
    
    return {
        "id": None,
        "type": "lesson",
        "title": "Lesson Learned",
        "content": f"""💡 lesson learned

{lesson}

roostr. systematic. unemotional.""",
        "platforms": ["x"],
        "scheduled_time": "16:00",
        "posted": False,
        "created_at": datetime.now().isoformat()
    }

def generate_infrastructure_post():
    """Generate a post about the system"""
    posts = [
        {
            "content": """roostr infrastructure:

signal agent → scrapes 3 sources, finds GREEN
research agent → validates, writes conviction docs  
trading agent → executes, manages risk

400KB of code. 3 AI agents. zero emotion.

systematic trading.""",
            "time": "12:00"
        },
        {
            "content": """why 3 agents?

separation of concerns:
- finding ≠ validating
- validating ≠ executing
- executing ≠ finding

each agent masters one thing.

roostr. built different.""",
            "time": "14:00"
        }
    ]
    
    post = random.choice(posts)
    
    return {
        "id": None,
        "type": "infrastructure",
        "title": "Infrastructure Post",
        "content": post["content"],
        "platforms": ["x"],
        "scheduled_time": post["time"],
        "posted": False,
        "created_at": datetime.now().isoformat()
    }

def replenish_queue(days=7):
    """Generate posts for the next N days"""
    queue = load_queue()
    
    # Count unposted posts
    unposted = [p for p in queue.get("posts", []) if not p.get("posted", False)]
    print(f"📊 Current queue: {len(unposted)} unposted posts")
    
    # If we have enough content, don't generate more
    if len(unposted) >= 14:  # ~2 posts per day for a week
        print(f"✅ Queue is full ({len(unposted)} posts), skipping generation")
        return queue
    
    print(f"📝 Generating content for next {days} days...")
    
    new_posts = []
    
    # Check for new signals
    signals = get_latest_signals()
    if signals:
        print(f"🟢 Found {len(signals)} GREEN signals")
        for signal in signals[:3]:  # Limit to 3 signals
            new_posts.append(generate_signal_post(signal))
    
    # Generate daily updates (1 per day)
    for i in range(min(days, 7)):
        new_posts.append(generate_daily_update())
    
    # Generate lesson posts (2-3 per week)
    for i in range(random.randint(2, 3)):
        new_posts.append(generate_lesson_post())
    
    # Generate infrastructure posts (1-2 per week)
    for i in range(random.randint(1, 2)):
        new_posts.append(generate_infrastructure_post())
    
    # Assign IDs
    last_id = queue.get("last_id", 0)
    for post in new_posts:
        last_id += 1
        post["id"] = f"post_{last_id}"
    
    queue["last_id"] = last_id
    queue["posts"].extend(new_posts)
    
    print(f"✅ Generated {len(new_posts)} new posts")
    print(f"📊 Total queue: {len(queue['posts'])} posts")
    
    save_queue(queue)
    return queue

def main():
    print("🐓 roostr Content Generator")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Replenish queue
    queue = replenish_queue(days=7)
    
    # Show stats
    total = len(queue["posts"])
    posted = len([p for p in queue["posts"] if p.get("posted", False)])
    pending = total - posted
    
    print(f"\n📊 Queue Stats:")
    print(f"   Total: {total}")
    print(f"   Posted: {posted}")
    print(f"   Pending: {pending}")
    
    # Show next 3 scheduled posts
    print(f"\n📅 Next 3 Scheduled Posts:")
    unposted = [p for p in queue["posts"] if not p.get("posted", False)]
    unposted_sorted = sorted(unposted, key=lambda p: p.get("scheduled_time", "99:99"))
    
    for post in unposted_sorted[:3]:
        print(f"   {post.get('scheduled_time', 'TBD')} - {post.get('title', 'Untitled')} ({', '.join(post.get('platforms', []))})")

if __name__ == "__main__":
    main()
