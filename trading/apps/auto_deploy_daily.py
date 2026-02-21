#!/usr/bin/env python3
"""
🐓 Auto-Deploy Daily Position
Runs daily deployment protocol:
1. Scans for top 10 opportunities
2. Runs top 3 through 18-agent system
3. Deploys highest conviction (even if 6.0-7.9)
4. Adjusts position size and stop-loss by conviction tier

Usage:
    python apps/auto_deploy_daily.py
    python apps/auto_deploy_daily.py --dry-run
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

TRADING_DIR = Path(__file__).parent.parent
AGENTS_DIR = TRADING_DIR / "agents"
OPPORTUNITIES_FILE = TRADING_DIR / "daily-opportunities.json"
POSITIONS_FILE = TRADING_DIR / "positions.csv"

# Add agents to path
sys.path.insert(0, str(AGENTS_DIR))

def scan_opportunities():
    """Run daily opportunity scanner"""
    print("🔍 Scanning market for opportunities...")
    result = subprocess.run(
        ["python3", "apps/daily_opportunity_scanner.py"],
        cwd=TRADING_DIR,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Scanner failed: {result.stderr}")
        return None
    
    # Load results
    with open(OPPORTUNITIES_FILE, 'r') as f:
        data = json.load(f)
    
    return data['top_10']

def evaluate_with_agents(ticker, price, catalyst=""):
    """Run ticker through 18-agent system"""
    print(f"\n🤖 Evaluating {ticker} with 18-agent system...")
    
    cmd = [
        "python3", "agents/run_18_agents.py",
        "--ticker", ticker,
        "--price", str(price),
        "--catalyst", catalyst
    ]
    
    result = subprocess.run(
        cmd,
        cwd=TRADING_DIR,
        capture_output=True,
        text=True
    )
    
    # Parse conviction from output
    conviction = 0.0
    decision = "HOLD"
    
    for line in result.stdout.split('\n'):
        if "Final Conviction:" in line:
            try:
                conviction = float(line.split(':')[1].split('/')[0].strip())
            except:
                pass
        if "FINAL DECISION:" in line:
            decision = line.split(':')[1].strip()
    
    return {
        'ticker': ticker,
        'conviction': conviction,
        'decision': decision,
        'output': result.stdout
    }

def calculate_position_params(conviction, price):
    """Calculate position size and stop-loss based on conviction tier"""
    
    # Conviction tiers
    if conviction >= 8.0:
        # High conviction: Full position, wider stop
        position_size = 20000  # $20k
        stop_loss_pct = 15.0
        tier = "HIGH"
    elif conviction >= 6.0:
        # Medium conviction: Half position, tighter stop
        position_size = 10000  # $10k
        stop_loss_pct = 10.0
        tier = "MEDIUM"
    elif conviction >= 5.0:
        # Low-medium conviction: Quarter position, very tight stop
        position_size = 5000  # $5k
        stop_loss_pct = 8.0
        tier = "LOW-MEDIUM"
    else:
        # Very low conviction: Skip
        return None
    
    shares = int(position_size / price)
    stop_loss_price = round(price * (1 - stop_loss_pct / 100), 2)
    
    return {
        'tier': tier,
        'position_size': position_size,
        'shares': shares,
        'stop_loss_pct': stop_loss_pct,
        'stop_loss_price': stop_loss_price
    }

def deploy_position(ticker, price, conviction, dry_run=False):
    """Deploy position (paper trading)"""
    
    params = calculate_position_params(conviction, price)
    
    if params is None:
        print(f"❌ {ticker}: Conviction too low ({conviction}/10). Skipping.")
        return False
    
    print(f"\n{'🧪 DRY RUN: ' if dry_run else ''}🎯 Deploying {ticker}")
    print(f"   Conviction: {conviction}/10 ({params['tier']})")
    print(f"   Entry Price: ${price:.2f}")
    print(f"   Position Size: ${params['position_size']:,}")
    print(f"   Shares: {params['shares']}")
    print(f"   Stop Loss: ${params['stop_loss_price']} (-{params['stop_loss_pct']}%)")
    
    if dry_run:
        print("\n✅ Dry run complete. No position deployed.")
        return True
    
    # TODO: Integrate with Alpaca API for actual execution
    # For now, just log to positions file
    
    import pandas as pd
    
    new_position = {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Ticker': ticker,
        'Entry': price,
        'Shares': params['shares'],
        'Position_Size': params['position_size'],
        'Stop_Loss': params['stop_loss_price'],
        'Conviction': conviction,
        'Tier': params['tier'],
        'Status': 'OPEN'
    }
    
    # Append to positions file
    try:
        df = pd.read_csv(POSITIONS_FILE)
    except:
        df = pd.DataFrame()
    
    df = pd.concat([df, pd.DataFrame([new_position])], ignore_index=True)
    df.to_csv(POSITIONS_FILE, index=False)
    
    print(f"\n✅ Position deployed: {ticker} @ ${price:.2f}")
    print(f"   Logged to: {POSITIONS_FILE}")
    
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Auto-deploy daily position")
    parser.add_argument('--dry-run', action='store_true', help='Simulate without deploying')
    args = parser.parse_args()
    
    print("🐓 Auto-Deploy Daily Position")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE PAPER TRADING'}")
    print()
    
    # Step 1: Scan for opportunities
    top_10 = scan_opportunities()
    
    if not top_10:
        print("❌ No opportunities found. Exiting.")
        return
    
    print(f"\n✅ Found {len(top_10)} opportunities")
    
    # Step 2: Evaluate top 3 with agents
    print("\n" + "=" * 60)
    print("🤖 Running top 3 through 18-agent system...")
    print("=" * 60)
    
    evaluations = []
    
    for i, opp in enumerate(top_10[:3], 1):
        ticker = opp['ticker']
        price = opp.get('price', 0)
        
        # Build catalyst from opportunity data
        catalyst_parts = []
        if 'sector' in opp:
            catalyst_parts.append(f"{opp['sector']} sector")
        if 'volume_ratio' in opp and opp['volume_ratio'] > 2:
            catalyst_parts.append(f"unusual volume ({opp['volume_ratio']:.1f}x)")
        if 'dividend_yield' in opp and opp['dividend_yield'] > 3:
            catalyst_parts.append(f"{opp['dividend_yield']:.1f}% dividend")
        
        catalyst = ", ".join(catalyst_parts) if catalyst_parts else "Market opportunity"
        
        result = evaluate_with_agents(ticker, price, catalyst)
        evaluations.append(result)
        
        print(f"\n{ticker}: Conviction {result['conviction']}/10, Decision: {result['decision']}")
    
    # Step 3: Deploy highest conviction
    evaluations.sort(key=lambda x: x['conviction'], reverse=True)
    best = evaluations[0]
    
    print("\n" + "=" * 60)
    print("🎯 Best Opportunity:")
    print("=" * 60)
    print(f"   {best['ticker']}: {best['conviction']}/10 ({best['decision']})")
    
    if best['conviction'] >= 5.0:
        # Get price from top_10
        price = next((o['price'] for o in top_10 if o['ticker'] == best['ticker']), 0)
        deploy_position(best['ticker'], price, best['conviction'], dry_run=args.dry_run)
    else:
        print(f"\n❌ Best conviction ({best['conviction']}/10) below minimum (5.0). No deployment today.")
        print("   Consider expanding opportunity sources or recalibrating agents.")
    
    print("\n" + "=" * 60)
    print("✅ Daily deployment process complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
