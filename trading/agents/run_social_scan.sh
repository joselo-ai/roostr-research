#!/bin/bash
# Daily Social Arbitrage Agent Scan
# Run this via cron: 0 9 * * * (every day at 9 AM EST)

WORKSPACE="/Users/agentjoselo/.openclaw/workspace/trading"
cd "$WORKSPACE"

echo "🐓 Starting Social Arbitrage Agent daily scan..."
echo "Time: $(date)"

# Activate venv and run agent
source venv/bin/activate
python agents/social_arbitrage_agent.py \
    --min-engagement 20 \
    --max-market-cap 5000000000 \
    --min-conviction 5.0

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Social Arbitrage scan complete"
else
    echo "❌ Social Arbitrage scan failed"
    exit 1
fi

# Update dashboard (if new signals found)
echo "📊 Updating dashboard..."
python apps/update_dashboard.py 2>/dev/null || echo "⚠️  Dashboard update skipped (script not found)"

echo "✅ Daily scan complete"
