#!/bin/bash

# Read the content queue to find next morning post
QUEUE_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/content-queue.json"
LOG_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/posted-log.json"

# Extract the next unposted morning post using jq
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
echo "Time: $(date)"
echo "Post ID: $POST_ID"
echo "Content preview: ${CONTENT:0:50}..."
echo ""

# Escape content for AppleScript
ESCAPED_CONTENT=$(echo "$CONTENT" | sed 's/"/\\"/g' | sed "s/'/\\\\'/g")

# Build the AppleScript
if [ -z "$REPLY_TO" ] || [ "$REPLY_TO" = "null" ] || [ "$REPLY_TO" = "previous" ]; then
    # Standalone tweet
    APPLESCRIPT="
tell application \"Google Chrome\"
    activate
    tell window 1
        set newTab to make new tab with properties {URL:\"https://x.com/compose/post\"}
        set active tab index to (count of tabs)
    end tell
    delay 5
    
    tell active tab of window 1
        execute javascript \"
            setTimeout(() => {
                const textarea = document.querySelector('[data-testid=\\\"tweetTextarea_0\\\"]');
                if (textarea) {
                    textarea.focus();
                    document.execCommand('insertText', false, \\\`$ESCAPED_CONTENT\\\`);
                }
            }, 2000);
        \"
    end tell
    
    delay 3
    
    tell active tab of window 1
        execute javascript \"
            setTimeout(() => {
                const postButton = document.querySelector('[data-testid=\\\"tweetButton\\\"]');
                if (postButton && !postButton.disabled) {
                    postButton.click();
                }
            }, 1000);
        \"
    end tell
    
    delay 10
    
    set tweetURL to URL of active tab of window 1
    return tweetURL
end tell
"
else
    # Reply to previous tweet
    APPLESCRIPT="
tell application \"Google Chrome\"
    activate
    tell window 1
        set newTab to make new tab with properties {URL:\"$REPLY_TO\"}
        set active tab index to (count of tabs)
    end tell
    delay 5
    
    tell active tab of window 1
        execute javascript \"
            setTimeout(() => {
                const replyButton = document.querySelector('[data-testid=\\\"reply\\\"]');
                if (replyButton) {
                    replyButton.click();
                }
            }, 2000);
        \"
    end tell
    
    delay 3
    
    tell active tab of window 1
        execute javascript \"
            setTimeout(() => {
                const textarea = document.querySelector('[data-testid=\\\"tweetTextarea_0\\\"]');
                if (textarea) {
                    textarea.focus();
                    document.execCommand('insertText', false, \\\`$ESCAPED_CONTENT\\\`);
                }
            }, 2000);
        \"
    end tell
    
    delay 3
    
    tell active tab of window 1
        execute javascript \"
            setTimeout(() => {
                const postButton = document.querySelector('[data-testid=\\\"tweetButton\\\"]');
                if (postButton && !postButton.disabled) {
                    postButton.click();
                }
            }, 1000);
        \"
    end tell
    
    delay 10
    
    set tweetURL to URL of active tab of window 1
    return tweetURL
end tell
"
fi

# Execute the AppleScript
echo "Posting tweet via Chrome..."
TWEET_URL=$(osascript -e "$APPLESCRIPT")

if [ $? -eq 0 ]; then
    echo "✅ Tweet posted successfully!"
    echo "URL: $TWEET_URL"
    
    # Update content-queue.json
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    cat "$QUEUE_FILE" | jq --arg id "$POST_ID" --arg url "$TWEET_URL" --arg ts "$TIMESTAMP" '
        (.posts[] | select(.id == $id)) |= (
            .posted = true |
            .posted_at = $ts |
            .tweet_url = $url
        ) |
        .metadata.updated = $ts |
        .metadata.latest_tweet = $url
    ' > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"
    
    # Update posted-log.json
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
    
    echo "✅ Files updated successfully!"
    echo "=== Automation Complete ==="
else
    echo "❌ Failed to post tweet"
    exit 1
fi
