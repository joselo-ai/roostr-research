#!/bin/bash
# 🐓 Hourly Update Script
# Runs price updater + dashboard data generator + git sync
# Called by cron every hour

cd /Users/agentjoselo/.openclaw/workspace/trading

echo "🐓 Hourly Update - $(date)"
echo "======================================"

# 1. Update prices
echo "💰 Updating prices..."
python3 apps/price_updater.py

# 2. Generate dashboard data
echo "📊 Generating dashboard data..."
python3 apps/generate_dashboard_data.py

# 3. Git sync
echo "📤 Syncing to GitHub..."
git add dashboard.html dashboard-data.json
git commit -m "Hourly update: prices + dashboard data $(date +%H:%M)" || echo "No changes to commit"
git push

echo "✅ Hourly update complete"
echo "======================================"
