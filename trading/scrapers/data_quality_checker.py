#!/usr/bin/env python3
"""
Data Quality Checker - 3-layer validation before database writes
Prevents garbage signals from polluting the trading system
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any
import re


class DataQualityChecker:
    """Validate signals before writing to database"""
    
    def __init__(
        self, 
        blacklist_file: str = 'config/ticker_blacklist.txt',
        database_file: str = '../signals-database.csv'
    ):
        """
        Initialize quality checker
        
        Args:
            blacklist_file: Path to ticker blacklist (common words)
            database_file: Path to existing signal database (for duplicate check)
        """
        self.blacklist = self._load_blacklist(blacklist_file)
        self.database_file = database_file
        self.existing_signals = self._load_existing_signals()
        
        # Approved sources
        self.approved_sources = [
            'Yieldschool', 'Yieldschool-YieldHub', 'Yieldschool-BlueChips', 'Yieldschool-MidCaps',
            'DumbMoney', 'ChartFanatics', 'ChartFanatics-Riz',
            'WhaleBotAlerts', 'TheTIE', 'UnusualWhales', 'CryptoCred', 'StockBeep'
        ]
        
        # Quality thresholds
        self.thresholds = {
            'min_conviction_yellow': 5,
            'min_conviction_green': 8,
            'max_age_hours_social': 48,
            'max_age_hours_crypto': 168,  # 7 days
            'max_age_hours_forex': 24
        }
    
    def _load_blacklist(self, filepath: str) -> set:
        """Load ticker blacklist from file"""
        try:
            with open(filepath, 'r') as f:
                words = {line.strip().upper() for line in f if line.strip()}
            print(f"✅ Loaded {len(words)} blacklisted words")
            return words
        except FileNotFoundError:
            print(f"⚠️  Blacklist not found: {filepath}")
            print("Creating default blacklist...")
            
            # Expanded blacklist (500+ common words)
            default_blacklist = self._get_default_blacklist()
            
            # Create file
            import os
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write('\n'.join(sorted(default_blacklist)))
            
            print(f"✅ Created blacklist with {len(default_blacklist)} words")
            return default_blacklist
    
    def _get_default_blacklist(self) -> set:
        """Return comprehensive blacklist of non-ticker words"""
        common_words = {
            # Common short words
            'A', 'I', 'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
            'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM',
            'HIS', 'HOW', 'MAN', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO',
            'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE',
            
            # Finance/trading jargon (not tickers)
            'CEO', 'CFO', 'CTO', 'IPO', 'ATH', 'ATL', 'FOMO', 'FUD', 'DYOR',
            'NFA', 'IMO', 'IMHO', 'TBH', 'HODL', 'REKT', 'BTFD', 'WAGMI',
            
            # Exchanges/platforms (not tickers)
            'NYSE', 'NASDAQ', 'CME', 'CBOE', 'DEX', 'CEX', 'USA', 'USD',
            
            # Common crypto (exclude from signals to avoid noise)
            'BTC', 'ETH', 'USDT', 'USDC', 'BUSD',  # Too common, scrape separately
            
            # Days/months
            'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN',
            'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
            
            # Common verbs/adjectives often in caps
            'BIG', 'GOOD', 'BEST', 'HIGH', 'LOW', 'LONG', 'SHORT', 'STOP', 'WAIT',
            'LOVE', 'HATE', 'NICE', 'COOL', 'EPIC', 'HUGE', 'MEGA', 'SUPER',
            
            # Numbers/measurements
            'ONE', 'TWO', 'TEN', 'HUNDRED', 'MILLION', 'BILLION',
            
            # Reactions/emotions
            'LOL', 'LMAO', 'ROFL', 'WTF', 'OMG', 'YOLO', 'GG', 'EZ', 'RIP',
            
            # More finance terms
            'CALL', 'PUT', 'BULL', 'BEAR', 'MOON', 'DUMP', 'PUMP', 'SCAM',
            'TRADE', 'CHART', 'LONG', 'SWING', 'SCALE', 'EXIT', 'ENTRY'
        }
        
        # Add common 3-letter words
        three_letter_common = {
            'ADD', 'AGE', 'AGO', 'AID', 'AIM', 'AIR', 'ANY', 'APE', 'APT', 'ARC',
            'ARM', 'ART', 'ASK', 'ATE', 'BAD', 'BAG', 'BAR', 'BAT', 'BAY', 'BED',
            'BET', 'BID', 'BIT', 'BOX', 'BUG', 'BUS', 'BUY', 'CAB', 'CAP', 'CAR',
            'CAT', 'COW', 'CRY', 'CUP', 'CUT', 'DAM', 'DIG', 'DOG', 'DOT', 'DRY',
            'DUE', 'EAR', 'EAT', 'EGG', 'END', 'ERA', 'EYE', 'FAN', 'FAR', 'FAT',
            'FEE', 'FEW', 'FIG', 'FIT', 'FIX', 'FLY', 'FOE', 'FOG', 'FUN', 'FUR',
            'GAP', 'GAS', 'GAY', 'GEM', 'GUN', 'GUT', 'GUY', 'GYM', 'HAD', 'HAM',
            'HAT', 'HIT', 'HOT', 'HUB', 'HUG', 'ICE', 'ILL', 'INK', 'INN', 'JAM',
            'JAR', 'JAW', 'JET', 'JOB', 'JOY', 'KEY', 'KID', 'KIT', 'LAB', 'LAD',
            'LAP', 'LAW', 'LAY', 'LEG', 'LID', 'LIE', 'LIP', 'LOG', 'LOT', 'LOW',
            'MAD', 'MAP', 'MAT', 'MAY', 'MEN', 'MET', 'MID', 'MIX', 'MOB', 'MUD',
            'NET', 'NOR', 'NUT', 'OAK', 'ODD', 'OFF', 'OIL', 'OPT', 'ORB', 'OWE',
            'OWN', 'PAD', 'PAL', 'PAN', 'PAT', 'PAW', 'PAY', 'PEA', 'PEN', 'PET',
            'PIE', 'PIG', 'PIN', 'PIT', 'POT', 'PRO', 'PUB', 'RAG', 'RAN', 'RAT',
            'RAW', 'RAY', 'RED', 'REP', 'RID', 'RIG', 'RIM', 'ROB', 'ROD', 'ROT',
            'ROW', 'RUB', 'RUG', 'RUM', 'RUN', 'RUT', 'SAD', 'SAG', 'SAT', 'SAW',
            'SET', 'SEW', 'SHY', 'SIN', 'SIP', 'SIR', 'SIT', 'SIX', 'SKI', 'SKY',
            'SOB', 'SON', 'SOT', 'SOW', 'SOY', 'SPA', 'SPY', 'STY', 'SUM', 'SUN',
            'TAB', 'TAG', 'TAN', 'TAP', 'TAR', 'TAX', 'TEA', 'TEN', 'TIE', 'TIN',
            'TIP', 'TOE', 'TON', 'TOP', 'TOT', 'TOW', 'TOY', 'TRY', 'TUB', 'TUG',
            'VAN', 'VAT', 'VIA', 'VIE', 'VOW', 'WAD', 'WAG', 'WAR', 'WAX', 'WEB',
            'WED', 'WET', 'WIG', 'WIN', 'WIT', 'WOE', 'WOK', 'WON', 'WOO', 'YAK',
            'YAM', 'YAP', 'YAW', 'YEA', 'YES', 'YET', 'YEW', 'YIN', 'ZIP', 'ZOO'
        }
        
        return common_words | three_letter_common
    
    def _load_existing_signals(self) -> List[Dict[str, Any]]:
        """Load existing signals from database for duplicate checking"""
        signals = []
        
        try:
            with open(self.database_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Ticker') and not row['Ticker'].startswith('#'):
                        signals.append(row)
        except FileNotFoundError:
            print(f"⚠️  Database file not found: {self.database_file}")
        
        return signals
    
    def validate_signal(self, signal: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """
        Run 3-layer validation on signal
        
        Args:
            signal: Signal dictionary from scraper
        
        Returns:
            Tuple of (is_valid, status, reasons)
            - is_valid: True if passed all checks
            - status: 'GREEN', 'YELLOW', or 'RED'
            - reasons: List of validation messages
        """
        reasons = []
        status = 'YELLOW'  # Default to YELLOW
        
        # ===== LAYER 1: INPUT VALIDATION =====
        
        # Check ticker format
        ticker = signal.get('ticker', '').strip().upper()
        if not ticker:
            return (False, 'RED', ['Missing ticker'])
        
        if not re.match(r'^[A-Z]{1,6}$', ticker):
            return (False, 'RED', [f'Invalid ticker format: {ticker}'])
        
        # Blacklist check
        if ticker in self.blacklist:
            return (False, 'RED', [f'Ticker is common word (blacklist): {ticker}'])
        
        # Source validation
        source = signal.get('source', '')
        if source not in self.approved_sources:
            reasons.append(f'⚠️  Unapproved source: {source}')
            # Don't reject, just warn
        
        # Timestamp validity
        try:
            timestamp = signal.get('date_found') or signal.get('timestamp') or signal.get('message_timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    signal_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    signal_time = timestamp
                
                # Not in future
                if signal_time > datetime.now():
                    return (False, 'RED', ['Timestamp in future (invalid)'])
                
                # Not too old (>90 days)
                age_days = (datetime.now() - signal_time).days
                if age_days > 90:
                    return (False, 'RED', [f'Signal too old: {age_days} days'])
            
        except Exception as e:
            reasons.append(f'⚠️  Timestamp parsing error: {e}')
        
        # ===== LAYER 2: SIGNAL QUALITY CHECKS =====
        
        # Conviction threshold
        conviction = signal.get('conviction_score', 0)
        if conviction < self.thresholds['min_conviction_yellow']:
            return (False, 'RED', [f'Conviction too low: {conviction} (min {self.thresholds["min_conviction_yellow"]})'])
        
        if conviction >= self.thresholds['min_conviction_green']:
            status = 'GREEN'
            reasons.append(f'✅ High conviction: {conviction}/10')
        else:
            reasons.append(f'ℹ️  Moderate conviction: {conviction}/10 (YELLOW)')
        
        # Freshness check
        if timestamp:
            age_hours = (datetime.now() - signal_time).total_seconds() / 3600
            
            # Determine freshness threshold by type
            if 'DumbMoney' in source or 'social' in source.lower():
                max_age = self.thresholds['max_age_hours_social']
            elif 'Chart' in source or 'forex' in source.lower():
                max_age = self.thresholds['max_age_hours_forex']
            else:
                max_age = self.thresholds['max_age_hours_crypto']
            
            if age_hours > max_age:
                return (False, 'RED', [f'Signal too stale: {age_hours:.1f}h old (max {max_age}h)'])
            
            if age_hours < 6:
                reasons.append(f'✅ Very fresh: {age_hours:.1f}h old')
            else:
                reasons.append(f'ℹ️  Moderate freshness: {age_hours:.1f}h old')
        
        # Author verification (if Dan/Riz mentioned)
        dan_endorsed = signal.get('dan_endorsed', False)
        if dan_endorsed:
            # Verify it's actually Dan (check author_id if available)
            author_id = signal.get('author_id')
            if author_id:
                # TODO: Replace with actual Dan's Discord ID
                DAN_USER_ID = "123456789012345678"  # Placeholder
                
                if author_id != DAN_USER_ID:
                    reasons.append('⚠️  Dan mentioned but not author (false endorsement)')
                    signal['dan_endorsed'] = False
                else:
                    status = 'GREEN'  # Dan's endorsement = instant GREEN
                    reasons.append('✅ Verified Dan endorsement')
        
        # Duplicate detection
        if self._is_duplicate(signal):
            return (False, 'RED', ['Duplicate signal (already in database)'])
        
        # Multi-source validation
        sources = signal.get('sources', [signal.get('source')])
        if len(sources) >= 2:
            status = 'GREEN'  # Multi-source validation = GREEN
            reasons.append(f'✅ Multi-source validated: {", ".join(sources)}')
        
        # ===== LAYER 3: EXTERNAL VALIDATION (DELEGATED) =====
        # This layer is handled by signal_validator.py (Dex, Google Trends)
        # We just check if external validation was already done
        
        if signal.get('validation_passed'):
            reasons.append('✅ Passed external validation')
        
        validation_reasons = signal.get('validation_reasons', '')
        if validation_reasons:
            reasons.append(f'External: {validation_reasons}')
        
        # Final decision
        return (True, status, reasons)
    
    def _is_duplicate(self, signal: Dict[str, Any]) -> bool:
        """
        Check if signal is duplicate of existing entry
        
        Args:
            signal: New signal to check
        
        Returns:
            True if duplicate found
        """
        ticker = signal.get('ticker', '').upper()
        date_found = signal.get('date_found', datetime.now().strftime('%Y-%m-%d'))
        
        for existing in self.existing_signals:
            # Exact duplicate (same ticker, same day)
            if existing.get('Ticker', '').upper() == ticker:
                if existing.get('Date_Found') == date_found:
                    return True
        
        # Check equivalent tickers (BTC vs WBTC)
        if self._are_equivalent_tickers(ticker, [s.get('Ticker', '') for s in self.existing_signals]):
            return True
        
        return False
    
    def _are_equivalent_tickers(self, ticker: str, existing_tickers: List[str]) -> bool:
        """Check if ticker is wrapped/equivalent version of existing"""
        equivalents = {
            'BTC': ['WBTC', 'BTCB', 'RENBTC'],
            'ETH': ['WETH', 'BETH'],
            'USD': ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD']
        }
        
        for base, variants in equivalents.items():
            if ticker == base:
                # Check if any variant exists
                if any(v in existing_tickers for v in variants):
                    return True
            elif ticker in variants:
                # Check if base exists
                if base in existing_tickers or any(v in existing_tickers for v in variants if v != ticker):
                    return True
        
        return False
    
    def batch_validate(self, signals: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        Validate multiple signals, return grouped by status
        
        Args:
            signals: List of signal dictionaries
        
        Returns:
            Dict with keys: GREEN, YELLOW, RED (lists of signals)
        """
        results = {
            'GREEN': [],
            'YELLOW': [],
            'RED': []
        }
        
        for signal in signals:
            is_valid, status, reasons = self.validate_signal(signal)
            
            # Add validation metadata
            signal['validation_status'] = status
            signal['validation_reasons'] = '; '.join(reasons)
            signal['validation_timestamp'] = datetime.now().isoformat()
            
            # Group by status
            results[status].append(signal)
        
        return results
    
    def generate_report(self, results: Dict[str, List[Dict]]) -> str:
        """Generate human-readable quality report"""
        total = sum(len(signals) for signals in results.values())
        
        report = f"""
╔═══════════════════════════════════════════════════════════╗
║           Data Quality Validation Report                  ║
╚═══════════════════════════════════════════════════════════╝

Total Signals Processed: {total}

├─ 🔴 RED (Rejected): {len(results['RED'])} ({len(results['RED'])/total*100:.0f}%)
│  Common reasons:
"""
        
        # Count rejection reasons
        red_reasons = {}
        for signal in results['RED']:
            for reason in signal['validation_reasons'].split('; '):
                red_reasons[reason] = red_reasons.get(reason, 0) + 1
        
        for reason, count in sorted(red_reasons.items(), key=lambda x: -x[1])[:5]:
            report += f"│  - {reason}: {count}\n"
        
        report += f"""│
├─ 🟡 YELLOW (Monitoring): {len(results['YELLOW'])} ({len(results['YELLOW'])/total*100:.0f}%)
│
└─ 🟢 GREEN (Deploy Ready): {len(results['GREEN'])} ({len(results['GREEN'])/total*100:.0f}%)

Quality Score: {(len(results['YELLOW']) + len(results['GREEN'])) / total * 100:.0f}/100

"""
        
        # Show GREEN signals
        if results['GREEN']:
            report += "🟢 GREEN Signals (Ready to Deploy):\n"
            for signal in results['GREEN'][:10]:
                report += f"  • {signal['ticker']} ({signal['source']}) - {signal['conviction_score']}/10\n"
                report += f"    {signal['validation_reasons']}\n"
        
        return report


# Standalone execution
if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║           Data Quality Checker v1.0                       ║
║        3-Layer Signal Validation System                   ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Initialize checker
    checker = DataQualityChecker()
    
    # Test signals (sample data)
    test_signals = [
        {
            'ticker': 'SOL',
            'source': 'Yieldschool-YieldHub',
            'conviction_score': 9,
            'date_found': datetime.now().isoformat(),
            'dan_endorsed': True
        },
        {
            'ticker': 'THE',  # Should be rejected (blacklist)
            'source': 'DumbMoney',
            'conviction_score': 7,
            'date_found': datetime.now().isoformat()
        },
        {
            'ticker': 'ASTS',
            'source': 'DumbMoney',
            'conviction_score': 6,
            'date_found': (datetime.now() - timedelta(hours=12)).isoformat(),
            'total_reactions': 34
        },
        {
            'ticker': 'SCAM',
            'source': 'RandomDiscord',
            'conviction_score': 3,
            'date_found': (datetime.now() - timedelta(days=10)).isoformat()
        }
    ]
    
    # Validate
    results = checker.batch_validate(test_signals)
    
    # Generate report
    report = checker.generate_report(results)
    print(report)
    
    # Save results
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("💾 Results saved to validation_results.json")
