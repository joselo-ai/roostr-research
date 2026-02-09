#!/usr/bin/env python3
"""
Quant Agent - Statistical Analysis & Backtesting System
========================================================

Specialized AI agent for quantitative analysis, backtesting, and strategy validation.

Features:
- Comprehensive backtesting framework
- Statistical validation (IC, p-values, Sharpe ratio)
- Performance metrics (win rate, max drawdown, CAGR)
- Risk/reward calculation
- Position sizing recommendations
- Overfitting detection

Author: OpenClaw Trading System
Version: 1.0.0
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backtest import Backtester, BacktestConfig, Trade
from validation import SignalValidator, generate_validation_report


class QuantAgent:
    """
    Main Quant Agent orchestrating backtesting and statistical analysis
    
    Usage:
        agent = QuantAgent()
        agent.analyze_strategy(signals_df)
        agent.generate_full_report()
    """
    
    def __init__(self, config: BacktestConfig = None):
        self.config = config or BacktestConfig(
            starting_capital=100000,
            position_size_pct=0.10,
            max_positions=5,
            commission_pct=0.001,
            slippage_pct=0.0005,
            stop_loss_pct=0.20,
            take_profit_pct=0.30,
            max_hold_days=90
        )
        
        self.backtester = Backtester(self.config)
        self.validator = SignalValidator()
        self.signals_df = None
        self.backtest_results = None
        self.validation_results = None
        
        # Paths
        self.workspace = Path(__file__).parent.parent
        self.reports_dir = self.workspace / 'reports'
        self.reports_dir.mkdir(exist_ok=True)
        
    def load_signals(self, source: str = 'database') -> pd.DataFrame:
        """
        Load trading signals from various sources
        
        Args:
            source: 'database', 'file', or path to CSV
            
        Returns:
            DataFrame with signals
        """
        if source == 'database':
            signal_path = self.workspace / 'signals-database.csv'
        else:
            signal_path = Path(source)
        
        if not signal_path.exists():
            raise FileNotFoundError(f"Signals file not found: {signal_path}")
        
        self.signals_df = pd.read_csv(signal_path)
        
        # Convert date column
        self.signals_df['Date_Found'] = pd.to_datetime(self.signals_df['Date_Found'])
        
        print(f"✅ Loaded {len(self.signals_df)} signals from {signal_path.name}")
        return self.signals_df
    
    def run_backtest(self) -> Dict:
        """
        Execute full backtesting simulation
        
        Returns:
            Backtest results dictionary
        """
        if self.signals_df is None:
            raise ValueError("No signals loaded. Call load_signals() first.")
        
        print("=" * 60)
        print("🔬 QUANT AGENT - BACKTESTING ENGINE")
        print("=" * 60)
        print(f"Configuration:")
        print(f"  Starting Capital: ${self.config.starting_capital:,.0f}")
        print(f"  Position Size: {self.config.position_size_pct*100}%")
        print(f"  Stop Loss: {self.config.stop_loss_pct*100}%")
        print(f"  Take Profit: {self.config.take_profit_pct*100}%")
        print(f"  Max Hold Days: {self.config.max_hold_days}")
        print("=" * 60)
        
        self.backtest_results = self.backtester.run_backtest(self.signals_df)
        
        return self.backtest_results
    
    def run_validation(self) -> Dict:
        """
        Execute statistical validation tests
        
        Returns:
            Validation results dictionary
        """
        if self.backtest_results is None:
            raise ValueError("No backtest results. Run run_backtest() first.")
        
        print("\n" + "=" * 60)
        print("📊 STATISTICAL VALIDATION")
        print("=" * 60)
        
        trades = self.backtest_results['trades']
        trades_df = pd.DataFrame(trades)
        returns = trades_df['return_pct'].values
        
        validation = {}
        
        # 1. Information Coefficient (if conviction scores available)
        if 'Conviction_Score' in self.signals_df.columns:
            print("Testing Information Coefficient...")
            predictions = self.signals_df['Conviction_Score'].values
            deployed_mask = self.signals_df['Status'] == 'GREEN'
            
            if deployed_mask.sum() > 0:
                deployed_predictions = self.signals_df[deployed_mask]['Conviction_Score'].values
                validation['ic'] = self.validator.calculate_information_coefficient(
                    deployed_predictions, 
                    returns[:len(deployed_predictions)]
                )
        
        # 2. Statistical Significance
        print("Testing statistical significance...")
        validation['significance'] = self.validator.test_signal_vs_random(returns)
        
        # 3. Sharpe Ratio Significance
        print("Testing Sharpe ratio significance...")
        validation['sharpe_test'] = self.validator.sharpe_ratio_significance(returns)
        
        # 4. Monte Carlo Simulation
        print("Running Monte Carlo simulation...")
        validation['monte_carlo'] = self.validator.monte_carlo_simulation(trades, n_simulations=1000)
        
        # 5. Correlation Analysis (if multiple features)
        numeric_cols = self.signals_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            print("Analyzing feature correlations...")
            validation['correlations'] = self.validator.correlation_matrix(self.signals_df)
        
        self.validation_results = validation
        
        return validation
    
    def calculate_position_sizing(self, 
                                  ticker: str,
                                  entry_price: float,
                                  risk_per_trade: float = 0.02) -> Dict:
        """
        Calculate optimal position size using Kelly Criterion and risk management
        
        Args:
            ticker: Stock/crypto symbol
            entry_price: Entry price
            risk_per_trade: Risk per trade as fraction of portfolio (default 2%)
            
        Returns:
            Position sizing recommendation
        """
        # Get current equity
        if self.backtester.equity_curve:
            current_equity = self.backtester.equity_curve[-1]['total_equity']
        else:
            current_equity = self.config.starting_capital
        
        # Calculate metrics from historical performance
        if self.backtest_results and self.backtest_results['trades']:
            trades_df = pd.DataFrame(self.backtest_results['trades'])
            win_rate = (trades_df['pnl_net'] > 0).mean()
            
            if win_rate > 0:
                avg_win = trades_df[trades_df['pnl_net'] > 0]['return_pct'].mean() / 100
                avg_loss = abs(trades_df[trades_df['pnl_net'] <= 0]['return_pct'].mean()) / 100
                
                # Kelly Criterion: f* = (p*b - q) / b
                # where p = win rate, q = loss rate, b = avg_win/avg_loss
                if avg_loss > 0:
                    b = avg_win / avg_loss
                    kelly_fraction = (win_rate * b - (1 - win_rate)) / b
                    kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
                else:
                    kelly_fraction = 0.10
            else:
                kelly_fraction = 0.10
        else:
            kelly_fraction = 0.10
        
        # Calculate position sizes
        max_risk_amount = current_equity * risk_per_trade
        stop_loss_price = entry_price * (1 - self.config.stop_loss_pct)
        risk_per_share = entry_price - stop_loss_price
        
        # Position size based on risk
        risk_based_shares = max_risk_amount / risk_per_share if risk_per_share > 0 else 0
        risk_based_value = risk_based_shares * entry_price
        
        # Position size based on Kelly
        kelly_position_value = current_equity * kelly_fraction
        kelly_shares = kelly_position_value / entry_price
        
        # Conservative position (use smaller of the two)
        recommended_value = min(risk_based_value, kelly_position_value)
        recommended_shares = recommended_value / entry_price
        
        return {
            'ticker': ticker,
            'entry_price': entry_price,
            'current_equity': round(current_equity, 2),
            'stop_loss_price': round(stop_loss_price, 2),
            'risk_per_trade_pct': risk_per_trade * 100,
            'max_risk_amount': round(max_risk_amount, 2),
            'kelly_fraction': round(kelly_fraction, 4),
            'recommended_shares': round(recommended_shares, 2),
            'recommended_value': round(recommended_value, 2),
            'recommended_pct_portfolio': round((recommended_value / current_equity) * 100, 2),
            'risk_reward_ratio': round(self.config.take_profit_pct / self.config.stop_loss_pct, 2)
        }
    
    def generate_full_report(self, save: bool = True) -> str:
        """
        Generate comprehensive analysis report combining backtest and validation
        
        Args:
            save: Whether to save report to file
            
        Returns:
            Full report string
        """
        if self.backtest_results is None:
            raise ValueError("No results to report. Run analysis first.")
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Generate individual reports
        backtest_report = self.backtester.generate_report()
        
        if self.validation_results:
            validation_report = generate_validation_report(
                self.signals_df,
                self.backtest_results
            )
        else:
            validation_report = "⚠️  Validation not run"
        
        # Combine reports
        full_report = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           QUANT AGENT - COMPREHENSIVE ANALYSIS               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Agent Version: 1.0.0

{backtest_report}

{validation_report}

╔══════════════════════════════════════════════════════════════╗
║                    RECOMMENDATIONS                           ║
╚══════════════════════════════════════════════════════════════╝

"""
        
        # Add recommendations based on results
        metrics = self.backtester.calculate_metrics()
        
        recommendations = []
        
        if metrics['win_rate_pct'] < 50:
            recommendations.append("⚠️  Win rate below 50% - Review entry criteria")
        
        if metrics['profit_factor'] < 1.5:
            recommendations.append("⚠️  Profit factor low - Consider tighter stops or better targets")
        
        if metrics['sharpe_ratio'] < 1.0:
            recommendations.append("⚠️  Sharpe ratio < 1.0 - Risk-adjusted returns need improvement")
        
        if abs(metrics['max_drawdown_pct']) > 25:
            recommendations.append("⚠️  Max drawdown > 25% - Reduce position sizes")
        
        if metrics['avg_hold_days'] > 60:
            recommendations.append("ℹ️  Long average hold time - Consider shorter timeframes")
        
        if not recommendations:
            recommendations.append("✅ Strategy metrics look healthy - Continue monitoring")
        
        for rec in recommendations:
            full_report += f"{rec}\n"
        
        full_report += "\n" + "═" * 60 + "\n"
        
        # Save reports
        if save:
            # Full report
            report_path = self.reports_dir / f'quant_report_{timestamp}.txt'
            with open(report_path, 'w') as f:
                f.write(full_report)
            print(f"\n📄 Full report saved: {report_path}")
            
            # Export trades
            trades_path = self.reports_dir / f'trades_{timestamp}.csv'
            self.backtester.export_trades(str(trades_path))
            
            # Export metrics as JSON
            metrics_path = self.reports_dir / f'metrics_{timestamp}.json'
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2)
            print(f"📊 Metrics saved: {metrics_path}")
        
        return full_report
    
    def analyze_strategy(self, signals_source: str = 'database') -> str:
        """
        Run full end-to-end analysis pipeline
        
        Args:
            signals_source: Source of signals ('database' or file path)
            
        Returns:
            Full analysis report
        """
        try:
            # Step 1: Load signals
            self.load_signals(signals_source)
            
            # Step 2: Run backtest
            self.run_backtest()
            
            # Step 3: Run validation
            self.run_validation()
            
            # Step 4: Generate report
            report = self.generate_full_report(save=True)
            
            print("\n" + "=" * 60)
            print("✅ ANALYSIS COMPLETE")
            print("=" * 60)
            
            return report
            
        except Exception as e:
            print(f"\n❌ Analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {e}"
    
    def quick_backtest(self, ticker: str, entry_price: float, entry_date: str) -> Dict:
        """
        Quick backtest for a single signal
        
        Args:
            ticker: Symbol
            entry_price: Entry price
            entry_date: Entry date (YYYY-MM-DD)
            
        Returns:
            Trade result
        """
        print(f"🔍 Quick backtesting: {ticker} @ ${entry_price} on {entry_date}")
        
        entry_dt = pd.to_datetime(entry_date)
        start_date = (entry_dt - timedelta(days=5)).strftime('%Y-%m-%d')
        end_date = (entry_dt + timedelta(days=self.config.max_hold_days + 30)).strftime('%Y-%m-%d')
        
        hist_data = self.backtester.load_historical_data(ticker, start_date, end_date)
        
        if hist_data.empty:
            return {'error': f'No data available for {ticker}'}
        
        trade = self.backtester.simulate_trade(ticker, entry_dt, entry_price, hist_data)
        
        if trade:
            print(f"✅ Trade simulated:")
            print(f"   Entry: ${trade.entry_price} on {trade.entry_date}")
            print(f"   Exit:  ${trade.exit_price} on {trade.exit_date} ({trade.exit_reason})")
            print(f"   P&L:   ${trade.pnl_net:,.2f} ({trade.return_pct:+.2f}%)")
            print(f"   Hold:  {trade.hold_days} days")
            
            return {
                'ticker': ticker,
                'entry_price': trade.entry_price,
                'exit_price': trade.exit_price,
                'pnl': trade.pnl_net,
                'return_pct': trade.return_pct,
                'hold_days': trade.hold_days,
                'exit_reason': trade.exit_reason
            }
        else:
            return {'error': 'Could not simulate trade'}


def main():
    """Command-line interface for Quant Agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Quant Agent - Statistical Analysis & Backtesting')
    parser.add_argument('--mode', choices=['full', 'quick'], default='full',
                       help='Analysis mode: full analysis or quick single-trade backtest')
    parser.add_argument('--signals', default='database',
                       help='Path to signals CSV or "database" for default')
    parser.add_argument('--ticker', help='Ticker for quick mode')
    parser.add_argument('--price', type=float, help='Entry price for quick mode')
    parser.add_argument('--date', help='Entry date (YYYY-MM-DD) for quick mode')
    parser.add_argument('--capital', type=float, default=100000,
                       help='Starting capital (default: 100000)')
    parser.add_argument('--position-size', type=float, default=0.10,
                       help='Position size as fraction (default: 0.10 = 10%%)')
    parser.add_argument('--stop-loss', type=float, default=0.20,
                       help='Stop loss percentage (default: 0.20 = 20%%)')
    parser.add_argument('--take-profit', type=float, default=0.30,
                       help='Take profit percentage (default: 0.30 = 30%%)')
    
    args = parser.parse_args()
    
    # Configure agent
    config = BacktestConfig(
        starting_capital=args.capital,
        position_size_pct=args.position_size,
        stop_loss_pct=args.stop_loss,
        take_profit_pct=args.take_profit
    )
    
    agent = QuantAgent(config)
    
    if args.mode == 'full':
        # Full analysis
        print("🚀 Launching full strategy analysis...")
        report = agent.analyze_strategy(args.signals)
        print(report)
        
    elif args.mode == 'quick':
        # Quick single-trade backtest
        if not all([args.ticker, args.price, args.date]):
            print("❌ Quick mode requires: --ticker, --price, --date")
            return
        
        result = agent.quick_backtest(args.ticker, args.price, args.date)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
