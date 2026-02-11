#!/bin/bash
# Setup cron job for Social Arbitrage Agent daily scans

echo "🐓 Setting up automated Social Arbitrage Agent scans"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "run_social_scan.sh"; then
    echo "✅ Cron job already exists:"
    crontab -l | grep "run_social_scan.sh"
    echo ""
    echo "To remove and re-add, run: crontab -e"
else
    echo "📝 Current crontab:"
    crontab -l 2>/dev/null || echo "(empty)"
    echo ""
    
    # Create temp file with existing crontab + new job
    crontab -l 2>/dev/null > /tmp/mycron || true
    
    # Add Social Arb scan (9 AM daily)
    echo "" >> /tmp/mycron
    echo "# Social Arbitrage Agent - Daily scan at 9 AM EST" >> /tmp/mycron
    echo "0 9 * * * /Users/agentjoselo/.openclaw/workspace/trading/agents/run_social_scan.sh >> /Users/agentjoselo/.openclaw/workspace/trading/logs/social_arb.log 2>&1" >> /tmp/mycron
    
    # Install new crontab
    crontab /tmp/mycron
    rm /tmp/mycron
    
    echo "✅ Cron job added:"
    crontab -l | grep "run_social_scan.sh"
    echo ""
    echo "📅 Schedule: Every day at 9:00 AM EST"
    echo "📁 Logs: trading/logs/social_arb.log"
fi

echo ""
echo "🧪 Test run now? (manual)"
echo "   cd /Users/agentjoselo/.openclaw/workspace/trading"
echo "   ./agents/run_social_scan.sh"
