#!/usr/bin/env python3
"""
Auto-Evaluate New Signals - Run 18 Agents on Latest Signals
============================================================

Checks signals-database.csv for new signals, runs 18-agent evaluation,
updates database with agent decision + conviction.

Usage:
    python agents/auto_evaluate_new_signals.py
    python agents/auto_evaluate_new_signals.py --lookback 7  # Check last 7 days

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

import sys
import os
import csv
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from portfolio_manager import PortfolioManager, RiskManager


def load_signals(lookback_days=1):
    """Load signals from database that need evaluation"""
    db_path = Path(__file__).parent.parent / "signals-database.csv"
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return []
    
    with open(db_path, 'r') as f:
        reader = csv.DictReader(f)
        all_signals = list(reader)
    
    # Filter to recent signals without agent evaluation
    cutoff_date = datetime.now() - timedelta(days=lookback_days)
    
    new_signals = []
    for row in all_signals:
        date_found = row.get('Date_Found', '')
        agent_decision = row.get('Agent_Decision', '')
        
        # Skip if already evaluated
        if agent_decision:
            continue
        
        # Skip if too old
        if date_found:
            try:
                signal_date = datetime.strptime(date_found, '%Y-%m-%d')
                if signal_date < cutoff_date:
                    continue
            except:
                pass
        
        new_signals.append(row)
    
    return new_signals


def evaluate_signal(row, portfolio_manager):
    """Run 18-agent evaluation on signal"""
    signal = {
        "ticker": row['Ticker'],
        "price": float(row.get('Price_Entry') or row.get('Price_Current', 0)),
        "catalyst": row.get('Notes', row.get('Catalyst', '')),
        "source": row.get('Source', 'Database'),
        "conviction": float(row.get('Conviction_Score', 5)),
        "asset_class": row.get('Asset_Class', 'unknown'),
        "date_found": row.get('Date_Found', datetime.now().strftime('%Y-%m-%d'))
    }
    
    try:
        conviction_doc = portfolio_manager.evaluate_signal(signal)
        return conviction_doc
    except Exception as e:
        print(f"❌ Error evaluating {signal['ticker']}: {e}")
        return None


def update_database(conviction_docs):
    """Update signals-database.csv with agent decisions"""
    db_path = Path(__file__).parent.parent / "signals-database.csv"
    
    # Read all rows
    with open(db_path, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        all_rows = list(reader)
    
    # Add new fields if needed
    if 'Agent_Decision' not in fieldnames:
        fieldnames = list(fieldnames) + ['Agent_Decision', 'Agent_Conviction', 'Agent_Evaluated']
    
    # Update rows
    ticker_to_doc = {doc['ticker']: doc for doc in conviction_docs if doc}
    
    for row in all_rows:
        ticker = row['Ticker']
        if ticker in ticker_to_doc:
            doc = ticker_to_doc[ticker]
            row['Agent_Decision'] = doc['final_decision']
            row['Agent_Conviction'] = doc['risk_validated_conviction']
            row['Agent_Evaluated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Write back
    with open(db_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    
    print(f"✅ Database updated: {db_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-evaluate new signals with 18 agents')
    parser.add_argument('--lookback', type=int, default=1, help='Look back N days for new signals')
    parser.add_argument('--all', action='store_true', help='Evaluate all signals (ignore Agent_Decision)')
    
    args = parser.parse_args()
    
    print("🐓 Auto-Evaluating New Signals with 18-Agent System")
    print("=" * 70)
    
    # Load signals
    if args.all:
        # Load all without filtering
        db_path = Path(__file__).parent.parent / "signals-database.csv"
        with open(db_path, 'r') as f:
            new_signals = list(csv.DictReader(f))
        print(f"Evaluating ALL {len(new_signals)} signals...")
    else:
        new_signals = load_signals(lookback_days=args.lookback)
        print(f"Found {len(new_signals)} new signals (last {args.lookback} days)")
    
    if not new_signals:
        print("✅ No new signals to evaluate")
        return
    
    # Initialize
    risk_manager = RiskManager()
    portfolio_manager = PortfolioManager(risk_manager=risk_manager)
    
    # Evaluate each
    conviction_docs = []
    buy_count = 0
    
    for row in new_signals:
        ticker = row['Ticker']
        print(f"\n📊 Evaluating {ticker}...")
        
        doc = evaluate_signal(row, portfolio_manager)
        
        if doc:
            conviction_docs.append(doc)
            
            decision = doc['final_decision']
            conviction = doc['risk_validated_conviction']
            
            print(f"   Result: {decision} (Conviction: {conviction}/10)")
            
            if decision == "BUY":
                buy_count += 1
                sizing = doc['position_sizing']
                print(f"   💰 Approved: {sizing['position_size']} ({sizing['pct_allocation']})")
    
    # Update database
    if conviction_docs:
        update_database(conviction_docs)
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 AUTO-EVALUATION COMPLETE")
    print("=" * 70)
    print(f"Evaluated: {len(conviction_docs)} signals")
    print(f"BUY signals: {buy_count}")
    print(f"HOLD signals: {len(conviction_docs) - buy_count}")
    
    if buy_count > 0:
        print(f"\n🚀 {buy_count} signals ready for deployment")
        print("   Check signals-database.csv for Agent_Decision = BUY")


if __name__ == "__main__":
    main()
