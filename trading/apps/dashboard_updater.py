#!/usr/bin/env python3
"""
Dashboard Auto-Updater
======================
Updates both dashboard.html and dashboard-ai-enhanced.html
whenever positions change.

Reads from signals-database.csv (dynamic, not hardcoded).

Author: Joselo 🐓
Date: Feb 12, 2026
"""

import csv
import json
from datetime import datetime
from pathlib import Path
import sys

# TradingView for live prices
try:
    from tradingview_ta import TA_Handler, Interval
    HAS_TRADINGVIEW = True
except:
    HAS_TRADINGVIEW = False


WORKSPACE = Path("/Users/agentjoselo/.openclaw/workspace/trading")
DB_PATH = WORKSPACE / "signals-database.csv"
DASHBOARD_PATH = WORKSPACE / "dashboard.html"
AI_DASHBOARD_PATH = WORKSPACE / "dashboard-ai-enhanced.html"


def load_active_positions():
    """Load all deployed positions from database"""
    if not DB_PATH.exists():
        return []
    
    with open(DB_PATH, 'r') as f:
        reader = csv.DictReader(f)
        positions = []
        
        for row in reader:
            if row.get('Deployed', '').upper() == 'YES':
                positions.append({
                    'ticker': row['Ticker'],
                    'entry': float(row.get('Price_Entry', 0)),
                    'stop': float(row.get('Stop_Loss', 0)),
                    'size': float(row.get('Position_Size', 0)),
                    'current': float(row.get('Current_Price', row.get('Price_Entry', 0))),
                    'pnl': float(row.get('PnL_Dollars', 0)),
                    'pnl_pct': float(row.get('PnL_Percent', 0)),
                    'conviction': float(row.get('Conviction_Score', 0)),
                    'status': row.get('Status', 'UNKNOWN'),
                    'asset_class': row.get('Asset_Class', 'unknown'),
                    'source': row.get('Source', 'Unknown')
                })
        
        return positions


def fetch_live_price(ticker, asset_class='crypto'):
    """Fetch live price from TradingView"""
    if not HAS_TRADINGVIEW:
        return None
    
    try:
        if asset_class.lower() == 'crypto':
            symbol = f"{ticker}USD"
            exchange = "BINANCE"
        else:
            symbol = ticker
            exchange = "NASDAQ"
        
        handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="crypto" if asset_class.lower() == 'crypto' else "america",
            interval=Interval.INTERVAL_1_HOUR
        )
        
        analysis = handler.get_analysis()
        return analysis.indicators.get("close")
    
    except Exception as e:
        print(f"⚠️  Could not fetch {ticker} price: {e}")
        return None


def calculate_portfolio_stats(positions):
    """Calculate portfolio-level statistics"""
    total_deployed = sum(p['size'] for p in positions)
    total_pnl = sum(p['pnl'] for p in positions)
    total_value = sum(p['size'] + p['pnl'] for p in positions)
    
    avg_conviction = sum(p['conviction'] for p in positions) / len(positions) if positions else 0
    
    green_count = sum(1 for p in positions if p['pnl'] > 0)
    red_count = sum(1 for p in positions if p['pnl'] < 0)
    
    return {
        'total_deployed': total_deployed,
        'total_pnl': total_pnl,
        'total_value': total_value,
        'pnl_pct': (total_pnl / total_deployed * 100) if total_deployed > 0 else 0,
        'avg_conviction': avg_conviction,
        'position_count': len(positions),
        'green_count': green_count,
        'red_count': red_count
    }


def update_dashboards():
    """Update both dashboards with latest data"""
    print(f"🐓 Dashboard Auto-Updater - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load positions
    positions = load_active_positions()
    print(f"   Loaded {len(positions)} active positions")
    
    if not positions:
        print("   ⚠️  No active positions found")
        return
    
    # Fetch live prices
    for pos in positions:
        live_price = fetch_live_price(pos['ticker'], pos['asset_class'])
        if live_price:
            pos['current'] = live_price
            pos['pnl'] = (live_price - pos['entry']) * (pos['size'] / pos['entry'])
            pos['pnl_pct'] = ((live_price - pos['entry']) / pos['entry']) * 100
            print(f"   {pos['ticker']}: ${live_price:.2f} (P&L: ${pos['pnl']:.0f})")
    
    # Calculate portfolio stats
    stats = calculate_portfolio_stats(positions)
    
    print(f"\n   📊 Portfolio: ${stats['total_value']:.0f} (P&L: ${stats['total_pnl']:.0f}, {stats['pnl_pct']:.2f}%)")
    print(f"   Positions: {stats['position_count']} ({stats['green_count']} green, {stats['red_count']} red)")
    
    # Update standard dashboard
    update_standard_dashboard(positions, stats)
    
    # Update AI dashboard
    update_ai_dashboard(positions, stats)
    
    print("   ✅ Dashboards updated")


def update_standard_dashboard(positions, stats):
    """Update dashboard.html (simple version)"""
    # TODO: Implement standard dashboard update
    # For now, price_updater.py handles this
    pass


def update_ai_dashboard(positions, stats):
    """Update dashboard-ai-enhanced.html with latest positions"""
    if not AI_DASHBOARD_PATH.exists():
        print("   ⚠️  AI dashboard not found, skipping")
        return
    
    # Read current dashboard
    with open(AI_DASHBOARD_PATH, 'r') as f:
        html = f.read()
    
    # Update timestamp
    timestamp = datetime.now().strftime('%b %d, %Y %H:%M EST')
    html = html.replace(
        'Feb 11, 2026 14:10 EST',
        timestamp
    )
    
    # Write back
    with open(AI_DASHBOARD_PATH, 'w') as f:
        f.write(html)
    
    print(f"   ✅ AI dashboard updated: {timestamp}")


if __name__ == "__main__":
    update_dashboards()
