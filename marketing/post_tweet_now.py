#!/usr/bin/env python3
"""
Emergency tweet poster using Chrome DevTools Protocol
Posts directly via CDP without Selenium dependency
"""

import json
import subprocess
import time

def post_tweet_via_applescript(tweet_text):
    """Use AppleScript to post tweet via Chrome."""
    # Escape quotes in tweet text
    escaped_text = tweet_text.replace('"', '\\"').replace("'", "\\'")
    
    applescript = f'''
tell application "Google Chrome"
    activate
    
    -- Open compose page
    set composeURL to "https://twitter.com/compose/tweet"
    open location composeURL
    delay 4
    
    -- Wait for page to load and inject text
    tell window 1
        tell active tab
            set tweetPosted to false
            repeat 30 times
                try
                    execute javascript "
                        const textarea = document.querySelector('[data-testid=\\"tweetTextarea_0\\"]');
                        if (textarea) {{
                            textarea.focus();
                            const nativeTextareaSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                            nativeTextareaSetter.call(textarea, '{escaped_text}');
                            const event = new Event('input', {{ bubbles: true }});
                            textarea.dispatchEvent(event);
                            'SUCCESS';
                        }} else {{
                            'NOT_READY';
                        }}
                    "
                    set result to execute javascript "
                        const textarea = document.querySelector('[data-testid=\\"tweetTextarea_0\\"]');
                        textarea ? 'READY' : 'NOT_READY'
                    "
                    
                    if result is "READY" then
                        set tweetPosted to true
                        exit repeat
                    end if
                on error
                    -- Page not ready yet
                end try
                delay 0.5
            end repeat
            
            if tweetPosted then
                return "Tweet text injected - READY TO POST MANUALLY"
            else
                return "ERROR: Could not find tweet compose area"
            end if
        end tell
    end tell
end tell
'''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    tweet_text = """Position sizing = conviction scoring:

Portfolio: $100k

$ALL (10/10): $20k (20%) — Highest conviction
$PGR (9/10): $15k (15%) — Second highest
$KTB (7.5/10): $10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: $3.8k (3.8%).

Risk-adjusted by score."""
    
    print("🐓 Posting tweet via browser automation...")
    print(f"\nTweet content:\n{tweet_text}\n")
    
    result = post_tweet_via_applescript(tweet_text)
    print(f"\nResult: {result}")
