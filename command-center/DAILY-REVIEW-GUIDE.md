# 🐓 Command Center — Daily Review Guide

**Purpose:** Track progress, celebrate wins, identify opportunities

**Time:** 5-10 minutes/day (morning or evening)

**URL:** http://localhost:8001/dashboard.html

---

## Daily Review Routine

### 1. **Today's Scorecard** (Top Section)

**What to Check:**
- Portfolio P&L (current positions)
- Actions completed today
- Signals generated this week

**Questions to Ask:**
- Are we profitable?
- Did we execute on priorities?
- Are new signals emerging?

**Actions:**
- If P&L negative but positions healthy → let ride
- If actions < 5 → identify why (blocked? stuck? need help?)
- If new signals → review conviction, decide deploy/wait

---

### 2. **Live Positions** (Crypto Ticker)

**What to Check:**
- Current prices (NANO, BAN, TAO, SOL)
- 24h price changes
- Position health vs stops

**Questions to Ask:**
- Are we near stops?
- Are positions moving as expected?
- Do we need to adjust?

**Actions:**
- Near stop (< 5%) → prepare exit plan
- Big moves (> 10%) → review thesis, decide hold/take profit
- Stagnant (< 2% move) → patience, let thesis play out

---

### 3. **Today's Achievements** (Wins)

**What to Check:**
- What got done today
- Quality of work (not just quantity)
- Momentum vs yesterday

**Questions to Ask:**
- What are we proud of?
- What moved the needle?
- Are we making progress?

**Actions:**
- Celebrate wins (even small ones)
- Identify patterns (what makes us productive?)
- Share wins publicly (Twitter, GitHub)

---

### 4. **Active Opportunities** (Next Moves)

**What to Check:**
- HIGH priority items (must do this week)
- MEDIUM priority (should do soon)
- LOW priority (when we have time)

**Questions to Ask:**
- What's blocking HIGH items?
- Can we knock out any quick wins?
- What should we delegate/automate?

**Actions:**
- Pick 1-3 HIGH priority items for tomorrow
- Unblock anything stuck
- Kill/defer low-value work

---

### 5. **Progress Toward Goals** (90-Day Targets)

**What to Check:**
- Portfolio performance (% toward $120k)
- Data sources (% toward 20+)
- AI agent team (% complete)
- Revenue (signal feed MRR)
- Team growth (advisors recruited)

**Questions to Ask:**
- Are we on track?
- What's ahead of schedule?
- What's lagging?

**Actions:**
- Celebrate milestones (each 10% progress)
- Course-correct if behind (what needs to change?)
- Double down on what's working

---

### 6. **Activity Feed** (Bottom Section)

**What to Check:**
- All actions logged today
- Categories (trading, marketing, research, automation, decisions)
- Full audit trail

**Questions to Ask:**
- Are we balanced across categories?
- Too much automation, not enough trading?
- Are we documenting decisions?

**Actions:**
- Filter by category to deep dive
- Review "Today Only" for daily recap
- Ensure all major actions are logged

---

## Daily Review Template (5-Min Version)

**Copy this into your daily notes:**

```
# roostr Daily Review — [DATE]

## Scorecard
- P&L: [$ / %]
- Actions: [count]
- Signals: [count]

## Wins Today
1. [Achievement 1]
2. [Achievement 2]
3. [Achievement 3]

## Top Opportunities
- HIGH: [What must happen this week]
- MEDIUM: [What should happen soon]

## Tomorrow's Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Blockers / Needs
- [Anything stuck or needs help]

## Notes
- [Key insights, decisions, or observations]
```

---

## Weekly Review (Sundays)

**In addition to daily:**

1. **Week-over-week comparison**
   - Portfolio performance (vs last Sunday)
   - Total actions (vs last week)
   - Signals generated (count + quality)

2. **Goal progress review**
   - Update all 5 progress bars
   - Adjust targets if needed
   - Celebrate milestones

3. **Opportunities pipeline**
   - Review all HIGH/MEDIUM items
   - Kill anything no longer relevant
   - Add new opportunities discovered

4. **Team reflection**
   - What did AI agents accomplish?
   - What did humans accomplish?
   - What needs to improve?

5. **Next week planning**
   - Set 3-5 HIGH priority goals
   - Block time for deep work
   - Schedule any calls/meetings

---

## Monthly Review (1st of Month)

**Deep dive:**

1. **Performance analysis**
   - Portfolio returns (vs S&P, vs target)
   - Win rate, Sharpe ratio, max drawdown
   - Best/worst trades (lessons learned)

2. **Systems audit**
   - What's working? (keep doing)
   - What's broken? (fix or kill)
   - What's missing? (build or buy)

3. **Goal reset**
   - Adjust 90-day targets based on reality
   - Add new goals if needed
   - Remove goals that don't matter

4. **Strategic decisions**
   - Deploy more capital?
   - Raise money?
   - Hire advisors/team?
   - Launch new products?

---

## Key Metrics to Track

### Trading Performance
- Total return (%)
- Win rate (%)
- Average gain per winner
- Average loss per loser
- Sharpe ratio
- Max drawdown

### Operations
- Actions/day (avg)
- Signals generated/week
- Data sources active
- AI agents operational

### Growth
- Revenue (signal feed MRR)
- Subscribers (count)
- Twitter followers
- GitHub stars

### Team
- Advisors recruited
- Hours saved by automation
- Response time to signals

---

## Red Flags to Watch

**Portfolio:**
- Drawdown > 15%
- 3+ losing trades in a row
- Position size > 25% of portfolio

**Operations:**
- Actions/day < 3 (low productivity)
- No signals for 7+ days (sources broken?)
- AI agents failing silently

**Growth:**
- Zero revenue after 30 days
- No new followers/subscribers
- No advisor responses

**Team:**
- Working alone for 60+ days
- Burnout signals (low energy, skipping reviews)
- Decision paralysis (too many options)

---

## Best Practices

**Do:**
- Review at same time daily (build habit)
- Celebrate small wins
- Log everything (memory is fallible)
- Share progress publicly
- Ask for help when stuck

**Don't:**
- Skip reviews (consistency > perfection)
- Focus only on wins (acknowledge losses)
- Hoard information (transparency builds trust)
- Work without breaks (rest = productivity)
- Compare to others (run your own race)

---

## Integration with Workflow

**Morning Routine:**
1. Open Command Center
2. Check overnight price action
3. Review yesterday's achievements
4. Set today's 3 priorities
5. Execute

**Evening Routine:**
1. Open Command Center
2. Review today's scorecard
3. Log any missing activities
4. Update opportunities (remove done, add new)
5. Set tomorrow's priorities

---

## Customization

**You can edit:**
- Opportunity cards (add/remove as needed)
- Goal targets (adjust based on reality)
- Priority labels (HIGH/MEDIUM/LOW)

**To update dashboard:**
```bash
# Edit the HTML
nano /Users/agentjoselo/.openclaw/workspace/command-center/dashboard.html

# Refresh browser
# Changes appear instantly (no rebuild needed)
```

---

## Support

**Questions:**
- "Joselo, update Command Center with [request]"
- "Joselo, add [metric] to daily scorecard"

**Troubleshooting:**
- Dashboard not loading? Check server: `python3 server.py`
- Data not updating? Check activity logger: `python3 activity_logger.py`
- Prices stale? CoinGecko API may be rate-limited (auto-retries)

---

**Built for daily collaboration between G and Joselo.**

**The Command Center is our shared reality.**

**What gets measured gets managed.**

🐓
