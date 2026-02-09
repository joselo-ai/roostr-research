#!/usr/bin/env python3
"""
Yieldschool Scraper - Extract crypto signals from Yieldschool Discord/platform
Runs daily to collect ticker mentions, conviction signals, and Dan's endorsements
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Any

class YieldschoolScraper:
    """Scrape Yieldschool for crypto signals"""
    
    def __init__(self):
        self.signals = []
        self.output_file = '../signals-database.csv'
        
    def scrape_yield_hub(self, messages: List[str]) -> List[Dict[str, Any]]:
        """
        Extract signals from Yield Hub messages
        
        Args:
            messages: List of message strings from Yield Hub
            
        Returns:
            List of signal dictionaries with ticker, conviction, price
        """
        signals = []
        
        for msg in messages:
            # Extract tickers (look for $ or uppercase 3-5 letter symbols)
            tickers = self._extract_tickers(msg)
            
            for ticker in tickers:
                # Count conviction signals
                conviction_score = self._calculate_conviction(msg, ticker)
                
                # Check if Dan endorsed
                dan_endorsed = 'Dan' in msg or '@Dan' in msg
                if dan_endorsed:
                    conviction_score += 2  # Dan's endorsement = +2 points
                
                signals.append({
                    'ticker': ticker,
                    'source': 'Yieldschool-YieldHub',
                    'date_found': datetime.now().strftime('%Y-%m-%d'),
                    'message_snippet': msg[:100],
                    'conviction_score': conviction_score,
                    'dan_endorsed': dan_endorsed
                })
        
        return signals
    
    def scrape_blue_chips(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Extract signals from Blue-Chips channel"""
        # Similar logic to yield_hub but for established projects
        return self._process_channel(messages, 'Yieldschool-BlueChips')
    
    def scrape_mid_caps(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Extract signals from Mid-Caps channel"""
        return self._process_channel(messages, 'Yieldschool-MidCaps')
    
    def _extract_tickers(self, message: str) -> List[str]:
        """
        Extract crypto tickers from message
        
        Returns:
            List of ticker symbols found
        """
        import re
        
        # Pattern 1: $TICKER format
        dollar_tickers = re.findall(r'\$([A-Z]{2,6})', message)
        
        # Pattern 2: Standalone uppercase 3-5 letters (common crypto format)
        standalone = re.findall(r'\b([A-Z]{3,5})\b', message)
        
        # Combine and dedupe
        all_tickers = list(set(dollar_tickers + standalone))
        
        # Filter out common words that aren't tickers
        blacklist = ['THE', 'AND', 'FOR', 'NOT', 'BUT', 'ARE', 'CAN', 'WILL', 'ETH', 'BTC']
        tickers = [t for t in all_tickers if t not in blacklist]
        
        return tickers
    
    def _calculate_conviction(self, message: str, ticker: str) -> int:
        """
        Calculate conviction score based on message content
        
        Returns:
            Score 1-10 (higher = more conviction)
        """
        score = 3  # Base score
        
        # Positive indicators
        if '🔥' in message:
            score += 1
        if '🚀' in message:
            score += 1
        if 'bullish' in message.lower():
            score += 1
        if 'buying' in message.lower():
            score += 1
        if 'accumulating' in message.lower():
            score += 1
        
        # Strong conviction phrases
        strong_phrases = ['high conviction', 'very bullish', 'loading up', 'going all in']
        if any(phrase in message.lower() for phrase in strong_phrases):
            score += 2
        
        # Cap at 10
        return min(score, 10)
    
    def _process_channel(self, messages: List[str], source: str) -> List[Dict[str, Any]]:
        """Generic channel processor"""
        signals = []
        
        for msg in messages:
            tickers = self._extract_tickers(msg)
            
            for ticker in tickers:
                conviction = self._calculate_conviction(msg, ticker)
                
                signals.append({
                    'ticker': ticker,
                    'source': source,
                    'date_found': datetime.now().strftime('%Y-%m-%d'),
                    'message_snippet': msg[:100],
                    'conviction_score': conviction,
                    'dan_endorsed': False
                })
        
        return signals
    
    def consolidate_signals(self, all_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Consolidate duplicate tickers, sum conviction scores
        
        Returns:
            Consolidated list with total conviction per ticker
        """
        ticker_map = {}
        
        for signal in all_signals:
            ticker = signal['ticker']
            
            if ticker not in ticker_map:
                ticker_map[ticker] = {
                    'ticker': ticker,
                    'sources': [],
                    'total_conviction': 0,
                    'mention_count': 0,
                    'dan_endorsed': False,
                    'date_found': signal['date_found']
                }
            
            ticker_map[ticker]['sources'].append(signal['source'])
            ticker_map[ticker]['total_conviction'] += signal['conviction_score']
            ticker_map[ticker]['mention_count'] += 1
            
            if signal.get('dan_endorsed'):
                ticker_map[ticker]['dan_endorsed'] = True
        
        # Convert to list and sort by conviction
        consolidated = list(ticker_map.values())
        consolidated.sort(key=lambda x: x['total_conviction'], reverse=True)
        
        return consolidated
    
    def save_to_csv(self, signals: List[Dict[str, Any]]):
        """Save signals to CSV database"""
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            
            for signal in signals:
                writer.writerow([
                    signal['ticker'],
                    ','.join(signal['sources']),
                    signal['date_found'],
                    '',  # price_entry (filled when deployed)
                    signal['total_conviction'],
                    'YELLOW',  # status (GREEN when validated)
                    'NO',  # deployed
                    '',  # position_size
                    '',  # stop_loss
                    '',  # target_1
                    '',  # target_2
                    '',  # current_price
                    '',  # pnl_dollars
                    '',  # pnl_percent
                    f"Mentions: {signal['mention_count']}, Dan endorsed: {signal['dan_endorsed']}"
                ])
        
        print(f"Saved {len(signals)} signals to {self.output_file}")
    
    def run(self, yield_hub_msgs: List[str], blue_chip_msgs: List[str], mid_cap_msgs: List[str]):
        """
        Main execution: scrape all channels and save results
        
        Args:
            yield_hub_msgs: Messages from Yield Hub
            blue_chip_msgs: Messages from Blue-Chips
            mid_cap_msgs: Messages from Mid-Caps
        """
        print("Scraping Yieldschool...")
        
        # Scrape each channel
        yh_signals = self.scrape_yield_hub(yield_hub_msgs)
        bc_signals = self.scrape_blue_chips(blue_chip_msgs)
        mc_signals = self.scrape_mid_caps(mid_cap_msgs)
        
        # Consolidate
        all_signals = yh_signals + bc_signals + mc_signals
        consolidated = self.consolidate_signals(all_signals)
        
        # Filter to GREEN candidates (high conviction)
        green_candidates = [s for s in consolidated if 
                           s['total_conviction'] >= 8 or 
                           s['dan_endorsed'] or 
                           s['mention_count'] >= 3]
        
        print(f"\nTotal signals: {len(consolidated)}")
        print(f"GREEN candidates: {len(green_candidates)}")
        
        # Display top signals
        print("\nTop 10 signals:")
        for i, signal in enumerate(consolidated[:10], 1):
            print(f"{i}. {signal['ticker']} - Conviction: {signal['total_conviction']}, "
                  f"Mentions: {signal['mention_count']}, Dan: {signal['dan_endorsed']}")
        
        # Save to database
        self.save_to_csv(consolidated)
        
        return green_candidates


# Example usage (replace with actual message scraping)
if __name__ == "__main__":
    # Placeholder - replace with actual Discord/platform scraping
    sample_yield_hub = [
        "$SOL looking very bullish here. Dan mentioned accumulating 🔥",
        "High conviction on $RNDR - AI narrative heating up 🚀",
        "$FET consolidating, waiting for breakout"
    ]
    
    sample_blue_chips = [
        "$ETH staking yields improving",
        "$AVAX subnet activity increasing"
    ]
    
    sample_mid_caps = [
        "$PENDLE real yield narrative 🔥",
        "$GMX v2 launch coming soon"
    ]
    
    scraper = YieldschoolScraper()
    green_signals = scraper.run(sample_yield_hub, sample_blue_chips, sample_mid_caps)
    
    print(f"\n🟢 Deploy these {len(green_signals)} signals:")
    for signal in green_signals:
        print(f"- {signal['ticker']} (Conviction: {signal['total_conviction']})")
