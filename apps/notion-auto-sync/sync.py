#!/usr/bin/env python3
"""
Notion Auto-Sync - Push trading signals, positions, and performance to Notion
Updates Control Tower automatically after every trade
"""

import json
import requests
from datetime import datetime
from typing import List, Dict, Any
import os

class NotionSync:
    """Sync trading data to Notion Control Tower"""
    
    def __init__(self):
        self.api_key = self._load_api_key()
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Page IDs (from MEMORY.md)
        self.control_tower_page_id = "2fe1df668e2c807e97f1edc151c5d6eb"
        self.test_page_id = "2fe1df668e2c80d8bfd4dfb29fce8004"
        
    def _load_api_key(self) -> str:
        """Load Notion API key from config"""
        api_key_file = os.path.expanduser("~/.config/notion/api_key")
        
        try:
            with open(api_key_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"ERROR: {api_key_file} not found")
            print("Creating from MEMORY.md credential...")
            
            # Create from known credential
            os.makedirs(os.path.dirname(api_key_file), exist_ok=True)
            api_key = "ntn_O8043007532UbzvdIxiywfFY2gUkQcRy7cVkQOqNPIPgJm"
            
            with open(api_key_file, 'w') as f:
                f.write(api_key)
            
            return api_key
    
    def create_signal_database(self, parent_page_id: str) -> str:
        """Create Signals database in Notion"""
        
        url = f"{self.base_url}/databases"
        
        payload = {
            "parent": {"page_id": parent_page_id},
            "title": [{"text": {"content": "🎯 Signal Pipeline"}}],
            "properties": {
                "Ticker": {"title": {}},
                "Status": {
                    "select": {
                        "options": [
                            {"name": "🟢 GREEN", "color": "green"},
                            {"name": "🟡 YELLOW", "color": "yellow"},
                            {"name": "🔴 RED", "color": "red"}
                        ]
                    }
                },
                "Source": {"select": {
                    "options": [
                        {"name": "Yieldschool", "color": "blue"},
                        {"name": "DumbMoney", "color": "purple"},
                        {"name": "Chart Fanatics", "color": "orange"}
                    ]
                }},
                "Conviction": {"number": {"format": "number"}},
                "Date Found": {"date": {}},
                "Deployed": {"checkbox": {}},
                "Entry Price": {"number": {"format": "dollar"}},
                "Position Size": {"number": {"format": "dollar"}},
                "P&L": {"number": {"format": "dollar"}},
                "Notes": {"rich_text": {}}
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            db_id = response.json()['id']
            print(f"✅ Created Signal Pipeline database: {db_id}")
            return db_id
        else:
            print(f"❌ Failed to create database: {response.status_code}")
            print(response.text)
            return None
    
    def create_position_database(self, parent_page_id: str) -> str:
        """Create Open Positions database"""
        
        url = f"{self.base_url}/databases"
        
        payload = {
            "parent": {"page_id": parent_page_id},
            "title": [{"text": {"content": "📊 Open Positions"}}],
            "properties": {
                "Ticker": {"title": {}},
                "Bucket": {
                    "select": {
                        "options": [
                            {"name": "Riz EURUSD", "color": "green"},
                            {"name": "Social Arb", "color": "purple"},
                            {"name": "Crypto", "color": "blue"},
                            {"name": "Opportunistic", "color": "orange"}
                        ]
                    }
                },
                "Entry Date": {"date": {}},
                "Entry Price": {"number": {"format": "dollar"}},
                "Current Price": {"number": {"format": "dollar"}},
                "Position Size": {"number": {"format": "dollar"}},
                "Stop Loss": {"number": {"format": "dollar"}},
                "Target": {"number": {"format": "dollar"}},
                "P&L $": {"number": {"format": "dollar"}},
                "P&L %": {"number": {"format": "percent"}},
                "Risk %": {"number": {"format": "percent"}},
                "Days Held": {"number": {}},
                "Thesis": {"rich_text": {}}
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            db_id = response.json()['id']
            print(f"✅ Created Open Positions database: {db_id}")
            return db_id
        else:
            print(f"❌ Failed to create database: {response.status_code}")
            return None
    
    def add_signal(self, database_id: str, signal: Dict[str, Any]) -> bool:
        """Add signal to Notion database"""
        
        url = f"{self.base_url}/pages"
        
        # Map status
        status_map = {
            'GREEN': '🟢 GREEN',
            'YELLOW': '🟡 YELLOW',
            'RED': '🔴 RED'
        }
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Ticker": {
                    "title": [{"text": {"content": signal.get('ticker', 'UNKNOWN')}}]
                },
                "Status": {
                    "select": {"name": status_map.get(signal.get('status', 'YELLOW'), '🟡 YELLOW')}
                },
                "Source": {
                    "select": {"name": signal.get('source', 'Unknown')}
                },
                "Conviction": {
                    "number": signal.get('conviction_score', 5)
                },
                "Date Found": {
                    "date": {"start": signal.get('date_found', datetime.now().strftime('%Y-%m-%d'))}
                },
                "Deployed": {
                    "checkbox": signal.get('deployed', False)
                },
                "Notes": {
                    "rich_text": [{"text": {"content": signal.get('notes', '')[:2000]}}]
                }
            }
        }
        
        # Add optional fields
        if signal.get('entry_price'):
            payload['properties']['Entry Price'] = {"number": float(signal['entry_price'])}
        
        if signal.get('position_size'):
            payload['properties']['Position Size'] = {"number": float(signal['position_size'])}
        
        if signal.get('pnl_dollars'):
            payload['properties']['P&L'] = {"number": float(signal['pnl_dollars'])}
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Added {signal.get('ticker')} to Notion")
            return True
        else:
            print(f"❌ Failed to add signal: {response.status_code}")
            print(response.text)
            return False
    
    def update_performance_block(self, page_id: str, metrics: Dict[str, Any]):
        """Update performance metrics block in Notion page"""
        
        # Append new content block with today's performance
        url = f"{self.base_url}/blocks/{page_id}/children"
        
        pnl_emoji = '📈' if metrics.get('total_pnl', 0) >= 0 else '📉'
        pnl_sign = '+' if metrics.get('total_pnl', 0) >= 0 else ''
        
        content = f"""
## 📊 Performance Update - {datetime.now().strftime('%b %d, %Y')}

**Capital Deployed:** ${metrics.get('total_deployed', 0):,.0f} / $100,000 ({metrics.get('total_deployed', 0)/1000:.0f}%)

**Net P&L:** {pnl_emoji} {pnl_sign}${abs(metrics.get('total_pnl', 0)):,.0f} ({pnl_sign}{metrics.get('pnl_percent', 0):.1f}%)

**Open Positions:** {metrics.get('open_positions', 0)}

**Buckets:**
- 🟢 Riz EURUSD: ${metrics.get('buckets', {}).get('Riz_EURUSD', {}).get('deployed', 0):,.0f}
- 🟣 Social Arb: ${metrics.get('buckets', {}).get('Social_Arb', {}).get('deployed', 0):,.0f}
- 🔵 Crypto: ${metrics.get('buckets', {}).get('Crypto', {}).get('deployed', 0):,.0f}
- 🟠 Opportunistic: ${metrics.get('buckets', {}).get('Opportunistic', {}).get('deployed', 0):,.0f}

---
"""
        
        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }
            ]
        }
        
        response = requests.patch(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Updated performance metrics in Notion")
            return True
        else:
            print(f"❌ Failed to update metrics: {response.status_code}")
            return False
    
    def sync_from_csv(self, csv_path: str, database_id: str):
        """Sync signals from CSV to Notion database"""
        import csv
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            count = 0
            for row in reader:
                if not row.get('Ticker'):
                    continue
                
                signal = {
                    'ticker': row['Ticker'],
                    'source': row['Source'],
                    'date_found': row['Date_Found'],
                    'conviction_score': int(row.get('Conviction_Score', 5)),
                    'status': row.get('Status', 'YELLOW'),
                    'deployed': row.get('Deployed', 'NO') == 'YES',
                    'entry_price': row.get('Price_Entry'),
                    'position_size': row.get('Position_Size'),
                    'pnl_dollars': row.get('PnL_Dollars'),
                    'notes': row.get('Notes', '')
                }
                
                if self.add_signal(database_id, signal):
                    count += 1
        
        print(f"\n✅ Synced {count} signals to Notion")


# Standalone functions for easy integration

def setup_notion_databases():
    """One-time setup: Create databases in Notion"""
    sync = NotionSync()
    
    print("Creating Notion databases...")
    print(f"Using page: {sync.test_page_id}")
    
    # Create databases
    signal_db = sync.create_signal_database(sync.test_page_id)
    position_db = sync.create_position_database(sync.test_page_id)
    
    # Save database IDs
    config = {
        'signal_database_id': signal_db,
        'position_database_id': position_db,
        'created': datetime.now().isoformat()
    }
    
    with open('notion_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Setup complete. Database IDs saved to notion_config.json")
    print(f"\nView in Notion: https://www.notion.so/{sync.test_page_id}")


def sync_signals():
    """Sync signals from CSV to Notion (run after scraping)"""
    sync = NotionSync()
    
    # Load database ID
    try:
        with open('notion_config.json', 'r') as f:
            config = json.load(f)
            db_id = config['signal_database_id']
    except FileNotFoundError:
        print("ERROR: Run setup_notion_databases() first")
        return
    
    # Sync from CSV
    csv_path = '../../trading/signals-database.csv'
    sync.sync_from_csv(csv_path, db_id)


def update_performance():
    """Update performance metrics in Notion (run after dashboard update)"""
    sync = NotionSync()
    
    # Load metrics from dashboard updater
    # (Placeholder - would import from update_dashboard.py)
    
    metrics = {
        'total_deployed': 0,
        'total_pnl': 0,
        'pnl_percent': 0,
        'open_positions': 0,
        'buckets': {}
    }
    
    sync.update_performance_block(sync.test_page_id, metrics)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 sync.py setup    # One-time database creation")
        print("  python3 sync.py signals  # Sync signals from CSV")
        print("  python3 sync.py perf     # Update performance metrics")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_notion_databases()
    elif command == "signals":
        sync_signals()
    elif command == "perf":
        update_performance()
    else:
        print(f"Unknown command: {command}")
