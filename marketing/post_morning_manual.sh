#!/bin/bash

# Read the content queue to find next morning post
QUEUE_FILE="/Users/agentjoselo/.openclaw/workspace/marketing/content-queue.json"

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

echo "=== Morning Post Ready ==="
echo "Post ID: $POST_ID"
echo ""
echo "--- CONTENT TO POST ---"
echo "$CONTENT"
echo "--- END CONTENT ---"
echo ""
if [ -n "$REPLY_TO" ] && [ "$REPLY_TO" != "null" ] && [ "$REPLY_TO" != "previous" ]; then
    echo "Reply to: $REPLY_TO"
    echo ""
fi
echo "Next steps:"
echo "1. Open X (twitter.com) in your browser"
if [ -n "$REPLY_TO" ] && [ "$REPLY_TO" != "null" ] && [ "$REPLY_TO" != "previous" ]; then
    echo "2. Navigate to: $REPLY_TO"
    echo "3. Click Reply button"
else
    echo "2. Click 'Post' or 'What's happening?'"
fi
echo "4. Paste the content above"
echo "5. Click 'Post'"
echo "6. Copy the tweet URL from your browser"
echo ""
echo "Then run:"
echo "  ./update_queue_after_post.sh $POST_ID <TWEET_URL>"
