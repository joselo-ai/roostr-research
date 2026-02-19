#!/usr/bin/env python3
"""Update dashboard with current stock positions"""

import yfinance as yf
from datetime import datetime

# Position data
positions = {
    'ALL': {'shares': 96.62, 'entry': 207.00, 'entry_value': 20000},
    'PGR': {'shares': 74.42, 'entry': 201.57, 'entry_value': 15000},
    'KTB': {'shares': 149.25, 'entry': 67.00, 'entry_value': 10000}
}

# Get current prices
for symbol, data in positions.items():
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1d')
    if len(hist) > 0:
        current_price = hist['Close'].iloc[-1]
        current_value = current_price * data['shares']
        pnl = current_value - data['entry_value']
        pnl_pct = (pnl / data['entry_value']) * 100
        
        positions[symbol]['current'] = current_price
        positions[symbol]['value'] = current_value
        positions[symbol]['pnl'] = pnl
        positions[symbol]['pnl_pct'] = pnl_pct
        
        print(f"{symbol}: ${current_price:.2f} | Value: ${current_value:.2f} | P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")

# Calculate totals
total_entry = sum(p['entry_value'] for p in positions.values())
total_current = sum(p['value'] for p in positions.values())
total_pnl = total_current - total_entry
total_pnl_pct = (total_pnl / total_entry) * 100

print(f"\nPortfolio: ${total_current:.2f} | P&L: ${total_pnl:+.2f} ({total_pnl_pct:+.2f}%)")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
