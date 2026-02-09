#!/bin/bash
# Reddit Integration - Quick Setup Script
# Run this after getting Reddit API credentials

set -e  # Exit on error

echo "🔥 Reddit Integration - Quick Setup"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
if pip3 install -r requirements-reddit.txt; then
    echo "✅ Dependencies installed"
else
    echo "⚠️  Dependency installation failed. Try manually:"
    echo "   pip3 install praw textblob"
    exit 1
fi

echo ""
echo "📥 Downloading TextBlob corpora..."
if python3 -m textblob.download_corpora; then
    echo "✅ TextBlob corpora downloaded"
else
    echo "⚠️  TextBlob download failed. Sentiment analysis may not work."
fi

echo ""

# Check for config
if [ ! -f "config/reddit_config.json" ]; then
    echo "⚠️  Reddit API config not found"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Create Reddit app: https://www.reddit.com/prefs/apps"
    echo "   2. Select 'script' type"
    echo "   3. Copy client_id and client_secret"
    echo "   4. Create config:"
    echo ""
    echo "      cp config/reddit_config.json.example config/reddit_config.json"
    echo "      # Edit config/reddit_config.json with your credentials"
    echo ""
    echo "   5. Run test: cd scrapers && python3 test_reddit_scraper.py"
    echo ""
else
    echo "✅ Reddit config found: config/reddit_config.json"
    echo ""
    echo "🧪 Running test with mock data..."
    cd scrapers
    if python3 test_reddit_scraper.py; then
        echo ""
        echo "✅ Test passed!"
        echo ""
        echo "🚀 Ready to run live scraper:"
        echo "   cd scrapers && python3 reddit_scraper.py"
        echo ""
        echo "📅 Add to cron (every 6 hours):"
        echo "   0 6,12,18,0 * * * cd $(pwd) && python3 reddit_scraper.py >> ../reddit-scraper.log 2>&1"
    else
        echo ""
        echo "⚠️  Test failed. Check configuration."
        echo "   See: REDDIT-SETUP.md for troubleshooting"
    fi
fi

echo ""
echo "📚 Documentation:"
echo "   • REDDIT-SETUP.md - Complete setup guide"
echo "   • REDDIT-INTEGRATION-COMPLETE.md - Full documentation"
echo "   • DELIVERY-SUMMARY.md - Quick reference"
echo ""
echo "✅ Setup complete!"
