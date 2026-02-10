#!/usr/bin/env python3
"""
TradingView Webhook Server
Receives alerts from TradingView and routes to Telegram
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
from pathlib import Path
import sys

app = Flask(__name__)

# Activity logging
sys.path.append('/Users/agentjoselo/.openclaw/workspace/command-center')
from activity_logger import log_trading, log_automation

ALERTS_LOG = Path(__file__).parent.parent / "tradingview-alerts.log"
TELEGRAM_QUEUE = Path(__file__).parent.parent / "telegram-queue.txt"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming TradingView alerts"""
    
    try:
        # Get alert data (can be JSON or plain text)
        if request.is_json:
            data = request.json
            alert_message = data.get('message', str(data))
        else:
            alert_message = request.data.decode('utf-8')
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")
        
        # Log the alert
        with open(ALERTS_LOG, 'a') as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"{alert_message}\n")
            f.write("-" * 60 + "\n")
        
        # Queue for Telegram
        telegram_msg = f"🚨 **TradingView Alert**\n\n{alert_message}\n\n_{timestamp}_"
        with open(TELEGRAM_QUEUE, 'w') as f:
            f.write(telegram_msg)
        
        log_automation("TradingView alert received", {
            "message": alert_message[:100],
            "timestamp": timestamp
        })
        
        print(f"✅ Alert received at {timestamp}")
        print(f"   Message: {alert_message}")
        print(f"   Queued for Telegram: {TELEGRAM_QUEUE}")
        
        return jsonify({
            "status": "success",
            "message": "Alert received and queued",
            "timestamp": timestamp
        }), 200
    
    except Exception as e:
        print(f"❌ Error processing alert: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "TradingView Webhook Server",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """View recent alerts"""
    try:
        if ALERTS_LOG.exists():
            with open(ALERTS_LOG, 'r') as f:
                recent = f.read().split('\n')[-50:]  # Last 50 lines
                return jsonify({
                    "recent_alerts": '\n'.join(recent)
                }), 200
        else:
            return jsonify({"recent_alerts": "No alerts yet"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 TradingView Webhook Server starting...")
    print("   Listening on: http://0.0.0.0:5555/webhook")
    print("   Health check: http://0.0.0.0:5555/health")
    print("   View alerts:  http://0.0.0.0:5555/alerts")
    print("\n📝 TradingView Setup:")
    print("   1. Create alert on TradingView")
    print("   2. Set webhook URL: http://YOUR_IP:5555/webhook")
    print("   3. Message format: {{ticker}} {{close}} {{interval}}")
    print("\n✅ Ready to receive alerts!")
    
    # Run on all interfaces, port 5555
    app.run(host='0.0.0.0', port=5555, debug=False)
