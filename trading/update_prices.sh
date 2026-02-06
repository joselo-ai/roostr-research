#!/bin/bash
#
# Auto Price Updater - Runs every 5 minutes via cron
# Fetches live prices for all open positions
# Updates signals-database.csv with current prices and P&L
# Regenerates dashboard automatically
#

set -e

# Configuration
WORKSPACE="/Users/agentjoselo/.openclaw/workspace/trading"
LOG_FILE="$WORKSPACE/price_updates.log"
MAX_LOG_LINES=1000

cd "$WORKSPACE" || exit 1

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Rotate log if too large
if [ -f "$LOG_FILE" ]; then
    LINE_COUNT=$(wc -l < "$LOG_FILE")
    if [ "$LINE_COUNT" -gt "$MAX_LOG_LINES" ]; then
        tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp"
        mv "$LOG_FILE.tmp" "$LOG_FILE"
        log "📝 Log rotated (was $LINE_COUNT lines)"
    fi
fi

log "========================================"
log "🤖 Starting automatic price update..."

# Run price updater
log "📊 Updating prices..."

if python3 "$WORKSPACE/update_prices_worker.py" >> "$LOG_FILE" 2>&1; then
    log "✅ Prices updated successfully"
    
    # Regenerate dashboard
    log "🔄 Regenerating dashboard..."
    if python3 update_dashboard.py >> "$LOG_FILE" 2>&1; then
        log "✅ Dashboard regenerated"
    else
        log "⚠️  Dashboard regeneration failed (non-critical)"
    fi
else
    log "❌ Price update failed"
    exit 1
fi

log "✅ Price update complete"
log "========================================"

exit 0
