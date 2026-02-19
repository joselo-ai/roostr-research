#!/bin/bash
# Setup Discord Signal Forwarder - Automated Cron Job
# Runs every 30 minutes to scan external Discord servers

WORKSPACE="/Users/agentjoselo/.openclaw/workspace/trading"
VENV_PYTHON="$WORKSPACE/venv/bin/python3"
SCRIPT="$WORKSPACE/apps/discord_signal_forwarder.py"
LOG_FILE="$WORKSPACE/logs/discord_forwarder.log"

echo "🐓 Setting up Discord Signal Forwarder automation..."

# Create logs directory
mkdir -p "$WORKSPACE/logs"

# Create cron job entry
CRON_ENTRY="*/30 * * * * cd $WORKSPACE && $VENV_PYTHON $SCRIPT >> $LOG_FILE 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "discord_signal_forwarder.py"; then
    echo "⚠️  Cron job already exists"
    echo "   Run 'crontab -l' to view"
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✅ Cron job added: Every 30 minutes"
fi

echo ""
echo "📋 Current crontab:"
crontab -l | grep discord_signal_forwarder.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "What happens now:"
echo "  • Bot scans Dumb Money / Yieldschool / Chart Fanatics every 30 min"
echo "  • High-conviction signals (≥7.0) → Posted to #trading-signals"
echo "  • 18-agent deliberation triggered automatically"
echo "  • Agent consensus → Posted to #18-agents-debate"
echo ""
echo "Logs: $LOG_FILE"
echo ""
echo "To test manually:"
echo "  cd $WORKSPACE && $VENV_PYTHON $SCRIPT"
echo ""
echo "To disable:"
echo "  crontab -e"
echo "  (Comment out or delete the discord_signal_forwarder.py line)"
