#!/bin/bash
# roostr Marketing Automation - System Test
# Quick verification that everything is working

echo "🐓 roostr Marketing Automation - System Test"
echo "=============================================="
echo ""

WORKSPACE="$HOME/.openclaw/workspace/marketing-agent"
AUTOMATION="$WORKSPACE/automation"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0

test_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - File not found: $1"
        ((FAILED++))
    fi
}

test_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - Not executable: $1"
        ((FAILED++))
    fi
}

test_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} $2 - Not installed: $1"
        ((FAILED++))
    fi
}

echo "📁 Checking Files..."
test_file "$WORKSPACE/posts-2026-02-06.md" "Today's posts"
test_file "$AUTOMATION/post_to_social.py" "Posting script"
test_file "$AUTOMATION/generate_content.py" "Content generator"
test_file "$AUTOMATION/setup_cron.sh" "Cron installer"
test_file "$AUTOMATION/content_queue.json" "Content queue"
test_file "$AUTOMATION/config.template.json" "Config template"
test_file "$AUTOMATION/README.md" "Documentation"
test_file "$WORKSPACE/QUICK-START.md" "Quick start guide"
test_file "$WORKSPACE/MISSION-COMPLETE.md" "Mission report"

echo ""
echo "🔧 Checking Executables..."
test_executable "$AUTOMATION/post_to_social.py" "Posting script executable"
test_executable "$AUTOMATION/generate_content.py" "Generator executable"
test_executable "$AUTOMATION/setup_cron.sh" "Setup script executable"

echo ""
echo "📦 Checking Dependencies..."
test_command "python3" "Python 3"
test_command "jq" "jq (JSON processor)"

echo ""
echo "🐍 Checking Python Packages..."
if python3 -c "import tweepy" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} tweepy (X/Twitter API)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} tweepy not installed (run: pip3 install tweepy)"
    ((FAILED++))
fi

if python3 -c "import instagrapi" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} instagrapi (Instagram API)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} instagrapi not installed (run: pip3 install instagrapi)"
fi

echo ""
echo "🧪 Testing Scripts..."

# Test content generator
echo -n "Testing content generator... "
if cd "$AUTOMATION" && python3 generate_content.py > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED++))
fi

# Test poster (dry run)
echo -n "Testing poster (dry run)... "
if cd "$AUTOMATION" && python3 post_to_social.py > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED++))
fi

# Check queue
echo -n "Checking content queue... "
QUEUE_SIZE=$(cat "$AUTOMATION/content_queue.json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len([p for p in data['posts'] if not p.get('posted', False)]))" 2>/dev/null)
if [ "$QUEUE_SIZE" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} ($QUEUE_SIZE posts ready)"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} (queue empty)"
    ((FAILED++))
fi

echo ""
echo "📊 Test Results"
echo "=============================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo ""
    echo "System is ready to deploy!"
    echo ""
    echo "Next steps:"
    echo "  1. Add API keys to automation/config.json"
    echo "  2. Test: python3 automation/post_to_social.py"
    echo "  3. Deploy: ./automation/setup_cron.sh"
    exit 0
else
    echo -e "${YELLOW}⚠️  SOME TESTS FAILED${NC}"
    echo ""
    echo "Fix the issues above before deploying."
    echo ""
    echo "Common fixes:"
    echo "  - Install Python packages: pip3 install tweepy instagrapi"
    echo "  - Install jq: brew install jq"
    exit 1
fi
