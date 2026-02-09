#!/usr/bin/env python3
"""
Dumb Money Deep Researcher
Actively scrapes Dumb Money Discord for social arbitrage opportunities
Generates conviction docs for high-signal stocks
Runs every 6 hours
"""

import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import os

DUMBMONEY_DATA = "/Users/agentjoselo/.openclaw/workspace/discord-scraping/dumbmoney"
SIGNALS_OUT = "/Users/agentjoselo/.openclaw/workspace/trading/dumbmoney-signals.json"
CONVICTION_DOCS_DIR = "/Users/agentjoselo/.openclaw/workspace/trading/conviction-docs"

# Reaction thresholds for conviction levels
REACTION_THRESHOLDS = {
    "GREEN": 25,   # 25+ fire/rocket reactions = strong conviction
    "YELLOW": 15,  # 15-24 reactions = moderate interest
    "RED": 5       # <5 reactions = noise
}

def load_dumbmoney_messages():
    """Load recent Dumb Money Discord messages"""
    messages = []
    
    # Check for latest scrape file
    if not os.path.exists(DUMBMONEY_DATA):
        print(f"⚠️ Dumb Money data directory not found: {DUMBMONEY_DATA}")
        return messages
    
    # Load all JSON files from last 7 days
    cutoff = datetime.now() - timedelta(days=7)
    
    for filename in os.listdir(DUMBMONEY_DATA):
        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(DUMBMONEY_DATA, filename)
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            for msg in data.get("messages", []):
                try:
                    msg_time = datetime.fromisoformat(msg.get("timestamp", "").replace('Z', '+00:00'))
                    if msg_time >= cutoff:
                        messages.append(msg)
                except:
                    continue
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    return messages

def extract_ticker_mentions(messages):
    """Extract tickers with reaction counts"""
    ticker_data = defaultdict(lambda: {
        "mentions": 0,
        "reactions": defaultdict(int),
        "total_reactions": 0,
        "messages": [],
        "first_seen": None,
        "latest_seen": None
    })
    
    for msg in messages:
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", "")
        reactions = msg.get("reactions", [])
        
        # Extract tickers
        tickers = set()
        # $TICKER format
        tickers.update(re.findall(r'\$([A-Z]{2,5})\b', content))
        # TICKER: format
        tickers.update(re.findall(r'\b([A-Z]{2,5})[\s:]-', content))
        
        # Exclude common words
        exclude = {'THE', 'AND', 'FOR', 'THIS', 'THAT', 'WITH', 'FROM', 
                   'WILL', 'BEEN', 'HAVE', 'WHAT', 'WHEN', 'THEY', 'CALLS',
                   'PUTS', 'PLAY', 'LONG', 'SHORT', 'BULL', 'BEAR'}
        tickers = {t for t in tickers if t not in exclude}
        
        for ticker in tickers:
            ticker_data[ticker]["mentions"] += 1
            ticker_data[ticker]["messages"].append({
                "content": content[:300],
                "timestamp": timestamp,
                "reactions": reactions
            })
            
            # Track timestamps
            if not ticker_data[ticker]["first_seen"]:
                ticker_data[ticker]["first_seen"] = timestamp
            ticker_data[ticker]["latest_seen"] = timestamp
            
            # Count reactions
            for reaction in reactions:
                emoji = reaction.get("emoji", {}).get("name", "")
                count = reaction.get("count", 0)
                ticker_data[ticker]["reactions"][emoji] += count
                ticker_data[ticker]["total_reactions"] += count
    
    return dict(ticker_data)

def calculate_conviction(ticker_data):
    """Calculate conviction level based on reactions + mentions"""
    conviction_signals = []
    
    for ticker, data in ticker_data.items():
        # Calculate conviction score
        fire_reactions = data["reactions"].get("🔥", 0)
        rocket_reactions = data["reactions"].get("🚀", 0)
        thumbs_reactions = data["reactions"].get("👍", 0)
        
        total_high_conviction = fire_reactions + rocket_reactions
        total_reactions = data["total_reactions"]
        mentions = data["mentions"]
        
        # Conviction level
        if total_high_conviction >= REACTION_THRESHOLDS["GREEN"]:
            conviction = "GREEN"
        elif total_high_conviction >= REACTION_THRESHOLDS["YELLOW"]:
            conviction = "YELLOW"
        else:
            conviction = "RED"
        
        # Skip RED signals
        if conviction == "RED":
            continue
        
        # Build signal
        signal = {
            "ticker": ticker,
            "conviction": conviction,
            "score": total_high_conviction,
            "fire_reactions": fire_reactions,
            "rocket_reactions": rocket_reactions,
            "thumbs_reactions": thumbs_reactions,
            "total_reactions": total_reactions,
            "mentions": mentions,
            "first_seen": data["first_seen"],
            "latest_seen": data["latest_seen"],
            "sample_messages": data["messages"][:3]  # Top 3 messages
        }
        
        conviction_signals.append(signal)
    
    # Sort by conviction score (fire + rocket)
    conviction_signals.sort(key=lambda x: x["score"], reverse=True)
    
    return conviction_signals

def generate_conviction_doc(signal):
    """Generate conviction document for a signal"""
    ticker = signal["ticker"]
    doc = f"""# ${ticker} - Social Arbitrage Conviction Doc
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Source:** Dumb Money Discord  
**Conviction:** {signal['conviction']} ({signal['score']}/10 community score)

---

## 📊 Community Metrics

**Reactions:**
- 🔥 Fire: {signal['fire_reactions']}
- 🚀 Rocket: {signal['rocket_reactions']}
- 👍 Thumbs: {signal['thumbs_reactions']}
- **Total:** {signal['total_reactions']}

**Activity:**
- Mentions: {signal['mentions']}
- First Seen: {signal['first_seen']}
- Latest: {signal['latest_seen']}

---

## 💬 Sample Messages

"""
    
    for i, msg in enumerate(signal["sample_messages"], 1):
        doc += f"### Message {i}:\n"
        doc += f"```\n{msg['content']}\n```\n"
        doc += f"Reactions: {msg.get('reactions', [])}\n\n"
    
    doc += f"""
---

## 🎯 Social Arbitrage Thesis

**Hypothesis:** Community conviction precedes market movement

**Validation Steps:**
1. ⬜ Check Google Trends (search volume spike?)
2. ⬜ Review company fundamentals (earnings, products)
3. ⬜ Verify social media traction (Twitter, TikTok)
4. ⬜ Check insider activity (buying/selling?)
5. ⬜ Confirm NOT already mainstream (CNBC/WSJ coverage = too late)

**Entry Criteria:**
- Community conviction: ✅ {signal['conviction']}
- Fundamental catalyst: ⬜ (manual research)
- Social confirmation: ⬜ (Google Trends + Twitter)
- Entry price: ⬜ (find support level)
- Stop loss: ⬜ (2% max risk)

**Risk:**
- Max position size: $10-15k
- Stop loss: 2% below entry
- Max loss: $200-300

---

## 📝 Research Notes

_Add manual research here_

**Company:** ${ticker}  
**Industry:**  
**Market Cap:**  
**Recent News:**  
**Catalyst:**  

**Decision:**
⬜ GREEN - Deploy capital  
⬜ YELLOW - Watch for catalyst  
⬜ RED - Pass (no edge)

---

**Next Steps:**
1. Complete validation checklist
2. If GREEN → Write entry plan
3. If YELLOW → Monitor for 7 days
4. If RED → Archive and move on
"""
    
    return doc

def main():
    print(f"🔍 Dumb Money Deep Researcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load messages
    print("Loading Dumb Money messages...")
    messages = load_dumbmoney_messages()
    print(f"✅ Loaded {len(messages)} messages from last 7 days\n")
    
    # Extract tickers
    print("Extracting ticker mentions...")
    ticker_data = extract_ticker_mentions(messages)
    print(f"✅ Found {len(ticker_data)} unique tickers\n")
    
    # Calculate conviction
    print("Calculating conviction levels...")
    signals = calculate_conviction(ticker_data)
    print(f"✅ {len(signals)} signals with GREEN/YELLOW conviction\n")
    
    # Save signals
    with open(SIGNALS_OUT, 'w') as f:
        json.dump(signals, f, indent=2)
    
    # Generate conviction docs for GREEN signals
    os.makedirs(CONVICTION_DOCS_DIR, exist_ok=True)
    
    green_count = 0
    yellow_count = 0
    
    for signal in signals:
        ticker = signal["ticker"]
        conviction = signal["conviction"]
        
        if conviction == "GREEN":
            # Generate full conviction doc
            doc = generate_conviction_doc(signal)
            doc_path = os.path.join(CONVICTION_DOCS_DIR, f"{ticker}-social-arb.md")
            with open(doc_path, 'w') as f:
                f.write(doc)
            print(f"🟢 ${ticker}: {signal['score']} reactions (GREEN) - Doc created")
            green_count += 1
        elif conviction == "YELLOW":
            print(f"🟡 ${ticker}: {signal['score']} reactions (YELLOW)")
            yellow_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   GREEN signals: {green_count} (conviction docs created)")
    print(f"   YELLOW signals: {yellow_count} (watch list)")
    print(f"\n💾 Output:")
    print(f"   Signals: {SIGNALS_OUT}")
    print(f"   Docs: {CONVICTION_DOCS_DIR}/")
    
    return 0

if __name__ == "__main__":
    exit(main())
