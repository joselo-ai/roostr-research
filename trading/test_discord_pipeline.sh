#!/bin/bash
# Test Discord Signal Pipeline - Verify everything works before enabling automation

WORKSPACE="/Users/agentjoselo/.openclaw/workspace/trading"
VENV_PYTHON="$WORKSPACE/venv/bin/python3"

echo "🐓 Testing Discord Signal Pipeline"
echo "="
echo ""

echo "1️⃣ Checking Discord bot connectivity..."
cd "$WORKSPACE/scrapers"
$VENV_PYTHON discover_channels.py 2>&1 | head -20
echo ""

echo "2️⃣ Testing Dumb Money scraper..."
echo "(This will fail if bot not in server yet - expected)"
$VENV_PYTHON dumbmoney_scraper.py --channels 1472686030204178534 --hours 168 --min-reactions 1 --output /tmp/test-dumbmoney.json 2>&1 | head -20
echo ""

echo "3️⃣ Testing signal forwarder..."
cd "$WORKSPACE"
$VENV_PYTHON apps/discord_signal_forwarder.py 2>&1 | head -30
echo ""

echo "4️⃣ Checking configuration..."
if [ -f "$WORKSPACE/config/discord_sources.json" ]; then
    echo "✅ Config file exists"
    cat "$WORKSPACE/config/discord_sources.json" | grep -E "(enabled|guild_id|conviction)" | head -10
else
    echo "❌ Config file missing"
fi
echo ""

echo "5️⃣ Checking logs directory..."
if [ -d "$WORKSPACE/logs" ]; then
    echo "✅ Logs directory exists"
    ls -lh "$WORKSPACE/logs/" | tail -5
else
    echo "⚠️  Creating logs directory..."
    mkdir -p "$WORKSPACE/logs"
    echo "✅ Created"
fi
echo ""

echo "="
echo "✅ Pipeline test complete"
echo ""
echo "Next steps:"
echo "  1. Invite bot to external Discord servers"
echo "  2. Update config/discord_sources.json with channel IDs"
echo "  3. Run: ./setup_discord_automation.sh"
echo "  4. Done! System runs automatically every 30 minutes"
