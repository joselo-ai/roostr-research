#!/usr/bin/env python3
"""
Automated Dashboard Updater - Regenerate dashboard.html from tracking data
Runs after every trade or daily update
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class DashboardUpdater:
    """Generate HTML dashboard from tracking data"""
    
    def __init__(self):
        self.signals_csv = 'signals-database.csv'
        self.paper_log = 'PAPER-TRADING-LOG.md'
        self.dashboard_html = 'dashboard.html'
        self.price_cache = '.price_cache.json'
        
    def get_last_price_update(self) -> str:
        """Get timestamp of last price update from cache"""
        try:
            if os.path.exists(self.price_cache):
                with open(self.price_cache, 'r') as f:
                    cache = json.load(f)
                    if 'timestamp' in cache:
                        ts = datetime.fromisoformat(cache['timestamp'])
                        # Calculate age
                        age_seconds = (datetime.now() - ts).total_seconds()
                        
                        if age_seconds < 60:
                            age_str = f"{int(age_seconds)}s ago"
                        elif age_seconds < 3600:
                            age_str = f"{int(age_seconds / 60)}m ago"
                        else:
                            age_str = f"{int(age_seconds / 3600)}h ago"
                        
                        # Mark as stale if > 10 minutes
                        status = "⚠️ STALE" if age_seconds > 600 else "✅ Fresh"
                        
                        return f"{ts.strftime('%H:%M:%S')} ({age_str}) {status}"
        except Exception:
            pass
        
        return "Never (automated updates not running)"
    
    def load_signals(self) -> List[Dict[str, Any]]:
        """Load signals from CSV database"""
        signals = []
        
        try:
            with open(self.signals_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Ticker'):  # Skip empty/header rows
                        signals.append(row)
        except FileNotFoundError:
            print(f"{self.signals_csv} not found, using empty dataset")
        
        return signals
    
    def calculate_portfolio_metrics(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate portfolio-level metrics"""
        deployed_positions = [s for s in signals if s.get('Deployed') == 'YES']
        
        total_deployed = sum(float(s.get('Position_Size', 0) or 0) for s in deployed_positions)
        total_pnl = sum(float(s.get('PnL_Dollars', 0) or 0) for s in deployed_positions)
        
        # Calculate by bucket
        buckets = {
            'Riz_EURUSD': {'deployed': 0, 'pnl': 0, 'count': 0, 'allocation': 40000},
            'Social_Arb': {'deployed': 0, 'pnl': 0, 'count': 0, 'allocation': 30000},
            'Crypto': {'deployed': 0, 'pnl': 0, 'count': 0, 'allocation': 20000},
            'Opportunistic': {'deployed': 0, 'pnl': 0, 'count': 0, 'allocation': 10000}
        }
        
        for pos in deployed_positions:
            source = pos.get('Source', '')
            size = float(pos.get('Position_Size', 0) or 0)
            pnl = float(pos.get('PnL_Dollars', 0) or 0)
            
            if 'Chart' in source:
                buckets['Riz_EURUSD']['deployed'] += size
                buckets['Riz_EURUSD']['pnl'] += pnl
                buckets['Riz_EURUSD']['count'] += 1
            elif 'DumbMoney' in source:
                buckets['Social_Arb']['deployed'] += size
                buckets['Social_Arb']['pnl'] += pnl
                buckets['Social_Arb']['count'] += 1
            elif 'Yieldschool' in source:
                buckets['Crypto']['deployed'] += size
                buckets['Crypto']['pnl'] += pnl
                buckets['Crypto']['count'] += 1
            else:
                buckets['Opportunistic']['deployed'] += size
                buckets['Opportunistic']['pnl'] += pnl
                buckets['Opportunistic']['count'] += 1
        
        return {
            'total_capital': 100000,
            'total_deployed': total_deployed,
            'cash_reserve': 100000 - total_deployed,
            'total_pnl': total_pnl,
            'pnl_percent': (total_pnl / 100000 * 100) if total_deployed > 0 else 0,
            'open_positions': len(deployed_positions),
            'buckets': buckets
        }
    
    def get_watchlist_signals(self, signals: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Group signals by status for watchlist"""
        watchlist = {
            'GREEN': [],
            'YELLOW': [],
            'RED': []
        }
        
        for signal in signals:
            status = signal.get('Status', 'YELLOW')
            if status in watchlist:
                watchlist[status].append(signal)
        
        return watchlist
    
    def generate_html(self, metrics: Dict[str, Any], watchlist: Dict[str, List]) -> str:
        """Generate complete HTML dashboard"""
        
        # Bucket HTML
        buckets_html = ""
        bucket_names = {
            'Riz_EURUSD': ('40% ($40,000) - Riz EURUSD', 'green', '8.5/10', '$120k+ annual'),
            'Social_Arb': ('30% ($30,000) - Social Arbitrage', 'green', '7.7/10', 'Camillo 77% annual'),
            'Crypto': ('20% ($20,000) - Crypto Fundamentals', 'yellow', 'Emerging', 'Dan $500→$500k'),
            'Opportunistic': ('10% ($10,000) - Opportunistic/Research', 'yellow', 'Variable', 'Testing new edges')
        }
        
        for bucket_key, bucket_data in metrics['buckets'].items():
            name, color, conviction, track = bucket_names[bucket_key]
            deployed_pct = (bucket_data['deployed'] / bucket_data['allocation'] * 100) if bucket_data['allocation'] > 0 else 0
            pnl_sign = '+' if bucket_data['pnl'] >= 0 else ''
            pnl_class = 'positive' if bucket_data['pnl'] > 0 else 'negative' if bucket_data['pnl'] < 0 else 'neutral'
            
            buckets_html += f'''
                <div class="signal {color}" style="margin: 10px;">
                    <div class="signal-header">{name}</div>
                    <div class="signal-meta">Conviction: {conviction} | Track Record: {track}</div>
                    <div class="signal-detail">
                        <strong>Deployed:</strong> ${bucket_data['deployed']:,.0f} / ${bucket_data['allocation']:,.0f} ({deployed_pct:.0f}%)<br>
                        <strong>P&L:</strong> <span class="{pnl_class}">${pnl_sign}{bucket_data['pnl']:,.0f} ({pnl_sign}{bucket_data['pnl']/bucket_data['allocation']*100 if bucket_data['allocation'] > 0 else 0:.1f}%)</span><br>
                        <strong>Open Positions:</strong> {bucket_data['count']}
                    </div>
                </div>
            '''
        
        # Watchlist HTML
        watchlist_html = ""
        
        # GREEN signals
        for signal in watchlist['GREEN'][:5]:  # Top 5
            watchlist_html += f'''
            <div class="signal green">
                <div class="signal-header">
                    <span class="badge green">GREEN</span>
                    {signal.get('Ticker', 'N/A')} - {signal.get('Source', 'Unknown')}
                </div>
                <div class="signal-meta">
                    Conviction: {signal.get('Conviction_Score', 'N/A')}/10 | Found: {signal.get('Date_Found', 'N/A')}
                </div>
                <div class="signal-detail">
                    <strong>Status:</strong> {"Deployed" if signal.get('Deployed') == 'YES' else "Ready to deploy"}<br>
                    {f"<strong>Entry:</strong> ${signal.get('Price_Entry', 'N/A')}<br>" if signal.get('Price_Entry') else ""}
                    <strong>Notes:</strong> {(signal.get('Notes') or 'No additional notes')[:150]}
                </div>
            </div>
            '''
        
        # YELLOW signals
        for signal in watchlist['YELLOW'][:3]:
            watchlist_html += f'''
            <div class="signal yellow">
                <div class="signal-header">
                    <span class="badge yellow">YELLOW</span>
                    {signal.get('Ticker', 'N/A')} - {signal.get('Source', 'Unknown')}
                </div>
                <div class="signal-meta">
                    Conviction: {signal.get('Conviction_Score', 'N/A')}/10 | Monitoring
                </div>
                <div class="signal-detail">
                    <strong>Notes:</strong> {(signal.get('Notes') or 'Awaiting validation')[:150]}
                </div>
            </div>
            '''
        
        # PnL class
        pnl_class = 'positive' if metrics['total_pnl'] > 0 else 'negative' if metrics['total_pnl'] < 0 else 'neutral'
        pnl_sign = '+' if metrics['total_pnl'] >= 0 else ''
        
        # Current date
        current_date = datetime.now().strftime('%b %d, %Y %H:%M EST')
        
        # Get last price update timestamp
        last_price_update = self.get_last_price_update()
        
        # Full HTML
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>roostr Trading Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{ margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 20px; }}
        h1 {{ color: #fff; font-size: 2.5em; margin-bottom: 10px; }}
        .rooster {{ font-size: 1.5em; }}
        .subtitle {{ color: #888; font-size: 0.9em; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 20px; }}
        .card h2 {{ color: #fff; margin-bottom: 15px; font-size: 1.3em; border-bottom: 1px solid #333; padding-bottom: 10px; }}
        .metric {{ display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background: #0f0f0f; border-radius: 4px; }}
        .metric-label {{ color: #888; }}
        .metric-value {{ color: #fff; font-weight: 600; }}
        .positive {{ color: #4ade80 !important; }}
        .negative {{ color: #f87171 !important; }}
        .neutral {{ color: #fbbf24 !important; }}
        .signal {{ padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 4px solid; }}
        .signal.green {{ background: rgba(74, 222, 128, 0.1); border-left-color: #4ade80; }}
        .signal.yellow {{ background: rgba(251, 191, 36, 0.1); border-left-color: #fbbf24; }}
        .signal.red {{ background: rgba(248, 113, 113, 0.1); border-left-color: #f87171; }}
        .signal-header {{ font-weight: 600; font-size: 1.1em; margin-bottom: 8px; }}
        .signal-meta {{ color: #888; font-size: 0.85em; margin-bottom: 8px; }}
        .signal-detail {{ color: #bbb; font-size: 0.9em; line-height: 1.5; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 0.8em; font-weight: 600; margin-right: 8px; }}
        .badge.green {{ background: #4ade80; color: #000; }}
        .badge.yellow {{ background: #fbbf24; color: #000; }}
        .badge.red {{ background: #f87171; color: #000; }}
        .full-width {{ grid-column: 1 / -1; }}
        .footer {{ margin-top: 40px; text-align: center; color: #666; font-size: 0.85em; padding-top: 20px; border-top: 1px solid #333; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><span class="rooster">🐓</span> roostr Trading Dashboard</h1>
            <p class="subtitle">Dashboard: {current_date} | Prices: {last_price_update} | Source: CoinGecko</p>
        </header>
        
        <!-- Allocation Overview -->
        <div class="card full-width">
            <h2>💰 Capital Allocation (Risk-Adjusted by Conviction)</h2>
            <div class="grid">
                {buckets_html}
            </div>
        </div>
        
        <!-- Performance Overview -->
        <div class="grid">
            <div class="card">
                <h2>📊 Portfolio Performance</h2>
                <div class="metric">
                    <span class="metric-label">Total Capital</span>
                    <span class="metric-value">${metrics['total_capital']:,.0f}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Deployed Capital</span>
                    <span class="metric-value">${metrics['total_deployed']:,.0f} ({metrics['total_deployed']/metrics['total_capital']*100:.0f}%)</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Cash Reserve</span>
                    <span class="metric-value">${metrics['cash_reserve']:,.0f} ({metrics['cash_reserve']/metrics['total_capital']*100:.0f}%)</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Net P&L</span>
                    <span class="metric-value {pnl_class}">{pnl_sign}${abs(metrics['total_pnl']):,.0f} ({pnl_sign}{metrics['pnl_percent']:.1f}%)</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Open Positions</span>
                    <span class="metric-value">{metrics['open_positions']}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status</span>
                    <span class="metric-value neutral">🟡 Phase 1 - Building Track Record</span>
                </div>
            </div>
        </div>
        
        <!-- Active Watchlist -->
        <div class="card full-width">
            <h2>🎯 Active Watchlist</h2>
            {watchlist_html if watchlist_html else '<p style="color: #666; padding: 20px; text-align: center;">No signals yet. First data collection tomorrow morning.</p>'}
        </div>
        
        <div class="footer">
            <p>roostr AI hedge fund · Paper trading + research validation phase</p>
            <p>Files: PAPER-TRADING-LOG.md | signals-database.csv | RESEARCH-CALLS-TRACKER.md</p>
            <p>Auto-updated after every trade by Joselo 🐓</p>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def update(self):
        """Main execution: load data and regenerate dashboard"""
        print("Updating dashboard...")
        
        # Load data
        signals = self.load_signals()
        print(f"Loaded {len(signals)} signals from database")
        
        # Calculate metrics
        metrics = self.calculate_portfolio_metrics(signals)
        print(f"Portfolio: ${metrics['total_deployed']:,.0f} deployed, "
              f"${metrics['total_pnl']:+,.0f} P&L ({metrics['pnl_percent']:+.1f}%)")
        
        # Get watchlist
        watchlist = self.get_watchlist_signals(signals)
        print(f"Watchlist: {len(watchlist['GREEN'])} GREEN, "
              f"{len(watchlist['YELLOW'])} YELLOW, {len(watchlist['RED'])} RED")
        
        # Generate HTML
        html = self.generate_html(metrics, watchlist)
        
        # Write to file
        with open(self.dashboard_html, 'w') as f:
            f.write(html)
        
        print(f"✅ Dashboard updated: {self.dashboard_html}")
        print(f"Open: file://{self.dashboard_html}")


# Run
if __name__ == "__main__":
    updater = DashboardUpdater()
    updater.update()
