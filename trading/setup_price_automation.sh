#!/bin/bash
#
# Setup Price Automation - Install cron jobs for automatic price updates
# Run this once to set up the automation, then forget about it
#

set -e

WORKSPACE="/Users/agentjoselo/.openclaw/workspace/trading"
CRON_COMMENT="# roostr price automation"

echo "========================================"
echo "🤖 roostr Price Automation Setup"
echo "========================================"
echo ""

# Validate workspace exists
if [ ! -d "$WORKSPACE" ]; then
    echo "❌ Workspace not found: $WORKSPACE"
    exit 1
fi

# Validate required scripts exist
REQUIRED_FILES=(
    "$WORKSPACE/update_prices.sh"
    "$WORKSPACE/price_fetcher.py"
    "$WORKSPACE/update_prices_worker.py"
    "$WORKSPACE/update_dashboard.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file not found: $file"
        exit 1
    fi
done

echo "✅ All required files present"
echo ""

# Make scripts executable
chmod +x "$WORKSPACE/update_prices.sh"
chmod +x "$WORKSPACE/price_fetcher.py"
chmod +x "$WORKSPACE/update_prices_worker.py"
chmod +x "$WORKSPACE/update_dashboard.py"

echo "✅ Scripts marked executable"
echo ""

# Get current crontab (or empty if none exists)
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2>/dev/null || echo "# crontab" > "$TEMP_CRON"

# Remove old roostr price automation entries if they exist
grep -v "$CRON_COMMENT" "$TEMP_CRON" > "$TEMP_CRON.new" || true
mv "$TEMP_CRON.new" "$TEMP_CRON"

# Add new cron jobs
cat >> "$TEMP_CRON" << CRON_JOBS

$CRON_COMMENT
# Update prices every 5 minutes (9 AM - 11 PM EST)
*/5 9-23 * * * cd $WORKSPACE && ./update_prices.sh >> price_updates.log 2>&1

$CRON_COMMENT - hourly backup
# Hourly broader market check (optional, can be disabled)
# 0 * * * * cd $WORKSPACE && python3 price_fetcher.py BTC ETH SOL TAO >> market_data.log 2>&1

CRON_JOBS

# Install new crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "✅ Cron jobs installed"
echo ""
echo "📅 Automation Schedule:"
echo "   • Every 5 minutes (9 AM - 11 PM): Update prices + regenerate dashboard"
echo "   • Logs written to: $WORKSPACE/price_updates.log"
echo ""

# Test the update script immediately
echo "🧪 Testing price update script..."
cd "$WORKSPACE"
if ./update_prices.sh; then
    echo ""
    echo "✅ Test successful!"
else
    echo ""
    echo "❌ Test failed - check logs"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ PRICE AUTOMATION ACTIVE"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Prices will auto-update every 5 minutes"
echo "  2. Dashboard auto-regenerates after each update"
echo "  3. Check logs: tail -f $WORKSPACE/price_updates.log"
echo "  4. View cron jobs: crontab -l"
echo ""
echo "To disable automation:"
echo "  crontab -e"
echo "  (Comment out or delete roostr price automation lines)"
echo ""
echo "🐓 Never depend on humans for data that can be automated!"
echo ""
