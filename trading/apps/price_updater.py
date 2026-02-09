#!/usr/bin/env python3
"""
Price Updater - Real-time dashboard updates
Fetches TAO/SOL prices from CoinGecko and updates dashboard.html
Run every 5 minutes via cron
"""

import requests
import json
from datetime import datetime
import re

# Activity logging
import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/command-center')
from activity_logger import log_trading, log_automation


COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
DASHBOARD_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/dashboard.html"
POSITIONS_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/PAPER-TRADING-LOG.md"

# Position details
POSITIONS = {
    "TAO": {
        "id": "bittensor",
        "entry": 176.05,
        "quantity": 56.8,
        "stop": 140.84
    },
    "SOL": {
        "id": "solana",
        "entry": 86.51,
        "quantity": 86.7,
        "stop": 73.53
    }
}

def fetch_prices():
    """Fetch current prices from CoinGecko"""
    ids = ",".join([p["id"] for p in POSITIONS.values()])
    
    try:
        response = requests.get(
            COINGECKO_API,
            params={
                "ids": ids,
                "vs_currencies": "usd"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        prices = {}
        for symbol, details in POSITIONS.items():
            price = data.get(details["id"], {}).get("usd")
            if price:
                prices[symbol] = price
        
        return prices
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

def calculate_pnl(symbol, current_price):
    """Calculate P&L for a position"""
    pos = POSITIONS[symbol]
    entry = pos["entry"]
    qty = pos["quantity"]
    
    current_value = current_price * qty
    entry_value = entry * qty
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
    if not prices:
        return False
    
    # Read dashboard
    with open(DASHBOARD_PATH, 'r') as f:
        html = f.read()
    
    # Calculate totals
    tao_pnl = calculate_pnl("TAO", prices["TAO"])
    sol_pnl = calculate_pnl("SOL", prices["SOL"])
    total_pnl = tao_pnl["pnl_dollars"] + sol_pnl["pnl_dollars"]
    total_deployed = 17500
    total_pnl_percent = (total_pnl / total_deployed) * 100
    
    # Update timestamp
    now = datetime.now().strftime("%b %d, %Y %H:%M EST")
    html = re.sub(
        r'Dashboard: [^|]+\|',
        f'Dashboard: {now} |',
        html
    )
    
    # Update Live Positions table - TAO
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">TAO</td>\s*<td[^>]*>\$176\.05</td>\s*<td[^>]*>)\$[\d.]+',
        f'\\1${prices["TAO"]:.2f}',
        html
    )
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">TAO</td>.*?<td[^>]*>)\$[\d,]+(?=</td>\s*<td[^>]*color: #4ade80)',
        f'\\1${tao_pnl["current_value"]:,.0f}',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">TAO</td>.*?color: #4ade80[^>]*>)\+\$[\d]+',
        f'\\1+${tao_pnl["pnl_dollars"]:.0f}',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">TAO</td>.*?color: #4ade80[^>]*>\+\$[\d]+</td>\s*<td[^>]*color: #4ade80[^>]*>)\+[\d.]+%',
        f'\\1+{tao_pnl["pnl_percent"]:.2f}%',
        html,
        flags=re.DOTALL
    )
    
    # Update Live Positions table - SOL
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">SOL</td>\s*<td[^>]*>\$86\.51</td>\s*<td[^>]*>)\$[\d.]+',
        f'\\1${prices["SOL"]:.2f}',
        html
    )
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">SOL</td>.*?<td[^>]*>)\$[\d,]+(?=</td>\s*<td[^>]*color: #4ade80)',
        f'\\1${sol_pnl["current_value"]:,.0f}',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">SOL</td>.*?color: #4ade80[^>]*>)\+\$[\d]+',
        f'\\1+${sol_pnl["pnl_dollars"]:.0f}',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<td style="padding: 10px; font-weight: 600;">SOL</td>.*?color: #4ade80[^>]*>\+\$[\d]+</td>\s*<td[^>]*color: #4ade80[^>]*>)\+[\d.]+%',
        f'\\1+{sol_pnl["pnl_percent"]:.2f}%',
        html,
        flags=re.DOTALL
    )
    
    # Update Portfolio Performance - Net P&L
    pnl_class = "positive" if total_pnl > 0 else "negative" if total_pnl < 0 else "neutral"
    html = re.sub(
        r'(<span class="metric-label">Net P&L</span>\s*<span class="metric-value (?:positive|negative|neutral)">)[^<]+',
        f'\\1{"+" if total_pnl >= 0 else ""}${total_pnl:.0f} ({"+" if total_pnl >= 0 else ""}{total_pnl_percent:.1f}%)',
        html
    )
    
    # Update Crypto bucket P&L
    html = re.sub(
        r'(<strong>P&L:</strong> <span class="(?:positive|negative|neutral)">)[^<]+(?=</span><br>\s*<strong>Open Positions:</strong> 2)',
        f'\\1{"+" if total_pnl >= 0 else ""}${total_pnl:.0f} ({"+" if total_pnl >= 0 else ""}{total_pnl_percent:.1f}%)',
        html
    )
    
    # Write updated dashboard
    with open(DASHBOARD_PATH, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard updated: TAO ${prices['TAO']:.2f}, SOL ${prices['SOL']:.2f}, P&L ${total_pnl:.0f}")
    log_trading("Price update", {"TAO": prices['TAO'], "SOL": prices['SOL'], "P&L": total_pnl})
    return True

def main():
    print(f"🐓 Price Updater - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    prices = fetch_prices()
    if prices and len(prices) == 2:
        update_dashboard(prices)
        return 0
    else:
        print("❌ Failed to fetch prices")
        return 1

if __name__ == "__main__":
    exit(main())
