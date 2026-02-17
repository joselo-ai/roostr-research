# Content Factory - Quick Start Guide ⚡

**Get your first content package in 5 minutes!**

---

## 🎯 What You'll Get

After running the pipeline, you'll have:

- ✅ **7 trending stories** with engagement scores and content angles
- ✅ **3 viral video scripts** (60-90 seconds, multiple formats)
- ✅ **2 HD thumbnails** (DALL-E generated, 16:9 ratio)
- ✅ **1-2 complete packages** ready to film and publish

All posted to Discord channels for easy review.

---

## 🚀 Run Your First Pipeline

### Option 1: Full Pipeline (Recommended)

```bash
cd ~/.openclaw/workspace/content-factory
python3 run_pipeline.py
```

This runs all 4 agents in sequence:
1. Research trending topics
2. Generate video scripts
3. Create thumbnails
4. Assemble packages

**Time**: ~3-5 minutes (depending on image generation)

### Option 2: Test Individual Agents

```bash
# Step 1: Find trending stories
python3 agent_research.py

# Step 2: Generate scripts (wait 10 seconds after step 1)
python3 agent_script_writer.py

# Step 3: Create thumbnails (wait 10 seconds after step 2)
python3 agent_thumbnail.py

# Step 4: Assemble packages (wait 10 seconds after step 3)
python3 agent_assembler.py
```

### Option 3: Single Agent Only

```bash
# Just research
python3 run_pipeline.py --agent research

# Just scripts
python3 run_pipeline.py --agent script

# Just thumbnails
python3 run_pipeline.py --agent thumbnail

# Just assembler
python3 run_pipeline.py --agent assembler
```

---

## 📱 Check Discord Channels

After running, check these channels:

| Channel | What You'll See |
|---------|-----------------|
| **#trending-stories** | 7 ranked stories with scores |
| **#scripts** | 3 video scripts with hooks/CTAs |
| **#thumbnails** | 2 HD thumbnail images |
| **#ready-to-publish** | Complete packages with checklists |

---

## ⚙️ Scheduling (Run Automatically)

### Cron Schedule (2x daily)

```bash
# Edit crontab
crontab -e

# Add this line (9 AM and 5 PM daily):
0 9,17 * * * cd ~/.openclaw/workspace/content-factory && python3 run_pipeline.py
```

### OpenClaw Heartbeat

Add to `~/.openclaw/workspace/HEARTBEAT.md`:

```markdown
## Content Factory Daily Run

Check time:
- If 9:00-9:05 AM or 5:00-5:05 PM EST
- Run: `python3 ~/.openclaw/workspace/content-factory/run_pipeline.py`
- Track in memory/heartbeat-state.json
```

---

## 🎨 Customize Content

### Change Target Topics

Edit `config.json`:

```json
{
  "relevant_keywords": [
    "your", "custom", "keywords", "here"
  ]
}
```

### Adjust Story Count

Edit `config.json`:

```json
{
  "agents": {
    "research": {
      "top_stories": 10  // Change from 7 to 10
    }
  }
}
```

### Change Script Formats

Scripts auto-detect format, but you can modify templates in `agent_script_writer.py`.

---

## 🐛 Common Issues

### "No messages found in channel"

**Solution**: Agents run in sequence. Make sure:
1. Research agent ran first
2. Wait 10+ seconds between agents
3. Check Discord channels have content

### "Image generation failed"

**Solution**: Check:
```bash
echo $OPENAI_API_KEY  # Should show your API key
```

If billing limit reached, thumbnails will skip. Scripts still work!

### "Failed to post to Discord"

**Solution**:
```bash
# Verify bot token exists
cat ~/.openclaw/workspace/.discord-bot-token

# Verify channels config
cat ~/.openclaw/workspace/.discord-channels.json
```

---

## 📊 Expected Output

### Trending Story Example

```
**#1 - Bitcoin Surges Past $100K as ETF Inflows Hit Record**

📰 Source: bloomberg.com
🔗 Link: https://bloomberg.com/...

📊 Why It's Trending:
• Virality: 85%
• Relevance: 90%
• Overall Score: 0.85/1.00

🎬 Content Angle Ideas:
📈 Trading: Technical analysis and price targets
🎯 Strategy: How traders should position themselves
```

### Script Example

```
🎬 SCRIPT READY - ENTERTAINING FORMAT

Hook: "Stop scrolling. Bitcoin just hit $100K. This is massive."

Body: "So here's what went down: Bitcoin reaches new all-time high 
amid massive institutional demand. The people who saw this coming 
are already winning..."

CTA: "SMASH that follow button right now!"
```

---

## 🎯 Next Steps

1. ✅ Run `python3 test_setup.py` to verify setup
2. ✅ Run `python3 run_pipeline.py` for full pipeline
3. ✅ Check Discord channels for output
4. ✅ Set up cron/heartbeat for automation
5. ✅ Start filming and publishing content!

---

## 📞 Need Help?

- **Setup issues**: Run `python3 test_setup.py`
- **Discord issues**: Check channel IDs in `.discord-channels.json`
- **Image issues**: Verify `OPENAI_API_KEY` is set
- **Full docs**: See `README.md`

---

**Ready to generate content at scale! 🚀**
