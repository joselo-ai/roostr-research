#!/usr/bin/env python3
"""
Video Script Generator
Converts trading logs/updates into HeyGen video scripts
"""

from datetime import datetime
from pathlib import Path
import json

def generate_daily_update_script(date, positions, pnl, top_signals):
    """Generate script for daily trading update"""
    
    date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
    
    script = f"""Hey everyone, this is your daily trading update for {date_str}.

Let me walk you through what's happening in our portfolio today.

"""
    
    # Portfolio summary
    if pnl >= 0:
        script += f"We're currently up {abs(pnl):.1f}% on the day. "
    else:
        script += f"We're down {abs(pnl):.1f}% today, but staying disciplined. "
    
    script += "\n\n"
    
    # Positions
    if positions:
        script += "Looking at our positions:\n\n"
        for pos in positions:
            ticker = pos['ticker']
            price = pos['price']
            pnl_pct = pos['pnl_pct']
            rsi = pos.get('rsi', 0)
            
            if pnl_pct >= 0:
                script += f"{ticker} is at ${price:.2f}, up {pnl_pct:.1f}%. "
            else:
                script += f"{ticker} is at ${price:.2f}, down {abs(pnl_pct):.1f}%. "
            
            if rsi:
                if rsi < 30:
                    script += f"RSI is {rsi:.1f}, which is oversold territory. "
                elif rsi > 70:
                    script += f"RSI is {rsi:.1f}, overbought. "
                else:
                    script += f"RSI at {rsi:.1f}, neutral zone. "
            
            script += "\n\n"
    
    # Top signals
    if top_signals:
        script += "We're watching a few opportunities:\n\n"
        for signal in top_signals[:3]:
            script += f"{signal['ticker']} looks interesting. "
            script += f"Conviction score is {signal['conviction']} out of 10. "
            script += f"{signal['notes']}\n\n"
    
    script += """That's it for today. 

Remember, we're building this in public. Wins and losses, all transparent.

See you tomorrow."""
    
    return script

def generate_system_update_script(title, description, impact):
    """Generate script for system/integration updates"""
    
    script = f"""Hey everyone, quick update.

We just deployed {title}.

{description}

{impact}

This is what building in public looks like. Fast iterations, real improvements.

Back to work."""
    
    return script

def generate_tradingview_integration_script():
    """Generate script about TradingView integration (today's win)"""
    
    return """Hey everyone, I want to show you what we just built in the last hour.

We integrated TradingView into our trading infrastructure.

Before, we were scraping prices from CoinGecko, dealing with rate limits, getting delayed data. Not ideal.

Now, we're pulling real-time prices, RSI indicators, and trading signals directly from TradingView. No rate limits. No delays.

We also built a webhook system. When TradingView fires an alert, like if TAO crosses above 160 dollars, it hits our server and sends a Telegram notification instantly.

This took 20 minutes to build. And it's already running.

Our risk monitor now has RSI context. Our price updates show technical signals. And we can set up custom alerts for any condition we want.

This is the kind of infrastructure that hedge funds spend months building. We did it in 20 minutes because we automated the right things.

Next up, we're adding more alerts, backtesting capabilities, and multi-asset tracking.

Building in public. Full transparency. No BS.

That's it for today."""

if __name__ == "__main__":
    # Test script generation
    script = generate_tradingview_integration_script()
    print("=" * 60)
    print("📝 Generated Script:")
    print("=" * 60)
    print(script)
    print("=" * 60)
    print(f"\n✅ Word count: {len(script.split())}")
    print(f"✅ Character count: {len(script)}")
