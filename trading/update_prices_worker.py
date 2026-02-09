#!/usr/bin/env python3
"""
Price Update Worker - Updates prices for all deployed positions
Called by update_prices.sh every 5 minutes
"""

import csv
import sys
from datetime import datetime
from price_fetcher import PriceFetcher

def update_prices():
    """Update all deployed positions with current prices"""
    
    # Read signals database
    signals = []
    with open('signals-database.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            signals.append(row)
    
    # Find deployed crypto positions
    deployed_tickers = []
    for signal in signals:
        if signal.get('Deployed') == 'YES' and signal.get('Ticker'):
            ticker = signal['Ticker'].upper()
            # Only update crypto (not stocks/forex)
            if ticker not in ['ASTS', 'TAC', 'AS', 'PYPL', 'EURUSD']:
                deployed_tickers.append(ticker)
    
    if not deployed_tickers:
        print("ℹ️  No deployed crypto positions to update")
        return 0
    
    print(f"📡 Fetching prices for {len(deployed_tickers)} positions: {', '.join(deployed_tickers)}")
    
    # Fetch prices
    fetcher = PriceFetcher(cache_dir='.')
    prices = fetcher.get_multiple_prices(deployed_tickers, use_cache=False)
    
    if not prices:
        print("❌ Failed to fetch any prices")
        return 1
    
    print(f"✅ Fetched {len(prices)} prices")
    
    # Update signals with new prices
    updates_made = 0
    
    for signal in signals:
        ticker = signal.get('Ticker', '').upper()
        
        if ticker in prices and signal.get('Deployed') == 'YES':
            price_data = prices[ticker]
            current_price = price_data['price']
            entry_price = float(signal.get('Price_Entry', 0))
            position_size = float(signal.get('Position_Size', 0))
            
            # Update current price
            signal['Current_Price'] = f"{current_price:.2f}"
            
            # Calculate P&L
            # Position_Size is in USD, so units = Position_Size / Entry_Price
            if entry_price > 0:
                position_units = position_size / entry_price
                pnl_dollars = (current_price - entry_price) * position_units
                pnl_percent = ((current_price - entry_price) / entry_price) * 100
                
                signal['PnL_Dollars'] = f"{pnl_dollars:.0f}"
                signal['PnL_Percent'] = f"{pnl_percent:.2f}"
                
                print(f"   {ticker}: ${current_price:.2f} | P&L: ${pnl_dollars:+,.0f} ({pnl_percent:+.1f}%)")
                updates_made += 1
    
    # Write back to CSV
    if updates_made > 0:
        with open('signals-database.csv', 'w', newline='') as f:
            fieldnames = signals[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(signals)
        
        print(f"✅ Updated {updates_made} positions in database")
    
    return 0

if __name__ == "__main__":
    sys.exit(update_prices())
