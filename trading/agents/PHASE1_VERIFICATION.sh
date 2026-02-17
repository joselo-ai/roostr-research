#!/bin/bash
# Phase 1 Verification Script
# Run this to verify Phase 1 is operational

echo "======================================================================"
echo "🐓 PHASE 1 VERIFICATION - 4 Quant Agents"
echo "======================================================================"
echo ""

# Check files exist
echo "📁 Checking files..."
files=("quant_agents_v2.py" "test_phase1.py" "quant_valuation.json" "quant_technicals.json" "quant_fundamentals.json" "quant_sentiment.json")
all_found=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file MISSING"
        all_found=false
    fi
done
echo ""

# Check virtual environment
echo "🔧 Checking virtual environment..."
if [ -d "venv" ]; then
    echo "  ✅ venv exists"
else
    echo "  ❌ venv MISSING - run: python3 -m venv venv"
    exit 1
fi
echo ""

# Activate and test
echo "🧪 Running test suite on SPHR..."
source venv/bin/activate
python3 test_phase1.py SPHR > /tmp/phase1_test.log 2>&1

if grep -q "PHASE 1 COMPLETE - ALL TESTS PASSED" /tmp/phase1_test.log; then
    echo "  ✅ All tests PASSED"
    echo ""
    grep "Consensus:" /tmp/phase1_test.log | head -1
    grep "Avg Conviction:" /tmp/phase1_test.log | head -1
    grep "ABSTAIN votes:" /tmp/phase1_test.log | head -1
else
    echo "  ❌ Tests FAILED - see /tmp/phase1_test.log"
    exit 1
fi

echo ""
echo "======================================================================"
echo "✅ PHASE 1 VERIFICATION COMPLETE"
echo "======================================================================"
echo ""
echo "Status: 🟢 GREEN - All agents operational"
echo "Location: $(pwd)"
echo "Documentation: PHASE1_COMPLETION_REPORT.md"
echo ""
