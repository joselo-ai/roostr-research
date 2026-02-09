#!/usr/bin/env python3
"""
Position Size Calculator - Calculate optimal position sizing for roostr trades
Enforces risk management rules across all 4 buckets
"""

from typing import Dict, Tuple
import sys

class PositionCalculator:
    """Calculate position sizes with risk management"""
    
    def __init__(self, total_capital: float = 100000):
        self.total_capital = total_capital
        
        # Bucket allocations
        self.buckets = {
            'riz_eurusd': {
                'allocation': 40000,
                'max_risk_per_trade': 0.005,  # 0.5%
                'max_deployed_pct': 0.40  # Max 40% of bucket at once
            },
            'social_arb': {
                'allocation': 30000,
                'max_risk_per_trade': 0.02,  # 2%
                'max_deployed_pct': 0.50  # Max 50% of bucket
            },
            'crypto': {
                'allocation': 20000,
                'max_risk_per_trade': 0.05,  # 5% (accept drawdowns)
                'max_deployed_pct': 0.60  # Can deploy 60%
            },
            'opportunistic': {
                'allocation': 10000,
                'max_risk_per_trade': 0.10,  # 10% (moonshots)
                'max_deployed_pct': 1.0  # Can deploy 100%
            }
        }
    
    def calculate_position(
        self,
        bucket: str,
        entry_price: float,
        stop_loss: float,
        conviction: int = 5
    ) -> Dict:
        """
        Calculate position size based on risk management rules
        
        Args:
            bucket: 'riz_eurusd', 'social_arb', 'crypto', 'opportunistic'
            entry_price: Entry price
            stop_loss: Stop loss price
            conviction: 1-10 scale (affects position size)
            
        Returns:
            Dict with position_size, shares, risk_dollars, risk_percent
        """
        
        if bucket not in self.buckets:
            raise ValueError(f"Invalid bucket: {bucket}")
        
        bucket_config = self.buckets[bucket]
        bucket_capital = bucket_config['allocation']
        max_risk_pct = bucket_config['max_risk_per_trade']
        
        # Risk per share
        risk_per_share = abs(entry_price - stop_loss)
        
        if risk_per_share == 0:
            raise ValueError("Entry and stop loss cannot be the same")
        
        # Base position size (risk-based)
        max_risk_dollars = self.total_capital * max_risk_pct
        shares = max_risk_dollars / risk_per_share
        position_size = shares * entry_price
        
        # Adjust for conviction (scale up/down by 20% max)
        conviction_multiplier = 0.8 + (conviction / 10) * 0.4  # Range: 0.8 to 1.2
        position_size *= conviction_multiplier
        shares *= conviction_multiplier
        
        # Cap at max deployed percentage
        max_position = bucket_capital * bucket_config['max_deployed_pct']
        if position_size > max_position:
            position_size = max_position
            shares = position_size / entry_price
        
        # Recalculate actual risk
        actual_risk_dollars = shares * risk_per_share
        actual_risk_pct = actual_risk_dollars / self.total_capital
        
        return {
            'bucket': bucket,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'position_size_dollars': round(position_size, 2),
            'shares': round(shares, 2),
            'risk_dollars': round(actual_risk_dollars, 2),
            'risk_percent': round(actual_risk_pct * 100, 2),
            'conviction': conviction,
            'bucket_allocation': bucket_capital,
            'pct_of_bucket': round(position_size / bucket_capital * 100, 1)
        }
    
    def print_position(self, result: Dict):
        """Pretty print position calculation"""
        
        print(f"\n{'='*60}")
        print(f"🎯 Position Size Calculator - {result['bucket'].upper().replace('_', ' ')}")
        print(f"{'='*60}")
        print(f"\n📊 ENTRY DETAILS")
        print(f"  Entry Price:        ${result['entry_price']:,.2f}")
        print(f"  Stop Loss:          ${result['stop_loss']:,.2f}")
        print(f"  Risk Per Share:     ${abs(result['entry_price'] - result['stop_loss']):,.2f}")
        print(f"  Conviction:         {result['conviction']}/10")
        
        print(f"\n💰 POSITION SIZE")
        print(f"  Shares/Units:       {result['shares']:,.2f}")
        print(f"  Position Value:     ${result['position_size_dollars']:,.2f}")
        print(f"  % of Bucket:        {result['pct_of_bucket']}%")
        
        print(f"\n⚠️  RISK MANAGEMENT")
        print(f"  Risk (if stopped):  ${result['risk_dollars']:,.2f}")
        print(f"  Risk % Portfolio:   {result['risk_percent']}%")
        print(f"  Bucket Allocation:  ${result['bucket_allocation']:,.0f}")
        
        # Warning if risk is high
        if result['risk_percent'] > 2.5:
            print(f"\n🚨 WARNING: Risk exceeds 2.5% of portfolio!")
        
        print(f"\n{'='*60}\n")
    
    def calculate_targets(
        self,
        entry_price: float,
        stop_loss: float,
        r_multiples: list = [2, 5, 10]
    ) -> Dict:
        """
        Calculate profit targets based on R multiples
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            r_multiples: List of R multiples (default: 2R, 5R, 10R)
            
        Returns:
            Dict with target prices and profit amounts
        """
        
        risk = abs(entry_price - stop_loss)
        direction = 1 if entry_price > stop_loss else -1
        
        targets = {}
        for r in r_multiples:
            target_price = entry_price + (direction * risk * r)
            targets[f"{r}R"] = round(target_price, 2)
        
        return targets
    
    def portfolio_risk_check(self, open_positions: list) -> Dict:
        """
        Check total portfolio risk across all positions
        
        Args:
            open_positions: List of position dicts with risk_dollars
            
        Returns:
            Dict with total risk and warnings
        """
        
        total_risk = sum(pos.get('risk_dollars', 0) for pos in open_positions)
        total_risk_pct = total_risk / self.total_capital * 100
        
        # Check per-bucket deployment
        bucket_deployed = {bucket: 0 for bucket in self.buckets.keys()}
        
        for pos in open_positions:
            bucket = pos.get('bucket', 'opportunistic')
            bucket_deployed[bucket] += pos.get('position_size_dollars', 0)
        
        warnings = []
        
        # Portfolio-level warnings
        if total_risk_pct > 10:
            warnings.append(f"🚨 CRITICAL: Total portfolio risk {total_risk_pct:.1f}% exceeds 10%")
        elif total_risk_pct > 5:
            warnings.append(f"⚠️  HIGH: Total portfolio risk {total_risk_pct:.1f}% exceeds 5%")
        
        # Bucket-level warnings
        for bucket, deployed in bucket_deployed.items():
            bucket_config = self.buckets[bucket]
            max_deployed = bucket_config['allocation'] * bucket_config['max_deployed_pct']
            
            if deployed > max_deployed:
                warnings.append(
                    f"⚠️  {bucket.upper()}: Deployed ${deployed:,.0f} exceeds max ${max_deployed:,.0f}"
                )
        
        return {
            'total_risk_dollars': round(total_risk, 2),
            'total_risk_percent': round(total_risk_pct, 2),
            'bucket_deployed': bucket_deployed,
            'warnings': warnings,
            'status': 'OK' if not warnings else 'WARNING'
        }


# CLI Interface

def interactive_mode():
    """Interactive position calculator"""
    
    calc = PositionCalculator()
    
    print("\n🐓 roostr Position Size Calculator")
    print("="*60)
    
    # Select bucket
    print("\nSelect bucket:")
    print("  1. Riz EURUSD (40% allocation)")
    print("  2. Social Arbitrage (30% allocation)")
    print("  3. Crypto Fundamentals (20% allocation)")
    print("  4. Opportunistic/Research (10% allocation)")
    
    bucket_map = {
        '1': 'riz_eurusd',
        '2': 'social_arb',
        '3': 'crypto',
        '4': 'opportunistic'
    }
    
    choice = input("\nChoice (1-4): ").strip()
    bucket = bucket_map.get(choice)
    
    if not bucket:
        print("Invalid choice")
        return
    
    # Get trade details
    try:
        entry = float(input("Entry Price: $").strip())
        stop = float(input("Stop Loss: $").strip())
        conviction = int(input("Conviction (1-10): ").strip())
        
        if not 1 <= conviction <= 10:
            print("Conviction must be 1-10")
            return
        
    except ValueError:
        print("Invalid input")
        return
    
    # Calculate
    result = calc.calculate_position(bucket, entry, stop, conviction)
    calc.print_position(result)
    
    # Show targets
    targets = calc.calculate_targets(entry, stop)
    print("🎯 PROFIT TARGETS (R multiples):")
    for target, price in targets.items():
        print(f"  {target}: ${price:,.2f}")
    
    print()


def quick_calc(bucket: str, entry: float, stop: float, conviction: int = 5):
    """Quick calculation via command line"""
    
    calc = PositionCalculator()
    result = calc.calculate_position(bucket, entry, stop, conviction)
    calc.print_position(result)
    
    targets = calc.calculate_targets(entry, stop)
    print("🎯 PROFIT TARGETS:")
    for target, price in targets.items():
        print(f"  {target}: ${price:,.2f}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Interactive mode
        interactive_mode()
    elif len(sys.argv) >= 4:
        # Quick mode: python3 calc.py crypto 100 95 8
        bucket = sys.argv[1]
        entry = float(sys.argv[2])
        stop = float(sys.argv[3])
        conviction = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        
        quick_calc(bucket, entry, stop, conviction)
    else:
        print("Usage:")
        print("  python3 calc.py                          # Interactive mode")
        print("  python3 calc.py <bucket> <entry> <stop> [conviction]")
        print("\nExample:")
        print("  python3 calc.py crypto 100 95 8")
        print("\nBuckets: riz_eurusd, social_arb, crypto, opportunistic")
