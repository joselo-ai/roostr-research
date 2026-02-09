# roostr Marketing Automation

**Never miss a post again.**

## What This Does

Automated daily posting system for roostr brand:
- Generates content from signals and performance data
- Posts to X and Instagram at scheduled times (9 AM, 12 PM, 4 PM, 7 PM)
- Maintains a 7-day content queue
- Logs everything
- Never needs manual intervention

## Quick Start

### 1. Install Dependencies

```bash
pip install tweepy instagrapi python-dotenv
```

### 2. Configure API Credentials

Create `config.json`:

```json
{
  "x_api_key": "your_x_api_key",
  "x_api_secret": "your_x_api_secret",
  "x_access_token": "your_x_access_token",
  "x_access_secret": "your_x_access_secret",
  "instagram_username": "roostrcapital",
  "instagram_password": "your_instagram_password",
  "dry_run": false
}
```

Or use environment variables:
```bash
export X_API_KEY="..."
export X_API_SECRET="..."
export X_ACCESS_TOKEN="..."
export X_ACCESS_SECRET="..."
export INSTAGRAM_USERNAME="roostrcapital"
export INSTAGRAM_PASSWORD="..."
```

### 3. Set Up Cron Jobs

```bash
cd automation
./setup_cron.sh
```

This installs:
- **8 AM**: Generate new content (replenish queue)
- **9 AM**: Morning post (signal/update)
- **12 PM**: Midday post (trade execution)
- **4 PM**: Afternoon post (lesson/infrastructure)
- **7 PM**: Evening recap

### 4. Verify It Works

```bash
# Generate initial content queue
python3 generate_content.py

# Test posting (dry run)
python3 post_to_social.py

# Check logs
tail -f ~/.openclaw/logs/marketing/post.log
```

## Files

- **`post_to_social.py`** - Posts content to X/Instagram
- **`generate_content.py`** - Generates posts from signals/data
- **`setup_cron.sh`** - Installs cron jobs
- **`content_queue.json`** - Queue of posts to publish
- **`posting_log.json`** - Log of what was posted
- **`config.json`** - API credentials (gitignored)

## Content Queue

The queue is a JSON file with posts scheduled for specific times:

```json
{
  "posts": [
    {
      "id": "post_1",
      "type": "signal",
      "title": "Signal: TAO",
      "content": "🟢 NEW SIGNAL\n\n$TAO - ...",
      "platforms": ["x", "instagram"],
      "scheduled_time": "09:00",
      "posted": false,
      "created_at": "2026-02-06T08:00:00"
    }
  ],
  "last_id": 1
}
```

## How It Works

### Content Generation
1. Checks for new GREEN signals from trading agent
2. Generates signal posts (when new signals found)
3. Generates daily updates (1 per day)
4. Generates lesson posts (2-3 per week)
5. Generates infrastructure posts (1-2 per week)
6. Maintains a 7-day queue (~14 posts)

### Posting
1. Runs at scheduled times (9 AM, 12 PM, 4 PM, 7 PM)
2. Checks queue for posts scheduled around current time
3. Posts to configured platforms
4. Marks as posted in queue
5. Logs result

### Safety
- Starts in **dry_run mode** (prints what it would post)
- Set `"dry_run": false` in config.json to go live
- All posts logged to `posting_log.json`
- Failed posts remain in queue for retry

## Manual Usage

### Generate Content Now
```bash
python3 generate_content.py
```

### Post Now (ignores schedule)
```bash
python3 post_to_social.py
```

### View Queue
```bash
cat content_queue.json | jq .
```

### View Logs
```bash
# Posting log
cat posting_log.json | jq '.posts[-10:]'  # Last 10 posts

# Cron logs
tail -f ~/.openclaw/logs/marketing/post.log
tail -f ~/.openclaw/logs/marketing/generate.log
```

### Clear Queue
```bash
# Remove all posted items
cat content_queue.json | jq '.posts = [.posts[] | select(.posted == false)]' > content_queue.json
```

## Integration with Trading Agent

The content generator automatically pulls from:
- `~/. openclaw/workspace/trading-agent/signals/{date}_signals.json`
- `~/.openclaw/workspace/trading-agent/performance/latest.json`

When new GREEN signals appear, posts are auto-generated.

## Customization

Edit templates in `generate_content.py`:
- `generate_signal_post()` - Signal announcements
- `generate_daily_update()` - Daily recaps
- `generate_lesson_post()` - Trading lessons
- `generate_infrastructure_post()` - System updates

## Troubleshooting

### Posts not showing up
- Check cron is running: `crontab -l`
- Check logs: `tail -f ~/.openclaw/logs/marketing/post.log`
- Verify queue has posts: `cat content_queue.json | jq '.posts[] | select(.posted == false)'`

### API errors
- Verify credentials in `config.json`
- Check rate limits (X: 50 posts/day, Instagram: varies)
- Check `posting_log.json` for error messages

### Dry run not posting
- Set `"dry_run": false` in `config.json`
- Or set environment variable: `DRY_RUN=false`

## X (Twitter) API Setup

1. Go to https://developer.twitter.com/
2. Create an app
3. Get API keys (v2 API with OAuth 1.0a)
4. Add to `config.json`

## Instagram API Setup

Instagram posting is more complex (no official API for posting):
- Option 1: Use `instagrapi` (unofficial, works but risky)
- Option 2: Use Meta Graph API (requires Business account)
- Option 3: Manual posting from queue (post from phone using queue as script)

Current implementation uses `instagrapi` (dry_run by default).

## Going Live

1. Verify dry_run works: `python3 post_to_social.py`
2. Check generated content quality: `cat content_queue.json`
3. Set `"dry_run": false` in `config.json`
4. Post once manually to test: `python3 post_to_social.py`
5. Verify on X/Instagram
6. Let cron take over

## Monitoring

Check daily:
```bash
# Quick status
cat posting_log.json | jq '.posts[-5:]'

# Posts scheduled for today
cat content_queue.json | jq '.posts[] | select(.posted == false) | .scheduled_time, .title'

# Cron job status
ps aux | grep post_to_social
```

Weekly:
- Review `posting_log.json` for failures
- Check engagement on posted content
- Adjust templates in `generate_content.py` if needed

---

**roostr. never miss a post again.** 🐓
