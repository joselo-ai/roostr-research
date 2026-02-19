#!/usr/bin/env python3
"""
Price Updater v3 - Stock Positions (ALL/PGR/KTB)
Fetches stock prices from Yahoo Finance and updates dashboard.html
Run hourly via cron
"""

import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/trading')
import yfinance as yf
from datetime import datetime
import re
from pathlib import Path

DASHBOARD_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/dashboard.html"

# Current positions (Feb 9, 2026)
POSITIONS = {
    "ALL": {
        "name": "Allstate",
        "shares": 96.62,
        "entry": 207.00,
        "entry_value": 20000,
        "stop": 186.30
    },
    "PGR": {
        "name": "Progressive",
        "shares": 74.42,
        "entry": 201.57,
        "entry_value": 15000,
        "stop": 181.41
    },
    "KTB": {
        "name": "Kontoor Brands",
        "shares": 149.25,
        "entry": 67.00,
        "entry_value": 10000,
        "stop": 60.30
    }
}

def fetch_prices():
    """Fetch current prices from Yahoo Finance"""
    prices = {}
    
    for symbol in POSITIONS.keys():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1d')
            if len(hist) > 0:
                prices[symbol] = hist['Close'].iloc[-1]
            else:
                return None
        except Exception as e:
            print(f"⚠️  Error fetching {symbol}: {e}")
            return None
    
    return prices

def calculate_pnl(symbol, current_price):
    """Calculate P&L for a position"""
    pos = POSITIONS[symbol]
    shares = pos["shares"]
    entry = pos["entry"]
    
    current_value = current_price * shares
    entry_value = pos["entry_value"]
    pnl_dollars = current_value - entry_value
    pnl_percent = (pnl_dollars / entry_value) * 100
    
    return {
        "current_price": current_price,
        "current_value": current_value,
        "pnl_dollars": pnl_dollars,
        "pnl_percent": pnl_percent
    }

def update_dashboard(prices):
    """Update dashboard.html with current prices"""
    if not prices or len(prices) != 3:
        return False
    
    # Read dashboard
    with open(DASHBOARD_PATH, 'r') as f:
        html = f.read()
    
    # Calculate P&L for each position
    all_pnl = calculate_pnl("ALL", prices["ALL"])
    pgr_pnl = calculate_pnl("PGR", prices["PGR"])
    ktb_pnl = calculate_pnl("KTB", prices["KTB"])
    
    total_pnl = all_pnl["pnl_dollars"] + pgr_pnl["pnl_dollars"] + ktb_pnl["pnl_dollars"]
    total_deployed = 45000
    total_pnl_percent = (total_pnl / total_deployed) * 100
    
    # Update timestamp
    now = datetime.now().strftime("%b %d, %Y %H:%M EST")
    html = re.sub(
        r'Dashboard: [^|]+\|',
        f'Dashboard: {now} |',
        html
    )
    
    # Update Portfolio Performance - Net P&L
    pnl_sign = "+" if total_pnl >= 0 else ""
    html = re.sub(
        r'(<span class="metric-label">Net P&L</span>\s*<span class="metric-value (?:positive|negative|neutral)">)[^<]+',
        f'\\1{pnl_sign}${total_pnl:.0f} ({pnl_sign}{total_pnl_percent:.1f}%)',
        html
    )
    
    # Update deployed capital
    html = re.sub(
        r'(<span class="metric-label">Deployed</span>\s*<span class="metric-value">)\$[\d,]+',
        f'\\1${total_deployed:,}',
        html
    )
    
    # Write updated dashboard
    with open(DASHBOARD_PATH, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard updated: ALL ${prices['ALL']:.2f}, PGR ${prices['PGR']:.2f}, KTB ${prices['KTB']:.2f}, P&L ${total_pnl:+.0f}")
    return True

def main():
    print(f"🐓 Price Updater v3 (Stocks) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Frequency: Hourly (0 * * * *)")
    
    prices = fetch_prices()
    if prices and len(prices) == 3:
        update_dashboard(prices)
        return 0
    else:
        print("⚠️  Price update skipped (will retry next hour)")
        return 0

if __name__ == "__main__":
    exit(main())
