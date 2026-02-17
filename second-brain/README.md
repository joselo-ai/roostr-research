# 2nd Brain Dashboard

**Status:** ✅ Built and ready (as of Feb 15, 2026)

Visual dashboard for reviewing memories, documents, tasks, and trading intelligence.

## Features

### 📊 Dashboard Pages

1. **Home** - Quick overview and navigation
2. **Memories** - View and edit MEMORY.md with live updates
3. **Documents** - Timeline view of all memory/*.md files
4. **Tasks** - Aggregated task list from all sources
5. **Trading Signals** - Integration with trading dashboard + recent signals
6. **Daily Logs** - Activity timeline and system events
7. **Search** - Search across all memory files (planned)

### 🎨 Design

- **Clean, minimal UI** - Fast and distraction-free
- **Tailwind CSS** - Responsive, mobile-friendly
- **Dark text on light background** - Easy reading
- **TypeScript** - Type-safe, maintainable code

## Structure

```
second-brain/
├── app/
│   ├── api/              # API routes
│   │   ├── memory/       # MEMORY.md read/write
│   │   ├── documents/    # List memory files
│   │   ├── document/     # Read individual files
│   │   └── tasks/        # Extract tasks
│   ├── components/       # Shared components
│   │   └── Navigation.tsx
│   ├── memories/         # Memories page
│   ├── documents/        # Documents page
│   ├── tasks/            # Tasks page
│   ├── trading/          # Trading page
│   ├── logs/             # Logs page
│   ├── search/           # Search page
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── public/               # Static assets
├── package.json
└── README.md
```

## Development

### Install Dependencies

```bash
cd /Users/agentjoselo/.openclaw/workspace/second-brain
npm install
```

### Run Development Server

```bash
npm run dev
```

Access at: **http://localhost:3000**

### Build for Production

```bash
npm run build
npm start
```

## API Routes

### GET `/api/memory`
Returns content of MEMORY.md

### POST `/api/memory`
Saves updated MEMORY.md content

**Body:**
```json
{
  "content": "Updated memory content..."
}
```

### GET `/api/documents`
Lists all memory/*.md files with metadata

**Response:**
```json
{
  "documents": [
    {
      "name": "2026-02-15.md",
      "path": "/path/to/file",
      "size": 1234,
      "modified": "2026-02-15T12:00:00Z",
      "preview": "First 200 chars..."
    }
  ]
}
```

### GET `/api/document/[name]`
Returns content of specific memory file

### GET `/api/tasks`
Extracts tasks from MEMORY.md, HEARTBEAT.md, and daily files

**Response:**
```json
{
  "tasks": [
    {
      "text": "Run social arb scan",
      "source": "HEARTBEAT.md",
      "completed": false
    }
  ]
}
```

## Features by Page

### Memories
- Display MEMORY.md content
- Inline editing with save/cancel
- Live updates
- Confirmation before saving

### Documents
- Timeline view of all memory files (newest first)
- Preview snippets
- Click to view full content
- File metadata (date, size)

### Tasks
- Aggregated from multiple sources
- Filter by: Active, Completed, All
- Grouped by source file
- Checkbox visualization

### Trading Signals
- Phase 1 status overview
- Allocation strategy visualization
- Recent signals with conviction scores
- Link to full trading dashboard

### Daily Logs
- Recent activity feed
- Categorized by type
- Timestamped entries
- Color-coded by level (info, success, warning, error)

### Search
- Full-text search across all memory files
- Line numbers and context
- Quick navigation to results

## File Locations

**Workspace root:** `/Users/agentjoselo/.openclaw/workspace`

**Files accessed:**
- `MEMORY.md` - Long-term memory
- `HEARTBEAT.md` - Heartbeat checklist
- `memory/*.md` - Daily memory files
- `trading/dashboard.html` - Trading dashboard

## Customization

### Add New Page

1. Create `app/new-page/page.tsx`
2. Add link in `app/components/Navigation.tsx`
3. Optional: Add API route in `app/api/new-route/route.ts`

### Modify Styling

Edit Tailwind classes in components or update `tailwind.config.ts`

### Add Data Sources

Extend API routes to read from additional files or databases

## Troubleshooting

**Port 3000 already in use?**
```bash
lsof -ti:3000 | xargs kill -9
```

**Build errors?**
```bash
rm -rf .next node_modules
npm install
npm run dev
```

**API routes not working?**
- Check file paths in API routes
- Verify workspace location
- Check console for errors

## Future Enhancements

- [ ] Implement actual search API with grep/ripgrep
- [ ] Add file upload for new memory files
- [ ] Real-time updates with WebSockets
- [ ] Export memory as PDF/markdown
- [ ] Tag system for organizing memories
- [ ] Calendar view of daily files
- [ ] Graph visualization of connections

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Runtime:** Node.js
- **Package Manager:** npm

---

**Created:** Feb 15, 2026  
**Last Updated:** Feb 15, 2026  
**Maintainer:** Joselo (agent)  
**Port:** 3000
