#!/usr/bin/env python3
"""
ROOSTR POSITION SIZING CALCULATOR
Based on Kelly Criterion and Risk Management Framework

Usage:
    python position_sizing_calculator.py --account 10000 --risk 2 --entry 100 --stop 95
"""

import argparse
import math


def kelly_criterion(win_rate, avg_win, avg_loss):
    """
    Calculate optimal Kelly fraction
    
    f* = (p * b - q) / b
    where:
        p = win rate
        q = loss rate (1 - p)
        b = avg_win / avg_loss (win/loss ratio)
    """
    if avg_loss == 0:
        return 0
    
    q = 1 - win_rate
    b = avg_win / avg_loss
    
    kelly_fraction = (win_rate * b - q) / b
    
    return max(0, kelly_fraction)  # Kelly can't be negative


def calculate_position_size(account_balance, risk_percent, entry_price, stop_loss_price, max_position_pct=5.0):
    """
    Calculate position size based on risk management rules
    
    Returns:
        - Position size in shares/units
        - Dollar amount at risk
        - Position value
        - Percent of portfolio
    """
    # Risk amount in dollars
    risk_dollars = account_balance * (risk_percent / 100)
    
    # Price risk per share
    price_risk = abs(entry_price - stop_loss_price)
    
    if price_risk == 0:
        return 0, 0, 0, 0
    
    # Position size (shares/units)
    position_size = risk_dollars / price_risk
    
    # Total position value
    position_value = position_size * entry_price
    
    # Position as % of portfolio
    position_pct = (position_value / account_balance) * 100
    
    # Enforce max position size limit
    if position_pct > max_position_pct:
        # Reduce position to hit max %
        position_size = (account_balance * (max_position_pct / 100)) / entry_price
        position_value = position_size * entry_price
        position_pct = max_position_pct
        risk_dollars = position_size * price_risk
        risk_percent = (risk_dollars / account_balance) * 100
    
    return position_size, risk_dollars, position_value, position_pct, risk_percent


def calculate_take_profit_targets(entry_price, stop_loss_price, r_multiples=[2, 3, 5]):
    """
    Calculate take profit targets based on R-multiples
    
    R = initial risk
    Target = Entry + (R * R_multiple)
    """
    risk = abs(entry_price - stop_loss_price)
    
    targets = []
    for r_mult in r_multiples:
        if entry_price > stop_loss_price:  # Long position
            target_price = entry_price + (risk * r_mult)
        else:  # Short position
            target_price = entry_price - (risk * r_mult)
        
        targets.append({
            'r_multiple': r_mult,
            'price': target_price,
            'gain_pct': ((target_price - entry_price) / entry_price) * 100
        })
    
    return targets


def main():
    parser = argparse.ArgumentParser(description='ROOSTR Position Sizing Calculator')
    parser.add_argument('--account', type=float, required=True, help='Account balance ($)')
    parser.add_argument('--risk', type=float, required=True, help='Risk per trade (%)')
    parser.add_argument('--entry', type=float, required=True, help='Entry price ($)')
    parser.add_argument('--stop', type=float, required=True, help='Stop loss price ($)')
    parser.add_argument('--max-position', type=float, default=5.0, help='Max position size (% of portfolio)')
    parser.add_argument('--targets', nargs='+', type=float, default=[2, 3, 5], help='R-multiple targets (default: 2 3 5)')
    
    # Kelly calculator mode
    parser.add_argument('--kelly', action='store_true', help='Calculate Kelly criterion')
    parser.add_argument('--win-rate', type=float, help='Historical win rate (%) for Kelly')
    parser.add_argument('--avg-win', type=float, help='Average win (%) for Kelly')
    parser.add_argument('--avg-loss', type=float, help='Average loss (%) for Kelly')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🧮 ROOSTR POSITION SIZING CALCULATOR")
    print("="*60 + "\n")
    
    # Calculate position size
    position_size, risk_dollars, position_value, position_pct, actual_risk_pct = calculate_position_size(
        args.account,
        args.risk,
        args.entry,
        args.stop,
        args.max_position
    )
    
    print(f"ACCOUNT BALANCE: ${args.account:,.2f}")
    print(f"RISK PER TRADE: {args.risk}% → ${risk_dollars:,.2f}")
    print(f"\n" + "-"*60)
    print("POSITION SIZING")
    print("-"*60)
    print(f"Entry Price: ${args.entry:.2f}")
    print(f"Stop Loss: ${args.stop:.2f}")
    print(f"Risk per Share: ${abs(args.entry - args.stop):.2f}\n")
    
    print(f"✅ POSITION SIZE: {position_size:.2f} shares/units")
    print(f"✅ POSITION VALUE: ${position_value:,.2f} ({position_pct:.1f}% of portfolio)")
    print(f"✅ ACTUAL RISK: ${risk_dollars:,.2f} ({actual_risk_pct:.2f}%)")
    
    if position_pct >= args.max_position:
        print(f"\n⚠️  WARNING: Position capped at {args.max_position}% portfolio limit!")
    
    # Take profit targets
    print(f"\n" + "-"*60)
    print("TAKE PROFIT TARGETS")
    print("-"*60)
    
    targets = calculate_take_profit_targets(args.entry, args.stop, args.targets)
    
    for i, target in enumerate(targets, 1):
        r_mult = target['r_multiple']
        price = target['price']
        gain_pct = target['gain_pct']
        profit_dollars = position_size * (price - args.entry)
        
        print(f"\nTarget {i} ({r_mult}R): ${price:.2f}")
        print(f"  └─ Gain: {gain_pct:+.1f}% (${profit_dollars:+,.2f})")
        print(f"  └─ Suggested exit: {[50, 30, 20][i-1] if i <= 3 else 100}% of position")
    
    # Risk/Reward analysis
    print(f"\n" + "-"*60)
    print("RISK/REWARD ANALYSIS")
    print("-"*60)
    
    risk_pct = ((args.stop - args.entry) / args.entry) * 100
    print(f"Risk: {abs(risk_pct):.2f}% from entry to stop")
    
    for target in targets:
        r_mult = target['r_multiple']
        reward_pct = target['gain_pct']
        print(f"{r_mult}R Target: {reward_pct:.2f}% potential gain (R:R = 1:{r_mult})")
    
    # Kelly Criterion (if requested)
    if args.kelly and args.win_rate and args.avg_win and args.avg_loss:
        print(f"\n" + "-"*60)
        print("KELLY CRITERION ANALYSIS")
        print("-"*60)
        
        win_rate_decimal = args.win_rate / 100
        avg_win_decimal = args.avg_win / 100
        avg_loss_decimal = abs(args.avg_loss) / 100
        
        kelly_full = kelly_criterion(win_rate_decimal, avg_win_decimal, avg_loss_decimal)
        kelly_half = kelly_full * 0.5
        kelly_quarter = kelly_full * 0.25
        
        print(f"Historical Win Rate: {args.win_rate}%")
        print(f"Avg Win: {args.avg_win}% | Avg Loss: {args.avg_loss}%")
        print(f"\nKelly Fraction (full): {kelly_full*100:.1f}% of portfolio")
        print(f"Kelly Fraction (half, recommended): {kelly_half*100:.1f}% of portfolio")
        print(f"Kelly Fraction (quarter, conservative): {kelly_quarter*100:.1f}% of portfolio")
        
        print(f"\n💡 RECOMMENDATION:")
        if kelly_half * 100 > 10:
            print(f"   Your edge is strong, but {kelly_half*100:.1f}% per position is aggressive.")
            print(f"   Consider 5-10% max position size for safety.")
        elif kelly_half * 100 < 2:
            print(f"   Your edge is weak ({kelly_half*100:.1f}%). Improve win rate or R-multiple.")
            print(f"   Recommended: Win rate >50% AND avg R-multiple >2.0")
        else:
            print(f"   Position size of {kelly_half*100:.1f}% is reasonable given your edge.")
    
    # Risk Warnings
    print(f"\n" + "-"*60)
    print("⚠️  RISK CHECKS")
    print("-"*60)
    
    warnings = []
    
    if args.risk > 5:
        warnings.append(f"Risk per trade ({args.risk}%) exceeds 5% - HIGH RISK!")
    
    if position_pct > 10:
        warnings.append(f"Position size ({position_pct:.1f}%) exceeds 10% - CONCENTRATION RISK!")
    
    if abs(risk_pct) > 20:
        warnings.append(f"Stop loss ({abs(risk_pct):.1f}%) is very wide - consider tighter stop")
    
    if len(targets) > 0 and targets[0]['r_multiple'] < 1.5:
        warnings.append(f"First target is <1.5R - consider wider profit target")
    
    if warnings:
        for warning in warnings:
            print(f"⚠️  {warning}")
    else:
        print("✅ All risk checks passed!")
    
    print(f"\n" + "="*60)
    print("Remember: A good trade is one you can walk away from.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
