#!/bin/bash
# Daily Morning Scraping Pipeline
# Runs at 9 AM EST via cron: 0 9 * * * /path/to/daily_scrape_morning.sh
# 
# This script:
# 1. Fetches Discord messages (last 24h)
# 2. Runs all scrapers
# 3. Validates signals with quality checks
# 4. Writes only GREEN/YELLOW to database
# 5. Updates dashboard
# 6. Sends summary notification

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_DIR="../logs"
LOG_FILE="$LOG_DIR/scraper_$(date +%Y-%m-%d).log"
ERROR_LOG="$LOG_DIR/errors_$(date +%Y-%m-%d).log"

# Create log directory
mkdir -p "$LOG_DIR"

# Helper: Log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$ERROR_LOG" >&2
}

# Start
log "═══════════════════════════════════════════════════════════"
log "Starting Morning Scraping Pipeline"
log "═══════════════════════════════════════════════════════════"

# ===== STEP 1: Fetch Discord Messages =====
log "Step 1: Fetching Discord messages (last 24h)..."

if [ ! -f "discord_fetcher.py" ]; then
    log_error "discord_fetcher.py not found!"
    exit 1
fi

# Check for Discord token
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    log_error "DISCORD_BOT_TOKEN not set. Skipping Discord fetch."
    log "Using cached messages if available..."
else
    python3 discord_fetcher.py --hours 24 --output fetched_messages.json >> "$LOG_FILE" 2>> "$ERROR_LOG"
    
    if [ $? -eq 0 ]; then
        log "✅ Discord fetch complete"
    else
        log_error "Discord fetch failed. Check error log."
    fi
fi

# ===== STEP 2: Run Scrapers =====
log "Step 2: Running scrapers..."

# Check if we have fetched messages
if [ ! -f "fetched_messages.json" ]; then
    log_error "No fetched messages found. Cannot run scrapers."
    exit 1
fi

# Yieldschool scraper
if [ -f "yieldschool_scraper.py" ]; then
    log "Running Yieldschool scraper..."
    python3 yieldschool_scraper.py --input fetched_messages.json --output yieldschool_signals.json >> "$LOG_FILE" 2>> "$ERROR_LOG"
    
    if [ $? -eq 0 ]; then
        log "✅ Yieldschool scraper complete"
    else
        log_error "Yieldschool scraper failed"
    fi
else
    log "⚠️  yieldschool_scraper.py not found, skipping"
fi

# Dumb Money scraper
if [ -f "dumbmoney_scraper.py" ]; then
    log "Running Dumb Money scraper..."
    python3 dumbmoney_scraper.py --input fetched_messages.json --output dumbmoney_signals.json >> "$LOG_FILE" 2>> "$ERROR_LOG"
    
    if [ $? -eq 0 ]; then
        log "✅ Dumb Money scraper complete"
    else
        log_error "Dumb Money scraper failed"
    fi
else
    log "⚠️  dumbmoney_scraper.py not found, skipping"
fi

# ===== STEP 3: Merge Signals =====
log "Step 3: Merging signals from all scrapers..."

# Combine all signal JSONs into one
python3 -c "
import json
import glob

all_signals = []
for file in glob.glob('*_signals.json'):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                all_signals.extend(data)
            else:
                all_signals.append(data)
    except Exception as e:
        print(f'Error loading {file}: {e}')

with open('merged_signals.json', 'w') as f:
    json.dump(all_signals, f, indent=2)

print(f'Merged {len(all_signals)} signals from scrapers')
" >> "$LOG_FILE" 2>> "$ERROR_LOG"

log "✅ Signal merge complete"

# ===== STEP 4: Quality Validation =====
log "Step 4: Running quality validation..."

if [ -f "data_quality_checker.py" ]; then
    python3 -c "
import json
from data_quality_checker import DataQualityChecker

# Load merged signals
with open('merged_signals.json', 'r') as f:
    signals = json.load(f)

# Validate
checker = DataQualityChecker()
results = checker.batch_validate(signals)

# Save results
with open('validated_signals.json', 'w') as f:
    json.dump(results, f, indent=2)

# Generate report
report = checker.generate_report(results)
print(report)

# Save report
with open('../logs/quality_report_$(date +%Y-%m-%d).txt', 'w') as f:
    f.write(report)
" >> "$LOG_FILE" 2>> "$ERROR_LOG"
    
    log "✅ Quality validation complete"
else
    log_error "data_quality_checker.py not found! Skipping validation."
    # Fallback: treat all signals as YELLOW
    python3 -c "
import json
with open('merged_signals.json', 'r') as f:
    signals = json.load(f)
results = {'GREEN': [], 'YELLOW': signals, 'RED': []}
with open('validated_signals.json', 'w') as f:
    json.dump(results, f, indent=2)
" >> "$LOG_FILE" 2>> "$ERROR_LOG"
fi

# ===== STEP 5: External Validation (Dex, Trends) =====
log "Step 5: Running external validation (Dexscreener, Google Trends)..."

if [ -f "signal_validator.py" ]; then
    python3 -c "
import json
from signal_validator import SignalValidator

# Load validated signals (GREEN + YELLOW only)
with open('validated_signals.json', 'r') as f:
    results = json.load(f)

# Validate GREEN and high-conviction YELLOW
to_validate = results['GREEN'] + [s for s in results['YELLOW'] if s.get('conviction_score', 0) >= 7]

if to_validate:
    validator = SignalValidator()
    externally_validated = validator.batch_validate(to_validate)
    
    # Update results
    results['GREEN'] = externally_validated
    
    # Save
    with open('validated_signals.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f'Externally validated {len(externally_validated)} signals')
else:
    print('No signals to externally validate')
" >> "$LOG_FILE" 2>> "$ERROR_LOG"
    
    log "✅ External validation complete"
else
    log "⚠️  signal_validator.py not found, skipping external validation"
fi

# ===== STEP 6: Write to Database =====
log "Step 6: Writing validated signals to database..."

python3 -c "
import json
import csv
from datetime import datetime

# Load validated signals
with open('validated_signals.json', 'r') as f:
    results = json.load(f)

# Only write GREEN and YELLOW (RED rejected)
to_write = results['GREEN'] + results['YELLOW']

if not to_write:
    print('No signals to write (all rejected)')
    exit(0)

# Append to CSV
with open('../signals-database.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    
    for signal in to_write:
        writer.writerow([
            signal['ticker'],
            signal['source'],
            signal.get('date_found', datetime.now().strftime('%Y-%m-%d')),
            signal.get('price_entry', ''),
            signal.get('conviction_score', 5),
            signal.get('validation_status', 'YELLOW'),
            'NO',  # deployed
            '',  # position_size
            '',  # stop_loss
            '',  # target_1
            '',  # target_2
            '',  # current_price
            '',  # pnl_dollars
            '',  # pnl_percent
            signal.get('validation_reasons', '')[:200]  # notes
        ])

print(f'Wrote {len(to_write)} signals to database')
" >> "$LOG_FILE" 2>> "$ERROR_LOG"

log "✅ Database write complete"

# ===== STEP 7: Update Dashboard =====
log "Step 7: Updating dashboard..."

if [ -f "../update_dashboard.py" ]; then
    python3 ../update_dashboard.py >> "$LOG_FILE" 2>> "$ERROR_LOG"
    log "✅ Dashboard updated"
else
    log "⚠️  update_dashboard.py not found, skipping"
fi

# ===== STEP 8: Generate Summary =====
log "Step 8: Generating summary..."

python3 -c "
import json
from datetime import datetime

# Load results
with open('validated_signals.json', 'r') as f:
    results = json.load(f)

summary = {
    'timestamp': datetime.now().isoformat(),
    'total_scraped': len(results['GREEN']) + len(results['YELLOW']) + len(results['RED']),
    'green_signals': len(results['GREEN']),
    'yellow_signals': len(results['YELLOW']),
    'red_signals': len(results['RED']),
    'top_green': [
        {'ticker': s['ticker'], 'source': s['source'], 'conviction': s['conviction_score']}
        for s in sorted(results['GREEN'], key=lambda x: x.get('conviction_score', 0), reverse=True)[:5]
    ]
}

# Save summary
with open('morning_run_results.json', 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary
print('╔═══════════════════════════════════════════════════════════╗')
print('║           Morning Scraping Summary                        ║')
print('╚═══════════════════════════════════════════════════════════╝')
print(f'Total Signals Scraped: {summary[\"total_scraped\"]}')
print(f'├─ 🟢 GREEN (Deploy Ready): {summary[\"green_signals\"]}')
print(f'├─ 🟡 YELLOW (Monitoring): {summary[\"yellow_signals\"]}')
print(f'└─ 🔴 RED (Rejected): {summary[\"red_signals\"]}')
print()

if summary['top_green']:
    print('Top GREEN Signals:')
    for sig in summary['top_green']:
        print(f'  • {sig[\"ticker\"]} ({sig[\"source\"]}) - Conviction: {sig[\"conviction\"]}/10')
else:
    print('No GREEN signals today.')
" | tee -a "$LOG_FILE"

# ===== STEP 9: Send Notification (Optional) =====
log "Step 9: Sending notification..."

# TODO: Implement notification (Discord webhook, email, etc.)
# For now, just log summary location
log "Summary saved to: morning_run_results.json"

# ===== CLEANUP =====
log "Cleaning up temporary files..."
rm -f yieldschool_signals.json dumbmoney_signals.json merged_signals.json

log "═══════════════════════════════════════════════════════════"
log "Morning scraping pipeline complete!"
log "Check logs: $LOG_FILE"
log "═══════════════════════════════════════════════════════════"
