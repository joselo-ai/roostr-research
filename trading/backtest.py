"""
Backtesting Module - Historical Strategy Testing Framework
===========================================================

Simulates trading strategies on historical data with realistic fees,
slippage, and position sizing. Generates comprehensive performance reports.

Author: Quant Agent
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass, asdict
import warnings
warnings.filterwarnings('ignore')


@dataclass
class Trade:
    """Represents a single trade execution"""
    entry_date: str
    exit_date: str
    ticker: str
    side: str  # 'LONG' or 'SHORT'
    entry_price: float
    exit_price: float
    position_size: float
    shares: float
    pnl_gross: float
    pnl_net: float
    fees: float
    slippage: float
    return_pct: float
    hold_days: int
    exit_reason: str  # 'STOP_LOSS', 'TARGET', 'TIME', 'SIGNAL'
    

@dataclass
class BacktestConfig:
    """Configuration for backtesting parameters"""
    starting_capital: float = 100000.0
    position_size_pct: float = 0.10  # 10% per trade
    max_positions: int = 5
    commission_pct: float = 0.001  # 0.1% per side
    slippage_pct: float = 0.0005  # 0.05% average slippage
    stop_loss_pct: float = 0.15  # 15% stop loss
    take_profit_pct: float = 0.30  # 30% take profit
    max_hold_days: int = 90  # Force exit after 90 days
    

class Backtester:
    """
    Core backtesting engine for strategy validation
    
    Usage:
        bt = Backtester(config)
        results = bt.run_backtest(signals_df)
        metrics = bt.calculate_metrics()
    """
    
    def __init__(self, config: BacktestConfig = None):
        self.config = config or BacktestConfig()
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict] = []
        self.daily_returns: pd.Series = None
        
    def load_historical_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load historical price data from yfinance
        
        Args:
            ticker: Stock/crypto ticker symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Add crypto suffix if needed
            symbol = ticker
            if ticker in ['BTC', 'ETH', 'SOL', 'TAO', 'RNDR', 'FET']:
                symbol = f"{ticker}-USD"
            
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                print(f"⚠️  No data found for {ticker}")
                return pd.DataFrame()
            
            # Flatten multi-index columns if present
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {ticker}: {e}")
            return pd.DataFrame()
    
    def simulate_trade(self, 
                       ticker: str,
                       entry_date: datetime,
                       entry_price: float,
                       historical_data: pd.DataFrame,
                       side: str = 'LONG') -> Optional[Trade]:
        """
        Simulate a single trade from entry to exit
        
        Args:
            ticker: Symbol
            entry_date: Entry datetime
            entry_price: Entry price
            historical_data: Price data
            side: 'LONG' or 'SHORT'
            
        Returns:
            Trade object with full execution details
        """
        # Calculate position sizing
        capital = self.config.starting_capital
        if self.equity_curve:
            capital = self.equity_curve[-1]['total_equity']
        
        position_value = capital * self.config.position_size_pct
        shares = position_value / entry_price
        
        # Apply entry slippage and fees
        entry_slippage = entry_price * self.config.slippage_pct
        entry_with_slippage = entry_price * (1 + self.config.slippage_pct)
        entry_fees = position_value * self.config.commission_pct
        
        # Calculate stop loss and take profit levels
        if side == 'LONG':
            stop_price = entry_price * (1 - self.config.stop_loss_pct)
            target_price = entry_price * (1 + self.config.take_profit_pct)
        else:
            stop_price = entry_price * (1 + self.config.stop_loss_pct)
            target_price = entry_price * (1 - self.config.take_profit_pct)
        
        # Simulate holding period
        future_data = historical_data[historical_data.index > entry_date]
        
        if future_data.empty:
            return None
        
        exit_date = None
        exit_price = None
        exit_reason = None
        
        for date, row in future_data.iterrows():
            days_held = (date - entry_date).days
            
            # Check stop loss
            if side == 'LONG' and row['Low'] <= stop_price:
                exit_date = date
                exit_price = stop_price
                exit_reason = 'STOP_LOSS'
                break
            elif side == 'SHORT' and row['High'] >= stop_price:
                exit_date = date
                exit_price = stop_price
                exit_reason = 'STOP_LOSS'
                break
            
            # Check take profit
            if side == 'LONG' and row['High'] >= target_price:
                exit_date = date
                exit_price = target_price
                exit_reason = 'TARGET'
                break
            elif side == 'SHORT' and row['Low'] <= target_price:
                exit_date = date
                exit_price = target_price
                exit_reason = 'TARGET'
                break
            
            # Check max hold period
            if days_held >= self.config.max_hold_days:
                exit_date = date
                exit_price = row['Close']
                exit_reason = 'TIME'
                break
        
        # If no exit condition met, exit at last available price
        if exit_date is None:
            exit_date = future_data.index[-1]
            exit_price = future_data.iloc[-1]['Close']
            exit_reason = 'END_OF_DATA'
        
        # Apply exit slippage and fees
        exit_with_slippage = exit_price * (1 - self.config.slippage_pct)
        exit_fees = (shares * exit_price) * self.config.commission_pct
        
        # Calculate P&L
        if side == 'LONG':
            pnl_gross = shares * (exit_price - entry_price)
        else:
            pnl_gross = shares * (entry_price - exit_price)
        
        total_fees = entry_fees + exit_fees
        total_slippage = shares * (entry_slippage + abs(exit_price * self.config.slippage_pct))
        pnl_net = pnl_gross - total_fees - total_slippage
        
        return_pct = (pnl_net / position_value) * 100
        
        return Trade(
            entry_date=entry_date.strftime('%Y-%m-%d'),
            exit_date=exit_date.strftime('%Y-%m-%d'),
            ticker=ticker,
            side=side,
            entry_price=entry_price,
            exit_price=exit_price,
            position_size=position_value,
            shares=shares,
            pnl_gross=pnl_gross,
            pnl_net=pnl_net,
            fees=total_fees,
            slippage=total_slippage,
            return_pct=return_pct,
            hold_days=(exit_date - entry_date).days,
            exit_reason=exit_reason
        )
    
    def run_backtest(self, signals: pd.DataFrame) -> Dict:
        """
        Run full backtesting simulation on signal dataset
        
        Args:
            signals: DataFrame with columns: Ticker, Date_Found, Price_Entry
            
        Returns:
            Dictionary with trades and performance summary
        """
        print("🔄 Starting backtest simulation...")
        self.trades = []
        self.equity_curve = []
        
        # Initialize equity tracking
        current_equity = self.config.starting_capital
        self.equity_curve.append({
            'date': signals['Date_Found'].min(),
            'total_equity': current_equity,
            'cash': current_equity,
            'positions_value': 0
        })
        
        # Sort signals by date
        signals = signals.sort_values('Date_Found').copy()
        
        # Process each signal
        for idx, signal in signals.iterrows():
            if pd.isna(signal['Price_Entry']):
                continue
            
            ticker = signal['Ticker']
            entry_date = pd.to_datetime(signal['Date_Found'])
            entry_price = float(signal['Price_Entry'])
            
            # Load historical data
            start_date = (entry_date - timedelta(days=5)).strftime('%Y-%m-%d')
            end_date = (entry_date + timedelta(days=self.config.max_hold_days + 30)).strftime('%Y-%m-%d')
            
            hist_data = self.load_historical_data(ticker, start_date, end_date)
            
            if hist_data.empty:
                continue
            
            # Simulate the trade
            trade = self.simulate_trade(ticker, entry_date, entry_price, hist_data)
            
            if trade:
                self.trades.append(trade)
                
                # Update equity curve
                current_equity += trade.pnl_net
                self.equity_curve.append({
                    'date': trade.exit_date,
                    'total_equity': current_equity,
                    'trade_pnl': trade.pnl_net,
                    'ticker': ticker
                })
        
        print(f"✅ Backtest complete: {len(self.trades)} trades executed")
        
        return {
            'trades': [asdict(t) for t in self.trades],
            'equity_curve': self.equity_curve,
            'config': asdict(self.config)
        }
    
    def calculate_metrics(self) -> Dict:
        """
        Calculate comprehensive performance metrics
        
        Returns:
            Dictionary with all performance statistics
        """
        if not self.trades:
            return {'error': 'No trades to analyze'}
        
        trades_df = pd.DataFrame([asdict(t) for t in self.trades])
        
        # Basic metrics
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.pnl_net > 0])
        losing_trades = len([t for t in self.trades if t.pnl_net <= 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # P&L metrics
        total_pnl = sum([t.pnl_net for t in self.trades])
        avg_win = trades_df[trades_df['pnl_net'] > 0]['pnl_net'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl_net'] <= 0]['pnl_net'].mean() if losing_trades > 0 else 0
        
        # Risk metrics
        profit_factor = abs(avg_win * winning_trades / (avg_loss * losing_trades)) if losing_trades > 0 and avg_loss != 0 else float('inf')
        
        # Calculate returns
        initial_capital = self.config.starting_capital
        final_equity = self.equity_curve[-1]['total_equity']
        total_return_pct = ((final_equity - initial_capital) / initial_capital) * 100
        
        # Drawdown calculation
        equity_series = pd.DataFrame(self.equity_curve)['total_equity']
        rolling_max = equity_series.expanding().max()
        drawdowns = (equity_series - rolling_max) / rolling_max * 100
        max_drawdown = drawdowns.min()
        
        # Sharpe Ratio (annualized)
        returns = trades_df['return_pct'].values
        if len(returns) > 1:
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        else:
            sharpe = 0
        
        # CAGR calculation
        total_days = (pd.to_datetime(self.equity_curve[-1]['date']) - 
                      pd.to_datetime(self.equity_curve[0]['date'])).days
        years = total_days / 365.25
        cagr = (((final_equity / initial_capital) ** (1 / years)) - 1) * 100 if years > 0 else 0
        
        # Average holding period
        avg_hold_days = trades_df['hold_days'].mean()
        
        # Exit reason breakdown
        exit_reasons = trades_df['exit_reason'].value_counts().to_dict()
        
        metrics = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate_pct': round(win_rate, 2),
            'total_pnl': round(total_pnl, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'total_return_pct': round(total_return_pct, 2),
            'max_drawdown_pct': round(max_drawdown, 2),
            'sharpe_ratio': round(sharpe, 2),
            'cagr_pct': round(cagr, 2),
            'avg_hold_days': round(avg_hold_days, 1),
            'initial_capital': initial_capital,
            'final_equity': round(final_equity, 2),
            'exit_reasons': exit_reasons,
            'total_fees_paid': round(trades_df['fees'].sum(), 2),
            'total_slippage': round(trades_df['slippage'].sum(), 2)
        }
        
        return metrics
    
    def generate_report(self, output_path: str = None) -> str:
        """
        Generate comprehensive backtest report
        
        Args:
            output_path: Optional file path to save report
            
        Returns:
            Formatted report string
        """
        metrics = self.calculate_metrics()
        
        if 'error' in metrics:
            return f"❌ {metrics['error']}"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          BACKTEST PERFORMANCE REPORT                         ║
║          Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                       ║
╚══════════════════════════════════════════════════════════════╝

📊 SUMMARY STATISTICS
{'─' * 60}
Total Trades:              {metrics['total_trades']}
Winning Trades:            {metrics['winning_trades']} ({metrics['win_rate_pct']}%)
Losing Trades:             {metrics['losing_trades']}
Average Hold Period:       {metrics['avg_hold_days']} days

💰 PROFIT & LOSS
{'─' * 60}
Initial Capital:           ${metrics['initial_capital']:,.2f}
Final Equity:              ${metrics['final_equity']:,.2f}
Total P&L:                 ${metrics['total_pnl']:,.2f}
Total Return:              {metrics['total_return_pct']}%
CAGR:                      {metrics['cagr_pct']}%

Average Win:               ${metrics['avg_win']:,.2f}
Average Loss:              ${metrics['avg_loss']:,.2f}
Profit Factor:             {metrics['profit_factor']}

⚠️  RISK METRICS
{'─' * 60}
Maximum Drawdown:          {metrics['max_drawdown_pct']}%
Sharpe Ratio:              {metrics['sharpe_ratio']}
Win Rate:                  {metrics['win_rate_pct']}%

💸 COSTS
{'─' * 60}
Total Fees Paid:           ${metrics['total_fees_paid']:,.2f}
Total Slippage:            ${metrics['total_slippage']:,.2f}

📈 EXIT ANALYSIS
{'─' * 60}
"""
        
        for reason, count in metrics['exit_reasons'].items():
            pct = (count / metrics['total_trades']) * 100
            report += f"{reason:20s}: {count:3d} ({pct:5.1f}%)\n"
        
        report += "\n" + "═" * 60 + "\n"
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {output_path}")
        
        return report
    
    def export_trades(self, output_path: str):
        """Export all trades to CSV for further analysis"""
        if not self.trades:
            print("❌ No trades to export")
            return
        
        trades_df = pd.DataFrame([asdict(t) for t in self.trades])
        trades_df.to_csv(output_path, index=False)
        print(f"💾 Trades exported to: {output_path}")


# Example usage
if __name__ == '__main__':
    # Example: Backtest current signals
    signals = pd.read_csv('../signals-database.csv')
    
    config = BacktestConfig(
        starting_capital=100000,
        position_size_pct=0.10,
        stop_loss_pct=0.20,
        take_profit_pct=0.30
    )
    
    bt = Backtester(config)
    results = bt.run_backtest(signals)
    print(bt.generate_report())
