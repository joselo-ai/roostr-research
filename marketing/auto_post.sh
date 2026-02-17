#!/bin/bash

# Open the previous tweet in Chrome
open -a "Google Chrome" "https://x.com/roostrcapital/status/2022053449681314006"

# Wait for page to load
sleep 8

# Use AppleScript to:
# 1. Press Tab to focus reply button (might need multiple tabs)
# 2. Press Enter to click reply
# 3. Type the tweet
# 4. Press Cmd+Enter to post

osascript <<'EOF'
tell application "System Events"
    tell process "Google Chrome"
        set frontmost to true
        delay 2
        
        -- Click reply button (using keyboard shortcut if available, or Tab to navigate)
        -- On X, pressing 'r' key replies to the current tweet
        keystroke "r"
        delay 3
        
        -- Now the compose box should be open, type the tweet
        keystroke "Position sizing = conviction scoring:

Portfolio: $100k

$ALL (10/10): $20k (20%) — Highest conviction
$PGR (9/10): $15k (15%) — Second highest
$KTB (7.5/10): $10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: $3.8k (3.8%).

Risk-adjusted by score."
        
        delay 2
        
        -- Post the tweet (Cmd+Enter)
        keystroke return using {command down}
        delay 5
    end tell
end tell
EOF

echo "Tweet posted! Check Chrome to verify and get the URL."
