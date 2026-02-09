# 🐓 roostr Intelligence Feed

**AI-Powered Trading Signals — $99/mo**

---

## Product Overview

**What:** Subscription service delivering institutional-grade trading signals from our AI hedge fund

**Price:** $99/month (cancel anytime)

**Delivery:** 
- Telegram alerts (instant)
- Email reports (daily digest)
- Web dashboard (live access)

**Output:**
- 2-4 GREEN signals/month
- Full conviction docs (10-20 pages each)
- Entry/exit prices, stops, position sizing
- Real-time updates on active positions

---

## How It Works

### 1. Signal Generation (Automated)

**Our 3 AI Agents:**
- **Scout:** Scrapes 20+ data sources (Yieldschool, Dumb Money, Chart Fanatics, Reddit, Twitter)
- **Atlas:** Validates signals (multi-source confirmation, statistical tests)
- **Quant:** Backtests, calculates risk/reward, sizes positions

**Traffic Light System:**
- 🟢 **GREEN:** Deploy (multi-source validated, conviction doc written, approved)
- 🟡 **YELLOW:** Watch (needs more data, 7-day window)
- 🔴 **RED:** Avoid (no conviction, red flags, mainstream)

**Only GREEN signals are sent to subscribers.**

### 2. Conviction Documents

Every GREEN signal includes:

- **Thesis:** Why we're buying
- **Valuation:** P/E, DCF, comparables
- **Catalyst:** What triggers the move
- **Risk Analysis:** What could go wrong
- **Position Sizing:** How much to deploy
- **Stops:** Exact exit price
- **Timeline:** Expected holding period

**Format:** Markdown + PDF  
**Length:** 10-20 pages  
**Delivery:** Instant (when signal goes GREEN)

### 3. Delivery Channels

**Telegram (Primary):**
```
🟢 GREEN SIGNAL: ACGL (Arch Capital)
Conviction: 8.5/10
Entry: $100.95
Target: $115-120 (15-20%)
Stop: $98
Deploy: $12k (30% of value bucket)

Full doc: https://roostr.ai/signals/ACGL
```

**Email:**
- Morning digest (7 AM EST)
- Signal alerts (real-time)
- Weekly recap (Sundays)

**Web Dashboard:**
- Live signal feed
- Active positions tracker
- Historical performance
- Conviction docs library

---

## Tech Stack

### Frontend
- Landing page: `signal-feed/index.html` (static)
- Dashboard: `signal-feed/dashboard.html` (member area)

### Backend
- Subscription: Stripe (recurring billing)
- Auth: Firebase or Supabase
- Database: SQLite → PostgreSQL
- Alerts: Telegram Bot API

### Delivery Pipeline
1. Signal goes GREEN → Write to database
2. Generate conviction doc (Scribe agent)
3. Send Telegram alert (all subscribers)
4. Send email (with PDF attachment)
5. Update dashboard (real-time)

---

## Pricing Tiers (Future)

### Basic — $99/mo
- 2-4 signals/month
- Full conviction docs
- Telegram + Email alerts
- Dashboard access

### Pro — $299/mo
- Everything in Basic
- 6-8 signals/month (includes YELLOW + opportunistic)
- Priority access (signals 1hr early)
- Monthly research call

### Enterprise — $999/mo
- Everything in Pro
- Unlimited signals
- API access (integrate with your systems)
- White-label reports
- Dedicated Slack channel

---

## Customer Acquisition Strategy

### 1. Twitter (Primary)
- Share 1 FREE signal/week publicly
- "Want more? Subscribe for $99/mo"
- Thread breakdowns of past winners
- Live trading updates (transparency builds trust)

### 2. GitHub
- Public track record (all signals logged)
- Conviction docs samples
- "See more in Intelligence Feed"

### 3. Substack Newsletter
- Free tier: Weekly market commentary
- Paid tier: Full signal feed ($99/mo)

### 4. Affiliate Program
- 30% recurring commission
- Affiliates get unique link
- Track via Stripe referrals

### 5. Reddit/Discord
- Provide value first (free insights)
- Link to Intelligence Feed in bio
- No spam, pure education

---

## Roadmap

### Phase 1: MVP (Week 1-2)
- ✅ Landing page live
- ✅ Stripe integration
- ✅ Telegram bot setup
- ✅ First 10 subscribers

### Phase 2: Scale (Week 3-8)
- ✅ Email automation
- ✅ Dashboard v1
- ✅ 100 subscribers ($10k MRR)
- ✅ Affiliate program

### Phase 3: Expand (Month 3-6)
- ✅ Pro + Enterprise tiers
- ✅ API access
- ✅ 500 subscribers ($50k MRR)
- ✅ Partnerships (brokerages, platforms)

---

## Metrics to Track

**Subscriber Growth:**
- New signups/week
- Churn rate (target: <5%/mo)
- LTV (lifetime value)

**Signal Performance:**
- Win rate (target: >60%)
- Average return per signal
- Max drawdown

**Engagement:**
- Open rate (emails)
- Click rate (conviction docs)
- Time on dashboard

---

## Legal/Compliance

**Disclaimers:**
- Not financial advice
- Past performance ≠ future results
- Risk disclosure on every signal

**Terms:**
- No refunds after 7 days
- Can cancel anytime
- We reserve right to pause/close fund if performance drops

**Audit Trail:**
- Every signal timestamped
- Track record public (GitHub)
- Cannot retroactively change signals

---

## Competitive Advantages

**1. Transparency**
- Full track record public
- Wins AND losses visible
- Conviction docs = education

**2. AI-Native**
- 24/7 signal discovery
- Multi-source validation
- Zero emotional bias

**3. Skin in the Game**
- We trade every signal we send
- roostr fund performance = your performance
- No conflicts of interest

**4. Quality > Quantity**
- Only GREEN signals sent
- High conviction (7+/10)
- Would rather send nothing than send junk

---

## Getting Started

### For Customers:
1. Visit: https://roostr.ai/intelligence-feed (or localhost:8001 for now)
2. Click "Subscribe Now"
3. Enter payment info (Stripe)
4. Join Telegram channel (link in confirmation email)
5. Receive first signal within 7 days

### For Developers:
```bash
# Serve landing page locally
cd signal-feed
python3 -m http.server 8001

# Open in browser
open http://localhost:8001
```

---

## Support

**Questions:** support@roostr.ai  
**Twitter:** https://x.com/roostrcapital  
**GitHub:** https://github.com/joselo-ai/roostr-research

---

**Built by roostr Capital**  
**The First AI-Native Hedge Fund**

🐓
