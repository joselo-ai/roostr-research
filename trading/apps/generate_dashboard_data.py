#!/usr/bin/env python3
"""
🐓 Dashboard Data Generator
Generates JSON data for Mission Control dashboard.

Runs: Hourly (syncs with price_updater)
Output: dashboard-data.json (consumed by Next.js frontend)
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import yfinance as yf

TRADING_DIR = Path(__file__).parent.parent
POSITIONS_FILE = TRADING_DIR / "positions.csv"
OUTPUT_FILE = TRADING_DIR / "dashboard-data.json"

def load_positions():
    """Load active positions from CSV"""
    try:
        df = pd.read_csv(POSITIONS_FILE)
        return df[df['Status'] == 'OPEN'].to_dict('records')
    except Exception as e:
        print(f"⚠️  Error loading positions: {e}")
        return []

def get_current_prices(tickers):
    """Fetch current prices for all tickers"""
    prices = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                prices[ticker] = hist['Close'].iloc[-1]
        except Exception as e:
            print(f"⚠️  Error fetching {ticker}: {e}")
            prices[ticker] = None
    return prices

def calculate_pnl(positions, prices):
    """Calculate P&L for each position"""
    results = []
    total_pnl = 0
    total_value = 0
    
    for pos in positions:
        ticker = pos['Ticker']
        entry = pos['Entry']
        shares = pos['Shares']
        position_size = pos['Position_Size']
        
        current = prices.get(ticker)
        if current is None:
            current = entry  # Fallback to entry if price unavailable
        
        current_value = current * shares
        pnl = current_value - position_size
        pnl_pct = (pnl / position_size) * 100 if position_size > 0 else 0
        
        results.append({
            'ticker': ticker,
            'entry': entry,
            'current': current,
            'shares': shares,
            'positionSize': position_size,
            'currentValue': current_value,
            'pnl': pnl,
            'pnlPct': pnl_pct,
            'stopLoss': pos['Stop_Loss'],
            'conviction': pos['Conviction'],
            'date': pos['Date'],
            'tier': pos.get('Tier', 'MEDIUM')
        })
        
        total_pnl += pnl
        total_value += position_size
    
    return results, total_pnl, total_value

def generate_performance_metrics(positions_with_pnl):
    """Calculate portfolio performance metrics"""
    if not positions_with_pnl:
        return {
            'winRate': 0,
            'avgConviction': 0,
            'maxDrawdown': 0,
            'positionsGreen': 0,
            'positionsTotal': 0
        }
    
    green = sum(1 for p in positions_with_pnl if p['pnl'] > 0)
    total = len(positions_with_pnl)
    win_rate = (green / total * 100) if total > 0 else 0
    
    avg_conviction = sum(p['conviction'] for p in positions_with_pnl) / total if total > 0 else 0
    
    max_dd = min((p['pnlPct'] for p in positions_with_pnl), default=0)
    
    return {
        'winRate': round(win_rate, 2),
        'avgConviction': round(avg_conviction, 2),
        'maxDrawdown': round(max_dd, 2),
        'positionsGreen': green,
        'positionsTotal': total
    }

def main():
    print("🐓 Generating Mission Control Dashboard Data")
    print("=" * 60)
    
    # Load positions
    positions = load_positions()
    print(f"📊 Active positions: {len(positions)}")
    
    if not positions:
        print("⚠️  No active positions found")
        output = {
            'timestamp': datetime.now().isoformat(),
            'positions': [],
            'totalPnL': 0,
            'totalValue': 0,
            'totalPnLPct': 0,
            'performance': generate_performance_metrics([])
        }
    else:
        # Get current prices
        tickers = [p['Ticker'] for p in positions]
        print(f"💰 Fetching prices for: {', '.join(tickers)}")
        prices = get_current_prices(tickers)
        
        # Calculate P&L
        positions_with_pnl, total_pnl, total_value = calculate_pnl(positions, prices)
        total_pnl_pct = (total_pnl / total_value * 100) if total_value > 0 else 0
        
        # Generate output
        output = {
            'timestamp': datetime.now().isoformat(),
            'positions': positions_with_pnl,
            'totalPnL': round(total_pnl, 2),
            'totalValue': round(total_value, 2),
            'totalPnLPct': round(total_pnl_pct, 2),
            'performance': generate_performance_metrics(positions_with_pnl)
        }
        
        print(f"\n💵 Total P&L: ${total_pnl:.2f} ({total_pnl_pct:.2f}%)")
        print(f"📈 Win Rate: {output['performance']['winRate']}%")
    
    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Dashboard data saved to: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
