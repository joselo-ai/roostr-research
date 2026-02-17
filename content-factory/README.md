# Content Factory 🏭

**Autonomous multi-agent pipeline for viral content generation**

Generate 5-10 publish-ready content packages daily with AI-powered research, scriptwriting, and thumbnail generation.

---

## 🎯 Overview

Content Factory is a production-ready pipeline that automatically:

1. **Researches** trending topics (AI, crypto, tech, business)
2. **Writes** viral video scripts (60-90 seconds)
3. **Generates** eye-catching thumbnails (DALL-E 3)
4. **Assembles** complete publish-ready packages

All outputs are posted to dedicated Discord channels for easy review and publishing.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT FACTORY PIPELINE                  │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Research   │ ─→ │    Script    │ ─→ │  Thumbnail   │ ─→ │   Package    │
│    Agent     │    │    Writer    │    │  Generator   │    │  Assembler   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                    │                    │                    │
       ▼                    ▼                    ▼                    ▼
#trending-stories      #scripts          #thumbnails        #ready-to-publish
```

### Agent Responsibilities

| Agent | Input | Output | Trigger |
|-------|-------|--------|---------|
| **Research Agent** | Web search | Top 7 trending stories with scores | Cron (9 AM, 5 PM EST) |
| **Script Writer** | #trending-stories | 3 viral video scripts | Event-driven |
| **Thumbnail Generator** | #scripts | 2 HD thumbnails | Event-driven |
| **Package Assembler** | All channels | Complete packages | Event-driven |

---

## 📁 File Structure

```
content-factory/
├── README.md                    # This file
├── config.json                  # Pipeline configuration
├── discord_helper.py            # Enhanced Discord API wrapper
├── agent_research.py            # Agent 1: Trending stories scanner
├── agent_script_writer.py       # Agent 2: Video script generator
├── agent_thumbnail.py           # Agent 3: Thumbnail image generator
├── agent_assembler.py           # Agent 4: Package assembler
├── run_pipeline.py              # Standalone pipeline orchestrator
├── openclaw_runner.py           # OpenClaw integration wrapper
└── generated_thumbnails/        # Output directory for images
```

---

## 🚀 Quick Start

### 1. Test Individual Agents

Test each agent standalone (uses mock data):

```bash
# Test research agent
cd ~/.openclaw/workspace/content-factory
python3 agent_research.py

# Test script writer (requires trending stories in Discord)
python3 agent_script_writer.py

# Test thumbnail generator (requires scripts in Discord)
python3 agent_thumbnail.py

# Test package assembler (requires all assets)
python3 agent_assembler.py
```

### 2. Run Full Pipeline

Run the complete pipeline (standalone mode):

```bash
python3 run_pipeline.py
```

Run individual agent:

```bash
python3 run_pipeline.py --agent research
python3 run_pipeline.py --agent script
python3 run_pipeline.py --agent thumbnail
python3 run_pipeline.py --agent assembler
```

### 3. Run from OpenClaw (with web_search)

From OpenClaw agent session:

```bash
cd ~/.openclaw/workspace/content-factory
python3 openclaw_runner.py
```

Or research only:

```bash
python3 openclaw_runner.py research-only
```

---

## 🤖 OpenClaw Integration

### Using web_search in Research Agent

The research agent needs live web data. OpenClaw provides `web_search`:

**Option 1: Spawn sub-agent to run pipeline**

```javascript
// From main OpenClaw agent
exec(`cd ~/.openclaw/workspace/content-factory && python3 openclaw_runner.py`)
```

**Option 2: Direct Python integration (advanced)**

Modify `openclaw_runner.py` to accept web_search as stdin JSON:

```python
import json
import sys

# Read search results from stdin (passed by OpenClaw)
if not sys.stdin.isatty():
    search_data = json.load(sys.stdin)
    # Use search_data in agent_research
```

### Scheduling with Cron

**Option 1: System cron** (runs without OpenClaw)

```bash
# Edit crontab
crontab -e

# Add lines (adjust paths):
0 9 * * * cd ~/.openclaw/workspace/content-factory && python3 run_pipeline.py --agent research
0 17 * * * cd ~/.openclaw/workspace/content-factory && python3 run_pipeline.py --agent research
```

**Option 2: OpenClaw heartbeat** (recommended)

Add to `HEARTBEAT.md`:

```markdown
## Content Factory

Run research agent at 9 AM and 5 PM EST:
- Check current time
- If 9:00-9:05 AM or 5:00-5:05 PM, run: `python3 ~/.openclaw/workspace/content-factory/openclaw_runner.py research-only`
- Track last run in `memory/heartbeat-state.json`
```

**Option 3: OpenClaw scheduled spawn**

```javascript
// Schedule research agent for 9 AM daily
// (Add to main agent's scheduling logic)
```

---

## 📊 Discord Channels

All outputs are posted to dedicated Discord channels in the **Content Factory** category:

| Channel | Purpose | Format |
|---------|---------|--------|
| **#trending-stories** | Research agent output | Story title, source, score, content angles |
| **#scripts** | Video scripts | Hook, body, CTA, visuals, production notes |
| **#thumbnails** | Generated images | HD image + title variations |
| **#ready-to-publish** | Complete packages | All assets + checklist + performance targets |

### Channel IDs

```json
{
  "trending-stories": "1472690048192348412",
  "scripts": "1472690073639321750",
  "thumbnails": "1472690097672421571",
  "ready-to-publish": "1472690120372126028"
}
```

---

## 🎨 Thumbnail Generation

### Requirements

- **OpenAI API key** set in environment: `OPENAI_API_KEY`
- **OpenAI image gen skill** installed: `/opt/homebrew/lib/node_modules/openclaw/skills/openai-image-gen/`

### How It Works

1. Script writer posts script to #scripts
2. Thumbnail agent monitors channel
3. Extracts story topic and format
4. Generates 3 style variations (bold text, reaction face, minimal, etc.)
5. Uses DALL-E 3 with optimized prompts
6. Posts HD image (1792x1024) to #thumbnails

### Thumbnail Styles

- **Bold Text Overlay**: Large text on dramatic background
- **Shocked Face**: Reaction-style clickbait (professional quality)
- **Minimal Clean**: Premium typography with gradients
- **Split Screen**: Before/after transformation theme
- **Question Mark**: Curiosity-driven intrigue

---

## 📝 Script Formats

The script writer generates 4 different formats:

### 1. Educational
- **Hook**: Question format
- **Tone**: Informative but engaging
- **Best for**: How-to, explanations, breakdowns

### 2. Entertaining
- **Hook**: Shocking statement
- **Tone**: Energetic and viral
- **Best for**: Surprising news, dramatic events

### 3. Controversy
- **Hook**: Hot take
- **Tone**: Bold and opinionated
- **Best for**: Debates, polarizing topics

### 4. Tutorial
- **Hook**: Promise of value
- **Tone**: Helpful and actionable
- **Best for**: Step-by-step guides, strategies

---

## 🎯 Scoring Algorithm

Stories are scored on 4 dimensions (weighted):

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **Virality** | 30% | Source authority + viral keywords (breaking, surges, etc.) |
| **Relevance** | 40% | Keyword match with audience interests (AI, crypto, tech, trading) |
| **Freshness** | 20% | Recency (all search results assumed fresh) |
| **Engagement** | 10% | Title has numbers, questions, or power words |

**Score range**: 0.00 - 1.00 (higher is better)

**Example scoring**:
```
Story: "Bitcoin Surges Past $100K as ETF Inflows Hit Record"

Virality: 0.85 (authority source + "surges")
Relevance: 0.90 (bitcoin, crypto keywords)
Freshness: 0.90 (today's news)
Engagement: 0.70 (has numbers)

Overall Score: 0.85
```

---

## 🔧 Configuration

Edit `config.json` to customize:

### Agent Settings

```json
{
  "agents": {
    "research": {
      "top_stories": 7,              // How many stories to post
      "search_queries": [...]        // What to search for
    },
    "script_writer": {
      "scripts_per_run": 3           // Scripts per execution
    },
    "thumbnail_generator": {
      "thumbnails_per_run": 2,       // Thumbnails per run
      "model": "dall-e-3",           // Image model
      "quality": "hd"                // Image quality
    }
  }
}
```

### Scoring Weights

```json
{
  "scoring_weights": {
    "virality": 0.3,
    "relevance": 0.4,
    "freshness": 0.2,
    "engagement_potential": 0.1
  }
}
```

### Relevant Keywords

Add or remove keywords to tune relevance scoring:

```json
{
  "relevant_keywords": [
    "ai", "crypto", "trading", "startup", ...
  ]
}
```

---

## 🧪 Testing

### Full Pipeline Test

Generate 1 complete package from start to finish:

```bash
# Run full pipeline (will take 2-3 minutes)
cd ~/.openclaw/workspace/content-factory
python3 run_pipeline.py

# Check Discord channels:
# 1. #trending-stories → 7 stories posted
# 2. #scripts → 3 scripts generated
# 3. #thumbnails → 2 thumbnails created
# 4. #ready-to-publish → 1-2 complete packages
```

### Individual Agent Testing

```bash
# Test research (mock data)
python3 agent_research.py

# Test script writer (needs stories in Discord first)
python3 agent_script_writer.py

# Test thumbnail gen (needs scripts in Discord first)
# NOTE: Requires OPENAI_API_KEY
python3 agent_thumbnail.py

# Test assembler (needs all assets in Discord)
python3 agent_assembler.py
```

---

## 📈 Production Usage

### Daily Automation

**Recommended schedule**:

- **9:00 AM EST**: Research agent runs → posts trending stories
- **9:10 AM EST**: Script writer runs → generates scripts
- **9:20 AM EST**: Thumbnail generator runs → creates images
- **9:30 AM EST**: Package assembler runs → posts complete packages

- **5:00 PM EST**: Research agent runs again
- **5:10 PM EST**: Script writer runs
- **5:20 PM EST**: Thumbnail generator runs
- **5:30 PM EST**: Package assembler runs

**Result**: 2-4 publish-ready packages per day (10-20 per week)

### Batch Mode (1x daily)

Run full pipeline once per day:

```bash
# 9 AM cron
0 9 * * * cd ~/.openclaw/workspace/content-factory && python3 run_pipeline.py --delay 15
```

This generates ~3-5 packages in one go.

---

## 🐛 Troubleshooting

### Discord API Issues

**Problem**: "Failed to post to Discord"

**Solutions**:
- Check bot token in `~/.openclaw/workspace/.discord-bot-token`
- Verify channel IDs in `.discord-channels.json`
- Ensure bot has permissions in Discord server

### Image Generation Fails

**Problem**: "Image generation failed"

**Solutions**:
- Check `OPENAI_API_KEY` is set: `echo $OPENAI_API_KEY`
- Verify image gen skill exists: `ls /opt/homebrew/lib/node_modules/openclaw/skills/openai-image-gen/`
- Check API quota/billing on OpenAI dashboard
- Review error logs in terminal

### No Messages Found

**Problem**: "No messages found in channel"

**Solutions**:
- Run agents in sequence (research → script → thumbnail → assembler)
- Check Discord channels have content
- Increase `--delay` between agents: `python3 run_pipeline.py --delay 15`

### Web Search Not Working

**Problem**: Research returns mock data

**Solutions**:
- Use `openclaw_runner.py` instead of `run_pipeline.py`
- Ensure running from OpenClaw agent session (not standalone terminal)
- Or: Implement direct web_search API integration

---

## 📁 Output Examples

### Trending Story Post

```
**#1 - OpenAI Announces GPT-5 with Revolutionary Reasoning**

📰 **Source:** techcrunch.com
🔗 **Link:** https://techcrunch.com/...

📊 **Why It's Trending:**
• Virality: 90% (source authority + viral keywords)
• Relevance: 85% (audience interest match)
• Freshness: 90% (recency)
• Engagement: 80% (click potential)
• **Overall Score: 0.87/1.00**

💬 **Estimated Engagement:** ~8,700 views potential

🎬 **Content Angle Ideas:**
🎓 Educational: How this AI advancement affects everyday users
💼 Business: Investment opportunities in AI sector
⚡ Quick Take: 60-second explanation for beginners
```

### Script Post

```
🎬 **SCRIPT READY - EDUCATIONAL FORMAT**

**Original Story:** OpenAI Announces GPT-5...

⏱️ **Duration:** ~65 seconds (162 words)
🎭 **Format:** Educational

**🎣 HOOK (0-5 sec):**
You know what everyone's talking about right now? OpenAI's GPT-5 announcement...

**📝 BODY (5-60 sec):**
First, the facts: OpenAI unveils GPT-5 with unprecedented reasoning...

**🎯 CTA (60-70 sec):**
If you want more analysis like this, hit that follow button...
```

### Ready to Publish Package

```
🚀 **READY TO PUBLISH - COMPLETE PACKAGE** 🚀

**Story:** OpenAI Announces GPT-5 with Revolutionary Reasoning
**Format:** Educational | **Duration:** ~65s

**✅ PUBLISHING CHECKLIST:**
☐ Review full script for accuracy and tone
☐ Check thumbnail text is readable on mobile
☐ Select best title variation (A/B test if possible)
...

🎬 **READY TO FILM AND PUBLISH!**
```

---

## 🔮 Future Enhancements

- [ ] Voice-over generation with ElevenLabs
- [ ] Automated video editing (B-roll insertion)
- [ ] YouTube auto-upload integration
- [ ] Performance tracking (views, engagement)
- [ ] A/B testing different script formats
- [ ] Multi-platform support (TikTok, Instagram, Twitter)
- [ ] Real-time trend monitoring (Twitter API)
- [ ] Automatic republishing of top performers

---

## 📞 Support

**Issues or questions?**

- Check Discord channels for agent output
- Review logs in terminal output
- Verify `config.json` settings
- Test individual agents before full pipeline

---

## 📄 License

MIT License - Built for OpenClaw autonomous agent system

---

**Built with ❤️ by the Content Factory pipeline**

*Generate publish-ready content at scale, fully autonomous.*
