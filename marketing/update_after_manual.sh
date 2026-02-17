#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <POST_ID> <TWEET_URL>"
    echo "Example: $0 w2-8 https://x.com/roostrcapital/status/1234567890"
    exit 1
fi

POST_ID="$1"
TWEET_URL="$2"

QUEUE_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/content-queue.json"
LOG_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/posted-log.json"

# Verify files exist
if [ ! -f "$QUEUE_FILE" ]; then
    echo "Error: $QUEUE_FILE not found"
    exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: $LOG_FILE not found"
    exit 1
fi

# Get the post data
POST_DATA=$(cat "$QUEUE_FILE" | jq --arg id "$POST_ID" '.posts[] | select(.id == $id)' | jq -c '.')

if [ -z "$POST_DATA" ]; then
    echo "Error: Post $POST_ID not found in queue"
    exit 1
fi

echo "Found post: $POST_ID"
echo "Updating with URL: $TWEET_URL"
echo ""

# Update timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Update content-queue.json
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

# Update posted-log.json
echo "Updating posted-log.json..."
cat "$LOG_FILE" | jq --argjson post "$POST_DATA" --arg url "$TWEET_URL" --arg ts "$TIMESTAMP" '
    .posted += [{
        id: $post.id,
        content: $post.content,
        platforms: $post.platforms,
        tweet_url: $url,
        reply_to: ($post.reply_to // null),
        posted_at: $ts,
        note: ($post.note // "Manual post \($post.id)")
    }]
' > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"

echo ""
echo "✅ Success!"
echo "Post $POST_ID marked as posted"
echo "URL: $TWEET_URL"
echo "Timestamp: $TIMESTAMP"
