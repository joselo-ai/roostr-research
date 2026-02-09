#!/usr/bin/env python3
"""
Integrate activity logging into existing automation scripts
Updates price_updater.py, signal_scraper.py, daily_summary.py
"""

import os
from pathlib import Path

# Add logging imports to each script
LOGGING_IMPORT = """
# Activity logging
import sys
sys.path.append('/Users/agentjoselo/.openclaw/workspace/command-center')
from activity_logger import log_trading, log_automation
"""

def integrate_price_updater():
    """Add logging to price updater"""
    file_path = Path("/Users/agentjoselo/.openclaw/workspace/trading/apps/price_updater.py")
    
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return
    
    content = file_path.read_text()
    
    # Check if already integrated
    if "activity_logger" in content:
        print("✅ price_updater.py already integrated")
        return
    
    # Add import at top (after existing imports)
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_pos = i + 1
    
    lines.insert(insert_pos, LOGGING_IMPORT)
    
    # Find where dashboard is updated and add logging
    for i, line in enumerate(lines):
        if 'Dashboard updated:' in line or 'print(' in line and 'Dashboard' in line:
            # Insert logging after the print
            log_line = f"""    log_trading("Price update", {{"TAO": tao_price, "SOL": sol_price, "P&L": total_pnl}})"""
            lines.insert(i + 1, log_line)
            break
    
    file_path.write_text('\n'.join(lines))
    print("✅ price_updater.py integrated")

def integrate_signal_scraper():
    """Add logging to signal scraper"""
    file_path = Path("/Users/agentjoselo/.openclaw/workspace/trading/apps/signal_scraper.py")
    
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return
    
    content = file_path.read_text()
    
    if "activity_logger" in content:
        print("✅ signal_scraper.py already integrated")
        return
    
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_pos = i + 1
    
    lines.insert(insert_pos, LOGGING_IMPORT)
    
    # Add logging at end of scrape
    for i, line in enumerate(lines):
        if 'Report saved' in line or 'new signals' in line.lower():
            log_line = f"""    log_automation("Signal scraper", {{"new_signals": len(new_signals) if 'new_signals' in locals() else 0}})"""
            lines.insert(i + 1, log_line)
            break
    
    file_path.write_text('\n'.join(lines))
    print("✅ signal_scraper.py integrated")

def integrate_daily_summary():
    """Add logging to daily summary"""
    file_path = Path("/Users/agentjoselo/.openclaw/workspace/trading/apps/daily_summary.py")
    
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return
    
    content = file_path.read_text()
    
    if "activity_logger" in content:
        print("✅ daily_summary.py already integrated")
        return
    
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_pos = i + 1
    
    lines.insert(insert_pos, LOGGING_IMPORT)
    
    # Add logging after summary generation
    for i, line in enumerate(lines):
        if 'Summary generated' in line:
            log_line = f"""    log_automation("Daily summary", {{"P&L": total_pnl if 'total_pnl' in locals() else 0}})"""
            lines.insert(i + 1, log_line)
            break
    
    file_path.write_text('\n'.join(lines))
    print("✅ daily_summary.py integrated")

if __name__ == "__main__":
    print("🐓 Integrating activity logging into automation scripts...\n")
    integrate_price_updater()
    integrate_signal_scraper()
    integrate_daily_summary()
    print("\n✅ Integration complete!")
    print("\n📊 Command Center: /Users/agentjoselo/.openclaw/workspace/command-center/dashboard.html")
