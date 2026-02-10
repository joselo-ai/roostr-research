#!/usr/bin/env python3
"""
Google Trends Validator - Social Arbitrage Confirmation Layer
Validates ticker signals by checking search volume momentum
Uses pytrends (unofficial Google Trends API - free, no auth required)
"""

from pytrends.request import TrendReq
import json
from datetime import datetime, timedelta
import time

OUTPUT_FILE = '/Users/agentjoselo/.openclaw/workspace/trading/google-trends-validation.json'

class GoogleTrendsValidator:
    """Validate stock signals using Google Trends search volume"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.rising_threshold = 20  # % increase to be considered "rising"
        
    def check_ticker_trend(self, ticker, timeframe='today 3-m'):
        """
        Check if ticker search volume is rising
        
        Args:
            ticker: Stock symbol (e.g., 'ASTS')
            timeframe: Google Trends timeframe
                - 'now 1-d' (past 24 hours)
                - 'now 7-d' (past 7 days)
                - 'today 1-m' (past month)
                - 'today 3-m' (past 3 months)
                - 'today 12-m' (past year)
            
        Returns:
            Validation result dictionary
        """
        try:
            # Build keyword (try with and without $ prefix)
            keywords = [f"{ticker} stock", ticker]
            
            # Get interest over time
            self.pytrends.build_payload(keywords, timeframe=timeframe)
            interest = self.pytrends.interest_over_time()
            
            if interest.empty:
                return {
                    'ticker': ticker,
                    'status': 'NO_DATA',
                    'trend': 'unknown',
                    'current_interest': 0,
                    'avg_interest': 0,
                    'change_percent': 0,
                    'validated': False
                }
            
            # Get primary keyword data (first one with data)
            keyword = keywords[0] if f"{ticker} stock" in interest.columns else ticker
            
            if keyword not in interest.columns:
                return {
                    'ticker': ticker,
                    'status': 'NO_DATA',
                    'trend': 'unknown',
                    'current_interest': 0,
                    'avg_interest': 0,
                    'change_percent': 0,
                    'validated': False
                }
            
            # Calculate trend
            data = interest[keyword]
            current_week = data.tail(7).mean()  # Last 7 days avg
            previous_week = data.iloc[-14:-7].mean()  # Previous 7 days avg
            overall_avg = data.mean()
            
            # Calculate change
            if previous_week > 0:
                change_percent = ((current_week - previous_week) / previous_week) * 100
            else:
                change_percent = 0
            
            # Determine trend
            if change_percent >= self.rising_threshold:
                trend = 'RISING'
            elif change_percent <= -self.rising_threshold:
                trend = 'FALLING'
            else:
                trend = 'STABLE'
            
            # Validate (RISING = good signal)
            validated = trend == 'RISING' and current_week > overall_avg
            
            result = {
                'ticker': ticker,
                'status': 'SUCCESS',
                'trend': trend,
                'current_interest': round(current_week, 2),
                'avg_interest': round(overall_avg, 2),
                'change_percent': round(change_percent, 2),
                'validated': validated,
                'timeframe': timeframe,
                'checked_at': datetime.now().isoformat()
            }
            
            # Get related queries
            try:
                related = self.pytrends.related_queries()
                if keyword in related and related[keyword]['rising'] is not None:
                    result['rising_queries'] = related[keyword]['rising'].head(5).to_dict('records')
            except:
                pass
            
            return result
        
        except Exception as e:
            print(f"Error checking ${ticker}: {e}")
            return {
                'ticker': ticker,
                'status': 'ERROR',
                'error': str(e),
                'validated': False
            }
    
    def validate_signals(self, signals, delay=2):
        """
        Validate a list of ticker signals
        
        Args:
            signals: List of signal dicts with 'ticker' field
            delay: Seconds to wait between API calls (avoid rate limit)
            
        Returns:
            List of validation results
        """
        validations = []
        
        for signal in signals:
            ticker = signal.get('ticker', signal) if isinstance(signal, dict) else signal
            
            print(f"   Checking ${ticker}...")
            result = self.check_ticker_trend(ticker)
            validations.append(result)
            
            # Add validation to original signal
            if isinstance(signal, dict):
                signal['google_trends'] = result
                signal['trends_validated'] = result['validated']
            
            # Rate limit protection
            time.sleep(delay)
        
        return validations
    
    def run(self, ticker_list):
        """Main execution"""
        print(f"🔍 Google Trends Validator - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"Validating {len(ticker_list)} tickers...")
        validations = self.validate_signals(ticker_list)
        
        # Save results
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(validations, f, indent=2)
        
        # Display results
        print(f"\n📊 Validation Results:")
        
        rising = [v for v in validations if v.get('trend') == 'RISING']
        stable = [v for v in validations if v.get('trend') == 'STABLE']
        falling = [v for v in validations if v.get('trend') == 'FALLING']
        no_data = [v for v in validations if v.get('status') == 'NO_DATA']
        errors = [v for v in validations if v.get('status') == 'ERROR']
        
        print(f"   🟢 RISING: {len(rising)} tickers")
        for v in rising:
            print(f"      ${v['ticker']}: +{v['change_percent']}% (interest: {v['current_interest']})")
        
        print(f"   🟡 STABLE: {len(stable)} tickers")
        print(f"   🔴 FALLING: {len(falling)} tickers")
        print(f"   ⚪ NO DATA: {len(no_data)} tickers")
        
        if errors:
            print(f"   ❌ ERRORS: {len(errors)} tickers (likely rate-limited)")
            print("      Wait 1 hour or increase delay between requests")
        
        print(f"\n💾 Saved {len(validations)} validations to {OUTPUT_FILE}")
        
        return validations


if __name__ == "__main__":
    # Example: Validate some tickers
    test_tickers = ['ASTS', 'PLTR', 'NVDA', 'GME']
    
    validator = GoogleTrendsValidator()
    results = validator.run(test_tickers)
