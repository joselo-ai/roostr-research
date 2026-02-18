#!/usr/bin/env python3
"""
Price Updater v2 - TradingView Integration
Fetches TAO/SOL prices + technicals from TradingView and updates index.html
Run hourly via cron (no rate limits!)
"""

from tradingview_ta import TA_Handler, Interval
import json
from datetime import datetime
import re
from pathlib import Path

# Activity logging
import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/command-center')
from activity_logger import log_trading, log_automation


DASHBOARD_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/dashboard.html"
POSITIONS_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/PAPER-TRADING-LOG.md"
CACHE_PATH = "/Users/agentjoselo/.openclaw/workspace/trading/.price_cache.json"

# Position details
POSITIONS = {
    "TAO": {
        "symbol": "TAOUSD",
        "exchange": "BINANCE",
        "entry": 176.05,
        "quantity": 56.8,
        "stop": 140.84
    },
    "SOL": {
        "symbol": "SOLUSD",
        "exchange": "BINANCE",
        "entry": 86.51,
        "quantity": 86.7,
        "stop": 73.53
    }
}

def load_cache():
    """Load cached prices"""
    if Path(CACHE_PATH).exists():
        try:
            with open(CACHE_PATH, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_cache(prices):
    """Save prices to cache"""
    try:
        with open(CACHE_PATH, 'w') as f:
            json.dump({
                "prices": prices,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save cache: {e}")

def fetch_prices():
    """Fetch current prices + technicals from TradingView"""
    prices = {}
    
    for symbol, details in POSITIONS.items():
        try:
            handler = TA_Handler(
                symbol=details["symbol"],
                exchange=details["exchange"],
                screener='crypto',
                interval=Interval.INTERVAL_1_HOUR
            )
            analysis = handler.get_analysis()
            
            prices[symbol] = {
                "price": analysis.indicators["close"],
                "rsi": analysis.indicators.get("RSI", 0),
                "recommendation": analysis.summary["RECOMMENDATION"],
                "oscillators": analysis.oscillators["RECOMMENDATION"],
                "moving_averages": analysis.moving_averages["RECOMMENDATION"]
            }
            
        except Exception as e:
            print(f"⚠️  Error fetching {symbol}: {e}")
            # Try cache
            cache = load_cache()
            if cache and symbol in cache.get("prices", {}):
                prices[symbol] = cache["prices"][symbol]
                print(f"   Using cached {symbol} from {cache.get('timestamp', 'unknown')}")
            else:
                return None
    
    # Save to cache
    if len(prices) == 2:
        save_cache(prices)
    
    return prices

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
    """Update index.html with current prices"""
    if not prices or len(prices) != 2:
        return False
    
    # Read dashboard
    with open(DASHBOARD_PATH, 'r') as f:
        html = f.read()
    
    # Calculate totals
    tao_pnl = calculate_pnl("TAO", prices["TAO"]["price"])
    sol_pnl = calculate_pnl("SOL", prices["SOL"]["price"])
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
        f'\\1${prices["TAO"]["price"]:.2f}',
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
        f'\\1${prices["SOL"]["price"]:.2f}',
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
    
    print(f"✅ Dashboard updated: TAO ${prices['TAO']['price']:.2f}, SOL ${prices['SOL']['price']:.2f}, P&L ${total_pnl:.0f}")
    print(f"   TAO: RSI {prices['TAO']['rsi']:.1f} | {prices['TAO']['recommendation']}")
    print(f"   SOL: RSI {prices['SOL']['rsi']:.1f} | {prices['SOL']['recommendation']}")
    
    log_trading("Price update (TradingView)", {
        "TAO": prices['TAO']['price'],
        "TAO_RSI": prices['TAO']['rsi'],
        "TAO_signal": prices['TAO']['recommendation'],
        "SOL": prices['SOL']['price'],
        "SOL_RSI": prices['SOL']['rsi'],
        "SOL_signal": prices['SOL']['recommendation'],
        "P&L": total_pnl
    })
    return True

def main():
    print(f"🐓 Price Updater v2 (TradingView) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Frequency: Hourly (0 * * * *)")
    
    prices = fetch_prices()
    if prices and len(prices) == 2:
        update_dashboard(prices)
        log_automation("Price update (TradingView)", {
            "status": "success",
            "TAO": prices["TAO"]["price"],
            "TAO_RSI": prices["TAO"]["rsi"],
            "SOL": prices["SOL"]["price"],
            "SOL_RSI": prices["SOL"]["rsi"]
        })
        return 0
    else:
        print("⚠️  Price update skipped (will retry next hour)")
        log_automation("Price update", {"status": "skipped", "reason": "tradingview_error"})
        return 0

if __name__ == "__main__":
    exit(main())
