#!/usr/bin/env python3
"""
EMERGENCY FIX - Correct TAO and SOL entries with REAL prices
Recalculate position sizes and P&L with verified CoinGecko data
"""

import csv
from datetime import datetime
from price_fetcher import PriceFetcher

def fix_positions():
    """Fix TAO and SOL positions with real prices"""
    
    print("=" * 70)
    print("🚨 EMERGENCY FIX - Correcting Fake Prices")
    print("=" * 70)
    
    # Initialize price fetcher
    fetcher = PriceFetcher(cache_dir='.')
    
    # Fetch REAL prices
    print("\n📡 Fetching REAL prices from CoinGecko...")
    prices = fetcher.get_multiple_prices(['SOL', 'TAO'], use_cache=False)
    
    if 'SOL' not in prices or 'TAO' not in prices:
        print("❌ Failed to fetch prices. Aborting.")
        return
    
    sol_real = prices['SOL']['price']
    tao_real = prices['TAO']['price']
    
    print(f"\n✅ Real Prices Verified:")
    print(f"   SOL: ${sol_real:.2f}")
    print(f"   TAO: ${tao_real:.2f}")
    
    # Read current database
    signals = []
    with open('signals-database.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            signals.append(row)
    
    # Fix positions
    fixes_made = []
    
    for signal in signals:
        ticker = signal.get('Ticker', '').upper()
        
        if ticker == 'SOL' and signal.get('Deployed') == 'YES':
            old_price = float(signal.get('Price_Entry', 0))
            old_size = float(signal.get('Position_Size', 0))
            
            # Calculate what position size SHOULD be at real price
            # If we allocated $6000, position size should be 6000 / real_price
            allocated_capital = old_price * old_size if old_price > 0 else old_size
            
            # Use the allocated capital to recalculate position at real price
            new_size = allocated_capital / sol_real if sol_real > 0 else 0
            
            signal['Price_Entry'] = f"{sol_real:.2f}"
            signal['Current_Price'] = f"{sol_real:.2f}"
            signal['Position_Size'] = f"{allocated_capital:.0f}"  # Keep dollar allocation same
            
            # Recalculate P&L (currently zero since we just "entered")
            signal['PnL_Dollars'] = "0"
            signal['PnL_Percent'] = "0.00"
            
            # Update notes
            signal['Notes'] = (f"PRICE CORRECTED: Was ${old_price:.2f} (fake), "
                              f"now ${sol_real:.2f} (verified CoinGecko {datetime.now().strftime('%Y-%m-%d %H:%M')}). "
                              f"{signal.get('Notes', '')}")
            
            fixes_made.append({
                'ticker': 'SOL',
                'old_price': old_price,
                'new_price': sol_real,
                'error_pct': ((old_price - sol_real) / sol_real * 100) if sol_real > 0 else 0
            })
        
        elif ticker == 'TAO' and signal.get('Deployed') == 'YES':
            old_price = float(signal.get('Price_Entry', 0))
            old_size = float(signal.get('Position_Size', 0))
            
            # Calculate allocated capital
            allocated_capital = old_price * old_size if old_price > 0 else old_size
            
            # Recalculate position at real price
            new_size = allocated_capital / tao_real if tao_real > 0 else 0
            
            signal['Price_Entry'] = f"{tao_real:.2f}"
            signal['Current_Price'] = f"{tao_real:.2f}"
            signal['Position_Size'] = f"{allocated_capital:.0f}"  # Keep dollar allocation same
            
            # Recalculate P&L
            signal['PnL_Dollars'] = "0"
            signal['PnL_Percent'] = "0.00"
            
            # Update notes
            signal['Notes'] = (f"PRICE CORRECTED: Was ${old_price:.2f} (fake), "
                              f"now ${tao_real:.2f} (verified CoinGecko {datetime.now().strftime('%Y-%m-%d %H:%M')}). "
                              f"{signal.get('Notes', '')}")
            
            fixes_made.append({
                'ticker': 'TAO',
                'old_price': old_price,
                'new_price': tao_real,
                'error_pct': ((old_price - tao_real) / tao_real * 100) if tao_real > 0 else 0
            })
    
    # Write back to CSV
    if fixes_made:
        print(f"\n🔧 Fixing {len(fixes_made)} positions...")
        
        with open('signals-database.csv', 'w', newline='') as f:
            fieldnames = signals[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(signals)
        
        print("✅ Database updated: signals-database.csv")
        
        # Show what was fixed
        print("\n📊 Corrections Made:")
        print("-" * 70)
        for fix in fixes_made:
            print(f"   {fix['ticker']}: ${fix['old_price']:.2f} → ${fix['new_price']:.2f} "
                  f"(ERROR: {fix['error_pct']:+.1f}%)")
        print("-" * 70)
        
        # Regenerate dashboard
        print("\n🔄 Regenerating dashboard with corrected prices...")
        import subprocess
        subprocess.run(['python3', 'update_dashboard.py'])
        
        print("\n" + "=" * 70)
        print("✅ POSITIONS FIXED - Dashboard Updated")
        print("=" * 70)
        print("\n💡 G was right: NEVER use placeholder prices again!")
        print("   Use validate_entry.py for all future positions.")
        
    else:
        print("\n⚠️  No positions found to fix.")


if __name__ == "__main__":
    fix_positions()
