# Morning Brief System

**Status:** ✅ Operational (as of Feb 15, 2026)

Automated daily morning briefing posted to Discord #morning-brief channel at 9 AM EST.

## Features

- **📰 News Stories** - Trading, AI, OpenClaw, and market news from the past 24h
- **💡 Business Ideas** - 2-3 creative ideas generated based on current trends
- **✅ Tasks** - Extracted from MEMORY.md, memory/YYYY-MM-DD.md, and HEARTBEAT.md
- **🎯 Recommendations** - Suggested tasks to do together
- **💪 Oura Stats** - Health/readiness metrics (placeholder for API integration)

## Structure

```
morning-brief/
├── generate_brief.py      # Main script
├── run_morning_brief.sh   # Cron wrapper
├── logs/                  # Execution logs
│   └── cron.log
├── output/                # Daily brief archives
│   └── YYYY-MM-DD.txt
└── README.md
```

## Configuration

**Discord Channel:**
- Channel: #morning-brief
- Channel ID: 1472688401558933578
- Token: `.discord-bot-token` (workspace root)

**Cron Schedule:**
```bash
0 9 * * * /Users/agentjoselo/.openclaw/workspace/morning-brief/run_morning_brief.sh
```

**News API:**
- Uses Brave Search API for news (set `BRAVE_API_KEY` env var)
- Fallback: Returns placeholder if API key not set

**Oura Integration:**
- Placeholder implemented (checks for `.oura-api-key` in workspace root)
- TODO: Implement actual Oura API calls

## Usage

### Manual Execution

```bash
cd /Users/agentjoselo/.openclaw/workspace/morning-brief
python3 generate_brief.py
```

### Check Logs

```bash
tail -f logs/cron.log
```

### View Past Briefs

```bash
ls output/
cat output/2026-02-15.txt
```

## Customization

### Add News Sources

Edit `generate_brief.py` and add more `get_web_news()` calls:

```python
crypto_news = get_web_news("cryptocurrency blockchain news", 2)
```

### Modify Business Ideas

Update `generate_business_ideas()` function with your own idea templates.

### Add Task Sources

Extend `extract_tasks()` to parse additional files or patterns.

## Dependencies

- Python 3.x
- `requests` library (install: `pip3 install requests`)
- Discord bot token with access to #morning-brief channel

## Testing

Test the script manually before relying on cron:

```bash
./run_morning_brief.sh
```

Check Discord #morning-brief for the posted message.

## Troubleshooting

**Brief not posting?**
- Check `logs/cron.log` for errors
- Verify Discord token is valid: `cat ../.discord-bot-token`
- Verify channel ID is correct: `1472688401558933578`

**Cron not running?**
- Check crontab: `crontab -l`
- Verify script is executable: `ls -la run_morning_brief.sh`
- Check system time: `date` (should be EST)

**News not loading?**
- Set BRAVE_API_KEY environment variable
- Or use OpenClaw `web_search` tool instead (requires modification)

## Future Enhancements

- [ ] Implement Oura API integration
- [ ] Add portfolio performance summary
- [ ] Include 18-agent deliberation highlights
- [ ] Add market sentiment analysis
- [ ] Weather trading opportunities from Simmer
- [ ] Social arbitrage signals from overnight scans

---

**Created:** Feb 15, 2026  
**Last Updated:** Feb 15, 2026  
**Maintainer:** Joselo (agent)
