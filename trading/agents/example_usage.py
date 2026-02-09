#!/usr/bin/env python3
"""
Quant Agent - Usage Examples
=============================

Demonstrates various ways to use the Quant Agent for backtesting
and statistical analysis.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.quant_agent import QuantAgent
from backtest import BacktestConfig, Backtester
from validation import SignalValidator
import pandas as pd


def example_1_quick_backtest():
    """Example 1: Quick single-trade backtest"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Quick Single-Trade Backtest")
    print("="*60)
    
    agent = QuantAgent()
    
    # Test the TAO signal
    result = agent.quick_backtest(
        ticker='TAO',
        entry_price=176.05,
        entry_date='2026-02-06'
    )
    
    print(f"\n📊 Result: {result['return_pct']:+.2f}% return over {result['hold_days']} days")
    

def example_2_full_analysis():
    """Example 2: Full strategy analysis with all signals"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Full Strategy Analysis")
    print("="*60)
    
    agent = QuantAgent()
    
    # Run complete analysis
    report = agent.analyze_strategy(signals_source='database')
    
    # Metrics are available
    metrics = agent.backtester.calculate_metrics()
    print(f"\n📈 Key Metrics:")
    print(f"   Win Rate: {metrics['win_rate_pct']:.1f}%")
    print(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"   Total Return: {metrics['total_return_pct']:+.2f}%")


def example_3_custom_config():
    """Example 3: Custom configuration"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Configuration")
    print("="*60)
    
    # Create custom configuration
    config = BacktestConfig(
        starting_capital=50000,      # Start with $50k
        position_size_pct=0.15,      # 15% per position
        stop_loss_pct=0.15,          # 15% stop loss
        take_profit_pct=0.40,        # 40% take profit target
        max_hold_days=60             # Exit after 60 days max
    )
    
    agent = QuantAgent(config)
    
    print(f"✅ Custom configuration loaded:")
    print(f"   Capital: ${config.starting_capital:,}")
    print(f"   Position Size: {config.position_size_pct*100}%")
    print(f"   Risk/Reward: {config.take_profit_pct/config.stop_loss_pct:.2f}:1")


def example_4_position_sizing():
    """Example 4: Calculate optimal position sizing"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Position Sizing Recommendation")
    print("="*60)
    
    agent = QuantAgent()
    
    # Load signals and run backtest to build performance history
    agent.load_signals('database')
    agent.run_backtest()
    
    # Now calculate position sizing for a new trade
    sizing = agent.calculate_position_sizing(
        ticker='BTC',
        entry_price=50000,
        risk_per_trade=0.02  # 2% risk per trade
    )
    
    print(f"\n💰 Position Sizing for BTC @ $50,000:")
    print(f"   Recommended Shares: {sizing['recommended_shares']:.2f}")
    print(f"   Position Value: ${sizing['recommended_value']:,.2f}")
    print(f"   % of Portfolio: {sizing['recommended_pct_portfolio']:.2f}%")
    print(f"   Stop Loss Price: ${sizing['stop_loss_price']:,.2f}")
    print(f"   Risk/Reward: {sizing['risk_reward_ratio']:.2f}:1")


def example_5_statistical_validation():
    """Example 5: Statistical validation standalone"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Statistical Validation")
    print("="*60)
    
    agent = QuantAgent()
    agent.load_signals('database')
    agent.run_backtest()
    
    # Run detailed validation tests
    validation = agent.run_validation()
    
    if 'significance' in validation:
        sig = validation['significance']
        print(f"\n📊 Statistical Significance:")
        print(f"   T-Statistic: {sig['t_statistic']:.4f}")
        print(f"   P-Value: {sig['p_value']:.4f}")
        print(f"   Mean Return: {sig['mean_return']:.2f}%")
        print(f"   Assessment: {sig['significance']}")
    
    if 'monte_carlo' in validation:
        mc = validation['monte_carlo']
        print(f"\n🎲 Monte Carlo Simulation:")
        print(f"   Percentile Rank: {mc['percentile_rank']:.1f}%")
        print(f"   Assessment: {mc['interpretation']}")


def example_6_compare_strategies():
    """Example 6: Compare different strategy configurations"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Strategy Comparison")
    print("="*60)
    
    strategies = [
        {
            'name': 'Conservative',
            'config': BacktestConfig(
                position_size_pct=0.05,
                stop_loss_pct=0.10,
                take_profit_pct=0.20
            )
        },
        {
            'name': 'Moderate',
            'config': BacktestConfig(
                position_size_pct=0.10,
                stop_loss_pct=0.20,
                take_profit_pct=0.30
            )
        },
        {
            'name': 'Aggressive',
            'config': BacktestConfig(
                position_size_pct=0.20,
                stop_loss_pct=0.30,
                take_profit_pct=0.50
            )
        }
    ]
    
    print("\n📊 Comparing 3 strategies...\n")
    
    results = []
    
    for strategy in strategies:
        agent = QuantAgent(strategy['config'])
        agent.load_signals('database')
        agent.run_backtest()
        metrics = agent.backtester.calculate_metrics()
        
        results.append({
            'name': strategy['name'],
            'return': metrics['total_return_pct'],
            'sharpe': metrics['sharpe_ratio'],
            'drawdown': metrics['max_drawdown_pct']
        })
    
    # Print comparison table
    print(f"{'Strategy':<15} {'Return %':<12} {'Sharpe':<10} {'Max DD %':<10}")
    print("-" * 50)
    for r in results:
        print(f"{r['name']:<15} {r['return']:>10.2f}  {r['sharpe']:>8.2f}  {r['drawdown']:>8.2f}")


def example_7_export_trades():
    """Example 7: Export and analyze individual trades"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Export Trade Details")
    print("="*60)
    
    agent = QuantAgent()
    agent.load_signals('database')
    agent.run_backtest()
    
    # Export trades to CSV
    export_path = Path(__file__).parent.parent / 'reports' / 'detailed_trades.csv'
    agent.backtester.export_trades(str(export_path))
    
    # Read back and analyze
    trades_df = pd.DataFrame([vars(t) for t in agent.backtester.trades])
    
    if not trades_df.empty:
        print(f"\n📊 Trade Analysis:")
        print(f"   Total Trades: {len(trades_df)}")
        print(f"\n   By Exit Reason:")
        print(trades_df['exit_reason'].value_counts())
        
        print(f"\n   Average Hold Time by Outcome:")
        wins = trades_df[trades_df['pnl_net'] > 0]['hold_days'].mean()
        losses = trades_df[trades_df['pnl_net'] <= 0]['hold_days'].mean()
        print(f"   Winners: {wins:.1f} days")
        print(f"   Losers: {losses:.1f} days")


def run_all_examples():
    """Run all examples in sequence"""
    examples = [
        example_1_quick_backtest,
        example_2_full_analysis,
        example_3_custom_config,
        example_4_position_sizing,
        example_5_statistical_validation,
        example_6_compare_strategies,
        example_7_export_trades
    ]
    
    print("\n" + "🚀 QUANT AGENT - USAGE EXAMPLES ".center(60, "="))
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Example failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Quant Agent Usage Examples')
    parser.add_argument('--example', type=int, choices=range(1, 8),
                       help='Run specific example (1-7), or all if not specified')
    
    args = parser.parse_args()
    
    if args.example:
        example_func = [
            example_1_quick_backtest,
            example_2_full_analysis,
            example_3_custom_config,
            example_4_position_sizing,
            example_5_statistical_validation,
            example_6_compare_strategies,
            example_7_export_trades
        ][args.example - 1]
        
        example_func()
    else:
        run_all_examples()
