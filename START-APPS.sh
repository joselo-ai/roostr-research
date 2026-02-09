#!/bin/bash
# Start roostr Apps - Quick Launcher
# Run this tomorrow morning before 9 AM

set -e

WORKSPACE="/Users/agentjoselo/.openclaw/workspace"

echo "=================================================="
echo "🐓 Starting roostr Apps"
echo "=================================================="
echo ""

# Get local IP
LOCAL_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1 || echo "127.0.0.1")

# Start web dashboard server
echo "📊 Starting Web Dashboard Server..."
cd "$WORKSPACE/apps/web-dashboard"
python3 server.py > /tmp/roostr-dashboard.log 2>&1 &
DASHBOARD_PID=$!
echo "  ✓ Dashboard server started (PID: $DASHBOARD_PID)"
echo "  ✓ Desktop: http://localhost:8080"
echo "  ✓ Mobile: http://$LOCAL_IP:8080/mobile.html"
echo ""

# Wait for server to start
sleep 2

# Start signal monitor
echo "🔔 Starting Signal Monitor..."
cd "$WORKSPACE/apps/signal-monitor"
python3 monitor.py > /tmp/roostr-monitor.log 2>&1 &
MONITOR_PID=$!
echo "  ✓ Monitor started (PID: $MONITOR_PID)"
echo "  ✓ Watching for GREEN signals"
echo "  ✓ Alerts via Telegram"
echo ""

# Save PIDs for later shutdown
echo "$DASHBOARD_PID" > /tmp/roostr-dashboard.pid
echo "$MONITOR_PID" > /tmp/roostr-monitor.pid

echo "=================================================="
echo "✅ Apps Running"
echo "=================================================="
echo ""
echo "📱 MOBILE ACCESS:"
echo "   Open on your phone: http://$LOCAL_IP:8080/mobile.html"
echo ""
echo "📊 DESKTOP ACCESS:"
echo "   http://localhost:8080"
echo ""
echo "🔔 ALERTS:"
echo "   Telegram notifications when GREEN signals appear"
echo ""
echo "📝 LOGS:"
echo "   Dashboard: tail -f /tmp/roostr-dashboard.log"
echo "   Monitor: tail -f /tmp/roostr-monitor.log"
echo ""
echo "🛑 STOP APPS:"
echo "   ./STOP-APPS.sh"
echo ""
echo "=================================================="
echo "Apps are running. Check your phone! 🔥"
echo "=================================================="
