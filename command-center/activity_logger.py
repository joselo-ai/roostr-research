#!/usr/bin/env python3
"""
Joselo Activity Logger
Tracks every action, decision, and automation run
"""

import json
import os
from datetime import datetime
from pathlib import Path

class ActivityLogger:
    def __init__(self, log_dir="/Users/agentjoselo/.openclaw/workspace/command-center"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "activity-log.jsonl"
        self.stats_file = self.log_dir / "stats.json"
        
    def log(self, category, action, details=None, status="success"):
        """Log an activity"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category,  # trading, marketing, research, automation, decision
            "action": action,
            "details": details or {},
            "status": status  # success, error, warning, info
        }
        
        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Update stats
        self._update_stats(category, status)
        
        return entry
    
    def _update_stats(self, category, status):
        """Update running statistics"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                "total_actions": 0,
                "by_category": {},
                "by_status": {},
                "last_updated": None
            }
        
        stats["total_actions"] += 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        stats["last_updated"] = datetime.now().isoformat()
        
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def get_recent(self, limit=50):
        """Get recent activities"""
        if not self.log_file.exists():
            return []
        
        activities = []
        with open(self.log_file, 'r') as f:
            for line in f:
                activities.append(json.loads(line))
        
        return activities[-limit:]
    
    def get_stats(self):
        """Get statistics"""
        if not self.stats_file.exists():
            return None
        
        with open(self.stats_file, 'r') as f:
            return json.load(f)
    
    def get_today(self):
        """Get today's activities"""
        today = datetime.now().date().isoformat()
        
        if not self.log_file.exists():
            return []
        
        activities = []
        with open(self.log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry["timestamp"].startswith(today):
                    activities.append(entry)
        
        return activities

# Convenience functions
logger = ActivityLogger()

def log_trading(action, details=None, status="success"):
    return logger.log("trading", action, details, status)

def log_marketing(action, details=None, status="success"):
    return logger.log("marketing", action, details, status)

def log_research(action, details=None, status="success"):
    return logger.log("research", action, details, status)

def log_automation(action, details=None, status="success"):
    return logger.log("automation", action, details, status)

def log_decision(action, details=None, status="success"):
    return logger.log("decision", action, details, status)

if __name__ == "__main__":
    # Test
    log_trading("Price update", {"TAO": 165.67, "SOL": 87.05, "P&L": -543})
    log_automation("Signal scraper", {"new_signals": 0})
    print("✅ Activity logged")
    print(f"📊 Stats: {logger.get_stats()}")
