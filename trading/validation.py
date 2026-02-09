"""
Statistical Validation Module - Signal Quality & Overfitting Detection
======================================================================

Tests signal quality using information coefficient, correlation analysis,
significance testing, and overfitting detection methodologies.

Author: Quant Agent
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr, ttest_ind, kstest
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class SignalValidator:
    """
    Statistical validation for trading signals
    
    Validates signal quality through multiple statistical tests:
    - Information Coefficient (IC)
    - Correlation analysis
    - Hypothesis testing
    - Overfitting detection
    """
    
    def __init__(self):
        self.results = {}
    
    def calculate_information_coefficient(self, 
                                          predictions: np.ndarray, 
                                          actual_returns: np.ndarray) -> Dict:
        """
        Calculate Information Coefficient (IC) - correlation between predictions and returns
        
        IC measures the quality of a predictive signal:
        - IC > 0.05: Good signal
        - IC > 0.10: Strong signal
        - IC < 0: Inverse relationship (bad signal)
        
        Args:
            predictions: Predicted returns or conviction scores
            actual_returns: Actual realized returns
            
        Returns:
            Dict with IC, p-value, and interpretation
        """
        # Remove NaN values
        mask = ~(np.isnan(predictions) | np.isnan(actual_returns))
        pred_clean = predictions[mask]
        actual_clean = actual_returns[mask]
        
        if len(pred_clean) < 3:
            return {'error': 'Insufficient data for IC calculation'}
        
        # Calculate both Pearson and Spearman IC
        pearson_ic, pearson_pval = pearsonr(pred_clean, actual_clean)
        spearman_ic, spearman_pval = spearmanr(pred_clean, actual_clean)
        
        # Interpret results
        if pearson_ic > 0.10:
            interpretation = "🟢 STRONG SIGNAL - High predictive power"
        elif pearson_ic > 0.05:
            interpretation = "🟡 GOOD SIGNAL - Moderate predictive power"
        elif pearson_ic > 0:
            interpretation = "🟡 WEAK SIGNAL - Low predictive power"
        else:
            interpretation = "🔴 BAD SIGNAL - Inverse or no relationship"
        
        return {
            'pearson_ic': round(pearson_ic, 4),
            'pearson_pval': round(pearson_pval, 4),
            'spearman_ic': round(spearman_ic, 4),
            'spearman_pval': round(spearman_pval, 4),
            'statistically_significant': pearson_pval < 0.05,
            'interpretation': interpretation,
            'sample_size': len(pred_clean)
        }
    
    def test_signal_vs_random(self, 
                              signal_returns: np.ndarray,
                              benchmark_returns: np.ndarray = None) -> Dict:
        """
        Test if signal-based returns are significantly different from random/benchmark
        
        Uses t-test to determine if strategy returns are statistically better
        than random chance or a benchmark.
        
        Args:
            signal_returns: Returns from signal-based trades
            benchmark_returns: Random or benchmark returns (if None, tests vs 0)
            
        Returns:
            Statistical test results
        """
        signal_clean = signal_returns[~np.isnan(signal_returns)]
        
        if len(signal_clean) < 3:
            return {'error': 'Insufficient data for significance testing'}
        
        if benchmark_returns is None:
            # One-sample t-test against 0
            t_stat, p_value = stats.ttest_1samp(signal_clean, 0)
            test_type = "one-sample (vs zero)"
        else:
            # Two-sample t-test
            benchmark_clean = benchmark_returns[~np.isnan(benchmark_returns)]
            t_stat, p_value = ttest_ind(signal_clean, benchmark_clean)
            test_type = "two-sample (vs benchmark)"
        
        # Effect size (Cohen's d)
        cohens_d = signal_clean.mean() / signal_clean.std() if signal_clean.std() > 0 else 0
        
        # Interpretation
        if p_value < 0.01:
            significance = "🟢 HIGHLY SIGNIFICANT (p < 0.01)"
        elif p_value < 0.05:
            significance = "🟡 SIGNIFICANT (p < 0.05)"
        else:
            significance = "🔴 NOT SIGNIFICANT (p >= 0.05)"
        
        return {
            'test_type': test_type,
            't_statistic': round(t_stat, 4),
            'p_value': round(p_value, 4),
            'cohens_d': round(cohens_d, 4),
            'mean_return': round(signal_clean.mean(), 4),
            'std_return': round(signal_clean.std(), 4),
            'significance': significance,
            'sample_size': len(signal_clean)
        }
    
    def correlation_matrix(self, signals_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate correlation matrix between different signals/features
        
        High correlations (> 0.7) indicate redundant signals.
        Helps identify multicollinearity issues.
        
        Args:
            signals_df: DataFrame with multiple signal columns
            
        Returns:
            Correlation matrix
        """
        # Select only numeric columns
        numeric_cols = signals_df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return pd.DataFrame({'error': ['Need at least 2 numeric columns']})
        
        corr_matrix = signals_df[numeric_cols].corr()
        
        # Flag high correlations
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    high_corr_pairs.append({
                        'signal_1': corr_matrix.columns[i],
                        'signal_2': corr_matrix.columns[j],
                        'correlation': round(corr_val, 3)
                    })
        
        if high_corr_pairs:
            print("⚠️  HIGH CORRELATION WARNING:")
            for pair in high_corr_pairs:
                print(f"   {pair['signal_1']} ↔ {pair['signal_2']}: {pair['correlation']}")
        
        return corr_matrix
    
    def detect_overfitting(self,
                          train_metrics: Dict,
                          test_metrics: Dict,
                          threshold: float = 0.20) -> Dict:
        """
        Detect overfitting by comparing train vs test performance
        
        Significant performance degradation from train to test suggests overfitting.
        
        Args:
            train_metrics: Performance metrics on training data
            test_metrics: Performance metrics on test/validation data
            threshold: Acceptable performance degradation (default 20%)
            
        Returns:
            Overfitting analysis
        """
        metrics_to_check = ['win_rate_pct', 'sharpe_ratio', 'total_return_pct']
        
        degradations = {}
        overfitting_detected = False
        
        for metric in metrics_to_check:
            if metric in train_metrics and metric in test_metrics:
                train_val = train_metrics[metric]
                test_val = test_metrics[metric]
                
                if train_val != 0:
                    degradation = ((train_val - test_val) / abs(train_val)) * 100
                else:
                    degradation = 0
                
                degradations[metric] = {
                    'train': round(train_val, 2),
                    'test': round(test_val, 2),
                    'degradation_pct': round(degradation, 2)
                }
                
                if degradation > (threshold * 100):
                    overfitting_detected = True
        
        # Overall assessment
        if overfitting_detected:
            assessment = "🔴 OVERFITTING DETECTED - Strategy may not generalize well"
            recommendation = "Consider: simplifying model, adding regularization, more training data"
        else:
            assessment = "🟢 NO OVERFITTING - Performance is consistent"
            recommendation = "Strategy appears to generalize well to unseen data"
        
        return {
            'overfitting_detected': overfitting_detected,
            'degradation_threshold_pct': threshold * 100,
            'metric_comparisons': degradations,
            'assessment': assessment,
            'recommendation': recommendation
        }
    
    def walk_forward_validation(self,
                               signals_df: pd.DataFrame,
                               window_size: int = 20,
                               test_size: int = 5) -> Dict:
        """
        Perform walk-forward validation (rolling window backtesting)
        
        Splits data into rolling train/test windows to validate consistency.
        More robust than single train/test split.
        
        Args:
            signals_df: Signal data with dates
            window_size: Training window size (number of signals)
            test_size: Test window size
            
        Returns:
            Walk-forward validation results
        """
        if len(signals_df) < window_size + test_size:
            return {'error': 'Insufficient data for walk-forward validation'}
        
        # Sort by date
        signals_df = signals_df.sort_values('Date_Found').reset_index(drop=True)
        
        windows = []
        position = 0
        
        while position + window_size + test_size <= len(signals_df):
            train_start = position
            train_end = position + window_size
            test_start = train_end
            test_end = test_start + test_size
            
            windows.append({
                'window_id': len(windows) + 1,
                'train_indices': (train_start, train_end),
                'test_indices': (test_start, test_end),
                'train_period': f"{signals_df.iloc[train_start]['Date_Found']} to {signals_df.iloc[train_end-1]['Date_Found']}",
                'test_period': f"{signals_df.iloc[test_start]['Date_Found']} to {signals_df.iloc[test_end-1]['Date_Found']}"
            })
            
            position += test_size  # Slide window
        
        return {
            'total_windows': len(windows),
            'window_size': window_size,
            'test_size': test_size,
            'windows': windows
        }
    
    def monte_carlo_simulation(self,
                              trades: List[Dict],
                              n_simulations: int = 1000,
                              randomize_order: bool = True) -> Dict:
        """
        Monte Carlo simulation to test strategy robustness
        
        Randomly reorders trades to see if performance was due to luck or skill.
        
        Args:
            trades: List of trade results
            n_simulations: Number of random simulations
            randomize_order: Whether to randomize trade order
            
        Returns:
            Monte Carlo results with confidence intervals
        """
        if len(trades) < 10:
            return {'error': 'Need at least 10 trades for Monte Carlo simulation'}
        
        trade_returns = np.array([t['return_pct'] for t in trades])
        original_total_return = trade_returns.sum()
        
        simulated_returns = []
        
        for _ in range(n_simulations):
            if randomize_order:
                sim_returns = np.random.choice(trade_returns, size=len(trade_returns), replace=True)
            else:
                sim_returns = trade_returns.copy()
                np.random.shuffle(sim_returns)
            
            simulated_returns.append(sim_returns.sum())
        
        simulated_returns = np.array(simulated_returns)
        
        # Calculate percentiles
        percentiles = {
            '5th': np.percentile(simulated_returns, 5),
            '25th': np.percentile(simulated_returns, 25),
            '50th': np.percentile(simulated_returns, 50),
            '75th': np.percentile(simulated_returns, 75),
            '95th': np.percentile(simulated_returns, 95)
        }
        
        # Where does original performance rank?
        percentile_rank = (simulated_returns < original_total_return).mean() * 100
        
        if percentile_rank > 95:
            interpretation = "🟢 EXCEPTIONAL - Performance in top 5% (likely skill-based)"
        elif percentile_rank > 75:
            interpretation = "🟡 GOOD - Performance above median (some skill)"
        elif percentile_rank > 25:
            interpretation = "🟡 AVERAGE - Performance near median (luck vs skill unclear)"
        else:
            interpretation = "🔴 POOR - Performance below average (unlucky or bad strategy)"
        
        return {
            'n_simulations': n_simulations,
            'original_return': round(original_total_return, 2),
            'mean_simulated_return': round(simulated_returns.mean(), 2),
            'std_simulated_return': round(simulated_returns.std(), 2),
            'percentiles': {k: round(v, 2) for k, v in percentiles.items()},
            'percentile_rank': round(percentile_rank, 2),
            'interpretation': interpretation
        }
    
    def sharpe_ratio_significance(self, 
                                  returns: np.ndarray,
                                  risk_free_rate: float = 0.02) -> Dict:
        """
        Test statistical significance of Sharpe ratio
        
        Uses Jobson-Korkie test to determine if Sharpe ratio is significantly > 0
        
        Args:
            returns: Array of returns
            risk_free_rate: Risk-free rate (annual)
            
        Returns:
            Sharpe significance test results
        """
        returns_clean = returns[~np.isnan(returns)]
        
        if len(returns_clean) < 3:
            return {'error': 'Insufficient data for Sharpe significance test'}
        
        # Calculate Sharpe ratio
        excess_returns = returns_clean - (risk_free_rate / 252)  # Daily risk-free
        sharpe = excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() > 0 else 0
        
        # Standard error of Sharpe ratio
        n = len(returns_clean)
        sharpe_se = np.sqrt((1 + (sharpe**2 / 2)) / n)
        
        # T-statistic
        t_stat = sharpe / sharpe_se if sharpe_se > 0 else 0
        
        # P-value (two-tailed test)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))
        
        # Confidence interval
        ci_95 = (
            sharpe - 1.96 * sharpe_se,
            sharpe + 1.96 * sharpe_se
        )
        
        if p_value < 0.05 and sharpe > 0:
            significance = "🟢 SIGNIFICANT - Sharpe ratio reliably positive"
        elif sharpe > 0:
            significance = "🟡 POSITIVE BUT NOT SIGNIFICANT"
        else:
            significance = "🔴 NOT SIGNIFICANT - Cannot confirm positive risk-adjusted returns"
        
        return {
            'sharpe_ratio': round(sharpe, 4),
            't_statistic': round(t_stat, 4),
            'p_value': round(p_value, 4),
            'confidence_interval_95': (round(ci_95[0], 4), round(ci_95[1], 4)),
            'standard_error': round(sharpe_se, 4),
            'significance': significance,
            'sample_size': n
        }


def generate_validation_report(signals_df: pd.DataFrame, 
                               backtest_results: Dict,
                               output_path: str = None) -> str:
    """
    Generate comprehensive statistical validation report
    
    Args:
        signals_df: Signal data
        backtest_results: Results from backtesting
        output_path: Optional file path to save
        
    Returns:
        Formatted validation report
    """
    validator = SignalValidator()
    
    # Extract data
    trades = backtest_results.get('trades', [])
    if not trades:
        return "❌ No trades to validate"
    
    trades_df = pd.DataFrame(trades)
    returns = trades_df['return_pct'].values
    
    # Run validation tests
    print("🔬 Running statistical validation tests...")
    
    # 1. Information Coefficient
    if 'Conviction_Score' in signals_df.columns:
        predictions = signals_df['Conviction_Score'].values
        ic_results = validator.calculate_information_coefficient(predictions, returns[:len(predictions)])
    else:
        ic_results = {'error': 'No conviction scores available'}
    
    # 2. Significance test
    sig_results = validator.test_signal_vs_random(returns)
    
    # 3. Sharpe significance
    sharpe_results = validator.sharpe_ratio_significance(returns)
    
    # 4. Monte Carlo
    mc_results = validator.monte_carlo_simulation(trades, n_simulations=1000)
    
    # Generate report
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║          STATISTICAL VALIDATION REPORT                       ║
║          Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}                       ║
╚══════════════════════════════════════════════════════════════╝

📊 INFORMATION COEFFICIENT (Signal Quality)
{'─' * 60}
"""
    
    if 'error' not in ic_results:
        report += f"""Pearson IC:                {ic_results['pearson_ic']} (p={ic_results['pearson_pval']})
Spearman IC:               {ic_results['spearman_ic']} (p={ic_results['spearman_pval']})
Sample Size:               {ic_results['sample_size']}
Assessment:                {ic_results['interpretation']}
"""
    else:
        report += f"⚠️  {ic_results['error']}\n"
    
    report += f"""
📈 STATISTICAL SIGNIFICANCE
{'─' * 60}
Test Type:                 {sig_results['test_type']}
T-Statistic:               {sig_results['t_statistic']}
P-Value:                   {sig_results['p_value']}
Effect Size (Cohen's d):   {sig_results['cohens_d']}
Mean Return:               {sig_results['mean_return']}%
Std Return:                {sig_results['std_return']}%
Assessment:                {sig_results['significance']}

⚡ SHARPE RATIO SIGNIFICANCE
{'─' * 60}
Sharpe Ratio:              {sharpe_results['sharpe_ratio']}
T-Statistic:               {sharpe_results['t_statistic']}
P-Value:                   {sharpe_results['p_value']}
95% CI:                    {sharpe_results['confidence_interval_95']}
Assessment:                {sharpe_results['significance']}

🎲 MONTE CARLO SIMULATION
{'─' * 60}
Simulations:               {mc_results['n_simulations']}
Original Return:           {mc_results['original_return']}%
Mean Simulated:            {mc_results['mean_simulated_return']}%
Std Simulated:             {mc_results['std_simulated_return']}%
Percentile Rank:           {mc_results['percentile_rank']}%
Assessment:                {mc_results['interpretation']}

Percentile Distribution:
  5th:  {mc_results['percentiles']['5th']}%
  25th: {mc_results['percentiles']['25th']}%
  50th: {mc_results['percentiles']['50th']}%
  75th: {mc_results['percentiles']['75th']}%
  95th: {mc_results['percentiles']['95th']}%

"""
    
    report += "═" * 60 + "\n"
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"📄 Validation report saved to: {output_path}")
    
    return report


# Example usage
if __name__ == '__main__':
    # Example validation
    validator = SignalValidator()
    
    # Mock data for demonstration
    predictions = np.random.randn(100) * 10
    actual_returns = predictions * 0.3 + np.random.randn(100) * 5
    
    ic_results = validator.calculate_information_coefficient(predictions, actual_returns)
    print("Information Coefficient:", ic_results)
