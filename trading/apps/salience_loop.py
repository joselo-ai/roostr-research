#!/usr/bin/env python3
"""
Salience-Based Self-Learning Loop

TRADE → JOURNAL → EXTRACT LEARNING → APPLY

Salience Score (0-1):
- Trade won with correct reasoning: +0.1
- Trade lost despite correct reasoning: -0.1
- Time decay: -0.02/week
- Manual boost/penalty from G

Knowledge Tiers:
- < 0.2: Archive to memory/failed-patterns.md (don't repeat)
- 0.2-0.8: Active in learnings.md (reference during deliberation)
- > 0.8: Promote to TRADING_DOCS (proven edge, cite in conviction docs)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Paths
WORKSPACE = Path("/Users/agentjoselo/.openclaw/workspace/trading")
PERFORMANCE_JOURNAL = WORKSPACE / "performance-journal.jsonl"
LEARNINGS_FILE = WORKSPACE / "learnings.md"
FAILED_PATTERNS = WORKSPACE / "memory/failed-patterns.md"
TRADING_DOCS = WORKSPACE / "TRADING_DOCS"
SALIENCE_DB = WORKSPACE / "salience-database.json"

# Thresholds
ARCHIVE_THRESHOLD = 0.2
PROMOTE_THRESHOLD = 0.8
WEEKLY_DECAY = 0.02


def load_salience_db():
    """Load salience scores for all learnings."""
    if SALIENCE_DB.exists():
        with open(SALIENCE_DB) as f:
            return json.load(f)
    return {}


def save_salience_db(db):
    """Save salience database."""
    with open(SALIENCE_DB, "w") as f:
        json.dump(db, f, indent=2)


def extract_learning_from_trade(trade):
    """
    Extract a learning from a closed trade.
    
    Returns:
    {
        "id": "learning_001",
        "pattern": "Brief description of what we learned",
        "evidence": "Trade details supporting this learning",
        "initial_salience": 0.5,
        "created": "2026-02-15",
        "last_updated": "2026-02-15"
    }
    """
    
    # Calculate initial salience based on trade outcome
    pnl = trade.get("pnl", 0)
    win = pnl > 0
    
    # Extract reasoning quality from deliberation
    conviction = trade.get("conviction", 5.0)
    reasoning = trade.get("reasoning", "")
    
    # Initial salience calculation
    if win and conviction >= 8.0:
        initial_salience = 0.6  # Good win with high conviction
    elif win and conviction < 8.0:
        initial_salience = 0.4  # Lucky win, lower confidence
    elif not win and conviction >= 8.0:
        initial_salience = 0.3  # Lost despite good reasoning (market risk)
    else:
        initial_salience = 0.1  # Low conviction loss (bad signal)
    
    # Generate learning pattern
    if win:
        pattern = f"✅ {trade['ticker']} strategy worked: {reasoning[:100]}"
    else:
        pattern = f"❌ {trade['ticker']} strategy failed: {reasoning[:100]}"
    
    learning = {
        "id": f"learning_{trade['ticker']}_{trade.get('entry_date', 'unknown')}",
        "ticker": trade.get("ticker"),
        "pattern": pattern,
        "evidence": {
            "entry": trade.get("entry_price"),
            "exit": trade.get("current_price"),
            "pnl": pnl,
            "conviction": conviction,
            "duration": trade.get("duration_days", 0)
        },
        "initial_salience": initial_salience,
        "current_salience": initial_salience,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    return learning


def apply_time_decay(salience_db):
    """Apply weekly time decay to all learnings."""
    now = datetime.now()
    
    for learning_id, data in salience_db.items():
        last_updated = datetime.fromisoformat(data["last_updated"])
        weeks_elapsed = (now - last_updated).days / 7
        
        if weeks_elapsed >= 1:
            decay = WEEKLY_DECAY * int(weeks_elapsed)
            data["current_salience"] = max(0, data["current_salience"] - decay)
            data["last_updated"] = now.strftime("%Y-%m-%d")
            
            print(f"   ⏰ Decayed {learning_id}: {data['current_salience']:.2f} (-{decay:.2f})")
    
    return salience_db


def organize_learnings(salience_db):
    """
    Organize learnings into tiers based on salience.
    
    < 0.2: Archive to failed-patterns.md
    0.2-0.8: Keep in learnings.md (active)
    > 0.8: Promote to TRADING_DOCS (proven)
    """
    
    archived = []
    active = []
    promoted = []
    
    for learning_id, data in salience_db.items():
        salience = data["current_salience"]
        
        if salience < ARCHIVE_THRESHOLD:
            archived.append(data)
        elif salience > PROMOTE_THRESHOLD:
            promoted.append(data)
        else:
            active.append(data)
    
    # Write to files
    write_failed_patterns(archived)
    write_active_learnings(active)
    write_promoted_docs(promoted)
    
    print(f"\n📊 Learning Organization:")
    print(f"   📦 Archived: {len(archived)} (salience < 0.2)")
    print(f"   📝 Active: {len(active)} (salience 0.2-0.8)")
    print(f"   ⭐ Promoted: {len(promoted)} (salience > 0.8)")
    
    return {"archived": archived, "active": active, "promoted": promoted}


def write_failed_patterns(patterns):
    """Write low-salience patterns to archive."""
    (WORKSPACE / "memory").mkdir(exist_ok=True)
    
    content = f"# Failed Patterns (Salience < 0.2)\n\n"
    content += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    content += "These patterns had low salience and have been archived. Avoid repeating.\n\n"
    
    for p in sorted(patterns, key=lambda x: x["current_salience"]):
        content += f"## {p['ticker']} ({p['created']})\n"
        content += f"**Salience:** {p['current_salience']:.2f}\n\n"
        content += f"{p['pattern']}\n\n"
        content += f"**Evidence:** {json.dumps(p['evidence'], indent=2)}\n\n"
        content += "---\n\n"
    
    with open(FAILED_PATTERNS, "w") as f:
        f.write(content)


def write_active_learnings(learnings):
    """Write mid-salience learnings to active file."""
    content = f"# Active Learnings (Salience 0.2-0.8)\n\n"
    content += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    content += "These patterns are actively referenced during trade deliberation.\n\n"
    
    for l in sorted(learnings, key=lambda x: -x["current_salience"]):
        content += f"## {l['ticker']} ({l['created']}) - Salience: {l['current_salience']:.2f}\n\n"
        content += f"{l['pattern']}\n\n"
        content += f"**Evidence:** {json.dumps(l['evidence'], indent=2)}\n\n"
        content += "---\n\n"
    
    with open(LEARNINGS_FILE, "w") as f:
        f.write(content)


def write_promoted_docs(proven):
    """Write high-salience patterns to TRADING_DOCS."""
    TRADING_DOCS.mkdir(exist_ok=True)
    
    for p in proven:
        filename = TRADING_DOCS / f"{p['id']}.md"
        
        content = f"# {p['ticker']} - Proven Pattern\n\n"
        content += f"**Salience:** {p['current_salience']:.2f} (PROMOTED)\n\n"
        content += f"**Created:** {p['created']}\n"
        content += f"**Last Updated:** {p['last_updated']}\n\n"
        content += f"## Pattern\n\n{p['pattern']}\n\n"
        content += f"## Evidence\n\n```json\n{json.dumps(p['evidence'], indent=2)}\n```\n\n"
        content += "**Status:** Cite this in future conviction documents for similar setups.\n"
        
        with open(filename, "w") as f:
            f.write(content)


def run_salience_loop():
    """Main salience loop: extract learnings, apply decay, organize."""
    
    print("🧠 Running Salience Loop")
    print("="*60)
    
    # Load existing salience database
    salience_db = load_salience_db()
    print(f"📊 Loaded {len(salience_db)} existing learnings")
    
    # Read performance journal for new closed trades
    if not PERFORMANCE_JOURNAL.exists():
        print("⚠️  No performance journal found")
        return
    
    with open(PERFORMANCE_JOURNAL) as f:
        trades = [json.loads(line) for line in f if line.strip()]
    
    # Find recently closed trades (not already processed)
    new_learnings = 0
    for trade in trades:
        if trade.get("status") == "CLOSED":
            learning_id = f"learning_{trade['ticker']}_{trade.get('entry_date', 'unknown')}"
            
            if learning_id not in salience_db:
                # Extract learning from this trade
                learning = extract_learning_from_trade(trade)
                salience_db[learning_id] = learning
                new_learnings += 1
                print(f"   ✅ Extracted: {learning['pattern'][:60]}... (salience: {learning['initial_salience']:.2f})")
    
    print(f"\n📈 Extracted {new_learnings} new learnings")
    
    # Apply time decay to all learnings
    print(f"\n⏰ Applying time decay...")
    salience_db = apply_time_decay(salience_db)
    
    # Organize into tiers
    print(f"\n📁 Organizing learnings...")
    organize_learnings(salience_db)
    
    # Save updated database
    save_salience_db(salience_db)
    print(f"\n💾 Salience database saved")
    
    print("\n✅ Salience loop complete\n")


if __name__ == "__main__":
    run_salience_loop()
