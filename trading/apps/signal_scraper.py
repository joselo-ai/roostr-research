#!/usr/bin/env python3
"""
Signal Scraper - Hunt new trading setups
Checks Yieldschool, Dumb Money, Chart Fanatics for fresh signals
Runs every 6 hours: 6 AM, 12 PM, 6 PM, 12 AM EST
"""

import json
import re
from datetime import datetime, timedelta
import os

# Activity logging
import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/command-center')
from activity_logger import log_trading, log_automation


SIGNALS_DB = "/Users/agentjoselo/.openclaw/workspace/trading/signals-database.csv"
DISCORD_DATA = "/Users/agentjoselo/.openclaw/workspace/discord-scraping"
NEW_SIGNALS_OUT = "/Users/agentjoselo/.openclaw/workspace/trading/new-signals.txt"

# Known sources to check
SOURCES = {
    "yieldschool": {
        "path": f"{DISCORD_DATA}/yieldschool-latest.json",
        "keywords": ["entry", "buy", "long", "accumulate", "bullish", "gem"]
    },
    "dumbmoney": {
        "path": f"{DISCORD_DATA}/dumbmoney-latest.json",
        "keywords": ["calls", "entry", "buy", "PT", "target", "play"]
    },
    "chartfanatics": {
        "path": f"{DISCORD_DATA}/chartfanatics-latest.json",
        "keywords": ["setup", "entry", "TP", "SL", "long", "short"]
    },
    "reddit": {
        "enabled": True,
        "script": "/Users/agentjoselo/.openclaw/workspace/trading/scrapers/reddit_scraper.py"
    }
}

def load_existing_signals():
    """Load existing signals to avoid duplicates"""
    if not os.path.exists(SIGNALS_DB):
        return set()
    
    signals = set()
    with open(SIGNALS_DB, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('Ticker'):
                ticker = line.split(',')[0].strip()
                signals.add(ticker)
    
    return signals

def extract_tickers(text):
    """Extract potential tickers from text"""
    # Match $TICKER or TICKER: patterns
    tickers = set()
    
    # $TICKER format
    matches = re.findall(r'\$([A-Z]{2,5})\b', text)
    tickers.update(matches)
    
    # TICKER: or TICKER - format
    matches = re.findall(r'\b([A-Z]{2,5})[\s:]-', text)
    tickers.update(matches)
    
    # Common words to exclude
    exclude = {'THE', 'AND', 'FOR', 'THIS', 'THAT', 'WITH', 'FROM', 'HAVE', 
               'WILL', 'WHEN', 'WHERE', 'WHAT', 'THEY', 'BEEN', 'WERE', 'JUST',
               'MORE', 'SOME', 'NEED', 'WANT', 'MUCH', 'WELL', 'ALSO', 'ONLY'}
    
    return [t for t in tickers if t not in exclude]

def check_source(source_name, config):
    """Check a source for new signals"""
    log_automation("Signal scraper", {"new_signals": len(new_signals) if 'new_signals' in locals() else 0})
    path = config["path"]
    keywords = config["keywords"]
    
    if not os.path.exists(path):
        return []
    
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except:
        return []
    
    new_signals = []
    cutoff = datetime.now() - timedelta(hours=24)
    
    # Process messages
    messages = data.get("messages", [])
    for msg in messages:
        timestamp = msg.get("timestamp", "")
        content = msg.get("content", "")
        
        # Check if recent
        try:
            msg_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            if msg_time < cutoff:
                continue
        except:
            continue
        
        # Check for keywords
        content_lower = content.lower()
        has_keyword = any(kw in content_lower for kw in keywords)
        
        if not has_keyword:
            continue
        
        # Extract tickers
        tickers = extract_tickers(content)
        
        for ticker in tickers:
            new_signals.append({
                "ticker": ticker,
                "source": source_name,
                "content": content[:200],
                "timestamp": timestamp
            })
    
    return new_signals

def filter_new_signals(signals, existing):
    """Filter out signals we already have"""
    return [s for s in signals if s["ticker"] not in existing]

def format_signal_report(signals):
    """Format new signals as report"""
    if not signals:
        return "✅ No new signals found in last 24h"
    
    report = f"🔍 **New Signals Found** ({len(signals)})\n"
    report += f"Scanned: {datetime.now().strftime('%b %d, %Y %I:%M %p EST')}\n\n"
    
    by_source = {}
    for sig in signals:
        source = sig["source"]
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(sig)
    
    for source, sigs in by_source.items():
        report += f"**{source.upper()}** ({len(sigs)} signals):\n"
        for sig in sigs:
            report += f"• ${sig['ticker']}\n"
            report += f"  {sig['content'][:150]}...\n\n"
    
    report += "\n🎯 Next step: Manual review → Conviction doc → GREEN/YELLOW/RED\n"
    report += "Dashboard: https://joselo-ai.github.io/roostr-research/trading/dashboard.html"
    
    return report

def run_reddit_scraper():
    """Run Reddit scraper as separate process"""
    import subprocess
    
    reddit_script = "/Users/agentjoselo/.openclaw/workspace/trading/scrapers/reddit_scraper.py"
    
    if not os.path.exists(reddit_script):
        print("⚠️  Reddit scraper not found")
        return []
    
    try:
        print("🔍 Running Reddit scraper...")
        result = subprocess.run(
            ['python3', reddit_script],
            capture_output=True,
            text=True,
            timeout=300  # 5 min timeout
        )
        
        if result.returncode == 0:
            # Parse output for signal count
            output = result.stdout
            if "Total signals extracted" in output:
                # Extract signal count from output
                import re
                match = re.search(r'Total signals extracted: (\d+)', output)
                if match:
                    count = int(match.group(1))
                    print(f"   ✅ Reddit: {count} signals processed")
                    
                    # Log to command center
                    log_trading("Reddit scraper", {
                        "signals": count,
                        "status": "success"
                    })
        else:
            print(f"   ⚠️  Reddit scraper error: {result.stderr[:200]}")
        
    except subprocess.TimeoutExpired:
        print("   ⏰ Reddit scraper timeout (>5min)")
    except Exception as e:
        print(f"   ❌ Reddit scraper failed: {e}")

def main():
    print(f"🐓 Signal Scraper - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load existing signals
    existing = load_existing_signals()
    print(f"📊 Tracking {len(existing)} existing signals")
    
    # Check Reddit first (if enabled)
    if SOURCES.get("reddit", {}).get("enabled"):
        run_reddit_scraper()
        print("")
    
    # Check all Discord sources
    all_new = []
    for source_name, config in SOURCES.items():
        # Skip Reddit (already ran)
        if source_name == "reddit":
            continue
            
        print(f"🔍 Checking {source_name}...")
        signals = check_source(source_name, config)
        print(f"   Found {len(signals)} potential signals")
        all_new.extend(signals)
    
    # Filter for genuinely new
    new_signals = filter_new_signals(all_new, existing)
    print(f"\n🎯 {len(new_signals)} NEW signals (not in database)")
    
    # Generate report
    report = format_signal_report(new_signals)
    
    # Write to file
    with open(NEW_SIGNALS_OUT, 'w') as f:
        f.write(report)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    print(f"\n✅ Report saved to {NEW_SIGNALS_OUT}")
    
    # Log activity
    log_automation("Signal scraper", {
        "new_signals": len(new_signals),
        "sources": len(SOURCES)
    })
    
    return 0

if __name__ == "__main__":
    exit(main())
