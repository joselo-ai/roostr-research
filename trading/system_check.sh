#!/bin/bash
echo "=========================================="
echo "🔍 Price Automation System Check"
echo "=========================================="
echo ""

# Check files exist
echo "📁 Checking files..."
files=(
    "price_fetcher.py"
    "validate_entry.py"
    "update_prices.sh"
    "update_prices_worker.py"
    "update_dashboard.py"
    "setup_price_automation.sh"
    "FIX_CURRENT_POSITIONS.py"
    "PRICE_AUTOMATION_README.md"
    "PRICE_AUTOMATION_DELIVERY.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file MISSING"
    fi
done

echo ""
echo "🧪 Testing components..."

# Test price fetcher
echo "  Testing price_fetcher.py..."
if python3 price_fetcher.py BTC > /dev/null 2>&1; then
    echo "  ✅ Price fetcher working"
else
    echo "  ❌ Price fetcher failed"
fi

# Test validator
echo "  Testing validate_entry.py..."
if python3 validate_entry.py SOL > /dev/null 2>&1; then
    echo "  ✅ Entry validator working"
else
    echo "  ❌ Entry validator failed"
fi

# Test updater
echo "  Testing update_prices.sh..."
if ./update_prices.sh > /dev/null 2>&1; then
    echo "  ✅ Price updater working"
else
    echo "  ❌ Price updater failed"
fi

# Check database
echo ""
echo "📊 Current positions:"
if [ -f "signals-database.csv" ]; then
    awk -F, 'NR==1{next} $7=="YES"{print "  " $1 ": Entry $" $4 ", Current $" $12 ", P&L $" $13}' signals-database.csv
else
    echo "  ❌ signals-database.csv not found"
fi

# Check cache
echo ""
echo "🕐 Last price update:"
if [ -f ".price_cache.json" ]; then
    python3 -c "import json; cache=json.load(open('.price_cache.json')); print('  ' + cache.get('timestamp', 'Unknown'))"
else
    echo "  No cache yet (prices not fetched)"
fi

# Check cron
echo ""
echo "⏰ Cron status:"
if crontab -l 2>/dev/null | grep -q "roostr"; then
    echo "  ✅ Cron automation installed"
    echo "  Schedule:"
    crontab -l 2>/dev/null | grep "roostr" | sed 's/^/  /'
else
    echo "  ⚠️  Cron not installed (run ./setup_price_automation.sh)"
fi

echo ""
echo "=========================================="
echo "✅ System Check Complete"
echo "=========================================="
