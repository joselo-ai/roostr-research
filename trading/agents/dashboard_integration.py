#!/usr/bin/env python3
"""
Dashboard Integration for Quant Agent
======================================

Integrates backtesting results into the trading dashboard.
Auto-updates dashboard with latest performance metrics.

Author: OpenClaw Trading System
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.quant_agent import QuantAgent
from backtest import BacktestConfig


def generate_performance_card(metrics: dict) -> str:
    """
    Generate HTML card for dashboard with backtest metrics
    
    Args:
        metrics: Dictionary with performance metrics
        
    Returns:
        HTML string for dashboard card
    """
    # Color coding based on performance
    if metrics.get('total_return_pct', 0) > 10:
        performance_class = "success"
        performance_icon = "🟢"
    elif metrics.get('total_return_pct', 0) > 0:
        performance_class = "warning"
        performance_icon = "🟡"
    else:
        performance_class = "danger"
        performance_icon = "🔴"
    
    html = f"""
    <div class="performance-card">
        <div class="card-header">
            <h3>{performance_icon} Strategy Performance</h3>
            <span class="timestamp">Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
        </div>
        <div class="card-body">
            <div class="metric-grid">
                <div class="metric">
                    <span class="label">Total Return</span>
                    <span class="value {performance_class}">{metrics.get('total_return_pct', 0):.2f}%</span>
                </div>
                <div class="metric">
                    <span class="label">Win Rate</span>
                    <span class="value">{metrics.get('win_rate_pct', 0):.1f}%</span>
                </div>
                <div class="metric">
                    <span class="label">Sharpe Ratio</span>
                    <span class="value">{metrics.get('sharpe_ratio', 0):.2f}</span>
                </div>
                <div class="metric">
                    <span class="label">Max Drawdown</span>
                    <span class="value danger">{metrics.get('max_drawdown_pct', 0):.2f}%</span>
                </div>
                <div class="metric">
                    <span class="label">Total Trades</span>
                    <span class="value">{metrics.get('total_trades', 0)}</span>
                </div>
                <div class="metric">
                    <span class="label">Profit Factor</span>
                    <span class="value">{metrics.get('profit_factor', 0):.2f}</span>
                </div>
            </div>
            
            <div class="summary">
                <p><strong>Final Equity:</strong> ${metrics.get('final_equity', 0):,.2f}</p>
                <p><strong>CAGR:</strong> {metrics.get('cagr_pct', 0):.2f}%</p>
            </div>
        </div>
    </div>
    """
    
    return html


def update_dashboard_with_backtest():
    """
    Run backtest and update dashboard with results
    """
    print("🔄 Running backtest for dashboard update...")
    
    try:
        # Initialize agent
        agent = QuantAgent()
        
        # Load signals
        agent.load_signals('database')
        
        # Run backtest
        agent.run_backtest()
        
        # Calculate metrics
        metrics = agent.backtester.calculate_metrics()
        
        # Generate HTML card
        html_card = generate_performance_card(metrics)
        
        # Save to dashboard component
        output_path = Path(__file__).parent.parent / 'dashboard_backtest_card.html'
        with open(output_path, 'w') as f:
            f.write(html_card)
        
        print(f"✅ Dashboard updated: {output_path}")
        
        # Also save metrics as JSON for other integrations
        json_path = Path(__file__).parent.parent / 'latest_backtest_metrics.json'
        with open(json_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics
            }, f, indent=2)
        
        print(f"📊 Metrics saved: {json_path}")
        
        return metrics
        
    except Exception as e:
        print(f"❌ Dashboard update failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def log_to_command_center(activity: str, details: dict):
    """
    Log backtesting activity to Command Center
    
    Args:
        activity: Activity description
        details: Activity details
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'agent': 'QuantAgent',
        'activity': activity,
        'details': details
    }
    
    # Append to activity log
    log_path = Path(__file__).parent.parent / 'command_center_activity.log'
    
    with open(log_path, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"📝 Logged to Command Center: {activity}")


def auto_backtest_on_new_signal(signal: dict):
    """
    Automatically backtest a new signal when it's added
    
    Args:
        signal: Signal dictionary with ticker, price, date
    """
    print(f"🔍 Auto-backtesting new signal: {signal['ticker']}")
    
    try:
        agent = QuantAgent()
        
        result = agent.quick_backtest(
            ticker=signal['ticker'],
            entry_price=signal['price'],
            entry_date=signal['date']
        )
        
        # Log to Command Center
        log_to_command_center(
            activity='New Signal Backtested',
            details={
                'ticker': signal['ticker'],
                'expected_return': result.get('return_pct', 0),
                'hold_days': result.get('hold_days', 0),
                'recommendation': 'DEPLOY' if result.get('return_pct', 0) > 5 else 'MONITOR'
            }
        )
        
        print(f"✅ Backtest complete: {result.get('return_pct', 0):+.2f}% expected return")
        
        return result
        
    except Exception as e:
        print(f"❌ Auto-backtest failed: {e}")
        return None


if __name__ == '__main__':
    # Run dashboard update
    update_dashboard_with_backtest()
