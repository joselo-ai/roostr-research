#!/usr/bin/env python3
"""
Deploy Signal - Add Position + Auto-Update Dashboard
====================================================

Called when a signal is approved for deployment.
Adds to signals-database.csv and triggers dashboard update.

Author: Joselo 🐓
Date: Feb 12, 2026
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

# Import dashboard updater
sys.path.insert(0, str(Path(__file__).parent))
from dashboard_updater import update_dashboards


DB_PATH = Path(__file__).parent.parent / "signals-database.csv"


def deploy_signal(
    ticker: str,
    entry_price: float,
    position_size: float,
    stop_loss: float,
    conviction: float,
    source: str,
    notes: str,
    asset_class: str = "stock"
):
    """
    Deploy a signal (add to database + update dashboards).
    
    Args:
        ticker: Stock/crypto symbol
        entry_price: Entry price
        position_size: Position size in dollars
        stop_loss: Stop loss price
        conviction: Agent conviction score
        source: Signal source
        notes: Full catalyst/reasoning
        asset_class: stock/crypto/forex
    """
    print(f"🐓 Deploying {ticker} @ ${entry_price}")
    
    # Read existing database
    with open(DB_PATH, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    # Create new position
    new_position = {
        'Ticker': ticker,
        'Source': source,
        'Date_Found': datetime.now().strftime('%Y-%m-%d'),
        'Price_Entry': str(entry_price),
        'Conviction_Score': str(conviction),
        'Status': 'GREEN',
        'Deployed': 'YES',
        'Position_Size': str(position_size),
        'Stop_Loss': str(stop_loss),
        'Target_1': '',
        'Target_2': '',
        'Current_Price': str(entry_price),
        'PnL_Dollars': '0',
        'PnL_Percent': '0.0',
        'Notes': notes,
        'Date_Entry': datetime.now().strftime('%Y-%m-%d'),
        'Agent_Decision': 'BUY',
        'Agent_Conviction': str(conviction),
        'Agent_Evaluated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'Asset_Class': asset_class
    }
    
    # Fill missing fields
    for field in fieldnames:
        if field not in new_position:
            new_position[field] = ''
    
    # Add to database
    rows.append(new_position)
    
    # Write back
    with open(DB_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"   ✅ Added to database")
    
    # Update dashboards
    print(f"   📊 Updating dashboards...")
    update_dashboards()
    
    print(f"   ✅ Deployment complete!")
    
    return new_position


if __name__ == "__main__":
    # Test deployment
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', required=True)
    parser.add_argument('--price', type=float, required=True)
    parser.add_argument('--size', type=float, required=True)
    parser.add_argument('--stop', type=float, required=True)
    parser.add_argument('--conviction', type=float, default=7.0)
    parser.add_argument('--source', default='Manual')
    parser.add_argument('--notes', default='Manual deployment')
    parser.add_argument('--asset-class', default='stock')
    
    args = parser.parse_args()
    
    deploy_signal(
        ticker=args.ticker,
        entry_price=args.price,
        position_size=args.size,
        stop_loss=args.stop,
        conviction=args.conviction,
        source=args.source,
        notes=args.notes,
        asset_class=args.asset_class
    )
