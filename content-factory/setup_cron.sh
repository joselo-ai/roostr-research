#!/bin/bash
# Setup cron jobs for Content Factory automation

echo "🏭 Content Factory - Cron Setup"
echo "================================"
echo ""
echo "This script will set up automatic content generation 2x daily (9 AM and 5 PM EST)"
echo ""

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Content Factory location: $SCRIPT_DIR"
echo ""
echo "Proposed cron schedule:"
echo "  • 9:00 AM EST - Full pipeline run"
echo "  • 5:00 PM EST - Full pipeline run"
echo ""
echo "Cron entry to add:"
echo "---"
echo "# Content Factory - Daily automation"
echo "0 9,17 * * * cd $SCRIPT_DIR && /opt/homebrew/bin/python3 run_pipeline.py --delay 10 >> $SCRIPT_DIR/logs/cron.log 2>&1"
echo "---"
echo ""

read -p "Add this to crontab? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Create logs directory
    mkdir -p "$SCRIPT_DIR/logs"
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "# Content Factory - Daily automation"; echo "0 9,17 * * * cd $SCRIPT_DIR && /opt/homebrew/bin/python3 run_pipeline.py --delay 10 >> $SCRIPT_DIR/logs/cron.log 2>&1") | crontab -
    
    echo "✅ Cron job added!"
    echo ""
    echo "To verify:"
    echo "  crontab -l"
    echo ""
    echo "To view logs:"
    echo "  tail -f $SCRIPT_DIR/logs/cron.log"
    echo ""
    echo "To remove:"
    echo "  crontab -e  # Delete the Content Factory lines"
else
    echo "❌ Cancelled. You can manually add the cron job later."
fi

echo ""
echo "================================"
