#!/usr/bin/env python3
"""
Dumb Money Discord Scraper - Extract social arbitrage signals
Focuses on high-conviction tickers (20+ reactions) posted recently (<48h)
"""

import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DumbMoneyScraper:
    """Scrape Dumb Money Discord for social arbitrage signals"""
    
    def __init__(self):
        self.output_file = '../signals-database.csv'
        self.reaction_threshold = 20  # Min reactions for GREEN
        self.hours_fresh = 48  # Only fresh theses (<48h)
        
    def scrape_channel(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract high-conviction stock signals
        
        Args:
            messages: List of message dicts with content, reactions, timestamp
            
        Returns:
            List of signal dictionaries
        """
        signals = []
        cutoff_time = datetime.now() - timedelta(hours=self.hours_fresh)
        
        for msg in messages:
            # Check if fresh
            msg_time = datetime.fromisoformat(msg.get('timestamp', datetime.now().isoformat()))
            if msg_time < cutoff_time:
                continue  # Skip stale messages
            
            # Extract tickers
            tickers = self._extract_tickers(msg['content'])
            
            # Count reactions
            reactions = msg.get('reactions', {})
            total_reactions = self._count_conviction_reactions(reactions)
            
            # Skip if low conviction
            if total_reactions < 15:  # Pre-filter (below threshold)
                continue
            
            # Extract thesis
            thesis = self._extract_thesis(msg['content'])
            
            for ticker in tickers:
                signal = {
                    'ticker': ticker,
                    'source': 'DumbMoney',
                    'date_found': datetime.now().strftime('%Y-%m-%d'),
                    'message_timestamp': msg_time.strftime('%Y-%m-%d %H:%M'),
                    'total_reactions': total_reactions,
                    'fire_reactions': reactions.get('🔥', 0),
                    'rocket_reactions': reactions.get('🚀', 0),
                    'thumbsup_reactions': reactions.get('👍', 0),
                    'muscle_reactions': reactions.get('💪', 0),
                    'thesis_snippet': thesis[:200],
                    'conviction_score': self._calculate_conviction(total_reactions, msg['content']),
                    'status': 'YELLOW'
                }
                
                # Mark as GREEN if meets threshold
                if total_reactions >= self.reaction_threshold:
                    signal['status'] = 'GREEN'
                
                signals.append(signal)
        
        return signals
    
    def _extract_tickers(self, content: str) -> List[str]:
        """
        Extract stock tickers from message
        
        Returns:
            List of ticker symbols (e.g., ['ASTS', 'TAC'])
        """
        import re
        
        # Pattern 1: $TICKER format (most common)
        dollar_tickers = re.findall(r'\$([A-Z]{1,5})', content)
        
        # Pattern 2: Standalone uppercase 1-5 letters near financial keywords
        # (More conservative than crypto - stocks often use longer names)
        financial_keywords = ['stock', 'shares', 'price', 'earnings', 'revenue', 'market cap']
        
        tickers = []
        
        # Add dollar tickers
        tickers.extend(dollar_tickers)
        
        # Filter common words
        blacklist = ['I', 'A', 'THE', 'AND', 'FOR', 'ARE', 'CAN', 'CEO', 'CFO', 'USA', 'NYSE', 'IMO']
        tickers = [t for t in tickers if t not in blacklist]
        
        # Dedupe
        return list(set(tickers))
    
    def _count_conviction_reactions(self, reactions: Dict[str, int]) -> int:
        """
        Count conviction reactions (🔥🚀👍💪)
        
        Returns:
            Total conviction reaction count
        """
        conviction_emojis = ['🔥', '🚀', '👍', '💪', '💎', '🙌']
        total = sum(reactions.get(emoji, 0) for emoji in conviction_emojis)
        return total
    
    def _extract_thesis(self, content: str) -> str:
        """
        Extract investment thesis from message
        
        Returns:
            Cleaned thesis string
        """
        # Remove links
        import re
        content = re.sub(r'http\S+', '', content)
        
        # Remove excessive whitespace
        content = ' '.join(content.split())
        
        return content
    
    def _calculate_conviction(self, total_reactions: int, content: str) -> int:
        """
        Calculate conviction score 1-10
        
        Args:
            total_reactions: Total conviction emoji reactions
            content: Message content
            
        Returns:
            Score 1-10
        """
        # Base score from reactions
        if total_reactions >= 30:
            score = 9
        elif total_reactions >= 25:
            score = 8
        elif total_reactions >= 20:
            score = 7
        elif total_reactions >= 15:
            score = 6
        else:
            score = 5
        
        # Bonus for quality thesis indicators
        quality_indicators = [
            'revenue growth',
            'earnings',
            'market share',
            'competitive advantage',
            'addressable market',
            'moat'
        ]
        
        if any(indicator in content.lower() for indicator in quality_indicators):
            score += 1
        
        # Penalty for hype language
        hype_words = ['moon', 'lambo', 'to the moon', '🚀🚀🚀']
        if any(word in content.lower() for word in hype_words):
            score -= 1
        
        # Cap at 10
        return min(max(score, 1), 10)
    
    def validate_freshness(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter to only fresh signals (<48h old)
        
        Returns:
            Filtered list of fresh signals
        """
        fresh = []
        cutoff = datetime.now() - timedelta(hours=self.hours_fresh)
        
        for signal in signals:
            msg_time = datetime.strptime(signal['message_timestamp'], '%Y-%m-%d %H:%M')
            if msg_time >= cutoff:
                fresh.append(signal)
        
        return fresh
    
    def consolidate_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Consolidate duplicate tickers, sum reactions
        
        Returns:
            Consolidated list with max conviction per ticker
        """
        ticker_map = {}
        
        for signal in signals:
            ticker = signal['ticker']
            
            if ticker not in ticker_map:
                ticker_map[ticker] = signal
            else:
                # Keep the one with more reactions
                if signal['total_reactions'] > ticker_map[ticker]['total_reactions']:
                    ticker_map[ticker] = signal
        
        # Convert to list and sort by reactions
        consolidated = list(ticker_map.values())
        consolidated.sort(key=lambda x: x['total_reactions'], reverse=True)
        
        return consolidated
    
    def save_to_csv(self, signals: List[Dict[str, Any]]):
        """Save signals to CSV database"""
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            
            for signal in signals:
                writer.writerow([
                    signal['ticker'],
                    signal['source'],
                    signal['date_found'],
                    '',  # price_entry (filled when deployed)
                    signal['conviction_score'],
                    signal['status'],
                    'NO',  # deployed
                    '',  # position_size
                    '',  # stop_loss
                    '',  # target_1
                    '',  # target_2
                    '',  # current_price
                    '',  # pnl_dollars
                    '',  # pnl_percent
                    f"Reactions: {signal['total_reactions']} (🔥{signal['fire_reactions']} 🚀{signal['rocket_reactions']}), Fresh: {signal['message_timestamp']}"
                ])
        
        print(f"Saved {len(signals)} signals to {self.output_file}")
    
    def run(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Main execution: scrape Dumb Money and return GREEN signals
        
        Args:
            messages: List of Discord message dicts
            
        Returns:
            List of GREEN signals ready to deploy
        """
        print("Scraping Dumb Money Discord...")
        
        # Extract all signals
        all_signals = self.scrape_channel(messages)
        
        # Filter to fresh only
        fresh_signals = self.validate_freshness(all_signals)
        
        # Consolidate duplicates
        consolidated = self.consolidate_signals(fresh_signals)
        
        # Filter to GREEN only (20+ reactions)
        green_signals = [s for s in consolidated if s['status'] == 'GREEN']
        
        print(f"\nTotal signals extracted: {len(all_signals)}")
        print(f"Fresh signals (<48h): {len(fresh_signals)}")
        print(f"After consolidation: {len(consolidated)}")
        print(f"GREEN signals (20+ reactions): {len(green_signals)}")
        
        # Display top signals
        print("\nTop 10 signals:")
        for i, signal in enumerate(consolidated[:10], 1):
            status_emoji = '🟢' if signal['status'] == 'GREEN' else '🟡'
            print(f"{status_emoji} {i}. {signal['ticker']} - "
                  f"{signal['total_reactions']} reactions (🔥{signal['fire_reactions']} 🚀{signal['rocket_reactions']}), "
                  f"Conviction: {signal['conviction_score']}/10")
            print(f"   Thesis: {signal['thesis_snippet'][:100]}...")
            print()
        
        # Save to database
        self.save_to_csv(consolidated)
        
        return green_signals


# Example usage
if __name__ == "__main__":
    # Sample messages (replace with actual Discord scraping)
    sample_messages = [
        {
            'content': "$ASTS SpaceMobile is the first-mover in satellite-to-cell. Partnerships with AT&T, Verizon. Waiting on FCC approval but when it hits, this could 3x. Market cap $38B but TAM is massive.",
            'reactions': {'🔥': 34, '🚀': 16, '👍': 8},
            'timestamp': datetime.now().isoformat()
        },
        {
            'content': "$TAC TransAlta Energy - undervalued renewable play. Revenue growing 15% YoY. Trading at 0.8x book value. Dividend yield 4.5%. Institutional accumulation visible.",
            'reactions': {'👍': 32, '🔥': 11},
            'timestamp': (datetime.now() - timedelta(hours=12)).isoformat()
        },
        {
            'content': "$AS to the moon! 🚀🚀🚀 This will 10x easy!",
            'reactions': {'🔥': 25, '💪': 10},
            'timestamp': (datetime.now() - timedelta(hours=6)).isoformat()
        }
    ]
    
    scraper = DumbMoneyScraper()
    green_signals = scraper.run(sample_messages)
    
    print(f"\n🟢 Deploy these {len(green_signals)} social arb signals:")
    for signal in green_signals:
        print(f"- {signal['ticker']} ({signal['total_reactions']} reactions, Conviction: {signal['conviction_score']}/10)")
