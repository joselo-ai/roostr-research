#!/bin/bash
# Stop roostr Apps

echo "🛑 Stopping roostr Apps..."
echo ""

# Stop dashboard server
if [ -f /tmp/roostr-dashboard.pid ]; then
    DASHBOARD_PID=$(cat /tmp/roostr-dashboard.pid)
    if ps -p $DASHBOARD_PID > /dev/null 2>&1; then
        kill $DASHBOARD_PID
        echo "  ✓ Stopped dashboard server (PID: $DASHBOARD_PID)"
    else
        echo "  ℹ Dashboard already stopped"
    fi
    rm /tmp/roostr-dashboard.pid
else
    echo "  ℹ No dashboard PID file found"
fi

# Stop signal monitor
if [ -f /tmp/roostr-monitor.pid ]; then
    MONITOR_PID=$(cat /tmp/roostr-monitor.pid)
    if ps -p $MONITOR_PID > /dev/null 2>&1; then
        kill $MONITOR_PID
        echo "  ✓ Stopped signal monitor (PID: $MONITOR_PID)"
    else
        echo "  ℹ Monitor already stopped"
    fi
    rm /tmp/roostr-monitor.pid
else
    echo "  ℹ No monitor PID file found"
fi

echo ""
echo "✅ All apps stopped"
