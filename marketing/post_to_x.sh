#!/bin/bash

# Tweet content
TWEET_CONTENT="Position sizing = conviction scoring:

Portfolio: \$100k

\$ALL (10/10): \$20k (20%) — Highest conviction
\$PGR (9/10): \$15k (15%) — Second highest
\$KTB (7.5/10): \$10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: \$3.8k (3.8%).

Risk-adjusted by score."

PREVIOUS_TWEET="https://x.com/roostrcapital/status/2022053449681314006"

# Open Chrome and navigate to the tweet
osascript <<EOF
tell application "Google Chrome"
    activate
    open location "$PREVIOUS_TWEET"
    delay 5
    
    -- Find the reply button and click it
    tell active tab of front window
        execute javascript "document.querySelector('[data-testid=\"reply\"]').click();"
    end tell
    delay 3
    
    -- Type the tweet content
    tell active tab of front window
        execute javascript "
            var tweetBox = document.querySelector('[data-testid=\"tweetTextarea_0\"]');
            tweetBox.textContent = '$TWEET_CONTENT';
            tweetBox.dispatchEvent(new Event('input', { bubbles: true }));
        "
    end tell
    delay 2
    
    -- Click the post button
    tell active tab of front window
        execute javascript "document.querySelector('[data-testid=\"tweetButton\"]').click();"
    end tell
    delay 5
    
    -- Get the current URL
    set currentURL to URL of active tab of front window
    return currentURL
end tell
EOF
