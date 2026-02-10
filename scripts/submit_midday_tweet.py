#!/usr/bin/env python3
"""
Submit midday tweet task to Smooth.sh (fast submission, check result manually)
"""

import sys
import json
import requests
from pathlib import Path

# Load API key
key_file = Path("/Users/agentjoselo/.openclaw/workspace/.smooth-api-key")
with open(key_file) as f:
    api_key = f.read().strip()

# Tweet content from w2-6
tweet_content = """How we validate signals:

1️⃣ Social: Dumb Money Discord reactions (18+ = strong)
2️⃣ Fundamental: Screener (P/E, ROE, debt)
3️⃣ Technical: Chart structure + volume
4️⃣ Catalyst: Earnings, news, insider activity
5️⃣ Analyst: Consensus + recent upgrades

Multi-source or no trade."""

task = f"""Go to x.com and log in as @roostrcapital (if not already logged in).

Then compose a new tweet with this exact content:

{tweet_content}

Post the tweet.

After posting, copy the tweet URL from the browser address bar and report it."""

# Submit task
headers = {
    "apikey": api_key,
    "Content-Type": "application/json"
}

data = {"task": task}

print("🐓 Submitting midday tweet (w2-6) to Smooth.sh...")
print("="*60)
print(f"Content:\n{tweet_content}\n")
print("="*60)

response = requests.post(
    "https://api.smooth.sh/api/v1/task",
    headers=headers,
    json=data,
    timeout=30
)

response.raise_for_status()
result = response.json()

task_id = result["r"]["id"]

print(f"\n✅ Task submitted!")
print(f"   Task ID: {task_id}")
print(f"   Live URL: https://app.smooth.sh/live")
print(f"   Check Activity Log for progress")
print(f"\nTo get result:")
print(f"   curl -H 'apikey: {api_key[:20]}...' https://api.smooth.sh/api/v1/task/{task_id}")
