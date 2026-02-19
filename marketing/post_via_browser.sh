#!/bin/bash
# Post tweet via browser automation
# Usage: ./post_via_browser.sh

cd /Users/agentjoselo/.openclaw/workspace/marketing

# Run the Python script to get tweet details
python3 twitter_browser_poster.py > /tmp/tweet_data.txt

# Extract tweet text and reply-to ID
# This will be used by OpenClaw's browser automation

cat /tmp/tweet_data.txt

echo ""
echo "🤖 Ready for browser automation"
echo "   Next: Use OpenClaw browser tool to navigate to X and post"
