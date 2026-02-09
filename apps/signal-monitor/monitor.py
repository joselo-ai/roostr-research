#!/usr/bin/env python3
"""
Signal Monitor - Real-time monitoring for trading signals
Sends alerts via Telegram when GREEN signals appear or positions hit targets
"""

import time
import csv
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

class SignalMonitor:
    """Monitor signals and send real-time alerts"""
    
    def __init__(self):
        self.signals_csv = Path('../../trading/signals-database.csv')
        self.state_file = Path('monitor_state.json')
        
        # Telegram bot config (from MEMORY.md)
        self.telegram_bot_token = self._load_telegram_token()
        self.telegram_user_id = "1425973061"  # G's user ID
        
        # Load previous state
        self.seen_signals = self._load_state()
    
    def _load_telegram_token(self) -> str:
        """Load Telegram bot token"""
        # In production, load from secure config
        # For now, return placeholder
        return "YOUR_BOT_TOKEN"  # Replace with actual token
    
    def _load_state(self) -> Set[str]:
        """Load previously seen signals"""
        
        if not self.state_file.exists():
            return set()
        
        with open(self.state_file, 'r') as f:
            state = json.load(f)
            return set(state.get('seen_signals', []))
    
    def _save_state(self):
        """Save state to disk"""
        
        state = {
            'seen_signals': list(self.seen_signals),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_signals(self) -> List[Dict]:
        """Load signals from CSV"""
        
        if not self.signals_csv.exists():
            return []
        
        signals = []
        with open(self.signals_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Ticker'):
                    signals.append(row)
        
        return signals
    
    def send_telegram(self, message: str):
        """Send Telegram alert"""
        
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        
        payload = {
            'chat_id': self.telegram_user_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✅ Alert sent: {message[:50]}...")
            else:
                print(f"❌ Failed to send alert: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Telegram error: {e}")
    
    def check_new_green_signals(self, signals: List[Dict]) -> List[Dict]:
        """Check for new GREEN signals"""
        
        new_green = []
        
        for signal in signals:
            ticker = signal.get('Ticker')
            status = signal.get('Status', 'YELLOW')
            signal_id = f"{ticker}_{status}"
            
            if status == 'GREEN' and signal_id not in self.seen_signals:
                new_green.append(signal)
                self.seen_signals.add(signal_id)
        
        return new_green
    
    def check_position_alerts(self, signals: List[Dict]) -> List[Dict]:
        """Check for position alerts (target hit, stop triggered)"""
        
        alerts = []
        
        for signal in signals:
            if signal.get('Deployed') != 'YES':
                continue
            
            ticker = signal.get('Ticker')
            current_price = float(signal.get('Current_Price') or 0)
            entry_price = float(signal.get('Price_Entry') or 0)
            stop_loss = float(signal.get('Stop_Loss') or 0)
            target_1 = float(signal.get('Target_1') or 0)
            
            if not current_price or not entry_price:
                continue
            
            # Check if stop triggered
            if stop_loss and current_price <= stop_loss:
                alert_id = f"{ticker}_stop_triggered"
                if alert_id not in self.seen_signals:
                    alerts.append({
                        'type': 'STOP_TRIGGERED',
                        'ticker': ticker,
                        'price': current_price,
                        'stop': stop_loss
                    })
                    self.seen_signals.add(alert_id)
            
            # Check if target 1 hit
            if target_1 and current_price >= target_1:
                alert_id = f"{ticker}_target1_hit"
                if alert_id not in self.seen_signals:
                    alerts.append({
                        'type': 'TARGET_HIT',
                        'ticker': ticker,
                        'price': current_price,
                        'target': target_1,
                        'target_level': 1
                    })
                    self.seen_signals.add(alert_id)
        
        return alerts
    
    def format_green_signal_alert(self, signal: Dict) -> str:
        """Format GREEN signal alert message"""
        
        ticker = signal.get('Ticker', 'UNKNOWN')
        source = signal.get('Source', 'Unknown')
        conviction = signal.get('Conviction_Score', 'N/A')
        notes = signal.get('Notes', '')[:100]
        
        message = f"""🟢 *NEW GREEN SIGNAL*

📊 *{ticker}* from {source}
⭐ Conviction: {conviction}/10

💡 {notes}

🎯 Ready to deploy!
"""
        
        return message
    
    def format_position_alert(self, alert: Dict) -> str:
        """Format position alert message"""
        
        if alert['type'] == 'STOP_TRIGGERED':
            return f"""🛑 *STOP LOSS TRIGGERED*

📊 *{alert['ticker']}*
💰 Current: ${alert['price']:.2f}
🚨 Stop: ${alert['stop']:.2f}

⚠️ Position stopped out
"""
        
        elif alert['type'] == 'TARGET_HIT':
            return f"""🎯 *TARGET HIT*

📊 *{alert['ticker']}*
💰 Current: ${alert['price']:.2f}
🎯 Target {alert['target_level']}: ${alert['target']:.2f}

✅ Take profits or trail stop!
"""
        
        return ""
    
    def run_check(self):
        """Run one monitoring cycle"""
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking signals...")
        
        # Load signals
        signals = self.load_signals()
        
        if not signals:
            print("  No signals found")
            return
        
        # Check for new GREEN signals
        new_green = self.check_new_green_signals(signals)
        
        for signal in new_green:
            message = self.format_green_signal_alert(signal)
            print(f"  🟢 New GREEN: {signal.get('Ticker')}")
            self.send_telegram(message)
        
        # Check for position alerts
        position_alerts = self.check_position_alerts(signals)
        
        for alert in position_alerts:
            message = self.format_position_alert(alert)
            print(f"  ⚠️  Alert: {alert['type']} on {alert['ticker']}")
            self.send_telegram(message)
        
        # Save state
        self._save_state()
        
        if not new_green and not position_alerts:
            print("  ✓ No new alerts")
    
    def run_continuous(self, interval: int = 60):
        """Run continuous monitoring"""
        
        print(f"\n{'='*60}")
        print(f"🐓 roostr Signal Monitor")
        print(f"{'='*60}")
        print(f"\n📊 Monitoring: {self.signals_csv}")
        print(f"⏱️  Check interval: {interval}s")
        print(f"📱 Alerts via Telegram to: {self.telegram_user_id}")
        print(f"\n🛑 Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_check()
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n✅ Monitor stopped")


# CLI

def main():
    import sys
    
    monitor = SignalMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'once':
        # Run once
        monitor.run_check()
    else:
        # Continuous monitoring
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else 60
        monitor.run_continuous(interval)


if __name__ == "__main__":
    main()
