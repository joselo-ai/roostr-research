#!/bin/bash

set -e

QUEUE_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/content-queue.json"
LOG_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/posted-log.json"

# Extract the next unposted morning post
NEXT_POST=$(cat "$QUEUE_FILE" | jq -r '.posts[] | select(.slot == "morning" and .posted == false) | @json' | head -1)

if [ -z "$NEXT_POST" ]; then
    echo "No unposted morning posts found"
    exit 1
fi

# Parse the post data
POST_ID=$(echo "$NEXT_POST" | jq -r '.id')
CONTENT=$(echo "$NEXT_POST" | jq -r '.content')
REPLY_TO=$(echo "$NEXT_POST" | jq -r '.reply_to // empty')

echo "=== Morning Post Automation ==="
echo "Post ID: $POST_ID"
echo ""

# Save content to clipboard
echo "$CONTENT" | pbcopy
echo "✅ Content copied to clipboard"

# Determine URL
if [ -n "$REPLY_TO" ] && [ "$REPLY_TO" != "null" ] && [ "$REPLY_TO" != "previous" ]; then
    TARGET_URL="$REPLY_TO"
    IS_REPLY=true
else
    TARGET_URL="https://x.com/compose/post"
    IS_REPLY=false
fi

echo "Opening: $TARGET_URL"

# Open URL and automate posting
if [ "$IS_REPLY" = true ]; then
    # Reply workflow
    osascript <<EOF
tell application "Google Chrome"
    activate
    open location "$TARGET_URL"
    delay 8
    
    tell active tab of front window
        -- Click reply button
        execute javascript "
            (function() {
                const replyBtn = document.querySelector('[data-testid=\"reply\"]');
                if (replyBtn) replyBtn.click();
            })();
        "
    end tell
    
    delay 4
    
    tell active tab of front window
        -- Focus textarea and paste
        execute javascript "
            (function() {
                const textarea = document.querySelector('[data-testid=\"tweetTextarea_0\"]');
                if (textarea) {
                    textarea.focus();
                    textarea.click();
                }
            })();
        "
    end tell
    
    delay 2
    
    -- Paste from clipboard using System Events
    tell application "System Events"
        keystroke "v" using command down
    end tell
    
    delay 3
    
    tell active tab of front window
        -- Click post button
        execute javascript "
            (function() {
                const postBtn = document.querySelector('[data-testid=\"tweetButton\"]');
                if (postBtn && !postBtn.disabled) {
                    postBtn.click();
                    return true;
                }
                return false;
            })();
        "
    end tell
    
    delay 8
    
    set tweetURL to URL of active tab of front window
    return tweetURL
end tell
EOF
else
    # Standalone tweet workflow
    osascript <<EOF
tell application "Google Chrome"
    activate
    open location "$TARGET_URL"
    delay 8
    
    tell active tab of front window
        -- Focus textarea
        execute javascript "
            (function() {
                const textarea = document.querySelector('[data-testid=\"tweetTextarea_0\"]');
                if (textarea) {
                    textarea.focus();
                    textarea.click();
                }
            })();
        "
    end tell
    
    delay 2
    
    -- Paste from clipboard using System Events
    tell application "System Events"
        keystroke "v" using command down
    end tell
    
    delay 3
    
    tell active tab of front window
        -- Click post button
        execute javascript "
            (function() {
                const postBtn = document.querySelector('[data-testid=\"tweetButton\"]');
                if (postBtn && !postBtn.disabled) {
                    postBtn.click();
                    return true;
                }
                return false;
            })();
        "
    end tell
    
    delay 8
    
    set tweetURL to URL of active tab of front window
    return tweetURL
end tell
EOF
fi

TWEET_URL=$?

echo ""
echo "✅ Tweet posted!"
echo "URL: $TWEET_URL"

# Update files
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "Updating files..."
cat "$QUEUE_FILE" | jq --arg id "$POST_ID" --arg url "$TWEET_URL" --arg ts "$TIMESTAMP" '
    (.posts[] | select(.id == $id)) |= (
        .posted = true |
        .posted_at = $ts |
        .tweet_url = $url
    ) |
    .metadata.updated = $ts |
    .metadata.latest_tweet = $url
' > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"

cat "$LOG_FILE" | jq --argjson post "$NEXT_POST" --arg url "$TWEET_URL" --arg ts "$TIMESTAMP" '
    .posted += [{
        id: $post.id,
        content: $post.content,
        platforms: $post.platforms,
        tweet_url: $url,
        reply_to: ($post.reply_to // null),
        posted_at: $ts,
        note: ($post.note // "Morning post \($post.id)")
    }]
' > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"

echo "✅ Automation Complete!"
