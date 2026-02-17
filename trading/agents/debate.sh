#!/bin/bash
# Simple wrapper script for launching 18-agent debates

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🎭 18 Legendary Investors Debate System"
echo ""

# Check if signal file provided
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./debate.sh                    # Use default ASTS signal"
    echo "  ./debate.sh [signal_file]      # Use custom signal"
    echo ""
    echo "Examples:"
    echo "  ./debate.sh signals/asts_signal.json"
    echo "  ./debate.sh ../research/ASTS_brief.md"
    echo ""
    
    read -p "Press Enter to start debate with default ASTS signal, or Ctrl+C to cancel..."
    python3 run_debate.py
else
    python3 run_debate.py "$1"
fi
