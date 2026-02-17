#!/usr/bin/env python3
"""
🐓 Autonomous Trade Executor v1.0
Executes high-conviction signals with strict safeguards.
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass

# Paths
BASE_DIR = Path(__file__).parent.parent
SIGNALS_DB = BASE_DIR / "signals-database.csv"
POSITIONS_FILE = BASE_DIR / "positions.json"
EXECUTION_LOG = BASE_DIR / "logs" / "execution.jsonl"
CONFIG_FILE = BASE_DIR / ".alpaca.env"

# Safeguards (Phase 1 - Conservative)
SAFEGUARDS = {
    "min_conviction": 8.0,           # Only execute ≥8/10 signals
    "max_position_size": 10000,      # $10k max per position (1% of $1M)
    "max_daily_trades": 3,           # Max 3 new positions per day
    "max_open_positions": 10,        # Max 10 concurrent positions
    "daily_loss_limit": 0.02,        # Pause if down >2% intraday
    "stop_loss_pct": 0.15,           # 15% stop-loss on all trades
    "require_catalyst": False,       # Disabled (no catalyst field in CSV yet)
}

class AutonomousExecutor:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.load_config()
        if not dry_run:
            self.client = TradingClient(
                api_key=self.api_key,
                secret_key=self.secret_key,
                paper=True  # Always paper for Phase 1
            )
        self.execution_log = []
        
    def load_config(self):
        """Load Alpaca API keys"""
        if not CONFIG_FILE.exists():
            raise FileNotFoundError(f"Config not found: {CONFIG_FILE}")
        
        config = {}
        with open(CONFIG_FILE) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    config[key] = val
        
        self.api_key = config.get('ALPACA_API_KEY', '').strip()
        self.secret_key = config.get('ALPACA_SECRET_KEY', '').strip()
        
        if self.api_key == 'your_key_here' or not self.api_key:
            raise ValueError("Alpaca API keys not configured in .alpaca.env")
    
    def get_account_status(self):
        """Check account status and buying power"""
        if self.dry_run:
            return {"buying_power": 1000000, "equity": 1000000}
        
        account = self.client.get_account()
        return {
            "buying_power": float(account.buying_power),
            "equity": float(account.equity),
            "cash": float(account.cash),
            "portfolio_value": float(account.portfolio_value),
        }
    
    def get_open_positions(self):
        """Get current open positions"""
        if self.dry_run:
            return []
        
        positions = self.client.get_all_positions()
        return [{
            "symbol": p.symbol,
            "qty": float(p.qty),
            "avg_entry": float(p.avg_entry_price),
            "current_price": float(p.current_price),
            "market_value": float(p.market_value),
            "unrealized_pl": float(p.unrealized_pl),
            "unrealized_plpc": float(p.unrealized_plpc),
        } for p in positions]
    
    def check_safeguards(self, signal):
        """Validate signal against all safeguards"""
        violations = []
        
        # Conviction threshold
        conviction = float(signal.get('Conviction_Score', 0))
        if conviction < SAFEGUARDS['min_conviction']:
            violations.append(f"Conviction {conviction} < {SAFEGUARDS['min_conviction']}")
        
        # Catalyst requirement
        if SAFEGUARDS['require_catalyst']:
            catalyst = float(signal.get('catalyst_score', 0))
            if catalyst < 5.0:
                violations.append(f"Catalyst {catalyst} < 5.0")
        
        # Max open positions
        positions = self.get_open_positions()
        if len(positions) >= SAFEGUARDS['max_open_positions']:
            violations.append(f"Max positions reached ({len(positions)})")
        
        # Daily trade limit
        today_trades = self.count_today_trades()
        if today_trades >= SAFEGUARDS['max_daily_trades']:
            violations.append(f"Max daily trades reached ({today_trades})")
        
        # Daily loss limit
        account = self.get_account_status()
        daily_pl_pct = self.calculate_daily_pl_pct()
        if daily_pl_pct < -SAFEGUARDS['daily_loss_limit']:
            violations.append(f"Daily loss limit hit ({daily_pl_pct:.2%})")
        
        return violations
    
    def count_today_trades(self):
        """Count trades executed today"""
        if not EXECUTION_LOG.exists():
            return 0
        
        today = datetime.now().date().isoformat()
        count = 0
        with open(EXECUTION_LOG) as f:
            for line in f:
                record = json.loads(line)
                if record.get('date', '').startswith(today):
                    count += 1
        return count
    
    def calculate_daily_pl_pct(self):
        """Calculate today's P&L %"""
        # Simplified - just check current unrealized
        positions = self.get_open_positions()
        if not positions:
            return 0.0
        
        total_pl = sum(p['unrealized_plpc'] for p in positions)
        return total_pl / len(positions) if positions else 0.0
    
    def calculate_position_size(self, signal, account):
        """Calculate position size based on conviction"""
        conviction = float(signal.get('Conviction_Score', 0))
        
        # Position size scales with conviction (8.0 = $5k, 10.0 = $10k)
        base_size = 5000
        max_size = SAFEGUARDS['max_position_size']
        
        # Linear scaling: 8.0→$5k, 9.0→$7.5k, 10.0→$10k
        position_size = base_size + (conviction - 8.0) * (max_size - base_size) / 2.0
        position_size = min(position_size, max_size)
        position_size = min(position_size, account['buying_power'] * 0.1)  # Max 10% of buying power
        
        return round(position_size, 2)
    
    def execute_signal(self, signal):
        """Execute a single signal with safeguards"""
        symbol = signal['Ticker']
        
        # Check safeguards
        violations = self.check_safeguards(signal)
        if violations:
            self.log_execution(signal, "BLOCKED", violations=violations)
            return {"status": "blocked", "violations": violations}
        
        # Get account status
        account = self.get_account_status()
        
        # Calculate position size
        position_size = self.calculate_position_size(signal, account)
        
        if self.dry_run:
            self.log_execution(signal, "DRY_RUN", position_size=position_size)
            return {"status": "dry_run", "size": position_size}
        
        # Get current price
        try:
            quote = self.client.get_latest_quote(symbol)
            current_price = float(quote.ask_price)
        except Exception as e:
            self.log_execution(signal, "ERROR", error=str(e))
            return {"status": "error", "error": str(e)}
        
        # Calculate quantity
        qty = int(position_size / current_price)
        if qty == 0:
            self.log_execution(signal, "ERROR", error="Position size too small")
            return {"status": "error", "error": "Position size too small"}
        
        # Calculate stop-loss price
        stop_loss_price = round(current_price * (1 - SAFEGUARDS['stop_loss_pct']), 2)
        
        # Place bracket order (entry + stop-loss)
        try:
            order_request = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY,
                order_class=OrderClass.BRACKET,
                stop_loss=StopLossRequest(stop_price=stop_loss_price)
            )
            
            order = self.client.submit_order(order_request)
            
            self.log_execution(signal, "EXECUTED", 
                             order_id=order.id,
                             qty=qty,
                             entry_price=current_price,
                             stop_loss=stop_loss_price,
                             position_size=position_size)
            
            return {
                "status": "executed",
                "order_id": order.id,
                "symbol": symbol,
                "qty": qty,
                "entry": current_price,
                "stop": stop_loss_price,
                "size": position_size
            }
            
        except Exception as e:
            self.log_execution(signal, "ERROR", error=str(e))
            return {"status": "error", "error": str(e)}
    
    def log_execution(self, signal, status, **kwargs):
        """Log execution attempt"""
        EXECUTION_LOG.parent.mkdir(exist_ok=True)
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "ticker": signal.get('Ticker'),
            "conviction": signal.get('Conviction_Score'),
            "status": status,
            **kwargs
        }
        
        with open(EXECUTION_LOG, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        self.execution_log.append(record)
    
    def scan_and_execute(self):
        """Scan signals DB and execute eligible trades"""
        if not SIGNALS_DB.exists():
            print("❌ Signals database not found")
            return
        
        # Load signals
        signals = []
        with open(SIGNALS_DB) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Status') == 'GREEN':  # Only execute GREEN signals
                    signals.append(row)
        
        if not signals:
            print("✅ No GREEN signals to execute")
            return
        
        # Sort by conviction (highest first)
        signals.sort(key=lambda x: float(x.get('Conviction_Score', 0)), reverse=True)
        
        print(f"🎯 Found {len(signals)} GREEN signals")
        print(f"📊 Safeguards: Conv≥{SAFEGUARDS['min_conviction']}, Max{SAFEGUARDS['max_daily_trades']}/day, ${SAFEGUARDS['max_position_size']}/position\n")
        
        executed = 0
        blocked = 0
        
        for signal in signals:
            result = self.execute_signal(signal)
            
            if result['status'] == 'executed':
                executed += 1
                print(f"✅ EXECUTED: {signal['Ticker']} | Conv:{signal['Conviction_Score']} | ${result['size']} | Stop:{result['stop']}")
            elif result['status'] == 'blocked':
                blocked += 1
                print(f"🚫 BLOCKED: {signal['Ticker']} | {', '.join(result['violations'])}")
            elif result['status'] == 'dry_run':
                print(f"🔍 DRY_RUN: {signal['Ticker']} | Conv:{signal['Conviction_Score']} | Would trade ${result['size']}")
        
        print(f"\n📊 Summary: {executed} executed, {blocked} blocked")
        return {"executed": executed, "blocked": blocked}

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐓 Autonomous Trade Executor")
    parser.add_argument('--dry-run', action='store_true', help='Simulation mode (no real trades)')
    parser.add_argument('--live', action='store_true', help='Execute real trades')
    args = parser.parse_args()
    
    if not args.dry_run and not args.live:
        print("❌ Must specify --dry-run or --live")
        print("   Start with: python3 autonomous_executor.py --dry-run")
        return
    
    mode = "DRY RUN" if args.dry_run else "LIVE EXECUTION"
    print(f"🐓 Autonomous Executor - {mode}")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    executor = AutonomousExecutor(dry_run=args.dry_run)
    executor.scan_and_execute()

if __name__ == "__main__":
    main()
