#!/usr/bin/env python3
"""
Value Agent - Buffett + Graham Methodology Stock Scanner
=========================================================

Hunts for undervalued stocks using value investing principles:
- Low P/E, P/B ratios (margin of safety)
- Strong fundamentals (FCF, ROE, debt levels)
- Economic moat (competitive advantages)
- Quality business at fair price

Inspired by: Warren Buffett, Charlie Munger, Ben Graham

Author: Joselo 🐓
Version: 1.0.0
Date: Feb 11, 2026
"""

import os
import json
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class ValueAgent:
    """
    Scans for undervalued stocks using Graham + Buffett criteria.
    
    Scoring Logic:
    1. Valuation Metrics (40%): P/E, P/B, PEG ratio
    2. Quality Metrics (30%): ROE, FCF, profit margins
    3. Safety Metrics (20%): Debt/equity, current ratio
    4. Growth Metrics (10%): Revenue growth, earnings growth
    """
    
    def __init__(self, 
                 max_pe=15.0,           # Graham: P/E < 15
                 max_pb=1.5,            # Graham: P/B < 1.5
                 min_roe=0.15,          # Buffett: ROE > 15%
                 max_debt_equity=0.5):  # Conservative debt levels
        
        self.max_pe = max_pe
        self.max_pb = max_pb
        self.min_roe = min_roe
        self.max_debt_equity = max_debt_equity
        self.signals = []
    
    def scan_universe(self, tickers: List[str]) -> List[Dict]:
        """
        Scan a universe of tickers for value opportunities.
        
        Args:
            tickers: List of ticker symbols to analyze
            
        Returns:
            List of value signals with conviction scores
        """
        print(f"💎 Scanning {len(tickers)} stocks for value opportunities...")
        
        signals = []
        for ticker in tickers:
            try:
                signal = self.analyze_stock(ticker)
                if signal and signal['conviction_score'] >= 5.0:
                    signals.append(signal)
                    print(f"   ✅ {ticker}: {signal['conviction_score']:.1f}/10")
            except Exception as e:
                print(f"   ⚠️  {ticker}: Error - {str(e)[:50]}")
                continue
        
        return signals
    
    def analyze_stock(self, ticker: str) -> Optional[Dict]:
        """
        Deep value analysis on a single stock.
        
        Returns None if data unavailable or doesn't meet basic criteria.
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Basic validation
        if not info or 'currentPrice' not in info:
            return None
        
        # Extract key metrics
        metrics = self._extract_metrics(info)
        if not metrics:
            return None
        
        # Calculate conviction score
        conviction = self._calculate_conviction(metrics)
        
        # Build signal
        signal = {
            'ticker': ticker,
            'source': 'Value-Agent',
            'conviction_score': conviction,
            'current_price': metrics['price'],
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': metrics.get('pe'),
            'pb_ratio': metrics.get('pb'),
            'roe': metrics.get('roe'),
            'debt_to_equity': metrics.get('debt_equity'),
            'fcf': metrics.get('fcf'),
            'found_date': datetime.now().strftime('%Y-%m-%d'),
            'notes': self._generate_analysis(ticker, metrics, conviction)
        }
        
        return signal
    
    def _extract_metrics(self, info: Dict) -> Optional[Dict]:
        """Extract relevant value metrics from yfinance info dict"""
        try:
            # Price metrics
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            if not price:
                return None
            
            # Valuation ratios
            pe = info.get('trailingPE') or info.get('forwardPE')
            pb = info.get('priceToBook')
            peg = info.get('pegRatio')
            
            # Quality metrics
            roe = info.get('returnOnEquity')
            profit_margin = info.get('profitMargins')
            
            # Safety metrics
            debt_equity = info.get('debtToEquity')
            current_ratio = info.get('currentRatio')
            
            # Growth metrics
            revenue_growth = info.get('revenueGrowth')
            earnings_growth = info.get('earningsGrowth')
            
            # Cash flow
            fcf = info.get('freeCashflow')
            
            return {
                'price': price,
                'pe': pe,
                'pb': pb,
                'peg': peg,
                'roe': roe,
                'profit_margin': profit_margin,
                'debt_equity': debt_equity,
                'current_ratio': current_ratio,
                'revenue_growth': revenue_growth,
                'earnings_growth': earnings_growth,
                'fcf': fcf
            }
        except Exception as e:
            return None
    
    def _calculate_conviction(self, metrics: Dict) -> float:
        """
        Calculate conviction score (0-10) based on value metrics.
        
        Weights:
        - Valuation (40%): P/E, P/B, PEG
        - Quality (30%): ROE, profit margins
        - Safety (20%): Debt, current ratio
        - Growth (10%): Revenue/earnings growth
        """
        score = 0.0
        
        # 1. Valuation Score (40 points max)
        valuation_score = 0.0
        
        # P/E ratio (15 points)
        pe = metrics.get('pe')
        if pe and pe > 0:
            if pe <= 10:
                valuation_score += 15
            elif pe <= 15:
                valuation_score += 10
            elif pe <= 20:
                valuation_score += 5
        
        # P/B ratio (15 points)
        pb = metrics.get('pb')
        if pb and pb > 0:
            if pb <= 1.0:
                valuation_score += 15
            elif pb <= 1.5:
                valuation_score += 10
            elif pb <= 2.0:
                valuation_score += 5
        
        # PEG ratio (10 points)
        peg = metrics.get('peg')
        if peg and peg > 0:
            if peg <= 1.0:
                valuation_score += 10
            elif peg <= 1.5:
                valuation_score += 5
        
        score += (valuation_score / 40) * 4.0  # Scale to 4.0 max (40% of 10)
        
        # 2. Quality Score (30 points max)
        quality_score = 0.0
        
        # ROE (20 points)
        roe = metrics.get('roe')
        if roe:
            if roe >= 0.20:  # 20%+
                quality_score += 20
            elif roe >= 0.15:  # 15%+
                quality_score += 15
            elif roe >= 0.10:  # 10%+
                quality_score += 10
        
        # Profit margin (10 points)
        margin = metrics.get('profit_margin')
        if margin:
            if margin >= 0.20:  # 20%+
                quality_score += 10
            elif margin >= 0.10:  # 10%+
                quality_score += 5
        
        score += (quality_score / 30) * 3.0  # Scale to 3.0 max (30% of 10)
        
        # 3. Safety Score (20 points max)
        safety_score = 0.0
        
        # Debt/Equity (15 points)
        debt_eq = metrics.get('debt_equity')
        if debt_eq is not None:
            if debt_eq <= 0.3:
                safety_score += 15
            elif debt_eq <= 0.5:
                safety_score += 10
            elif debt_eq <= 1.0:
                safety_score += 5
        
        # Current ratio (5 points)
        current = metrics.get('current_ratio')
        if current:
            if current >= 2.0:
                safety_score += 5
            elif current >= 1.5:
                safety_score += 3
        
        score += (safety_score / 20) * 2.0  # Scale to 2.0 max (20% of 10)
        
        # 4. Growth Score (10 points max)
        growth_score = 0.0
        
        # Revenue growth (5 points)
        rev_growth = metrics.get('revenue_growth')
        if rev_growth:
            if rev_growth >= 0.15:  # 15%+
                growth_score += 5
            elif rev_growth >= 0.10:  # 10%+
                growth_score += 3
        
        # Earnings growth (5 points)
        earn_growth = metrics.get('earnings_growth')
        if earn_growth:
            if earn_growth >= 0.15:  # 15%+
                growth_score += 5
            elif earn_growth >= 0.10:  # 10%+
                growth_score += 3
        
        score += (growth_score / 10) * 1.0  # Scale to 1.0 max (10% of 10)
        
        return min(10.0, score)
    
    def _generate_analysis(self, ticker: str, metrics: Dict, conviction: float) -> str:
        """Generate human-readable analysis text"""
        notes = []
        
        # Valuation summary
        pe = metrics.get('pe')
        pb = metrics.get('pb')
        if pe and pb:
            notes.append(f"Valuation: P/E {pe:.1f}, P/B {pb:.2f}")
        
        # Quality summary
        roe = metrics.get('roe')
        margin = metrics.get('profit_margin')
        if roe:
            notes.append(f"ROE: {roe*100:.1f}%")
        if margin:
            notes.append(f"Profit Margin: {margin*100:.1f}%")
        
        # Safety summary
        debt_eq = metrics.get('debt_equity')
        if debt_eq is not None:
            notes.append(f"Debt/Equity: {debt_eq:.2f}")
        
        # Conviction reason
        if conviction >= 8.0:
            notes.append("✅ Strong value opportunity - excellent metrics across board")
        elif conviction >= 7.0:
            notes.append("✅ Good value - solid fundamentals")
        elif conviction >= 5.0:
            notes.append("⚠️ Moderate value - some strengths")
        else:
            notes.append("🔴 Weak value - insufficient margin of safety")
        
        return " | ".join(notes)
    
    def get_russell_2000_sample(self, n=50) -> List[str]:
        """
        Get sample of Russell 2000 tickers for scanning.
        
        In production, this would query the full Russell 2000 list.
        For now, returns a diverse sample of small/mid caps.
        """
        # Sample tickers from various sectors (Russell 2000 style)
        sample = [
            # Financials
            'ALLY', 'EWBC', 'IBKR', 'GBCI', 'WTFC',
            # Industrials
            'PRIM', 'ROAD', 'GATX', 'KAMN', 'NPO',
            # Tech
            'CWAN', 'LITE', 'FORM', 'CALX', 'OSIS',
            # Healthcare
            'TMDX', 'NVST', 'NEOG', 'OMCL', 'CORT',
            # Consumer
            'ARKO', 'BOOT', 'CASY', 'PDCO', 'PFGC',
            # Energy
            'CIVI', 'CTRA', 'MGY', 'MTDR', 'OVV',
            # Materials
            'CENX', 'ASIX', 'WOR', 'SLVM', 'CLW',
            # Real Estate
            'EQC', 'GMRE', 'JBGS', 'NSA', 'SAFE',
            # Utilities
            'AWR', 'CWT', 'MSEX', 'NWE', 'SJW',
            # Telecom
            'CABO', 'CNSL', 'LUMN', 'SHEN', 'USM'
        ]
        
        return sample[:n]
    
    def save_to_database(self, signals: List[Dict], db_path='signals-database.csv'):
        """Append signals to signals database"""
        if not signals:
            print("⚠️  No signals to save.")
            return
        
        # Convert to DataFrame
        df_new = pd.DataFrame(signals)
        
        # Rename columns to match database schema
        df_new = df_new.rename(columns={
            'ticker': 'Ticker',
            'conviction_score': 'Conviction_Score',
            'source': 'Source',
            'found_date': 'Date_Found',
            'notes': 'Notes',
            'current_price': 'Price_Entry'
        })
        
        # Add missing columns
        df_new['Status'] = 'Monitoring'
        df_new['Date_Entry'] = None
        
        # Select columns
        cols = ['Ticker', 'Source', 'Date_Found', 'Conviction_Score', 'Status', 
                'Price_Entry', 'Date_Entry', 'Notes']
        df_new = df_new[cols]
        
        # Load existing database
        if os.path.exists(db_path):
            df_existing = pd.read_csv(db_path)
            
            # Avoid duplicates
            df_new = df_new[~df_new[['Ticker', 'Date_Found']].apply(tuple, axis=1).isin(
                df_existing[['Ticker', 'Date_Found']].apply(tuple, axis=1)
            )]
            
            if df_new.empty:
                print("✅ All signals already in database.")
                return
            
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        
        # Save
        df_combined.to_csv(db_path, index=False)
        print(f"✅ Saved {len(df_new)} new value signals to {db_path}")
    
    def generate_report(self, signals: List[Dict]) -> str:
        """Generate human-readable report"""
        report = []
        report.append("=" * 80)
        report.append("💎 VALUE AGENT REPORT (Graham + Buffett)")
        report.append("=" * 80)
        report.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M EST')}")
        report.append(f"Signals Found: {len(signals)}")
        report.append("")
        
        if not signals:
            report.append("❌ No value opportunities found meeting criteria.")
            return "\n".join(report)
        
        # Sort by conviction
        signals = sorted(signals, key=lambda x: x['conviction_score'], reverse=True)
        
        for i, signal in enumerate(signals, 1):
            report.append(f"\n📊 SIGNAL #{i}: {signal['ticker']}")
            report.append(f"   Conviction: {signal['conviction_score']:.1f}/10")
            report.append(f"   Price: ${signal['current_price']:.2f}")
            report.append(f"   Market Cap: ${signal['market_cap']/1e9:.2f}B")
            
            if signal.get('pe_ratio'):
                report.append(f"   P/E: {signal['pe_ratio']:.1f}")
            if signal.get('pb_ratio'):
                report.append(f"   P/B: {signal['pb_ratio']:.2f}")
            if signal.get('roe'):
                report.append(f"   ROE: {signal['roe']*100:.1f}%")
            
            report.append(f"   Analysis: {signal['notes']}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def run_scan(self, tickers=None, save=True, min_conviction=5.0) -> List[Dict]:
        """
        Main entry point: Run full value scan pipeline.
        
        Returns: List of high-conviction value signals
        """
        print("\n" + "=" * 80)
        print("💎 VALUE AGENT - Graham + Buffett Value Scan")
        print("=" * 80)
        
        # Get universe
        if tickers is None:
            tickers = self.get_russell_2000_sample(50)
            print(f"📊 Scanning Russell 2000 sample: {len(tickers)} stocks")
        
        # Scan universe
        signals = self.scan_universe(tickers)
        print(f"\n✅ Found {len(signals)} signals with conviction ≥{min_conviction}/10")
        
        # Filter by conviction
        high_conviction = [s for s in signals if s['conviction_score'] >= min_conviction]
        
        # Generate report
        report = self.generate_report(high_conviction)
        print("\n" + report)
        
        # Save to database
        if save and high_conviction:
            self.save_to_database(high_conviction)
        
        return high_conviction


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Value Agent - Graham + Buffett value stock scanner')
    parser.add_argument('--max-pe', type=float, default=15.0, help='Maximum P/E ratio')
    parser.add_argument('--max-pb', type=float, default=1.5, help='Maximum P/B ratio')
    parser.add_argument('--min-roe', type=float, default=0.15, help='Minimum ROE')
    parser.add_argument('--min-conviction', type=float, default=5.0, help='Minimum conviction score')
    parser.add_argument('--no-save', action='store_true', help='Do not save to database')
    parser.add_argument('--tickers', nargs='+', help='Specific tickers to analyze')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ValueAgent(
        max_pe=args.max_pe,
        max_pb=args.max_pb,
        min_roe=args.min_roe
    )
    
    # Run scan
    signals = agent.run_scan(
        tickers=args.tickers,
        save=not args.no_save,
        min_conviction=args.min_conviction
    )
    
    print(f"\n✅ Scan complete. Found {len(signals)} high-conviction value signals.")


if __name__ == '__main__':
    main()
