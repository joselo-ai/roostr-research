#!/usr/bin/env python3
"""
18-Agent Trading System - Master Execution Script
==================================================

Runs complete multi-agent evaluation pipeline:
- 12 Legendary Investors
- 4 Quantitative Agents
- Risk Manager (Joselo 🐓)
- Portfolio Manager (final decision)

Usage:
    python agents/run_18_agents.py --ticker TAO --price 176.05 --catalyst "AI blockchain"
    python agents/run_18_agents.py --from-database --ticker TAO
    python agents/run_18_agents.py --scan-all

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 12, 2026
"""

import sys
import os
import argparse
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add agents directory to path
sys.path.insert(0, os.path.dirname(__file__))

from portfolio_manager import PortfolioManager, RiskManager
from legendary_investors import LEGENDARY_INVESTORS
from quant_agents import QUANT_AGENTS


def load_signal_from_database(ticker: str) -> dict:
    """Load signal from signals-database.csv"""
    db_path = Path(__file__).parent.parent / "signals-database.csv"
    
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    df = pd.read_csv(db_path)
    
    # Find most recent signal for ticker
    ticker_signals = df[df['Ticker'].str.upper() == ticker.upper()]
    
    if ticker_signals.empty:
        raise ValueError(f"No signals found for {ticker}")
    
    # Get most recent
    latest = ticker_signals.iloc[-1]
    
    signal = {
        "ticker": latest['Ticker'],
        "price": latest.get('Price_Entry', latest.get('Price_Current', 0)),
        "catalyst": latest.get('Notes', latest.get('Catalyst', '')),
        "source": latest.get('Source', 'Database'),
        "conviction": latest.get('Conviction_Score', 5),
        "asset_class": latest.get('Asset_Class', 'unknown'),
        "date_found": latest.get('Date_Found', datetime.now().strftime('%Y-%m-%d'))
    }
    
    return signal


def scan_all_signals() -> list:
    """Load all signals from database"""
    db_path = Path(__file__).parent.parent / "signals-database.csv"
    
    if not db_path.exists():
        return []
    
    df = pd.read_csv(db_path)
    
    signals = []
    for _, row in df.iterrows():
        signal = {
            "ticker": row['Ticker'],
            "price": row.get('Price_Entry', row.get('Price_Current', 0)),
            "catalyst": row.get('Notes', row.get('Catalyst', '')),
            "source": row.get('Source', 'Database'),
            "conviction": row.get('Conviction_Score', 5),
            "asset_class": row.get('Asset_Class', 'unknown'),
            "date_found": row.get('Date_Found', datetime.now().strftime('%Y-%m-%d'))
        }
        signals.append(signal)
    
    return signals


def save_conviction_document(conviction_doc: dict, output_dir: Path):
    """Save conviction document to file"""
    ticker = conviction_doc['ticker']
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"conviction_{ticker}_{timestamp}.json"
    
    output_path = output_dir / filename
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(conviction_doc, f, indent=2, default=str)
    
    print(f"\n✅ Conviction document saved: {output_path}")
    
    return output_path


def print_summary(conviction_doc: dict):
    """Print human-readable summary"""
    print("\n" + "=" * 70)
    print(f"🐓 roostr Capital - 18-Agent Evaluation: {conviction_doc['ticker']}")
    print("=" * 70)
    
    print(f"\n📊 FINAL DECISION: {conviction_doc['final_decision']}")
    print(f"💯 Conviction: {conviction_doc['risk_validated_conviction']}/10 ({conviction_doc['conviction_rating']})")
    print(f"📅 Date: {conviction_doc['timestamp']}")
    print(f"💵 Entry Price: ${conviction_doc['entry_price']}")
    
    print(f"\n🏛️ LEGENDARY INVESTORS (12 agents)")
    print(f"   Consensus: {conviction_doc['legendary_investors']['consensus']}")
    print(f"   Avg Conviction: {conviction_doc['legendary_investors']['avg_conviction']}/10")
    print(f"   Votes: {conviction_doc['legendary_investors']['votes']}")
    
    print(f"\n📈 QUANT AGENTS (4 agents)")
    print(f"   Consensus: {conviction_doc['quant_agents']['consensus']}")
    print(f"   Avg Score: {conviction_doc['quant_agents']['avg_score']}/10")
    print(f"   Votes: {conviction_doc['quant_agents']['votes']}")
    
    if conviction_doc['risk_concerns']:
        print(f"\n⚠️  RISK CONCERNS:")
        for concern in conviction_doc['risk_concerns']:
            print(f"   - {concern}")
    
    if conviction_doc.get('position_sizing'):
        sizing = conviction_doc['position_sizing']
        print(f"\n💰 POSITION SIZING:")
        print(f"   Allocation: {sizing['pct_allocation']} (${sizing['position_size']})")
        print(f"   Entry: ${sizing['entry_price']}")
        print(f"   Stop: ${sizing['stop_price']} ({sizing['stop_loss']})")
        print(f"   Max Risk: {sizing['max_risk']}")
    
    print(f"\n📝 REASONING:")
    print(conviction_doc['reasoning'])
    
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description='Run 18-agent trading evaluation')
    
    # Input modes
    parser.add_argument('--ticker', help='Ticker symbol')
    parser.add_argument('--price', type=float, help='Entry price')
    parser.add_argument('--catalyst', help='Catalyst/reasoning')
    parser.add_argument('--source', default='Manual', help='Signal source')
    parser.add_argument('--asset-class', default='unknown', help='Asset class (stock/crypto)')
    
    parser.add_argument('--from-database', action='store_true', help='Load from signals-database.csv')
    parser.add_argument('--scan-all', action='store_true', help='Evaluate all signals in database')
    
    # Output
    parser.add_argument('--output-dir', default='../conviction-docs', help='Output directory for conviction docs')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')
    
    args = parser.parse_args()
    
    # Initialize managers
    risk_manager = RiskManager()
    portfolio_manager = PortfolioManager(risk_manager=risk_manager)
    
    output_dir = Path(__file__).parent.parent / args.output_dir
    
    # Determine input mode
    if args.scan_all:
        # Scan all signals
        signals = scan_all_signals()
        print(f"🐓 Evaluating {len(signals)} signals from database...")
        
        results = []
        for signal in signals:
            try:
                conviction_doc = portfolio_manager.evaluate_signal(signal)
                
                if not args.quiet:
                    print_summary(conviction_doc)
                
                save_conviction_document(conviction_doc, output_dir)
                results.append(conviction_doc)
                
            except Exception as e:
                print(f"❌ Error evaluating {signal['ticker']}: {e}")
        
        # Summary
        print(f"\n✅ Evaluated {len(results)} signals")
        buy_count = sum(1 for r in results if r['final_decision'] == 'BUY')
        print(f"   BUY signals: {buy_count}")
        
    elif args.from_database:
        # Load specific ticker from database
        if not args.ticker:
            print("❌ Error: --ticker required with --from-database")
            sys.exit(1)
        
        signal = load_signal_from_database(args.ticker)
        conviction_doc = portfolio_manager.evaluate_signal(signal)
        
        if not args.quiet:
            print_summary(conviction_doc)
        
        save_conviction_document(conviction_doc, output_dir)
        
    else:
        # Manual signal input
        if not args.ticker or not args.price or not args.catalyst:
            print("❌ Error: --ticker, --price, and --catalyst required for manual input")
            print("   Or use --from-database --ticker SYMBOL")
            print("   Or use --scan-all")
            sys.exit(1)
        
        signal = {
            "ticker": args.ticker,
            "price": args.price,
            "catalyst": args.catalyst,
            "source": args.source,
            "asset_class": args.asset_class,
            "conviction": 5  # Default
        }
        
        conviction_doc = portfolio_manager.evaluate_signal(signal)
        
        if not args.quiet:
            print_summary(conviction_doc)
        
        save_conviction_document(conviction_doc, output_dir)
    
    print("\n🐓 roostr 18-Agent System Complete")


if __name__ == "__main__":
    main()
