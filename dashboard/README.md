# 🦂 Joselo Control Dashboard

Live task tracking with color-coded status (Red/Yellow/Green).

## Quick Start

**Open dashboard:**
```bash
open /Users/agentjoselo/.openclaw/workspace/dashboard/index.html
```

Or just double-click `index.html` in Finder.

## How It Works

- **Source of truth:** `tasks.json`
- **UI:** `index.html` (auto-refreshes every 30 seconds)
- **Updates:** I edit `tasks.json`, dashboard reflects changes instantly

## Status Colors

- 🔴 **Red** = Not Started
- 🟡 **Yellow** = In Progress
- 🟢 **Green** = Completed

## KPIs Tracked

- Total Tasks
- Completed
- In Progress
- Not Started
- Completion Rate (%)

## Adding Tasks

I update `tasks.json` programmatically. You can also edit it manually if needed.

Example task:
```json
{
  "id": 7,
  "title": "New task name",
  "status": "not-started",
  "priority": "high",
  "category": "trading",
  "created": "2026-02-04",
  "notes": "Optional description"
}
```

## Categories

- `setup` - Infrastructure/accounts
- `trading` - Trading operations
- `development` - Code/projects
- `operations` - Day-to-day tasks

## Priority Levels

- `high`
- `medium`
- `low`
