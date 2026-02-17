#!/bin/bash

set -e

QUEUE_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/content-queue.json"
LOG_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/posted-log.json"
TEMP_CONTENT="/tmp/tweet_content_$$.txt"

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
echo "Content length: ${#CONTENT} chars"
echo ""

# Save content to temp file
echo "$CONTENT" > "$TEMP_CONTENT"

# Copy to clipboard
cat "$TEMP_CONTENT" | pbcopy
echo "✅ Content copied to clipboard"

# Determine URL to open
if [ -n "$REPLY_TO" ] && [ "$REPLY_TO" != "null" ] && [ "$REPLY_TO" != "previous" ]; then
    TARGET_URL="$REPLY_TO"
    echo "Opening reply to: $TARGET_URL"
else
    TARGET_URL="https://x.com/compose/post"
    echo "Opening compose page: $TARGET_URL"
fi

# Open X in Chrome
osascript <<EOF
tell application "Google Chrome"
    activate
    tell window 1
        set newTab to make new tab with properties {URL:"$TARGET_URL"}
    end tell
end tell
EOF

echo ""
echo "⏳ Browser opened. Waiting 15 seconds for page load..."
sleep 15

# Provide instructions
echo ""
echo "📋 MANUAL STEP NEEDED:"
echo "1. The content is in your clipboard (already copied)"
if [ -n "$REPLY_TO" ] && [ "$REPLY_TO" != "null" ] && [ "$REPLY_TO" != "previous" ]; then
    echo "2. Click the 'Reply' button in the browser"
else
    echo "2. The compose box should be visible"
fi
echo "3. Click in the text area"
echo "4. Press Cmd+V to paste"
echo "5. Click 'Post'"
echo "6. Wait for the tweet to appear"
echo ""
read -p "Press ENTER once the tweet is posted..."

# Get the current URL from Chrome
TWEET_URL=$(osascript -e 'tell application "Google Chrome" to get URL of active tab of front window')

echo ""
echo "Tweet URL: $TWEET_URL"
echo ""

# Confirm with user
read -p "Is this the correct tweet URL? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter the correct tweet URL: " TWEET_URL
fi

# Update files
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "Updating content-queue.json..."
cat "$QUEUE_FILE" | jq --arg id "$POST_ID" --arg url "$TWEET_URL" --arg ts "$TIMESTAMP" '
    (.posts[] | select(.id == $id)) |= (
        .posted = true |
        .posted_at = $ts |
        .tweet_url = $url
    ) |
    .metadata.updated = $ts |
    .metadata.latest_tweet = $url
' > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"

echo "Updating posted-log.json..."
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

# Cleanup
rm -f "$TEMP_CONTENT"

echo ""
echo "✅ Automation Complete!"
echo "Tweet URL: $TWEET_URL"
echo "Files updated successfully"
