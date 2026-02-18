#!/usr/bin/env python3
"""
Daily Signal Hunter - Systematic Opportunity Discovery
Scans all 7 data sources, auto-scores signals, generates daily report

Run: 7 AM daily via cron
Output: Telegram report + hunting-log.jsonl + watch-list.csv
"""

import json
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# Paths
BASE_DIR = Path(__file__).parent.parent
HUNTING_LOG = BASE_DIR / "hunting-log.jsonl"
WATCH_LIST = BASE_DIR / "watch-list.csv"
SIGNALS_DB = BASE_DIR / "signals-database.csv"

# Scoring weights (matches MARKET-ANALYSIS-FRAMEWORK.md)
SCORE_WEIGHTS = {
    'source_quality': 2.0,
    'catalyst_strength': 2.0,
    'fundamentals': 2.0,
    'technicals': 2.0,
    'social_validation': 2.0
}

def log_to_file(message):
    """Helper to log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def scan_yieldschool():
    """
    Scan Yieldschool Discord for new crypto signals
    Returns: list of {symbol, source, reason, score_components}
    """
    log_to_file("📊 Scanning Yieldschool...")
    
    # TODO: Implement Discord scraping when API available
    # For now, return placeholder
    signals = []
    
    # Example signal format:
    # {
    #     'symbol': 'TAO',
    #     'source': 'yieldschool-dan',
    #     'reason': 'Decentralized ML, category creation',
    #     'score_components': {
    #         'source_quality': 2.0,  # Dan = max quality
    #         'catalyst_strength': 1.0,
    #         'fundamentals': 1.8,
    #         'technicals': 1.0,
    #         'social_validation': 1.5
    #     }
    # }
    
    log_to_file(f"   Found {len(signals)} Yieldschool signals")
    return signals

def scan_dumb_money():
    """
    Scan Dumb Money Discord for social arbitrage signals
    Returns: list of signals with reaction counts
    """
    log_to_file("👍 Scanning Dumb Money...")
    
    # TODO: Discord scraping for emoji reactions
    signals = []
    
    log_to_file(f"   Found {len(signals)} Dumb Money signals")
    return signals

def scan_chart_fanatics():
    """
    Check Chart Fanatics for Riz's EURUSD setups
    Returns: list of forex signals
    """
    log_to_file("📈 Scanning Chart Fanatics...")
    
    # TODO: Discord scraping for Riz posts
    signals = []
    
    log_to_file(f"   Found {len(signals)} Chart Fanatics signals")
    return signals

def scan_reddit():
    """
    Scrape Reddit for trending stocks
    Uses existing reddit_scraper.py
    """
    log_to_file("🔍 Scanning Reddit...")
    
    signals = []
    
    try:
        # Import and run Reddit scraper
        reddit_scraper_path = BASE_DIR / 'scrapers' / 'reddit_scraper.py'
        
        if reddit_scraper_path.exists():
            result = subprocess.run(
                ['python3', str(reddit_scraper_path), '--json'],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(BASE_DIR / 'scrapers')
            )
            
            # Try to parse JSON output
            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, list):
                        for item in data[:10]:  # Top 10 signals
                            ticker = item.get('ticker', '').strip('$')
                            upvotes = item.get('upvotes', 0)
                            
                            if upvotes >= 100 and ticker:  # Minimum threshold
                                signals.append({
                                    'symbol': ticker,
                                    'source': 'reddit',
                                    'reason': f'{upvotes} upvotes: {item.get("title", "")[:50]}',
                                    'score_components': {
                                        'source_quality': 0.5,  # Reddit = lower quality
                                        'catalyst_strength': 0.5,
                                        'fundamentals': 0.0,  # Need to validate
                                        'technicals': 0.0,
                                        'social_validation': min(2.0, upvotes / 500)  # Scale by upvotes
                                    }
                                })
                except json.JSONDecodeError:
                    log_to_file(f"   ⚠️  Could not parse Reddit JSON output")
        else:
            log_to_file(f"   ⚠️  Reddit scraper not found at {reddit_scraper_path}")
            
    except Exception as e:
        log_to_file(f"   ⚠️  Reddit scan error: {e}")
    
    log_to_file(f"   Found {len(signals)} Reddit signals")
    return signals

def scan_dexscreener():
    """
    Query Dexscreener for high-volume new pairs
    """
    log_to_file("🔗 Scanning Dexscreener...")
    
    # TODO: Implement Dexscreener API integration
    signals = []
    
    log_to_file(f"   Found {len(signals)} Dexscreener signals")
    return signals

def scan_google_trends():
    """
    Check Google Trends for emerging search terms
    """
    log_to_file("📊 Scanning Google Trends...")
    
    # TODO: Implement Google Trends API
    signals = []
    
    log_to_file(f"   Found {len(signals)} Google Trends signals")
    return signals

def scan_dexter():
    """
    Query Dexter for fundamentally strong stocks
    """
    log_to_file("📚 Scanning Dexter (SEC filings)...")
    
    # TODO: Query Dexter for earnings beats, insider buying
    signals = []
    
    log_to_file(f"   Found {len(signals)} Dexter signals")
    return signals

def add_manual_test_signals():
    """
    Add manual test signals to demonstrate pipeline
    Remove this function once real data sources are connected
    """
    log_to_file("🧪 Adding manual test signals...")
    
    signals = []
    
    # Example GREEN signal (high conviction)
    signals.append({
        'symbol': 'TEST-GREEN',
        'source': 'manual-test',
        'reason': 'Test signal: Multiple catalysts, strong fundamentals',
        'score_components': {
            'source_quality': 2.0,  # Max quality (simulating Yieldschool Dan)
            'catalyst_strength': 1.8,  # Strong catalyst
            'fundamentals': 1.9,  # Excellent fundamentals
            'technicals': 1.5,  # Good technical setup
            'social_validation': 1.5  # Strong social validation
        }
    })
    
    # Example YELLOW signal (watch)
    signals.append({
        'symbol': 'TEST-YELLOW',
        'source': 'manual-test',
        'reason': 'Test signal: Emerging opportunity, needs validation',
        'score_components': {
            'source_quality': 1.0,  # Medium quality
            'catalyst_strength': 1.2,  # Moderate catalyst
            'fundamentals': 1.0,  # Decent fundamentals
            'technicals': 0.8,  # Neutral technicals
            'social_validation': 0.8  # Some social validation
        }
    })
    
    # Example RED signal (avoid)
    signals.append({
        'symbol': 'TEST-RED',
        'source': 'manual-test',
        'reason': 'Test signal: Weak setup, insufficient conviction',
        'score_components': {
            'source_quality': 0.5,  # Low quality
            'catalyst_strength': 0.3,  # Weak catalyst
            'fundamentals': 0.2,  # Poor fundamentals
            'technicals': 0.5,  # Weak technicals
            'social_validation': 0.4  # Minimal validation
        }
    })
    
    log_to_file(f"   Added {len(signals)} test signals")
    return signals

def calculate_conviction_score(components):
    """
    Calculate 0-10 conviction score from components
    Formula from MARKET-ANALYSIS-FRAMEWORK.md
    
    Each component is 0-2.0, so total is 0-10.0
    """
    total = sum(components.values())
    return round(total, 1)

def classify_signal(score):
    """Classify signal by conviction score"""
    if score >= 8.0:
        return "GREEN"
    elif score >= 7.0:
        return "YELLOW+"
    elif score >= 5.0:
        return "YELLOW"
    else:
        return "RED"

def log_signal_to_hunting_log(signal, conviction_score, classification):
    """Append signal to hunting-log.jsonl"""
    entry = {
        'timestamp': datetime.now().isoformat(),
        'symbol': signal['symbol'],
        'source': signal['source'],
        'reason': signal['reason'],
        'score': conviction_score,
        'classification': classification,
        'components': signal['score_components']
    }
    
    with open(HUNTING_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def update_watch_list(signal, conviction_score):
    """Add/update YELLOW signals in watch-list.csv"""
    # Read existing watch list
    watch_list = []
    if WATCH_LIST.exists():
        with open(WATCH_LIST, 'r') as f:
            reader = csv.DictReader(f)
            watch_list = list(reader)
    
    # Check if symbol already exists
    found = False
    for item in watch_list:
        if item['symbol'] == signal['symbol']:
            # Update existing entry
            item['last_seen'] = datetime.now().isoformat()
            item['score'] = conviction_score
            item['source'] = signal['source']
            item['reason'] = signal['reason']
            found = True
            break
    
    if not found:
        # Add new entry
        watch_list.append({
            'symbol': signal['symbol'],
            'source': signal['source'],
            'score': conviction_score,
            'first_seen': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat(),
            'reason': signal['reason'],
            'status': 'watching'
        })
    
    # Write updated watch list
    with open(WATCH_LIST, 'w', newline='') as f:
        fieldnames = ['symbol', 'source', 'score', 'first_seen', 'last_seen', 'reason', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(watch_list)

def add_to_signals_database(signal, conviction_score, classification):
    """Add GREEN signals to signals-database.csv for deployment consideration"""
    if classification != "GREEN":
        return
    
    fieldnames = ['ticker', 'source', 'conviction', 'date_found', 'catalyst', 'status', 'entry_clarity']
    
    # Check if already in database
    existing = []
    if SIGNALS_DB.exists():
        with open(SIGNALS_DB, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only keep fields that match our schema
                existing.append({k: row.get(k, '') for k in fieldnames})
    
    # Check for duplicates
    for item in existing:
        if item.get('ticker') == signal['symbol']:
            log_to_file(f"   Signal {signal['symbol']} already in database")
            return
    
    # Add new signal
    new_entry = {
        'ticker': signal['symbol'],
        'source': signal['source'],
        'conviction': conviction_score,
        'date_found': datetime.now().strftime('%Y-%m-%d'),
        'catalyst': signal['reason'][:100],  # Truncate
        'status': 'new',
        'entry_clarity': 5.0  # Default, will be refined
    }
    existing.append(new_entry)
    
    # Write updated database
    with open(SIGNALS_DB, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    
    log_to_file(f"   ✅ Added {signal['symbol']} to signals database (GREEN)")

def generate_telegram_report(all_signals, green_count, yellow_count, red_count):
    """Generate Telegram report of today's hunt"""
    
    report = f"""🐓 **Daily Signal Hunt Report**
{datetime.now().strftime('%Y-%m-%d %H:%M EST')}

📊 **Summary:**
Total Scanned: {len(all_signals)}
🟢 GREEN (≥8.0): {green_count}
🟡 YELLOW (5.0-7.9): {yellow_count}
🔴 RED (<5.0): {red_count}

"""

    # Add GREEN signals (high priority)
    green_signals = [s for s in all_signals if s['classification'] == 'GREEN']
    if green_signals:
        report += "**🟢 GREEN Signals (Deploy):**\n"
        for sig in green_signals:
            report += f"• **{sig['symbol']}** ({sig['score']}/10)\n"
            report += f"  Source: {sig['source']}\n"
            report += f"  {sig['reason']}\n\n"
    
    # Add YELLOW+ signals (strong watch)
    yellow_plus = [s for s in all_signals if s['classification'] == 'YELLOW+']
    if yellow_plus:
        report += "**🟡 YELLOW+ Signals (Strong Watch):**\n"
        for sig in yellow_plus:
            report += f"• {sig['symbol']} ({sig['score']}/10) - {sig['source']}\n"
    
    # Watch list update
    if WATCH_LIST.exists():
        with open(WATCH_LIST, 'r') as f:
            reader = csv.DictReader(f)
            watch_count = len(list(reader))
        report += f"\n📋 **Watch List:** {watch_count} symbols tracking\n"
    
    report += f"\n🔍 **Hunting Log:** {HUNTING_LOG}\n"
    report += f"📊 **Full Framework:** roostr-research/trading/MARKET-ANALYSIS-FRAMEWORK.md"
    
    return report

def send_telegram_report(report):
    """Send report to Telegram"""
    log_to_file("📱 Sending Telegram report...")
    
    # Use OpenClaw message tool (would be called by system)
    # For now, just print and save to file
    report_file = BASE_DIR / f"daily-hunt-{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    log_to_file(f"   Report saved: {report_file}")
    print("\n" + "="*60)
    print(report)
    print("="*60 + "\n")

def main():
    """Main hunting pipeline"""
    log_to_file("🐓 Starting Daily Signal Hunt")
    log_to_file("="*60)
    
    # Scan all 7 sources
    all_signals = []
    all_signals.extend(scan_yieldschool())
    all_signals.extend(scan_dumb_money())
    all_signals.extend(scan_chart_fanatics())
    all_signals.extend(scan_reddit())
    all_signals.extend(scan_dexscreener())
    all_signals.extend(scan_google_trends())
    all_signals.extend(scan_dexter())
    
    # Add test signals to demonstrate pipeline (remove once real sources are connected)
    all_signals.extend(add_manual_test_signals())
    
    # Score and classify each signal
    processed_signals = []
    green_count = yellow_count = red_count = 0
    
    for signal in all_signals:
        # Calculate conviction score
        conviction_score = calculate_conviction_score(signal['score_components'])
        classification = classify_signal(conviction_score)
        
        # Count by classification
        if classification == "GREEN":
            green_count += 1
        elif classification.startswith("YELLOW"):
            yellow_count += 1
        else:
            red_count += 1
        
        # Log to hunting log
        log_signal_to_hunting_log(signal, conviction_score, classification)
        
        # Add to watch list if YELLOW
        if classification.startswith("YELLOW"):
            update_watch_list(signal, conviction_score)
        
        # Add to signals database if GREEN
        add_to_signals_database(signal, conviction_score, classification)
        
        # Store for report
        processed_signals.append({
            'symbol': signal['symbol'],
            'source': signal['source'],
            'reason': signal['reason'],
            'score': conviction_score,
            'classification': classification
        })
        
        log_to_file(f"   {classification:8} {signal['symbol']:6} {conviction_score}/10 - {signal['source']}")
    
    log_to_file("="*60)
    log_to_file(f"✅ Hunt complete: {len(all_signals)} signals processed")
    log_to_file(f"   🟢 GREEN: {green_count}")
    log_to_file(f"   🟡 YELLOW: {yellow_count}")
    log_to_file(f"   🔴 RED: {red_count}")
    
    # Generate and send report
    report = generate_telegram_report(processed_signals, green_count, yellow_count, red_count)
    send_telegram_report(report)
    
    return 0

if __name__ == "__main__":
    exit(main())
