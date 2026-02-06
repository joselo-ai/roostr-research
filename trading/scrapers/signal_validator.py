#!/usr/bin/env python3
"""
Signal Validator - Validate signals with Google Trends, Dexscreener, fundamental checks
Filters false positives before deployment
"""

import json
import requests
from typing import Dict, Any, List
from datetime import datetime

class SignalValidator:
    """Validate signals before marking as GREEN"""
    
    def __init__(self):
        self.dex_api = "https://api.dexscreener.com/latest/dex/search"
        
    def validate_crypto(self, ticker: str, source_conviction: int) -> Dict[str, Any]:
        """
        Validate crypto signal with on-chain data
        
        Args:
            ticker: Crypto ticker (e.g., 'SOL', 'RNDR')
            source_conviction: Initial conviction from scraping
            
        Returns:
            Validation result with adjusted conviction
        """
        result = {
            'ticker': ticker,
            'validated': False,
            'conviction_adjusted': source_conviction,
            'reasons': [],
            'dex_data': None,
            'deploy': False
        }
        
        # Check Dexscreener
        dex_data = self._check_dexscreener(ticker)
        
        if dex_data:
            result['dex_data'] = dex_data
            
            # Liquidity check
            liquidity = dex_data.get('liquidity', 0)
            if liquidity < 100_000:
                result['reasons'].append(f"Low liquidity: ${liquidity:,.0f}")
                result['conviction_adjusted'] -= 2
            elif liquidity > 1_000_000:
                result['reasons'].append(f"Strong liquidity: ${liquidity:,.0f}")
                result['conviction_adjusted'] += 1
            
            # Volume check
            volume_24h = dex_data.get('volume_24h', 0)
            if volume_24h < 50_000:
                result['reasons'].append(f"Low volume: ${volume_24h:,.0f}")
                result['conviction_adjusted'] -= 1
            
            # Price chart check (not already 10x'd recently)
            price_change_24h = dex_data.get('price_change_24h', 0)
            if price_change_24h > 100:  # Already 2x'd in 24h
                result['reasons'].append(f"Already pumped: +{price_change_24h}% today")
                result['conviction_adjusted'] -= 3
            
            # Scam check (basic)
            if dex_data.get('honeypot_risk', False):
                result['reasons'].append("Honeypot risk detected")
                result['conviction_adjusted'] = 0  # Kill signal
        else:
            result['reasons'].append("Not found on DEX (may be CEX-only or invalid)")
            result['conviction_adjusted'] -= 1
        
        # Decision
        if result['conviction_adjusted'] >= 7:
            result['validated'] = True
            result['deploy'] = True
            result['reasons'].append("✅ VALIDATED - Deploy")
        elif result['conviction_adjusted'] >= 5:
            result['validated'] = True
            result['deploy'] = False
            result['reasons'].append("⚠️ VALIDATED but wait for better setup")
        else:
            result['reasons'].append("❌ REJECTED - Low conviction after validation")
        
        return result
    
    def validate_stock(self, ticker: str, source_conviction: int, thesis: str) -> Dict[str, Any]:
        """
        Validate stock signal with Google Trends and fundamental checks
        
        Args:
            ticker: Stock ticker (e.g., 'ASTS', 'TAC')
            source_conviction: Initial conviction from reactions
            thesis: Investment thesis text
            
        Returns:
            Validation result with adjusted conviction
        """
        result = {
            'ticker': ticker,
            'validated': False,
            'conviction_adjusted': source_conviction,
            'reasons': [],
            'google_trends': None,
            'deploy': False
        }
        
        # Google Trends check
        trends_data = self._check_google_trends(ticker)
        
        if trends_data:
            result['google_trends'] = trends_data
            
            trend_direction = trends_data.get('direction', 'flat')
            
            if trend_direction == 'rising':
                result['reasons'].append("Google Trends: Rising ✅")
                result['conviction_adjusted'] += 1
            elif trend_direction == 'peaked':
                result['reasons'].append("Google Trends: Already peaked ⚠️")
                result['conviction_adjusted'] -= 2
            elif trend_direction == 'flat':
                result['reasons'].append("Google Trends: Flat (early or no interest)")
        else:
            result['reasons'].append("Google Trends: No data")
        
        # Fundamental thesis check
        fundamental_score = self._score_thesis_quality(thesis)
        result['reasons'].append(f"Thesis quality: {fundamental_score}/10")
        
        if fundamental_score >= 7:
            result['conviction_adjusted'] += 1
        elif fundamental_score <= 3:
            result['conviction_adjusted'] -= 2
            result['reasons'].append("Weak thesis (hype-based)")
        
        # Decision
        if result['conviction_adjusted'] >= 8:
            result['validated'] = True
            result['deploy'] = True
            result['reasons'].append("✅ VALIDATED - Deploy")
        elif result['conviction_adjusted'] >= 6:
            result['validated'] = True
            result['deploy'] = False
            result['reasons'].append("⚠️ VALIDATED but needs better entry")
        else:
            result['reasons'].append("❌ REJECTED - Failed validation")
        
        return result
    
    def _check_dexscreener(self, ticker: str) -> Dict[str, Any]:
        """
        Query Dexscreener API for on-chain data
        
        Returns:
            DEX data dict or None if not found
        """
        try:
            # Placeholder - actual implementation would hit real API
            # For now, return mock data structure
            
            # In production:
            # response = requests.get(f"{self.dex_api}?q={ticker}")
            # if response.status_code == 200:
            #     data = response.json()
            #     # Parse and return relevant fields
            
            # Mock response for development
            mock_data = {
                'ticker': ticker,
                'liquidity': 500_000,  # USD
                'volume_24h': 150_000,
                'price_change_24h': 5.2,  # %
                'honeypot_risk': False
            }
            
            return mock_data
            
        except Exception as e:
            print(f"Dexscreener API error: {e}")
            return None
    
    def _check_google_trends(self, ticker: str) -> Dict[str, Any]:
        """
        Check Google Trends for search volume direction
        
        Returns:
            Trends data dict or None
        """
        try:
            # Placeholder - actual implementation would use pytrends or API
            
            # In production:
            # from pytrends.request import TrendReq
            # pytrends = TrendReq()
            # pytrends.build_payload([ticker], timeframe='now 7-d')
            # data = pytrends.interest_over_time()
            # direction = 'rising' if data increasing else 'peaked' if data decreasing else 'flat'
            
            # Mock response
            mock_data = {
                'ticker': ticker,
                'direction': 'rising',  # or 'peaked' or 'flat'
                'current_interest': 65,  # 0-100 scale
                'peak_interest': 100,
                'interest_change_7d': 15  # % change
            }
            
            return mock_data
            
        except Exception as e:
            print(f"Google Trends error: {e}")
            return None
    
    def _score_thesis_quality(self, thesis: str) -> int:
        """
        Score investment thesis quality 1-10
        
        Returns:
            Quality score
        """
        score = 5  # Base
        
        # Positive indicators (fundamental analysis)
        fundamental_words = [
            'revenue', 'earnings', 'profit', 'growth', 'market share',
            'competitive advantage', 'moat', 'management', 'valuation',
            'cash flow', 'addressable market', 'tam', 'partnerships'
        ]
        
        fundamental_count = sum(1 for word in fundamental_words if word in thesis.lower())
        score += min(fundamental_count, 3)  # Cap bonus at +3
        
        # Negative indicators (hype/speculation)
        hype_words = [
            'moon', 'lambo', '🚀🚀', 'guaranteed', 'can''t lose',
            '100x', 'to the moon', 'ape in'
        ]
        
        hype_count = sum(1 for word in hype_words if word.lower() in thesis.lower())
        score -= min(hype_count * 2, 4)  # Hype penalty up to -4
        
        # Length check (detailed thesis > short hype)
        if len(thesis) > 200:
            score += 1
        if len(thesis) < 50:
            score -= 1
        
        return max(min(score, 10), 1)
    
    def batch_validate(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate multiple signals and return deploy-ready ones
        
        Args:
            signals: List of signal dicts from scrapers
            
        Returns:
            List of validated signals ready to deploy
        """
        validated = []
        
        for signal in signals:
            ticker = signal['ticker']
            source = signal.get('source', 'Unknown')
            conviction = signal.get('conviction_score', 5)
            
            print(f"\nValidating {ticker} from {source}...")
            
            # Route to correct validator
            if 'Yieldschool' in source:
                result = self.validate_crypto(ticker, conviction)
            elif 'DumbMoney' in source:
                thesis = signal.get('thesis_snippet', '')
                result = self.validate_stock(ticker, conviction, thesis)
            else:
                print(f"Unknown source: {source}, skipping")
                continue
            
            # Display result
            print(f"  Conviction: {conviction} → {result['conviction_adjusted']}")
            for reason in result['reasons']:
                print(f"  {reason}")
            
            if result['deploy']:
                validated.append({
                    **signal,
                    'conviction_score': result['conviction_adjusted'],
                    'validation_passed': True,
                    'validation_reasons': ', '.join(result['reasons'])
                })
        
        return validated


# Example usage
if __name__ == "__main__":
    validator = SignalValidator()
    
    # Sample signals to validate
    sample_signals = [
        {
            'ticker': 'SOL',
            'source': 'Yieldschool-YieldHub',
            'conviction_score': 8,
            'dan_endorsed': True
        },
        {
            'ticker': 'ASTS',
            'source': 'DumbMoney',
            'conviction_score': 7,
            'thesis_snippet': 'SpaceMobile is first-mover in satellite-to-cell. Partnerships with AT&T and Verizon. Waiting on FCC approval. Market cap $38B but TAM is massive. Revenue starting 2026.',
            'total_reactions': 34
        },
        {
            'ticker': 'SCAM',
            'source': 'Yieldschool-LowCaps',
            'conviction_score': 6,
            'dan_endorsed': False
        }
    ]
    
    validated = validator.batch_validate(sample_signals)
    
    print(f"\n{'='*60}")
    print(f"✅ VALIDATED & READY TO DEPLOY: {len(validated)} signals")
    print(f"{'='*60}")
    
    for signal in validated:
        print(f"\n{signal['ticker']} ({signal['source']})")
        print(f"  Conviction: {signal['conviction_score']}/10")
        print(f"  Reasons: {signal['validation_reasons']}")
