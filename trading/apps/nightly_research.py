#!/usr/bin/env python3
"""
🐓 Nightly Research & Conviction Generator
Runs at 2 AM EST to prepare next day's deployment opportunities.

Mission: Move roostr Capital closer to autonomous 24/7 fund
Actions:
1. Scan global markets (US + international if available)
2. Generate top 10 opportunities
3. Run top 5 through 18-agent system
4. Create conviction documents
5. Prepare deployment plan
6. Alert G via Telegram/Discord with summary

Output: Next day's deployment candidates ready for market open
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

TRADING_DIR = Path(__file__).parent.parent
AGENTS_DIR = TRADING_DIR / "agents"
OPPORTUNITIES_FILE = TRADING_DIR / "nightly-opportunities.json"
DEPLOYMENT_PLAN_FILE = TRADING_DIR / "next-day-deployment-plan.md"

sys.path.insert(0, str(AGENTS_DIR))

def scan_markets():
    """Run both base and enhanced scanners"""
    print("🌍 Scanning global markets...")
    print("=" * 60)
    
    # Run base scanner
    print("\n1️⃣ Base scanner (value/growth/volume)...")
    result1 = subprocess.run(
        ["python3", "apps/daily_opportunity_scanner.py"],
        cwd=TRADING_DIR,
        capture_output=True,
        text=True
    )
    
    # Run enhanced scanner
    print("2️⃣ Enhanced scanner (earnings/insider/analyst/momentum)...")
    result2 = subprocess.run(
        ["python3", "apps/enhanced_scanner.py"],
        cwd=TRADING_DIR,
        capture_output=True,
        text=True
    )
    
    # Merge results
    opportunities = []
    
    try:
        with open(TRADING_DIR / "daily-opportunities.json", 'r') as f:
            base_data = json.load(f)
            opportunities.extend(base_data.get('top_10', []))
    except:
        pass
    
    try:
        with open(TRADING_DIR / "enhanced-opportunities.json", 'r') as f:
            enhanced_data = json.load(f)
            opportunities.extend(enhanced_data.get('top_15', []))
    except:
        pass
    
    # Deduplicate by ticker, keep highest score
    ticker_map = {}
    for opp in opportunities:
        ticker = opp['ticker']
        score = opp.get('score', 0) + opp.get('opportunity_score', 0)
        
        if ticker not in ticker_map or score > ticker_map[ticker].get('combined_score', 0):
            opp['combined_score'] = score
            ticker_map[ticker] = opp
    
    # Sort by score
    ranked = sorted(ticker_map.values(), key=lambda x: x['combined_score'], reverse=True)
    
    print(f"\n✅ Found {len(ranked)} unique opportunities")
    return ranked[:10]  # Top 10

def evaluate_with_agents(opportunities):
    """Run top 5 through 18-agent system"""
    print("\n🤖 Evaluating top 5 with 18-agent system...")
    print("=" * 60)
    
    evaluations = []
    
    for i, opp in enumerate(opportunities[:5], 1):
        ticker = opp['ticker']
        price = opp.get('price', 0)
        catalyst = opp.get('catalyst', 'Market opportunity')
        
        print(f"\n{i}/5: Analyzing {ticker}...")
        
        cmd = [
            "python3", "agents/run_18_agents.py",
            "--ticker", ticker,
            "--price", str(price),
            "--catalyst", catalyst
        ]
        
        result = subprocess.run(
            cmd,
            cwd=TRADING_DIR,
            capture_output=True,
            text=True
        )
        
        # Parse conviction
        conviction = 0.0
        decision = "HOLD"
        
        for line in result.stdout.split('\n'):
            if "Final Conviction:" in line:
                try:
                    conviction = float(line.split(':')[1].split('/')[0].strip())
                except:
                    pass
            if "FINAL DECISION:" in line:
                decision = line.split(':')[1].strip()
        
        evaluations.append({
            'ticker': ticker,
            'price': price,
            'catalyst': catalyst,
            'conviction': conviction,
            'decision': decision,
            'source': opp.get('source', 'unknown')
        })
        
        print(f"   → {ticker}: {conviction}/10 ({decision})")
    
    # Sort by conviction
    evaluations.sort(key=lambda x: x['conviction'], reverse=True)
    
    return evaluations

def generate_deployment_plan(evaluations):
    """Create next-day deployment plan"""
    print("\n📋 Generating deployment plan...")
    
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    
    plan = f"""# 🐓 roostr Capital - Deployment Plan
**Generated:** {now.strftime('%Y-%m-%d %I:%M %p %Z')}  
**For Market Open:** {tomorrow.strftime('%A, %B %d, %Y')} @ 9:30 AM EST

---

## Mission Statement
**"Autonomous AI hedge fund that compounds capital 24/7 through systematic, disciplined, transparent execution."**

---

## Top 5 Opportunities (Agent-Evaluated)

"""
    
    for i, ev in enumerate(evaluations, 1):
        tier = "🟢 HIGH" if ev['conviction'] >= 8.0 else "🟡 MEDIUM" if ev['conviction'] >= 6.0 else "🟠 LOW-MEDIUM" if ev['conviction'] >= 5.0 else "🔴 SKIP"
        
        plan += f"""
### {i}. ${ev['ticker']} - {tier}
- **Conviction:** {ev['conviction']}/10
- **Decision:** {ev['decision']}
- **Price:** ${ev['price']:.2f}
- **Catalyst:** {ev['catalyst']}
- **Source:** {ev['source']}
"""
        
        if ev['conviction'] >= 5.0:
            size = 20000 if ev['conviction'] >= 8.0 else 10000 if ev['conviction'] >= 6.0 else 5000
            stop_pct = 15 if ev['conviction'] >= 8.0 else 10 if ev['conviction'] >= 6.0 else 8
            stop_price = ev['price'] * (1 - stop_pct / 100)
            
            plan += f"""- **Recommended Size:** ${size:,}
- **Stop Loss:** ${stop_price:.2f} (-{stop_pct}%)
"""
    
    # Deployment recommendation
    deployable = [e for e in evaluations if e['conviction'] >= 5.0]
    
    plan += f"""

---

## Deployment Recommendation

"""
    
    if deployable:
        best = deployable[0]
        plan += f"""**Deploy:** ${best['ticker']} @ ${best['price']:.2f}  
**Conviction:** {best['conviction']}/10  
**Rationale:** Highest conviction from overnight research

**Alternative:** Review all {len(deployable)} deployable candidates and pick manually
"""
    else:
        plan += """**No deployable opportunities found (all <5.0 conviction)**

Action: Wait for market open, re-scan at 9:00 AM
"""
    
    plan += f"""

---

## Next Steps

1. **9:00 AM:** Review this plan
2. **9:15 AM:** Check pre-market price action
3. **9:30 AM:** Execute deployment (auto or manual)
4. **9:35 AM:** Confirm position logged to dashboard

---

**Generated by:** 🐓 Joselo (Nightly Research Agent)  
**Conviction Docs:** `conviction-docs/` (full 18-agent deliberations)
"""
    
    # Save to file
    with open(DEPLOYMENT_PLAN_FILE, 'w') as f:
        f.write(plan)
    
    print(f"✅ Plan saved to: {DEPLOYMENT_PLAN_FILE}")
    
    return plan, deployable

def send_telegram_alert(plan_summary, deployable_count):
    """Send summary to Telegram"""
    print("\n📱 Sending Telegram alert...")
    
    message = f"""🐓 **roostr Nightly Research Complete**

🌍 Scanned global markets
🤖 18 agents evaluated top 5 opportunities

**Deployable:** {deployable_count} position(s) ready
**Plan:** `trading/next-day-deployment-plan.md`

Wake up and review! Market opens in ~7.5 hours.

Good night. 🌙"""
    
    # Use OpenClaw message tool (Telegram)
    # This will be called via cron, no direct access to message tool
    # So we'll write to a file that cron can read and send
    
    alert_file = TRADING_DIR / "nightly-telegram-alert.txt"
    with open(alert_file, 'w') as f:
        f.write(message)
    
    print(f"✅ Alert saved for cron delivery: {alert_file}")

def main():
    print("🐓 Nightly Research & Conviction Generator")
    print("=" * 60)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %I:%M %p %Z')}")
    print()
    print("Mission: Prepare tomorrow's deployment opportunities")
    print("=" * 60)
    
    # Step 1: Scan markets
    opportunities = scan_markets()
    
    # Step 2: Evaluate with agents
    evaluations = evaluate_with_agents(opportunities)
    
    # Step 3: Generate deployment plan
    plan, deployable = generate_deployment_plan(evaluations)
    
    # Step 4: Send alert
    send_telegram_alert(plan, len(deployable))
    
    print("\n" + "=" * 60)
    print("✅ Nightly research complete")
    print("=" * 60)
    print(f"\n📊 Results:")
    print(f"   - Scanned: {len(opportunities)} opportunities")
    print(f"   - Evaluated: 5 with 18-agent system")
    print(f"   - Deployable: {len(deployable)} positions")
    print(f"\n📋 Plan: {DEPLOYMENT_PLAN_FILE}")
    print(f"📱 Alert: Ready for Telegram delivery")
    print(f"\n💤 Sleep well. Tomorrow's trades are ready.")

if __name__ == "__main__":
    main()
