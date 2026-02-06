#!/usr/bin/env python3
"""
Entry Price Validator - Fetch REAL prices before entering positions
NEVER use placeholder/guess prices again
"""

import sys
from datetime import datetime
from price_fetcher import PriceFetcher

def validate_entry(ticker: str, show_targets: bool = True):
    """
    Validate entry price for a ticker before deploying
    
    Args:
        ticker: Crypto ticker (e.g., SOL, TAO, BTC)
        show_targets: Calculate suggested stop-loss and targets
    
    Returns:
        Price data dict or None if validation fails
    """
    
    print("=" * 70)
    print(f"🔍 ENTRY PRICE VALIDATION - {ticker.upper()}")
    print("=" * 70)
    
    # Fetch live price
    fetcher = PriceFetcher(cache_dir='.')
    price_data = fetcher.get_price(ticker, use_cache=False)
    
    if not price_data:
        print(f"\n❌ VALIDATION FAILED: Could not fetch price for {ticker}")
        print("   Cannot enter position without verified price.")
        return None
    
    # Display validation results
    print(f"\n✅ Price Verified from CoinGecko:")
    print(f"   Ticker: {price_data['ticker']}")
    print(f"   Entry Price: ${price_data['price']:,.2f}")
    print(f"   24h Change: {price_data['price_change_24h']:+.2f}%")
    print(f"   Market Cap: ${price_data['market_cap']:,.0f}")
    print(f"   Last Updated: {price_data['last_updated']}")
    print(f"   Source: {price_data['source']}")
    
    # Calculate suggested targets (optional)
    if show_targets:
        entry = price_data['price']
        
        print(f"\n📊 Suggested Risk/Reward Levels:")
        print(f"   Stop Loss (-20%): ${entry * 0.80:,.2f}")
        print(f"   Target 1 (+20%):  ${entry * 1.20:,.2f}")
        print(f"   Target 2 (+50%):  ${entry * 1.50:,.2f}")
        print(f"   Target 3 (+100%): ${entry * 2.00:,.2f}")
    
    # Log entry
    log_entry(ticker, price_data)
    
    print("\n" + "=" * 70)
    print(f"✅ VALIDATED - Ready to enter {ticker.upper()} at ${price_data['price']:,.2f}")
    print("=" * 70)
    
    return price_data


def log_entry(ticker: str, price_data: dict):
    """Log validated entry to file"""
    log_file = 'VALIDATED_ENTRIES.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')
    
    log_line = (f"{timestamp} | {ticker.upper()} | "
                f"${price_data['price']:,.2f} | "
                f"24h: {price_data['price_change_24h']:+.2f}% | "
                f"Source: {price_data['source']}\n")
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_line)
        print(f"\n📝 Logged to {log_file}")
    except Exception as e:
        print(f"\n⚠️  Warning: Could not write to log: {e}")


def calculate_position_size(capital: float, price: float, risk_percent: float = 2.0) -> dict:
    """
    Calculate position size based on capital and risk
    
    Args:
        capital: Total capital to allocate
        price: Entry price per unit
        risk_percent: Risk tolerance (default 2%)
    
    Returns:
        Dict with position sizing info
    """
    position_value = capital
    position_units = position_value / price
    
    # Calculate stop-loss (20% default)
    stop_loss_price = price * 0.80
    risk_per_unit = price - stop_loss_price
    max_units = (capital * (risk_percent / 100)) / risk_per_unit
    
    return {
        'capital_allocated': position_value,
        'entry_price': price,
        'position_units': position_units,
        'position_value_usd': position_value,
        'stop_loss_price': stop_loss_price,
        'risk_per_unit': risk_per_unit,
        'max_units_at_2pct_risk': max_units,
        'recommended_size': min(position_units, max_units)
    }


# CLI Interface
def main():
    """Command-line interface"""
    
    if len(sys.argv) < 2:
        print("Usage: python validate_entry.py <TICKER> [CAPITAL]")
        print("")
        print("Examples:")
        print("  python validate_entry.py SOL")
        print("  python validate_entry.py TAO 8000")
        print("")
        sys.exit(1)
    
    ticker = sys.argv[1]
    capital = float(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # Validate entry price
    price_data = validate_entry(ticker, show_targets=True)
    
    if not price_data:
        sys.exit(1)
    
    # Show position sizing if capital provided
    if capital:
        print(f"\n💰 Position Sizing for ${capital:,.0f} capital:")
        sizing = calculate_position_size(capital, price_data['price'])
        
        print(f"   Entry Price: ${sizing['entry_price']:,.2f}")
        print(f"   Position Value: ${sizing['position_value_usd']:,.0f}")
        print(f"   Units: {sizing['position_units']:,.4f}")
        print(f"   Stop Loss: ${sizing['stop_loss_price']:,.2f}")
        print(f"   Risk per Unit: ${sizing['risk_per_unit']:,.2f}")
        print(f"   Recommended Size (2% risk): {sizing['recommended_size']:,.4f} units")
    
    print("\n✅ Ready to deploy. Use this EXACT price in signals-database.csv")
    print(f"   Entry: {price_data['price']:.2f}")


if __name__ == "__main__":
    main()
