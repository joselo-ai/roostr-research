# 2nd Brain Systems - Complete Documentation

**Status:** ✅ Both systems operational (Feb 15, 2026)
**Created by:** Joselo (subagent)
**For:** G

---

## System 1: Morning Brief (PRIORITY 1) ✅

### Overview
Automated morning briefing posted to Discord #morning-brief every day at 9 AM EST.

### What It Includes
- **📰 News Stories** - Trading, AI, OpenClaw, markets (via Brave Search API)
- **💡 Business Ideas** - 2-3 creative ideas based on current trends
- **✅ Tasks for Today** - Extracted from MEMORY.md, memory/YYYY-MM-DD.md, HEARTBEAT.md
- **🎯 Recommendations** - Suggested tasks to do together
- **💪 Oura Stats** - Placeholder (ready for API integration)

### Location
```
/Users/agentjoselo/.openclaw/workspace/morning-brief/
├── generate_brief.py        # Main script
├── run_morning_brief.sh     # Cron wrapper
├── logs/cron.log            # Execution logs
├── output/YYYY-MM-DD.txt    # Daily brief archives
└── README.md                # Full documentation
```

### Configuration

**Discord Channel:**
- Channel: #morning-brief
- Channel ID: `1472688401558933578`
- Token: `.discord-bot-token` (workspace root)

**Cron Schedule:**
```bash
0 9 * * * /Users/agentjoselo/.openclaw/workspace/morning-brief/run_morning_brief.sh
```

**Cron Status:**
```bash
# Check if scheduled
crontab -l | grep morning-brief

# View logs
tail -f /Users/agentjoselo/.openclaw/workspace/morning-brief/logs/cron.log
```

### Manual Execution

```bash
cd /Users/agentjoselo/.openclaw/workspace/morning-brief
python3 generate_brief.py
```

**First run today:** ✅ Posted successfully (Message ID: 1472689085524213996)

### News API Setup (Optional)

Set `BRAVE_API_KEY` environment variable for live news:
```bash
export BRAVE_API_KEY="your_api_key_here"
```

Without API key, the script will work with placeholder content.

### Oura Integration (Pending)

To add Oura stats:
1. Get API key from Oura dashboard
2. Save to `/Users/agentjoselo/.openclaw/workspace/.oura-api-key`
3. Implement API calls in `generate_brief.py` (placeholder exists)

### Customization

**Add news sources:**
```python
# In generate_brief.py
crypto_news = get_web_news("cryptocurrency blockchain news", 2)
```

**Modify business ideas:**
Edit `generate_business_ideas()` function with your templates

**Add task sources:**
Extend `extract_tasks()` to parse additional files

---

## System 2: NextJS 2nd Brain Dashboard (PRIORITY 2) ✅

### Overview
Visual dashboard for reviewing memories, documents, tasks, and trading intelligence.

### Access
- **URL:** http://localhost:3000
- **Network:** http://192.168.1.175:3000 (accessible from phone/tablet)
- **Status:** ✅ Running (background process)

### Features

#### 1. Dashboard Home (`/`)
- Quick overview cards
- Navigation to all sections
- Stats summary

#### 2. Memories (`/memories`)
- Display MEMORY.md
- **Editable** - Save changes directly
- Full CRUD operations

#### 3. Documents (`/documents`)
- Timeline view of all `memory/*.md` files
- Newest first
- Click to view full content
- File metadata (date, size, preview)

#### 4. Tasks (`/tasks`)
- Aggregated from MEMORY.md, HEARTBEAT.md, daily files
- Filter: Active, Completed, All
- Grouped by source
- Visual checkboxes

#### 5. Trading Signals (`/trading`)
- Phase 1 status overview
- Allocation strategy (40/30/20/10 split)
- Recent signals with conviction scores
- Link to full `trading/dashboard.html`

#### 6. Daily Logs (`/logs`)
- Recent activity feed
- Categorized and timestamped
- Color-coded by level

#### 7. Search (`/search`)
- Search across all memory files
- Line numbers and context
- (Placeholder - ready for implementation)

### Location
```
/Users/agentjoselo/.openclaw/workspace/second-brain/
├── app/
│   ├── api/              # Backend routes
│   │   ├── memory/       # MEMORY.md CRUD
│   │   ├── documents/    # List files
│   │   ├── document/     # Read file
│   │   └── tasks/        # Extract tasks
│   ├── components/       # Shared UI
│   ├── memories/         # Pages
│   ├── documents/
│   ├── tasks/
│   ├── trading/
│   ├── logs/
│   ├── search/
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── package.json
└── README.md
```

### Start/Stop Server

**Start:**
```bash
cd /Users/agentjoselo/.openclaw/workspace/second-brain
npm run dev
```

**Stop:**
```bash
# Find process
lsof -ti:3000

# Kill process
lsof -ti:3000 | xargs kill -9
```

**Build for production:**
```bash
npm run build
npm start
```

### Tech Stack
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Node.js runtime

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/memory` | GET | Read MEMORY.md |
| `/api/memory` | POST | Save MEMORY.md |
| `/api/documents` | GET | List memory files |
| `/api/document/[name]` | GET | Read specific file |
| `/api/tasks` | GET | Extract tasks |

### Mobile Access

From phone/tablet on same network:
```
http://192.168.1.175:3000
```

---

## Quick Start Guide

### Morning Brief
1. **Already scheduled** - Runs automatically at 9 AM EST
2. **Check logs:** `tail -f morning-brief/logs/cron.log`
3. **View archive:** `ls morning-brief/output/`
4. **Test now:** `cd morning-brief && python3 generate_brief.py`

### Dashboard
1. **Already running** - Access at http://localhost:3000
2. **Mobile:** http://192.168.1.175:3000
3. **Edit memory:** Go to /memories and click "Edit"
4. **View tasks:** Go to /tasks
5. **Check trading:** Go to /trading

---

## File Access Map

Both systems read from:
- `/Users/agentjoselo/.openclaw/workspace/MEMORY.md`
- `/Users/agentjoselo/.openclaw/workspace/HEARTBEAT.md`
- `/Users/agentjoselo/.openclaw/workspace/memory/*.md`
- `/Users/agentjoselo/.openclaw/workspace/trading/`

---

## Troubleshooting

### Morning Brief Not Posting?
```bash
# Check cron
crontab -l | grep morning-brief

# Check logs
tail -f morning-brief/logs/cron.log

# Test manually
cd morning-brief && python3 generate_brief.py

# Verify Discord token
cat ../.discord-bot-token
```

### Dashboard Not Loading?
```bash
# Check if server running
lsof -ti:3000

# Restart server
lsof -ti:3000 | xargs kill -9
cd second-brain && npm run dev

# Check for errors
# Open browser console (F12)
```

### Files Not Found?
```bash
# Verify workspace path
echo $PWD
# Should be: /Users/agentjoselo/.openclaw/workspace

# Check files exist
ls MEMORY.md HEARTBEAT.md
ls memory/
```

---

## Future Enhancements

### Morning Brief
- [ ] Implement Oura API integration
- [ ] Add portfolio performance summary
- [ ] Include 18-agent deliberation highlights
- [ ] Weather trading opportunities from Simmer
- [ ] Social arbitrage signals from overnight scans

### Dashboard
- [ ] Implement actual search API (grep/ripgrep)
- [ ] Real-time updates with WebSockets
- [ ] File upload for new memory files
- [ ] Export memory as PDF/markdown
- [ ] Tag system for organizing memories
- [ ] Calendar view of daily files
- [ ] Graph visualization of memory connections

---

## Maintenance

### Daily
- Morning brief posts automatically at 9 AM EST
- Check Discord #morning-brief for delivery
- Dashboard runs 24/7 (or restart as needed)

### Weekly
- Review `morning-brief/logs/cron.log` for errors
- Check `morning-brief/output/` for archived briefs
- Update business ideas templates if needed

### Monthly
- Clean old log files
- Review and optimize task extraction logic
- Add new data sources as needed

---

## Architecture

### Morning Brief Flow
```
Cron (9 AM EST)
  ↓
run_morning_brief.sh
  ↓
generate_brief.py
  ↓
1. Fetch news (Brave API)
2. Generate business ideas
3. Extract tasks (MEMORY.md, HEARTBEAT.md, daily files)
4. Get recommendations
5. Check Oura stats
  ↓
Format Discord message
  ↓
Post to #morning-brief (ID: 1472688401558933578)
  ↓
Save to output/YYYY-MM-DD.txt
  ↓
Log to logs/cron.log
```

### Dashboard Flow
```
Browser → http://localhost:3000
  ↓
NextJS App Router
  ↓
Pages render (React components)
  ↓
API calls to /api/* endpoints
  ↓
Read files from workspace (fs.readFileSync)
  ↓
Return JSON to frontend
  ↓
Display in UI (Tailwind CSS)
```

---

## Summary

### ✅ Deliverable 1: Morning Brief
- **Script:** Built and tested
- **Cron:** Scheduled for 9 AM EST daily
- **First run:** Successful (posted to Discord)
- **Logs:** `morning-brief/logs/cron.log`
- **Archive:** `morning-brief/output/YYYY-MM-DD.txt`

### ✅ Deliverable 2: NextJS Dashboard
- **App:** Built and running on localhost:3000
- **Pages:** 7 pages (Dashboard, Memories, Documents, Tasks, Trading, Logs, Search)
- **Edit capability:** MEMORY.md editable via UI
- **API:** 5 endpoints operational
- **Design:** Clean, minimal, fast

### ✅ Deliverable 3: Documentation
- **Morning Brief:** `morning-brief/README.md`
- **Dashboard:** `second-brain/README.md`
- **Master Doc:** This file (`2ND-BRAIN-SYSTEMS.md`)

---

## Contact & Support

**Created:** Feb 15, 2026 at 3:18 PM EST
**By:** Joselo (subagent)
**Session:** agent:main:subagent:2ad5fc72-bef7-4e17-a6d2-82d84a878b9c
**For:** G

Both systems are production-ready and operational. Enjoy your 2nd Brain! 🧠

---

**Next Steps for G:**
1. Check Discord #morning-brief tomorrow at 9 AM
2. Visit http://localhost:3000 to explore dashboard
3. Edit MEMORY.md via dashboard to test save functionality
4. Review tasks aggregated from all sources
5. Consider adding Oura API key for health stats
6. Add BRAVE_API_KEY for live news (optional)
