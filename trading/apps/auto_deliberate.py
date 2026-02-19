#!/usr/bin/env python3
"""
Auto-Deliberate Green Signals
Reads signals-database.csv and runs 18-agent deliberation on GREEN signals (≥7.0)

Usage:
    python3 auto_deliberate.py [--threshold 7.0] [--limit 3]
"""

import csv
import sys
import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
SIGNALS_DB = BASE_DIR / "signals-database.csv"
AGENTS_DIR = BASE_DIR / "agents"
DELIBERATIONS_DIR = BASE_DIR / "deliberations"
VENV_PYTHON = BASE_DIR / "venv" / "bin" / "python3"

def load_green_signals(threshold=7.0):
    """Load GREEN signals from signals-database.csv"""
    
    if not SIGNALS_DB.exists():
        print(f"❌ Signals database not found: {SIGNALS_DB}")
        return []
    
    signals = []
    with open(SIGNALS_DB, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                conviction = float(row.get('conviction', 0))
                if conviction >= threshold:
                    signals.append({
                        'ticker': row.get('ticker', '').upper(),
                        'source': row.get('source', ''),
                        'conviction': conviction,
                        'catalyst': row.get('catalyst', ''),
                        'status': row.get('status', 'new')
                    })
            except ValueError:
                continue
    
    return signals

def run_18_agent_deliberation(ticker):
    """Run 18-agent system on ticker"""
    
    print(f"\n{'='*80}")
    print(f"🤖 Running 18-Agent Deliberation: {ticker}")
    print(f"{'='*80}\n")
    
    legendary_v2 = AGENTS_DIR / "legendary_investors_v2.py"
    
    if not legendary_v2.exists():
        print(f"❌ Agent script not found: {legendary_v2}")
        return None
    
    try:
        result = subprocess.run(
            [str(VENV_PYTHON), str(legendary_v2), ticker],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(AGENTS_DIR)
        )
        
        if result.returncode == 0:
            print(result.stdout)
            return result.stdout
        else:
            print(f"❌ Deliberation failed: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"⚠️  Deliberation timed out after 120s")
        return None
    except Exception as e:
        print(f"❌ Error running deliberation: {e}")
        return None

def save_deliberation_log(ticker, conviction, output):
    """Save deliberation to log file"""
    
    DELIBERATIONS_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = DELIBERATIONS_DIR / f"{timestamp}_{ticker}_{conviction}.txt"
    
    with open(log_file, 'w') as f:
        f.write(f"Ticker: {ticker}\n")
        f.write(f"Conviction: {conviction}/10\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("="*80 + "\n\n")
        f.write(output)
    
    print(f"\n📄 Deliberation saved: {log_file}")
    return log_file

def main():
    """Main pipeline"""
    
    # Parse args
    threshold = 7.0
    limit = None
    
    if "--threshold" in sys.argv:
        idx = sys.argv.index("--threshold")
        if idx + 1 < len(sys.argv):
            threshold = float(sys.argv[idx + 1])
    
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])
    
    print(f"🐓 Auto-Deliberate Pipeline")
    print(f"   Threshold: {threshold}/10")
    print(f"   Limit: {limit if limit else 'No limit'}")
    print()
    
    # Load signals
    signals = load_green_signals(threshold)
    
    if not signals:
        print(f"ℹ️  No signals found with conviction ≥ {threshold}/10")
        return 0
    
    print(f"✅ Found {len(signals)} signals ≥ {threshold}/10\n")
    
    # Apply limit
    if limit:
        signals = signals[:limit]
    
    # Run deliberations
    for idx, signal in enumerate(signals, 1):
        ticker = signal['ticker']
        conviction = signal['conviction']
        
        print(f"\n[{idx}/{len(signals)}] Processing {ticker} ({conviction}/10)")
        print(f"   Source: {signal['source']}")
        print(f"   Catalyst: {signal['catalyst']}")
        
        # Run 18-agent system
        output = run_18_agent_deliberation(ticker)
        
        if output:
            # Save to log
            save_deliberation_log(ticker, conviction, output)
        
        print()
    
    print(f"\n✅ Deliberations complete: {len(signals)} signals processed")
    return 0

if __name__ == "__main__":
    exit(main())
