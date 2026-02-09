#!/bin/bash

# 🐓 ROOSTR Trading Hub Launcher
# Quick launch script for the trading terminal

echo "🐓 ROOSTR Trading Hub"
echo "===================="
echo ""
echo "Starting local server on port 8080..."
echo ""
echo "📊 Trading Terminal: http://localhost:8080/trading-hub.html"
echo "📄 Dashboard: http://localhost:8080/dashboard.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 -m http.server 8080
