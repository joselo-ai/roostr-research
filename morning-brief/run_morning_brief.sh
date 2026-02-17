#!/bin/bash
# Morning Brief Runner - Called by cron at 9 AM EST daily

set -e

# Set working directory
cd /Users/agentjoselo/.openclaw/workspace/morning-brief

# Set environment
export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$PATH"
export BRAVE_API_KEY="${BRAVE_API_KEY:-}"

# Log start
echo "[$(date)] Starting morning brief generation..." >> logs/cron.log

# Run the Python script
python3 generate_brief.py >> logs/cron.log 2>&1

# Log completion
echo "[$(date)] Morning brief completed" >> logs/cron.log

exit 0
