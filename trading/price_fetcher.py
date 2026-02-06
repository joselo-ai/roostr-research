#!/usr/bin/env python3
"""
Real-Time Price Fetcher for roostr Trading
Uses CoinGecko API (free tier, no API key needed)
Fetches live prices for BTC, ETH, SOL, TAO, and any crypto ticker
"""

import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import urllib.request
import urllib.error

class PriceFetcher:
    """Fetch real-time crypto prices from CoinGecko"""
    
    # Ticker → CoinGecko ID mapping
    TICKER_MAP = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'SOL': 'solana',
        'TAO': 'bittensor',
        'RNDR': 'render-token',
        'FET': 'fetch-ai',
        'NEAR': 'near',
        'AVAX': 'avalanche-2',
        'MATIC': 'matic-network',
        'DOT': 'polkadot',
        'LINK': 'chainlink',
        'UNI': 'uniswap',
        'AAVE': 'aave',
        'ATOM': 'cosmos',
        'ADA': 'cardano'
    }
    
    BASE_URL = 'https://api.coingecko.com/api/v3'
    CACHE_FILE = '.price_cache.json'
    CACHE_TTL = 60  # Cache valid for 60 seconds
    
    def __init__(self, cache_dir: str = '.'):
        """Initialize price fetcher with cache directory"""
        self.cache_dir = cache_dir
        self.cache_path = os.path.join(cache_dir, self.CACHE_FILE)
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load price cache from disk"""
        if not os.path.exists(self.cache_path):
            return {}
        
        try:
            with open(self.cache_path, 'r') as f:
                cache = json.load(f)
                # Validate cache age
                if 'timestamp' in cache:
                    cache_time = datetime.fromisoformat(cache['timestamp'])
                    if datetime.now() - cache_time > timedelta(seconds=self.CACHE_TTL):
                        return {}  # Cache expired
                return cache
        except (json.JSONDecodeError, ValueError):
            return {}
    
    def _save_cache(self):
        """Save price cache to disk"""
        self.cache['timestamp'] = datetime.now().isoformat()
        try:
            with open(self.cache_path, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _fetch_from_api(self, url: str, timeout: int = 10) -> Optional[Dict]:
        """Fetch JSON data from CoinGecko API"""
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'roostr-trading-bot/1.0')
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                return json.loads(data.decode('utf-8'))
        
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"⚠️  Rate limited by CoinGecko (429). Using cached data.")
            else:
                print(f"❌ HTTP Error {e.code}: {e.reason}")
            return None
        
        except urllib.error.URLError as e:
            print(f"❌ Network error: {e.reason}")
            return None
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_coingecko_id(self, ticker: str) -> Optional[str]:
        """Convert ticker to CoinGecko ID"""
        ticker = ticker.upper()
        
        # Check known mappings first
        if ticker in self.TICKER_MAP:
            return self.TICKER_MAP[ticker]
        
        # Try searching CoinGecko (rate-limited, use sparingly)
        print(f"⚠️  Unknown ticker {ticker}, searching CoinGecko...")
        url = f"{self.BASE_URL}/search?query={ticker}"
        data = self._fetch_from_api(url)
        
        if data and 'coins' in data and len(data['coins']) > 0:
            # Take first result
            coin = data['coins'][0]
            coingecko_id = coin['id']
            print(f"✓ Found {ticker} → {coingecko_id} (name: {coin['name']})")
            
            # Cache this mapping
            self.TICKER_MAP[ticker] = coingecko_id
            return coingecko_id
        
        print(f"❌ Could not find {ticker} on CoinGecko")
        return None
    
    def get_price(self, ticker: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Get current price for a ticker
        
        Returns:
            {
                'ticker': 'SOL',
                'price': 86.60,
                'price_change_24h': -2.5,
                'market_cap': 42000000000,
                'last_updated': '2026-02-06T12:08:00Z',
                'source': 'coingecko'
            }
        """
        ticker = ticker.upper()
        
        # Check cache first
        if use_cache and ticker in self.cache:
            cached = self.cache[ticker]
            if 'timestamp' in cached:
                cache_time = datetime.fromisoformat(cached['timestamp'])
                if datetime.now() - cache_time < timedelta(seconds=self.CACHE_TTL):
                    return cached
        
        # Get CoinGecko ID
        coingecko_id = self.get_coingecko_id(ticker)
        if not coingecko_id:
            return None
        
        # Fetch live price
        url = (f"{self.BASE_URL}/simple/price"
               f"?ids={coingecko_id}"
               f"&vs_currencies=usd"
               f"&include_market_cap=true"
               f"&include_24hr_change=true"
               f"&include_last_updated_at=true")
        
        data = self._fetch_from_api(url)
        
        if not data or coingecko_id not in data:
            print(f"❌ No price data for {ticker}")
            return None
        
        coin_data = data[coingecko_id]
        
        result = {
            'ticker': ticker,
            'coingecko_id': coingecko_id,
            'price': coin_data.get('usd', 0),
            'price_change_24h': coin_data.get('usd_24h_change', 0),
            'market_cap': coin_data.get('usd_market_cap', 0),
            'last_updated': datetime.fromtimestamp(
                coin_data.get('last_updated_at', time.time())
            ).isoformat(),
            'source': 'coingecko',
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache result
        self.cache[ticker] = result
        self._save_cache()
        
        return result
    
    def get_multiple_prices(self, tickers: List[str], use_cache: bool = True) -> Dict[str, Dict]:
        """
        Fetch prices for multiple tickers (batch)
        More efficient than calling get_price() multiple times
        """
        results = {}
        
        # Convert all tickers to CoinGecko IDs
        ticker_to_id = {}
        for ticker in tickers:
            ticker = ticker.upper()
            coingecko_id = self.get_coingecko_id(ticker)
            if coingecko_id:
                ticker_to_id[ticker] = coingecko_id
        
        if not ticker_to_id:
            print("❌ No valid tickers found")
            return results
        
        # Build batch request
        ids = ','.join(ticker_to_id.values())
        url = (f"{self.BASE_URL}/simple/price"
               f"?ids={ids}"
               f"&vs_currencies=usd"
               f"&include_market_cap=true"
               f"&include_24hr_change=true"
               f"&include_last_updated_at=true")
        
        data = self._fetch_from_api(url)
        
        if not data:
            print("❌ Failed to fetch batch prices")
            return results
        
        # Parse results
        for ticker, coingecko_id in ticker_to_id.items():
            if coingecko_id in data:
                coin_data = data[coingecko_id]
                
                result = {
                    'ticker': ticker,
                    'coingecko_id': coingecko_id,
                    'price': coin_data.get('usd', 0),
                    'price_change_24h': coin_data.get('usd_24h_change', 0),
                    'market_cap': coin_data.get('usd_market_cap', 0),
                    'last_updated': datetime.fromtimestamp(
                        coin_data.get('last_updated_at', time.time())
                    ).isoformat(),
                    'source': 'coingecko',
                    'timestamp': datetime.now().isoformat()
                }
                
                results[ticker] = result
                
                # Cache result
                self.cache[ticker] = result
        
        # Save cache after batch update
        self._save_cache()
        
        return results
    
    def is_cache_fresh(self, max_age_seconds: int = 60) -> bool:
        """Check if cache is fresh enough"""
        if not self.cache or 'timestamp' not in self.cache:
            return False
        
        cache_time = datetime.fromisoformat(self.cache['timestamp'])
        age = (datetime.now() - cache_time).total_seconds()
        return age < max_age_seconds


# CLI Interface
def main():
    """Command-line interface for testing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python price_fetcher.py <TICKER> [TICKER2 TICKER3 ...]")
        print("Example: python price_fetcher.py SOL TAO BTC")
        sys.exit(1)
    
    tickers = sys.argv[1:]
    fetcher = PriceFetcher(cache_dir='.')
    
    if len(tickers) == 1:
        # Single ticker
        result = fetcher.get_price(tickers[0], use_cache=False)
        if result:
            print(f"\n✅ {result['ticker']} Price Data:")
            print(f"   Price: ${result['price']:,.2f}")
            print(f"   24h Change: {result['price_change_24h']:+.2f}%")
            print(f"   Market Cap: ${result['market_cap']:,.0f}")
            print(f"   Last Updated: {result['last_updated']}")
            print(f"   Source: {result['source']}")
        else:
            print(f"❌ Failed to fetch price for {tickers[0]}")
            sys.exit(1)
    else:
        # Multiple tickers (batch)
        results = fetcher.get_multiple_prices(tickers, use_cache=False)
        print(f"\n✅ Fetched {len(results)} / {len(tickers)} prices:\n")
        
        for ticker, data in results.items():
            print(f"{ticker:8} ${data['price']:>10,.2f}   ({data['price_change_24h']:+6.2f}%)")
        
        # Show failed tickers
        failed = set(t.upper() for t in tickers) - set(results.keys())
        if failed:
            print(f"\n❌ Failed to fetch: {', '.join(failed)}")


if __name__ == "__main__":
    main()
