#!/usr/bin/env python3
"""
roostr Web Dashboard Server - Serve trading dashboard on local network
Access from phone, tablet, or any device on the network
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import csv
from datetime import datetime
from pathlib import Path
import socket

class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom handler for dashboard API endpoints"""
    
    def do_GET(self):
        """Handle GET requests"""
        
        # API endpoints
        if self.path == '/api/signals':
            self.serve_signals_json()
        elif self.path == '/api/positions':
            self.serve_positions_json()
        elif self.path == '/api/performance':
            self.serve_performance_json()
        elif self.path == '/api/refresh':
            self.refresh_data()
        elif self.path == '/' or self.path == '/index.html':
            self.serve_dashboard()
        else:
            # Serve static files
            super().do_GET()
    
    def serve_signals_json(self):
        """Serve signals as JSON"""
        
        signals = self.load_signals()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(signals, indent=2).encode())
    
    def serve_positions_json(self):
        """Serve open positions as JSON"""
        
        signals = self.load_signals()
        positions = [s for s in signals if s.get('Deployed') == 'YES']
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(positions, indent=2).encode())
    
    def serve_performance_json(self):
        """Serve performance metrics as JSON"""
        
        signals = self.load_signals()
        metrics = self.calculate_metrics(signals)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(metrics, indent=2).encode())
    
    def refresh_data(self):
        """Trigger data refresh"""
        
        # Regenerate dashboard
        import subprocess
        subprocess.run(['python3', '../../trading/update_dashboard.py'])
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps({'status': 'refreshed'}).encode())
    
    def serve_dashboard(self):
        """Serve main dashboard HTML"""
        
        dashboard_path = Path('../../trading/dashboard.html')
        
        if dashboard_path.exists():
            with open(dashboard_path, 'r') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            self.wfile.write(content.encode())
        else:
            self.send_error(404, "Dashboard not found")
    
    def load_signals(self):
        """Load signals from CSV"""
        
        signals = []
        csv_path = Path('../../trading/signals-database.csv')
        
        if not csv_path.exists():
            return signals
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Ticker'):
                    signals.append(row)
        
        return signals
    
    def calculate_metrics(self, signals):
        """Calculate portfolio metrics"""
        
        positions = [s for s in signals if s.get('Deployed') == 'YES']
        
        total_deployed = sum(
            float(s.get('Position_Size', 0) or 0) for s in positions
        )
        
        total_pnl = sum(
            float(s.get('PnL_Dollars', 0) or 0) for s in positions
        )
        
        return {
            'total_capital': 100000,
            'total_deployed': total_deployed,
            'cash_reserve': 100000 - total_deployed,
            'total_pnl': total_pnl,
            'pnl_percent': (total_pnl / 100000 * 100) if total_deployed > 0 else 0,
            'open_positions': len(positions),
            'last_updated': datetime.now().isoformat()
        }


def get_local_ip():
    """Get local IP address for network access"""
    
    try:
        # Connect to external server (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def create_mobile_dashboard():
    """Create mobile-optimized dashboard HTML"""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>roostr Mobile</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 10px;
        }
        .header {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            text-align: center;
        }
        .header h1 { font-size: 1.5em; margin-bottom: 5px; }
        .header .subtitle { color: #888; font-size: 0.8em; }
        .card {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #333;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { color: #888; font-size: 0.9em; }
        .metric-value { font-weight: 600; }
        .positive { color: #4ade80; }
        .negative { color: #f87171; }
        .position {
            background: rgba(74, 222, 128, 0.1);
            border-left: 4px solid #4ade80;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
        }
        .position-header { font-weight: 600; margin-bottom: 5px; }
        .position-detail { font-size: 0.85em; color: #bbb; }
        .refresh-btn {
            background: #4ade80;
            color: #000;
            border: none;
            border-radius: 6px;
            padding: 12px;
            width: 100%;
            font-weight: 600;
            font-size: 1em;
            margin-top: 10px;
        }
        .loading { text-align: center; padding: 20px; color: #888; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐓 roostr</h1>
        <div class="subtitle" id="last-update">Loading...</div>
    </div>
    
    <div class="card">
        <h2 style="margin-bottom: 15px; font-size: 1.2em;">📊 Performance</h2>
        <div id="performance">
            <div class="loading">Loading performance data...</div>
        </div>
    </div>
    
    <div class="card">
        <h2 style="margin-bottom: 15px; font-size: 1.2em;">📈 Open Positions</h2>
        <div id="positions">
            <div class="loading">Loading positions...</div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="refreshData()">🔄 Refresh</button>
    
    <script>
        function loadData() {
            // Load performance
            fetch('/api/performance')
                .then(r => r.json())
                .then(data => {
                    const pnlClass = data.total_pnl >= 0 ? 'positive' : 'negative';
                    const pnlSign = data.total_pnl >= 0 ? '+' : '';
                    
                    document.getElementById('performance').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Deployed</span>
                            <span class="metric-value">$${data.total_deployed.toLocaleString()}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Cash</span>
                            <span class="metric-value">$${data.cash_reserve.toLocaleString()}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Net P&L</span>
                            <span class="metric-value ${pnlClass}">${pnlSign}$${Math.abs(data.total_pnl).toLocaleString()} (${pnlSign}${data.pnl_percent.toFixed(1)}%)</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Positions</span>
                            <span class="metric-value">${data.open_positions}</span>
                        </div>
                    `;
                    
                    document.getElementById('last-update').textContent = 
                        'Updated ' + new Date(data.last_updated).toLocaleTimeString();
                });
            
            // Load positions
            fetch('/api/positions')
                .then(r => r.json())
                .then(data => {
                    if (data.length === 0) {
                        document.getElementById('positions').innerHTML = 
                            '<div class="loading">No open positions yet</div>';
                        return;
                    }
                    
                    const html = data.map(pos => {
                        const pnl = parseFloat(pos.PnL_Dollars || 0);
                        const pnlClass = pnl >= 0 ? 'positive' : 'negative';
                        const pnlSign = pnl >= 0 ? '+' : '';
                        
                        return `
                            <div class="position">
                                <div class="position-header">${pos.Ticker} - ${pos.Source}</div>
                                <div class="position-detail">
                                    Entry: $${pos.Price_Entry || 'N/A'} | 
                                    Size: $${parseFloat(pos.Position_Size || 0).toLocaleString()}<br>
                                    P&L: <span class="${pnlClass}">${pnlSign}$${Math.abs(pnl).toFixed(2)}</span>
                                </div>
                            </div>
                        `;
                    }).join('');
                    
                    document.getElementById('positions').innerHTML = html;
                });
        }
        
        function refreshData() {
            fetch('/api/refresh')
                .then(() => {
                    setTimeout(loadData, 1000);
                });
        }
        
        // Load on page load
        loadData();
        
        // Auto-refresh every 30 seconds
        setInterval(loadData, 30000);
    </script>
</body>
</html>"""
    
    with open('mobile.html', 'w') as f:
        f.write(html)
    
    print("✅ Created mobile.html")


def start_server(port=8080):
    """Start dashboard web server"""
    
    # Create mobile dashboard
    create_mobile_dashboard()
    
    # Get local IP
    local_ip = get_local_ip()
    
    # Start server
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    
    print(f"\n{'='*60}")
    print(f"🐓 roostr Dashboard Server")
    print(f"{'='*60}")
    print(f"\n📱 Access from this device:")
    print(f"   http://localhost:{port}")
    print(f"\n📱 Access from other devices on network:")
    print(f"   http://{local_ip}:{port}")
    print(f"\n📊 API Endpoints:")
    print(f"   /api/signals      - All signals")
    print(f"   /api/positions    - Open positions")
    print(f"   /api/performance  - Performance metrics")
    print(f"   /api/refresh      - Refresh data")
    print(f"\n💡 Mobile optimized dashboard:")
    print(f"   http://{local_ip}:{port}/mobile.html")
    print(f"\n🛑 Press Ctrl+C to stop")
    print(f"{'='*60}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")
        server.shutdown()


if __name__ == "__main__":
    import sys
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    start_server(port)
