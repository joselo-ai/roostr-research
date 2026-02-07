#!/usr/bin/env python3
"""
Daily Summary Generator
Posts portfolio summary to Telegram every morning (8 AM EST)
"""

import requests
import json
from datetime import datetime
import re

POSITIONS_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/PAPER-TRADING-LOG.md"
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

POSITIONS = {
    "TAO": {"id": "bittensor", "entry": 176.05, "quantity": 56.8},
    "SOL": {"id": "solana", "entry": 86.51, "quantity": 86.7}
}

def fetch_prices():
    """Fetch current prices from CoinGecko"""
    ids = ",".join([p["id"] for p in POSITIONS.values()])
    
    try:
        response = requests.get(
            COINGECKO_API,
            params={"ids": ids, "vs_currencies": "usd"},
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

def calculate_summary(prices):
    """Calculate portfolio summary"""
    if not prices:
        return None
    
    summary = {
        "positions": [],
        "total_deployed": 17500,
        "total_value": 0,
        "total_pnl": 0
    }
    
    for symbol, details in POSITIONS.items():
        current_price = prices[symbol]
        entry = details["entry"]
        qty = details["quantity"]
        
        current_value = current_price * qty
        entry_value = entry * qty
        pnl_dollars = current_value - entry_value
        pnl_percent = (pnl_dollars / entry_value) * 100
        
        summary["positions"].append({
            "symbol": symbol,
            "entry": entry,
            "current": current_price,
            "qty": qty,
            "value": current_value,
            "pnl_dollars": pnl_dollars,
            "pnl_percent": pnl_percent
        })
        
        summary["total_value"] += current_value
        summary["total_pnl"] += pnl_dollars
    
    summary["total_pnl_percent"] = (summary["total_pnl"] / summary["total_deployed"]) * 100
    
    return summary

def format_summary(summary):
    """Format summary as Telegram message"""
    if not summary:
        return "❌ Unable to fetch portfolio data"
    
    date = datetime.now().strftime("%b %d, %Y %I:%M %p EST")
    
    msg = f"🐓 **roostr Daily Summary**\n{date}\n\n"
    msg += "**📊 Portfolio:**\n"
    msg += f"Total Deployed: ${summary['total_deployed']:,}\n"
    msg += f"Current Value: ${summary['total_value']:,.0f}\n"
    
    pnl_emoji = "🟢" if summary['total_pnl'] > 0 else "🔴" if summary['total_pnl'] < 0 else "⚪"
    msg += f"{pnl_emoji} Net P&L: ${summary['total_pnl']:+.0f} ({summary['total_pnl_percent']:+.1f}%)\n\n"
    
    msg += "**📍 Positions:**\n"
    for pos in summary["positions"]:
        emoji = "🟢" if pos['pnl_dollars'] > 0 else "🔴" if pos['pnl_dollars'] < 0 else "⚪"
        msg += f"{emoji} **{pos['symbol']}:** ${pos['current']:.2f}\n"
        msg += f"   Entry: ${pos['entry']:.2f} | Qty: {pos['qty']}\n"
        msg += f"   P&L: ${pos['pnl_dollars']:+.0f} ({pos['pnl_percent']:+.1f}%)\n\n"
    
    msg += f"Dashboard: https://joselo-ai.github.io/roostr-research/trading/dashboard.html"
    
    return msg

def post_to_telegram(message):
    """Post summary to Telegram via OpenClaw message tool"""
    # Just print for now - OpenClaw will handle sending via sessions
    print("\n" + "="*50)
    print(message)
    print("="*50 + "\n")
    return message

def main():
    print(f"🐓 Generating daily summary...")
    
    prices = fetch_prices()
    summary = calculate_summary(prices)
    message = format_summary(summary)
    post_to_telegram(message)
    
    # Write to file for OpenClaw to pick up
    with open("/Users/agentjoselo/.openclaw/workspace/trading/daily-summary.txt", "w") as f:
        f.write(message)
    
    print("✅ Summary generated and saved")
    return 0

if __name__ == "__main__":
    exit(main())
