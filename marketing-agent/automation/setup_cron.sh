#!/bin/bash
# roostr Marketing Automation - Cron Setup
# Sets up automated daily posting

WORKSPACE="$HOME/.openclaw/workspace/marketing-agent/automation"
PYTHON=$(which python3)

echo "🐓 roostr Marketing Automation - Cron Setup"
echo ""

# Check if scripts exist
if [ ! -f "$WORKSPACE/post_to_social.py" ]; then
    echo "❌ post_to_social.py not found at $WORKSPACE"
    exit 1
fi

if [ ! -f "$WORKSPACE/generate_content.py" ]; then
    echo "❌ generate_content.py not found at $WORKSPACE"
    exit 1
fi

# Make scripts executable
chmod +x "$WORKSPACE/post_to_social.py"
chmod +x "$WORKSPACE/generate_content.py"
echo "✅ Scripts made executable"

# Create log directory
mkdir -p "$HOME/.openclaw/logs/marketing"
echo "✅ Log directory created"

# Generate crontab entries
CRON_FILE="/tmp/roostr_cron.txt"

cat > "$CRON_FILE" << EOF
# roostr Marketing Automation
# Generated on $(date)

# Generate content queue (daily at 8 AM)
0 8 * * * $PYTHON $WORKSPACE/generate_content.py >> $HOME/.openclaw/logs/marketing/generate.log 2>&1

# Post to social media (4 times per day)
0 9 * * * $PYTHON $WORKSPACE/post_to_social.py >> $HOME/.openclaw/logs/marketing/post.log 2>&1
0 12 * * * $PYTHON $WORKSPACE/post_to_social.py >> $HOME/.openclaw/logs/marketing/post.log 2>&1
0 16 * * * $PYTHON $WORKSPACE/post_to_social.py >> $HOME/.openclaw/logs/marketing/post.log 2>&1
0 19 * * * $PYTHON $WORKSPACE/post_to_social.py >> $HOME/.openclaw/logs/marketing/post.log 2>&1

EOF

echo ""
echo "📅 Proposed Cron Schedule:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "$CRON_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This will:"
echo "  • Generate new content daily at 8 AM"
echo "  • Post at 9 AM (morning update)"
echo "  • Post at 12 PM (midday signal/trade)"
echo "  • Post at 4 PM (afternoon content)"
echo "  • Post at 7 PM (daily recap)"
echo ""
read -p "Install this cron schedule? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup existing crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null
    
    # Add new entries (removing old roostr entries first)
    (crontab -l 2>/dev/null | grep -v "roostr Marketing Automation" | grep -v "generate_content.py" | grep -v "post_to_social.py"; cat "$CRON_FILE") | crontab -
    
    echo "✅ Cron jobs installed"
    echo ""
    echo "📋 Current crontab:"
    crontab -l | grep -A 10 "roostr Marketing Automation"
    echo ""
    echo "✅ Marketing automation is now running"
    echo ""
    echo "To check logs:"
    echo "  tail -f $HOME/.openclaw/logs/marketing/post.log"
    echo "  tail -f $HOME/.openclaw/logs/marketing/generate.log"
    echo ""
    echo "To remove cron jobs:"
    echo "  crontab -e  # then delete the roostr lines"
else
    echo "❌ Installation cancelled"
    echo ""
    echo "To install manually, add these lines to your crontab (crontab -e):"
    cat "$CRON_FILE"
fi

rm -f "$CRON_FILE"
