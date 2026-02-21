"""
Backtester - Simulate strategies on historical data
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from strategy_dna import StrategyDNA

class Backtester:
    """Backtest trading strategies on historical data"""
    
    def __init__(self, universe: List[str], lookback_days: int = 365):
        """
        Args:
            universe: List of stock tickers to test on
            lookback_days: How far back to test
        """
        self.universe = universe
        self.lookback_days = lookback_days
        self.historical_data = {}
        
    def load_data(self, ticker: str) -> pd.DataFrame:
        """Load historical data for a ticker"""
        if ticker in self.historical_data:
            return self.historical_data[ticker]
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.lookback_days + 100)  # Extra for indicators
            
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if df.empty:
                return None
            
            # Calculate technical indicators
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            df['SMA_100'] = df['Close'].rolling(window=100).mean()
            df['SMA_200'] = df['Close'].rolling(window=200).mean()
            
            # RSI
            df['RSI_7'] = self._calculate_rsi(df['Close'], 7)
            df['RSI_14'] = self._calculate_rsi(df['Close'], 14)
            df['RSI_21'] = self._calculate_rsi(df['Close'], 21)
            
            # Volume average
            df['Volume_Avg'] = df['Volume'].rolling(window=20).mean()
            df['Volume_Ratio'] = df['Volume'] / df['Volume_Avg']
            
            self.historical_data[ticker] = df
            return df
            
        except Exception as e:
            print(f"Error loading {ticker}: {e}")
            return None
    
    def _calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def check_entry_signal(self, df: pd.DataFrame, idx: int, strategy: StrategyDNA) -> bool:
        """Check if entry conditions are met"""
        if idx < 200:  # Need enough history for indicators
            return False
        
        entry = strategy.genes["entry"]
        filters = strategy.genes["filters"]
        
        row = df.iloc[idx]
        
        # Check filters first
        if row['Close'] < filters['min_market_cap']:  # Using price as proxy for now
            return False
        
        # Check entry conditions
        rsi_col = f"RSI_{entry['rsi_period']}"
        if rsi_col not in df.columns:
            return False
        
        rsi_value = row[rsi_col]
        if pd.isna(rsi_value) or rsi_value >= entry['rsi_oversold']:
            return False
        
        # Volume spike
        if row['Volume_Ratio'] < entry['volume_spike']:
            return False
        
        # Price above SMA
        sma_col = f"SMA_{entry['price_above_sma']}"
        if sma_col not in df.columns or pd.isna(row[sma_col]):
            return False
        
        if row['Close'] <= row[sma_col]:
            return False
        
        # Minimum price
        if row['Close'] < entry['min_price']:
            return False
        
        return True
    
    def simulate_trade(self, df: pd.DataFrame, entry_idx: int, strategy: StrategyDNA) -> Dict:
        """Simulate a single trade from entry to exit"""
        exit_rules = strategy.genes["exit"]
        
        entry_price = df.iloc[entry_idx]['Close']
        entry_date = df.index[entry_idx]
        
        profit_target = entry_price * (1 + exit_rules['profit_target'])
        stop_loss = entry_price * (1 - exit_rules['stop_loss'])
        max_exit_idx = min(entry_idx + exit_rules['max_hold_days'], len(df) - 1)
        
        highest_price = entry_price
        
        for i in range(entry_idx + 1, max_exit_idx + 1):
            current_price = df.iloc[i]['Close']
            
            # Update trailing stop
            if exit_rules['trailing_stop']:
                if current_price > highest_price:
                    highest_price = current_price
                    stop_loss = highest_price * (1 - exit_rules['stop_loss'])
            
            # Check exit conditions
            if current_price >= profit_target:
                # Hit profit target
                return {
                    "entry_price": entry_price,
                    "exit_price": profit_target,
                    "entry_date": entry_date,
                    "exit_date": df.index[i],
                    "return": exit_rules['profit_target'],
                    "reason": "profit_target"
                }
            
            if current_price <= stop_loss:
                # Hit stop loss
                return {
                    "entry_price": entry_price,
                    "exit_price": stop_loss,
                    "entry_date": entry_date,
                    "exit_date": df.index[i],
                    "return": (stop_loss - entry_price) / entry_price,
                    "reason": "stop_loss"
                }
        
        # Time-based exit (max hold days)
        exit_price = df.iloc[max_exit_idx]['Close']
        return {
            "entry_price": entry_price,
            "exit_price": exit_price,
            "entry_date": entry_date,
            "exit_date": df.index[max_exit_idx],
            "return": (exit_price - entry_price) / entry_price,
            "reason": "time_exit"
        }
    
    def backtest_strategy(self, strategy: StrategyDNA) -> Dict:
        """Run full backtest on strategy across universe"""
        all_trades = []
        
        for ticker in self.universe:
            df = self.load_data(ticker)
            if df is None or len(df) < 250:
                continue
            
            # Scan for entry signals
            i = 200  # Start after enough history for indicators
            while i < len(df) - 1:
                if self.check_entry_signal(df, i, strategy):
                    trade = self.simulate_trade(df, i, strategy)
                    trade['ticker'] = ticker
                    all_trades.append(trade)
                    
                    # Skip ahead to avoid overlapping trades
                    i += strategy.genes["exit"]["max_hold_days"]
                else:
                    i += 1
        
        # Calculate performance metrics
        if not all_trades:
            return {
                "total_trades": 0,
                "roi": 0,
                "win_rate": 0,
                "max_drawdown": 0,
                "sharpe": 0
            }
        
        returns = [t['return'] for t in all_trades]
        winning_trades = [r for r in returns if r > 0]
        
        total_return = sum(returns)
        avg_return = np.mean(returns)
        win_rate = len(winning_trades) / len(returns) if returns else 0
        
        # Calculate max drawdown
        cumulative = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max)
        max_drawdown = abs(drawdown.min()) if len(drawdown) > 0 else 0
        
        # Calculate Sharpe ratio (simplified)
        sharpe = (avg_return / np.std(returns)) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        results = {
            "total_trades": len(all_trades),
            "roi": total_return,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "sharpe": sharpe,
            "avg_return_per_trade": avg_return,
            "trades": all_trades[:10]  # Save first 10 trades as examples
        }
        
        # Update strategy fitness
        strategy.calculate_fitness(
            roi=total_return,
            win_rate=win_rate,
            max_drawdown=max_drawdown,
            sharpe=sharpe
        )
        
        return results

def get_sp500_tickers(limit: int = 50) -> List[str]:
    """Get top N tickers from S&P 500 for testing"""
    # Start with most liquid stocks
    top_tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B',
        'UNH', 'JNJ', 'V', 'XOM', 'JPM', 'PG', 'MA', 'HD', 'CVX', 'MRK',
        'ABBV', 'LLY', 'AVGO', 'PEP', 'KO', 'COST', 'WMT', 'TMO', 'MCD',
        'ACN', 'CSCO', 'ABT', 'ADBE', 'DHR', 'VZ', 'NKE', 'CRM', 'NFLX',
        'DIS', 'TXN', 'WFC', 'PM', 'ORCL', 'BMY', 'INTC', 'CMCSA', 'UNP',
        'AMD', 'LOW', 'QCOM', 'NEE', 'HON'
    ]
    return top_tickers[:limit]
