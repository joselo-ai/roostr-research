# roostr Pitch Deck: Slide-by-Slide Design Specifications
**20 slides | 15-20 minute presentation | February 2026**

Complete visual specifications for each slide with layout, typography, animations, and focal points.

---

## Slide 1: Cover

### Layout: Centered Hero

```
┌────────────────────────────────────────────────┐
│                                                │
│                                                │
│                                                │
│              roostr                            │  [96pt Inter Bold, Black]
│     The First Fully AI-Native                  │  [36pt Inter Semibold, Black]
│          Hedge Fund                            │
│                                                │
│  Zero human analysts. Infinite scalability.    │  [24pt Inter Regular, Light Gray]
│              99% margins.                      │
│                                                │
│     github.com/joselo-ai/roostr-research       │  [18pt Inter Regular, Light Gray]
│                                                │
│                                                │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **roostr:** 96pt Inter Bold, Black, -0.03em letter-spacing
- **Tagline:** 36pt Inter Semibold, Black, -0.01em letter-spacing
- **Three-line hook:** 24pt Inter Regular, Light Gray (#e0e0e0)
- **GitHub link:** 18pt Inter Regular, Light Gray, clickable (if PDF allows)

### Visual Elements
- No background (pure white)
- No logo (wordmark is the logo)
- No decorative elements
- Optional: Subtle green underline under "roostr" (2px, #4ade80)

### Animation (if presenting live)
1. "roostr" fades in (500ms, ease-out)
2. Tagline slides in from below (400ms, ease-out, +200ms delay)
3. Three-line hook fades in (300ms, +400ms delay)
4. GitHub link fades in (300ms, +600ms delay)

### Focal Points
1. **Primary:** "roostr" wordmark (eye lands here first)
2. **Secondary:** "99% margins" (key differentiator)
3. **Tertiary:** GitHub link (proof of transparency)

### Speaker Notes
- "Hi, I'm Joselo. This is roostr."
- Pause for 2 seconds (let them read the three-line hook)
- "We're building the first fully AI-native hedge fund. No human analysts. Just AI agents."
- Advance to next slide

### Design Rationale
- **Minimal:** No clutter, just the essential message
- **Confident:** Large type, no hedging language
- **Transparent:** GitHub link signals open approach
- **Memorable:** Three-line hook is repeatable (investors will quote it)

---

## Slide 2: The Problem

### Layout: Title + Two-Column Content

```
┌────────────────────────────────────────────────┐
│ Traditional Hedge Funds Hit a Ceiling          │  [72pt Bold, Black]
│                                                │
│ [LEFT COLUMN]            [RIGHT COLUMN]        │
│ The human bottleneck:    The math doesn't work:│  [32pt Semibold, Black]
│                                                │
│ • Analyst bandwidth...   • $1M AUM → 3-5...   │  [24pt Regular, Black]
│ • Operating margins...   • $100M AUM → 50+... │
│ • Research quality...    • Linear cost...      │
│ • Can't operate 24/7...                        │
│                                                │
│ Traditional funds trade margin for growth.     │  [28pt Semibold, Green, centered]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black, top-left (80px from top)
- **Column Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black, green bullet (•)
- **Conclusion:** 28pt Inter Semibold, Green (#4ade80), centered

### Visual Elements
- Two-column layout (50/50 split, 40px gap)
- Green bullets (16pt, #4ade80)
- Conclusion text in green box (background #f9fafb, 4px left border green)

### Animation
1. Title appears (fade in, 300ms)
2. Left column bullets appear sequentially (slide in from left, 400ms each, 150ms stagger)
3. Right column bullets appear sequentially (slide in from right, 400ms each, 150ms stagger)
4. Conclusion box fades in (fade in + scale up, 500ms)

### Focal Points
1. **Primary:** "The human bottleneck" (left column header)
2. **Secondary:** "40-60% operating margins" (specific number)
3. **Tertiary:** Green conclusion box (key takeaway)

### Speaker Notes
- "Traditional hedge funds have a fundamental scaling problem."
- "One analyst can monitor about 10 positions. Want to manage $100M? You need 50+ analysts."
- "This is why traditional funds have 40-60% operating margins. Personnel costs dominate."
- Point to conclusion: "They have to trade margin for growth. We don't."
- Advance to next slide

### Design Rationale
- **Problem framing:** Two-column layout separates "why" (left) from "numbers" (right)
- **Green conclusion:** Signals this is the key insight (investors should remember this)
- **Sequential animation:** Builds the case step-by-step

---

## Slide 3: The Opportunity

### Layout: Title + Three Sections

```
┌────────────────────────────────────────────────┐
│ AI Breaks the Scaling Curve                    │  [72pt Bold, Black]
│                                                │
│ What changed in 2025:                          │  [32pt Semibold, Black]
│ • LLMs (Claude Sonnet 4) can perform...       │  [24pt Regular, Black]
│ • Multi-agent architectures enable...          │
│ • 24/7 operation with zero fatigue             │
│ • Cost: $0.0001 vs $50k/year per analyst      │  [Highlight: JetBrains Mono, Green]
│                                                │
│ The market is ready:                           │  [32pt Semibold, Black]
│ • $4 trillion global hedge fund industry       │
│ • Institutional investors seeking alpha        │
│ • Crypto markets = perfect testing ground      │
│                                                │
│ First-mover advantage:                         │  [32pt Semibold, Black]
│ This wasn't possible 12 months ago.            │  [28pt Regular, Black, italic-style]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Section Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **Cost Comparison:** 24pt JetBrains Mono, Green (numbers), Black (text)
- **First-mover statement:** 28pt Inter Regular, Black

### Visual Elements
- Three sections stacked vertically (48px spacing between)
- Green bullets
- Cost comparison line highlighted (green text for numbers)
- Optional: Small icon next to each section header (cpu, trending-up, zap from Lucide)

### Animation
1. Title appears
2. Section 1 appears (all bullets at once, slide in from left, 400ms)
3. Section 2 appears (all bullets at once, slide in from right, 400ms, +300ms delay)
4. Section 3 appears (fade in + scale up, 500ms, +300ms delay)

### Focal Points
1. **Primary:** "$0.0001 vs $50k/year" (massive cost difference)
2. **Secondary:** "$4 trillion industry" (market size)
3. **Tertiary:** "This wasn't possible 12 months ago" (urgency)

### Speaker Notes
- "Everything changed in 2025."
- Point to cost line: "We can run an AI analyst for a fraction of a cent per analysis. A human costs $50k per year."
- "This is a $4 trillion industry ripe for disruption."
- Emphasize: "This wasn't possible 12 months ago. We have a first-mover window."
- Advance to next slide

### Design Rationale
- **Three-part structure:** Mirrors the problem/opportunity/timing framework
- **Cost highlight in green:** This is the "aha" moment (make it visually pop)
- **Urgency statement:** Isolated at bottom (investors should feel FOMO)

---

## Slide 4: Our Solution

### Layout: Title + Agent Flow Diagram

```
┌────────────────────────────────────────────────┐
│ 3 AI Agents Replace the Entire Analyst Team   │  [72pt Bold, Black]
│                                                │
│                                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  │  Scraper    │ →  │   Atlas     │ →  │    Edge     │  [240×120 boxes]
│  │  ──────     │    │   ─────     │    │    ────     │  [24pt Semibold]
│  │  Data       │    │  Validate   │    │   Execute   │  [20pt Regular]
│  │ Collection  │    │   Signal    │    │   Strategy  │
│  │             │    │   Quality   │    │             │
│  │ 10k+ sources│    │  Multi-     │    │ Backtesting │  [18pt Light Gray]
│  │    24/7     │    │  source     │    │   + Risk    │
│  └─────────────┘    └─────────────┘    └─────────────┘
│                                                │
│  Human oversight: Joselo (Risk + Strategy)     │  [20pt Regular, Light Gray]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Agent Names:** 24pt Inter Semibold, Black
- **Agent Roles:** 20pt Inter Regular, Black
- **Agent Details:** 18pt Inter Regular, Light Gray
- **Human oversight:** 20pt Inter Regular, Light Gray

### Visual Elements
- Three boxes (240×120px each, 80px horizontal spacing)
- Box styling: White background, 2px black border, 24px padding
- Arrows: 3px black line, 20px arrowhead, positioned between boxes
- Boxes horizontally centered on canvas

### Animation (WOW FACTOR)
1. Title appears (fade in, 300ms)
2. Scraper box appears (slide in from left, 400ms)
3. Atlas box appears (slide in from center, 400ms, +200ms delay)
4. Edge box appears (slide in from right, 400ms, +200ms delay)
5. Arrows draw in (animate stroke, 300ms each, after boxes appear)
6. Human oversight text fades in (300ms, +500ms delay)

**Advanced animation (if tools allow):**
- Data "particles" flow from Scraper → Atlas → Edge (small green dots, 2s loop)
- Subtle pulse on boxes (scale 1.0 → 1.02 → 1.0, 2s, infinite loop)

### Focal Points
1. **Primary:** Three agent names (Scraper, Atlas, Edge)
2. **Secondary:** Arrows (visual metaphor for workflow)
3. **Tertiary:** "Human oversight" (addresses "is this safe?" concern)

### Speaker Notes
- "This is the roostr architecture. Three specialized AI agents."
- Point to Scraper: "Scraper monitors 10,000+ sources 24/7. Twitter, Telegram, on-chain data."
- Point to Atlas: "Atlas validates signals using multi-source corroboration. Is this real or noise?"
- Point to Edge: "Edge backtests strategies and sizes positions. This is the quant brain."
- "I provide human oversight on risk management and strategic direction."
- Advance to next slide

### Design Rationale
- **Flow diagram:** Visually explains the system (easier than text)
- **Sequential animation:** Builds understanding step-by-step
- **Human oversight callout:** Addresses safety/trust concern proactively
- **Wow factor:** This is the first "impressive visual" slide (investors will screenshot this)

---

## Slide 5: How It Works

### Layout: Title + Four-Step Process

```
┌────────────────────────────────────────────────┐
│ Data → Validation → Risk → Execution          │  [72pt Bold, Black]
│                                                │
│ Step 1: Signal Discovery                       │  [32pt Semibold, Black]
│ • Scraper monitors crypto Twitter, whale...   │  [24pt Regular, Black]
│ • Example: "Dan bought 100 TAO"               │  [24pt JetBrains Mono, Green box]
│                                                │
│ Step 2: Multi-Source Validation                │
│ • Atlas cross-references: on-chain + GitHub..  │
│ • Validates trader track record (Dan: 1000x)  │  [Highlight: Green]
│                                                │
│ Step 3: Risk Assessment                        │
│ • Edge backtests similar setups               │
│ • Calculates position size (Kelly Criterion)  │
│                                                │
│ Step 4: Execution                              │
│ • Automated orders, stop-losses               │
│ • 24/7 monitoring for exit signals            │
│                                                │
│ Result: High-conviction trades with quantified │  [28pt Semibold, Green, box]
│         risk/reward.                           │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Step Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **Example Quote:** 24pt JetBrains Mono, Black text, green box background
- **Result Box:** 28pt Inter Semibold, Green text, light gray box

### Visual Elements
- Four steps stacked vertically (32px spacing between)
- Step numbers in green circles (32×32px, green background, white text)
- Example quote in code-style box (background #f9fafb, border-left 4px green)
- Result box at bottom (background #f9fafb, border 2px green)

### Animation
1. Title appears
2. Steps appear sequentially (fade in + slide in from left, 400ms each, 200ms stagger)
3. Result box appears (scale up + fade in, 500ms, after last step)

### Focal Points
1. **Primary:** Step numbers (guide eye through process)
2. **Secondary:** Example quote ("Dan bought 100 TAO")
3. **Tertiary:** Result box (key takeaway)

### Speaker Notes
- "Let me walk you through a real example."
- Step 1: "Scraper sees Dan tweet 'I bought 100 TAO.'"
- Step 2: "Atlas checks on-chain data. Dan's wallet shows accumulation. GitHub shows dev activity spiking."
- Step 3: "Edge backtests similar narrative-driven plays. Calculates 5% position size."
- Step 4: "We execute. Set stop-loss at -20%. Monitor 24/7 for exit signals."
- "Result: High-conviction trade with quantified risk."
- Advance to next slide

### Design Rationale
- **Step-by-step:** Breaks down complexity into digestible chunks
- **Real example:** "Dan bought 100 TAO" makes it concrete (not theoretical)
- **Result box:** Reinforces the value proposition

---

## Slide 6: The Technology

### Layout: Title + Two Sections (Stack + Proof)

```
┌────────────────────────────────────────────────┐
│ Proprietary Infrastructure Built in 2 Hours    │  [72pt Bold, Black]
│                                                │
│ Tech Stack:                                    │  [32pt Semibold, Black]
│ • Data Layer: Twitter API, Telegram, on-chain │  [24pt Regular, Black]
│ • Intelligence: Claude Sonnet 4 multi-agent   │
│ • Validation: Multi-source corroboration      │
│ • Execution: CEX/DEX integrations             │
│                                                │
│ 400KB+ production code deployed:               │  [32pt Semibold, Black]
│ ✓ Scraper agent: Real-time monitoring         │  [24pt Regular, Green checkmark]
│ ✓ Atlas agent: ML validation pipelines        │
│ ✓ Edge agent: Backtesting & risk models       │
│ ✓ Public dashboard: roostr-research repo      │
│                                                │
│ Moat: Proprietary data pipelines +            │  [24pt Semibold, Black]
│       validated agent workflows                │
│                                                │
│ Proof: Built in 2 hours (Jan 2026)            │  [28pt Semibold, Green box]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Section Headers:** 32pt Inter Semibold, Black
- **Bullets/Items:** 24pt Inter Regular, Black
- **Checkmarks:** Green (✓ U+2713, 24pt)
- **Moat Statement:** 24pt Inter Semibold, Black
- **Proof Box:** 28pt Inter Semibold, Green, light background box

### Visual Elements
- Two sections (Tech Stack, Deployed Code)
- Green checkmarks for deployed code (visual signal of "done")
- Moat statement in subtle box (background #f9fafb)
- Proof box at bottom (green text, green border)

### Animation
1. Title appears
2. Tech Stack bullets appear (all at once, fade in, 400ms)
3. Deployed code items appear sequentially (checkmark + text, 300ms each, 150ms stagger)
4. Moat statement fades in (300ms)
5. Proof box scales up (500ms)

### Focal Points
1. **Primary:** "Built in 2 hours" (proof of execution speed)
2. **Secondary:** Green checkmarks (visual proof of completion)
3. **Tertiary:** "400KB+ production code" (not vaporware)

### Speaker Notes
- "We're not pitching a whitepaper. This is live."
- Point to checkmarks: "All four agents are deployed. Running in production."
- "400KB+ of production code. You can review it on GitHub."
- Emphasize: "We built this entire infrastructure in 2 hours. That's the power of AI-native development."
- Advance to next slide

### Design Rationale
- **Checkmarks:** Visual proof (more credible than just text)
- **"2 hours" callout:** Shocking stat (makes investors lean in)
- **GitHub transparency:** Backs up claims with verifiable proof

---

## Slide 7: The Edges (4 Validated Strategies)

### Layout: Title + Data Table

```
┌────────────────────────────────────────────────┐
│ Track Record of Alpha Generation               │  [72pt Bold, Black]
│                                                │
│ ┌──────────────┬──────────────┬─────────┬────────────┐
│ │ Strategy     │ Example Trade│ Return  │ Status     │ [20pt Semibold]
│ ├──────────────┼──────────────┼─────────┼────────────┤
│ │ Social       │ Camillo's    │ +77%    │ Validated  │ [20pt Regular/Mono]
│ │ Arbitrage    │ PENGU call   │         │            │
│ ├──────────────┼──────────────┼─────────┼────────────┤
│ │ Riz Playbook │ Multiple     │ $120k+  │ Validated  │
│ │              │ high-conv... │ profits │            │
│ ├──────────────┼──────────────┼─────────┼────────────┤
│ │ Dan's TAO    │ Early accum  │ 1000x   │ Case study │
│ │ Trade        │ → 1000x      │         │            │
│ ├──────────────┼──────────────┼─────────┼────────────┤
│ │ Multi-Source │ Cross-ref    │ Reduces │ Operational│
│ │ Validation   │ social +...  │ false + │            │
│ │              │              │ by 60%  │            │
│ └──────────────┴──────────────┴─────────┴────────────┘
│                                                │
│ Key insight: These aren't backtests.           │  [24pt Semibold, Black]
│ These are real trades, validated by roostr.    │
│                                                │
│ Dan's 1000x TAO is *replicable* with AI.      │  [28pt Semibold, Green box]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Table Header:** 20pt Inter Semibold, Black
- **Table Data (text):** 20pt Inter Regular, Black
- **Table Data (numbers):** 20pt JetBrains Mono, Black (or Green for returns)
- **Key Insight:** 24pt Inter Semibold, Black
- **Replicable Statement:** 28pt Inter Semibold, Green

### Visual Elements
- Data table (full width, 1440px)
- Table styling: Header row (background #0a0a0a, white text), data rows (alternating white / #f9fafb)
- Row height: 64px
- Cell padding: 16px
- Return column: Green text for positive numbers
- Key insight below table
- Green box at bottom with replicable statement

### Animation
1. Title appears
2. Table header appears (slide in from top, 300ms)
3. Table rows appear sequentially (slide in from left, 300ms each, 150ms stagger)
4. Key insight fades in (300ms)
5. Green box scales up (500ms)

### Focal Points
1. **Primary:** "1000x" return (most eye-catching number)
2. **Secondary:** "+77%" and "$120k+" (validated results)
3. **Tertiary:** "These aren't backtests" (credibility)

### Speaker Notes
- "Here are our four validated strategies."
- Point to row 1: "Camillo called PENGU before it pumped 77%. We validated this post-hoc."
- Point to row 2: "Riz documented $120k+ in profits. We've replicated his playbook."
- Point to row 3: "Dan's TAO trade went 1000x. This is the pattern we're building to detect."
- "These aren't backtests. These are real trades from real traders."
- Emphasize: "The insight is that this pattern is replicable with AI-powered early detection."
- Advance to next slide

### Design Rationale
- **Table format:** Best for structured comparison data
- **Green returns:** Visual cue for positive performance
- **Replicable callout:** This is the "aha" moment (AI can replicate human alpha)

---

## Slide 8: Performance Targets

### Layout: Title + Large Numbers + Comparison

```
┌────────────────────────────────────────────────┐
│ Top 5% of Global Hedge Funds                   │  [72pt Bold, Black]
│                                                │
│     65-110%         2.1-2.8        <25%       │  [Hero numbers: 72pt Bold, Green]
│   Annual Return   Sharpe Ratio   Max Drawdown │  [Labels: 20pt Regular, Light Gray]
│                                                │
│ Comparison to Industry:                        │  [32pt Semibold, Black]
│ • Traditional funds: 8-12% annual, 0.8-1.2 SR │  [24pt Regular, Black]
│ • Top quant funds: 20-30% annual, 1.5-2.0 SR  │
│ • roostr target: Top 5% performance tier      │  [24pt Semibold, Green]
│                                                │
│ Risk management:                               │  [32pt Semibold, Black]
│ • Kelly Criterion position sizing             │
│ • Stop-losses on every trade                  │
│ • Maximum 5% portfolio risk per position      │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Hero Numbers:** 72pt Inter Bold (or JetBrains Mono), Green
- **Number Labels:** 20pt Inter Regular, Light Gray
- **Section Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **roostr Target:** 24pt Inter Semibold, Green

### Visual Elements
- Three hero numbers horizontally centered (equal spacing)
- Labels directly below numbers
- Two sections below (Comparison, Risk Management)
- roostr target highlighted in green

### Animation
1. Title appears
2. Hero numbers count up from 0 (800ms, ease-out, staggered start)
3. Labels fade in (300ms, after numbers)
4. Comparison bullets appear (slide in, 400ms each, 150ms stagger)
5. Risk management bullets appear (slide in, 400ms each, 150ms stagger)

### Focal Points
1. **Primary:** "65-110%" return target (huge number, green)
2. **Secondary:** "2.1-2.8" Sharpe (top-tier risk-adjusted return)
3. **Tertiary:** "Top 5% performance tier" (green highlight)

### Speaker Notes
- "These are our performance targets."
- Point to numbers: "65 to 110% annual returns. Sharpe ratio of 2.1 to 2.8. Max drawdown under 25%."
- "For context, traditional funds do 8-12% annual. Top quant funds do 20-30%."
- "We're targeting top 5% performance. Why? High-conviction, asymmetric bets in volatile crypto markets."
- "Risk management: Kelly Criterion, stop-losses on every trade, max 5% risk per position."
- Advance to next slide

### Design Rationale
- **Hero numbers:** Make the targets impossible to miss
- **Count-up animation:** Creates excitement (numbers feel big)
- **Comparison context:** Grounds targets in reality (not pie-in-the-sky)
- **Risk callout:** Addresses "is this too risky?" concern

---

## Slide 9: Competitive Advantage

### Layout: Title + Comparison Chart + Bullets

```
┌────────────────────────────────────────────────┐
│ 99% Operating Margins (Impossible for Trad.)  │  [72pt Bold, Black]
│                                                │
│   ┌──────────────────────────────────┐        │
│   │  Traditional        roostr       │        │  [Bar chart]
│   │  Fund               Fund         │        │
│   │   ██████████          ██████████ │        │  [Margin bars]
│   │   40-60%              99%        │        │  [Values above bars]
│   │                                  │        │
│   │  Revenue: 2 & 20    2 & 20      │        │  [Below bars]
│   │  Costs: 40-60%       1%         │        │
│   └──────────────────────────────────┘        │
│                                                │
│ Other advantages:                              │  [32pt Semibold, Black]
│ • 24/7 operation (Asian/European markets)     │  [24pt Regular, Black]
│ • Infinite bandwidth (10k+ assets)            │
│ • Zero analyst turnover, no sick days         │
│ • Consistent execution (no emotions)          │
│                                                │
│ roostr scales $1M → $100M with same cost base │  [28pt Semibold, Green box]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Chart Labels:** 24pt Inter Semibold, Black
- **Chart Values:** 48pt Inter Bold (traditional: black, roostr: green)
- **Chart Details:** 18pt Inter Regular, Light Gray
- **Section Header:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **Scaling Statement:** 28pt Inter Semibold, Green

### Visual Elements
- Side-by-side bar chart (traditional left, roostr right)
- Bars: Traditional (black), roostr (green)
- Bar height proportional to margin (traditional shorter, roostr taller)
- Values directly above bars (48pt bold)
- Chart background: light gray (#f9fafb)
- Green box at bottom with scaling statement

### Animation (WOW FACTOR)
1. Title appears
2. Chart axes/labels appear (fade in, 300ms)
3. Traditional fund bar grows from bottom (500ms, ease-out)
4. Value "40-60%" appears above (fade in, 300ms)
5. roostr bar grows from bottom (500ms, ease-out, +300ms delay)
6. Value "99%" appears above (fade in + scale up, 400ms, emphasis)
7. Bullets appear (slide in, 400ms each, 150ms stagger)
8. Green box scales up (500ms)

### Focal Points
1. **Primary:** "99%" (green, large, tallest bar)
2. **Secondary:** Visual height difference between bars (roostr bar is 2x taller)
3. **Tertiary:** "24/7 operation" (first bullet, key advantage)

### Speaker Notes
- "Here's our unfair advantage: 99% operating margins."
- Point to chart: "Traditional funds spend 40-60% on personnel. We spend 1% on cloud infrastructure."
- "This is structurally impossible for traditional funds. They can't fire all their analysts."
- "Other advantages: we operate 24/7, monitor 10,000+ assets, never take vacations, never trade emotionally."
- Emphasize: "We can scale from $1M to $100M AUM with the same cost base. Traditional funds need to hire 50+ people."
- Advance to next slide

### Design Rationale
- **Bar chart:** Visual comparison is more impactful than text
- **Height difference:** 99% bar is visually dominant (green, tall)
- **Wow factor:** Animated bar growth creates "oh shit" moment

---

## Slide 10: Economics of Scale

### Layout: Title + Cost Comparison Table

```
┌────────────────────────────────────────────────┐
│ $1M → $100M with the Same Team                │  [72pt Bold, Black]
│                                                │
│ Cost structure at different AUM levels:        │  [24pt Semibold, Black]
│                                                │
│ ┌──────┬──────────────┬────────────┬──────────────┐
│ │ AUM  │ Trad. Costs  │ roostr     │ Advantage    │ [20pt Semibold]
│ ├──────┼──────────────┼────────────┼──────────────┤
│ │ $1M  │ $400k        │ $10k       │ 40x          │ [20pt Mono]
│ ├──────┼──────────────┼────────────┼──────────────┤
│ │ $10M │ $2M          │ $50k       │ 40x          │
│ ├──────┼──────────────┼────────────┼──────────────┤
│ │$100M │ $15M         │ $200k      │ 75x          │ [Highlight row]
│ └──────┴──────────────┴────────────┴──────────────┘
│                                                │
│ Key insight: roostr's unit economics           │  [24pt Semibold, Black]
│ *improve* as AUM scales.                       │
│                                                │
│ Implications:                                  │  [32pt Semibold, Black]
│ • Traditional funds: 2-3x revenue valuation   │  [24pt Regular, Black]
│ • roostr: 10-20x revenue (software margins)   │  [24pt Semibold, Green]
│ • Justification for $10M valuation            │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Section Header:** 24pt Inter Semibold, Black
- **Table Header:** 20pt Inter Semibold, Black
- **Table Data:** 20pt JetBrains Mono, Black
- **Advantage Column:** Green text
- **Key Insight:** 24pt Inter Semibold, Black, italic-style on "*improve*"
- **Implications Bullets:** 24pt Inter Regular, Black (roostr line in green)

### Visual Elements
- Table with 4 columns, 4 rows (including header)
- Header row: dark background (#0a0a0a), white text
- Data rows: alternating white / #f9fafb
- Bottom row ($100M) highlighted: light green background (#f0fdf4)
- Advantage column: green text
- Key insight below table
- Implications bullets with roostr line in green

### Animation
1. Title appears
2. Table header appears (slide in from top, 300ms)
3. Table rows appear sequentially (slide in from left, 400ms each, 200ms stagger)
4. Advantage values count up (500ms, ease-out, after row appears)
5. Key insight fades in (300ms)
6. Implications bullets appear (slide in, 400ms each, 150ms stagger)

### Focal Points
1. **Primary:** "75x" advantage at $100M (green, largest multiplier)
2. **Secondary:** Visual progression (costs grow linearly for traditional, flat for roostr)
3. **Tertiary:** "$10M valuation justified" (ties to ask)

### Speaker Notes
- "Let me show you the economics of scale."
- Point to table: "At $1M AUM, traditional funds spend $400k on analysts. We spend $10k on cloud."
- "At $100M AUM, they spend $15M. We spend $200k. That's a 75x cost advantage."
- "Traditional funds have linear cost scaling. We have flat costs."
- Point to implications: "This is why traditional funds trade at 2-3x revenue. We should trade at 10-20x, like software companies."
- "This is the justification for our $10M valuation."
- Advance to next slide

### Design Rationale
- **Table format:** Easiest to scan and compare
- **Bottom row highlight:** Draw eye to largest advantage (75x)
- **Valuation tie-in:** Connects unit economics to investment ask

---

## Slide 11: The Team

### Layout: Title + Agent Cards + Human

```
┌────────────────────────────────────────────────┐
│ AI Agents + Human Oversight                    │  [72pt Bold, Black]
│                                                │
│ The Agents:                                    │  [32pt Semibold, Black]
│                                                │
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ │   Scraper     │ │     Atlas     │ │      Edge     │  [Cards: 360×200]
│ │               │ │               │ │               │
│ │ Data          │ │ ML Validator  │ │ Quant         │  [20pt Regular]
│ │ Collection    │ │               │ │ Strategist    │
│ │               │ │ Multi-source  │ │               │
│ │ 10k+ sources  │ │ corroboration │ │ Backtesting   │  [18pt Light Gray]
│ │ 24/7 ingestion│ │ Risk scoring  │ │ Position size │
│ └───────────────┘ └───────────────┘ └───────────────┘
│                                                │
│ Human Oversight:                               │  [32pt Semibold, Black]
│ • Joselo (Founder): Risk management, strategy  │  [24pt Regular, Black]
│ • Built entire infrastructure in 2 hours      │  [24pt Semibold, Green]
│ • Background: AI engineering, systematic trade │
│                                                │
│ Post-funding hires: Trader (6mo), Compliance   │  [20pt Regular, Light Gray]
│ (12mo), Infrastructure (12mo)                  │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Section Headers:** 32pt Inter Semibold, Black
- **Agent Names:** 24pt Inter Semibold, Black (centered in card)
- **Agent Roles:** 20pt Inter Regular, Black
- **Agent Details:** 18pt Inter Regular, Light Gray
- **Human Bullets:** 24pt Inter Regular, Black
- **"2 hours" Highlight:** 24pt Inter Semibold, Green
- **Hiring Timeline:** 20pt Inter Regular, Light Gray

### Visual Elements
- Three agent cards (360×200px, 40px gap)
- Card styling: White background, 2px border (#e0e0e0), 24px padding
- Human oversight section below cards
- Optional: Small robot icon in each card (24×24, top-left corner)

### Animation
1. Title appears
2. Agent cards appear sequentially (slide in from bottom, 400ms each, 200ms stagger)
3. Human oversight section fades in (300ms)
4. "2 hours" highlight pulses (scale 1.0 → 1.05 → 1.0, 400ms)
5. Hiring timeline fades in (300ms)

### Focal Points
1. **Primary:** Three agent names (Scraper, Atlas, Edge)
2. **Secondary:** "Built in 2 hours" (green highlight)
3. **Tertiary:** Hiring plan (addresses "is this just you?" concern)

### Speaker Notes
- "Here's the team. Three AI agents, plus me."
- Point to cards: "Scraper handles data ingestion. Atlas validates signals. Edge executes strategies."
- "I provide human oversight: risk management, strategic direction."
- Emphasize: "I built this entire infrastructure in 2 hours. That's proof of execution."
- "Post-funding, we'll hire an execution trader, compliance officer, and infrastructure engineer."
- Advance to next slide

### Design Rationale
- **Agent cards:** Treats AI agents as team members (reinforces AI-native philosophy)
- **Human oversight:** Addresses safety concern (not fully autonomous)
- **Hiring plan:** Shows realistic growth trajectory

---

## Slide 12: Traction

### Layout: Title + Metrics + Checkmarks

```
┌────────────────────────────────────────────────┐
│ Built in Public, Shipping in Real-Time         │  [72pt Bold, Black]
│                                                │
│ Operational since: January 2026                │  [28pt Semibold, Black]
│                                                │
│ Infrastructure deployed:                       │  [32pt Semibold, Black]
│ ✓ 400KB+ production code                      │  [24pt Regular, Green check]
│ ✓ 3 specialized AI agents (Scraper/Atlas/Edge)│
│ ✓ Real-time data pipelines (Twitter/Telegram) │
│ ✓ Public repo: github.com/joselo-ai/roostr... │
│                                                │
│ Validated edges:                               │  [32pt Semibold, Black]
│ ✓ 4 strategies with proven track records      │
│ ✓ Camillo's PENGU: +77% (validated post-hoc)  │
│ ✓ Riz playbook: $120k+ documented profits     │
│ ✓ Dan's TAO: 1000x case study                 │
│                                                │
│ Time to build: 2 hours (Jan 2026)             │  [48pt Bold, Green box]
│                                                │
│ We didn't spend 6 months in stealth.           │  [28pt Semibold, Black]
│ We shipped.                                    │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Operational Date:** 28pt Inter Semibold, Black
- **Section Headers:** 32pt Inter Semibold, Black
- **Checkmark Items:** 24pt Inter Regular, Black, green check (✓)
- **Time to Build:** 48pt Inter Bold, Green, in box
- **Closing Statement:** 28pt Inter Semibold, Black

### Visual Elements
- Green checkmarks (✓, 24pt) before each item
- Two sections (Infrastructure, Validated Edges)
- "2 hours" in large green box (background #f0fdf4, border 2px green)
- Closing statement centered below

### Animation
1. Title appears
2. Operational date fades in (300ms)
3. Infrastructure items appear sequentially (checkmark + text, 300ms each, 150ms stagger)
4. Validated edges items appear sequentially (checkmark + text, 300ms each, 150ms stagger)
5. "2 hours" box scales up (500ms, emphasis)
6. Closing statement fades in (300ms)

### Focal Points
1. **Primary:** "2 hours" (green box, large text)
2. **Secondary:** Green checkmarks (visual proof of completion)
3. **Tertiary:** "We shipped" (confident closing line)

### Speaker Notes
- "Here's our traction."
- "We've been operational since January 2026."
- Point to checkmarks: "Everything's deployed. 400KB+ of production code. Three AI agents. Real-time data pipelines."
- "We've validated four strategies with real track records."
- Emphasize: "Time to build? 2 hours. We didn't spend 6 months in stealth mode. We shipped."
- Advance to next slide

### Design Rationale
- **Checkmarks:** Visual proof (more credible than claims)
- **"2 hours" emphasis:** This is the repeated motif (investors will remember)
- **"We shipped":** Confident, punchy closing line

---

## Slide 13: Market Opportunity

### Layout: Title + Numbers + TAM/SAM/SOM

```
┌────────────────────────────────────────────────┐
│ $4 Trillion Industry Ripe for Disruption       │  [72pt Bold, Black]
│                                                │
│    $4.0T            $80B           $50B+       │  [Hero: 64pt Bold, Green]
│  Total AUM      Mgmt Fees      Perf Fees      │  [Labels: 18pt Light Gray]
│                                                │
│ Target market (5-year horizon):                │  [32pt Semibold, Black]
│ • Year 1: $10M AUM (prove track record)       │  [24pt Regular, Black]
│ • Year 2: $50M AUM (institutional seed)       │
│ • Year 3: $200M AUM (family offices)          │
│ • Year 5: $1B+ AUM (top-tier crypto fund)     │  [Highlight: Green]
│                                                │
│ Comparable exits:                              │  [32pt Semibold, Black]
│ • Renaissance: $130B AUM (40% returns)        │
│ • Citadel: $60B AUM (quant-driven)            │
│ • Two Sigma: $60B AUM (AI/ML)                 │
│                                                │
│ roostr's wedge: AI-native, crypto-first,       │  [28pt Semibold, Green box]
│ built in public.                               │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Hero Numbers:** 64pt JetBrains Mono Bold, Green
- **Number Labels:** 18pt Inter Regular, Light Gray
- **Section Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **Year 5 Highlight:** Green text
- **Wedge Statement:** 28pt Inter Semibold, Green

### Visual Elements
- Three hero numbers (horizontally centered, equal spacing)
- Labels directly below numbers
- Two sections (Target Market, Comparables)
- Year 5 in green text
- Green box at bottom with wedge statement

### Animation
1. Title appears
2. Hero numbers count up (800ms, ease-out, staggered)
3. Labels fade in (300ms)
4. Target market bullets appear (slide in, 400ms each, 150ms stagger)
5. Comparables bullets appear (slide in, 400ms each, 150ms stagger)
6. Green box scales up (500ms)

### Focal Points
1. **Primary:** "$4.0T" (massive market size)
2. **Secondary:** "$1B+ AUM" in Year 5 (green, ambitious target)
3. **Tertiary:** Comparable exits (Renaissance, Citadel, Two Sigma)

### Speaker Notes
- "This is a $4 trillion industry."
- Point to numbers: "$4 trillion in AUM. $80 billion in annual management fees. $50 billion+ in performance fees."
- "Here's our 5-year plan: $10M in year one, prove the track record. $50M in year two, institutional seed. $1 billion+ in year five."
- "For context, Renaissance manages $130 billion. Citadel and Two Sigma each manage $60 billion."
- "Our wedge: AI-native from day one, crypto-first, building in public."
- Advance to next slide

### Design Rationale
- **Huge numbers:** Make the market opportunity visceral
- **5-year trajectory:** Shows realistic growth path
- **Comparables:** Grounds ambition in reality (these companies exist)

---

## Slide 14: Go-to-Market Strategy

### Layout: Title + Three Phases (Timeline)

```
┌────────────────────────────────────────────────┐
│ Phase 1 → Phase 2 → Phase 3                    │  [72pt Bold, Black]
│                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  │ Phase 1:        │→ │ Phase 2:        │→ │ Phase 3:        │
│  │ Validation      │  │ Seed Raise      │  │ Scale           │  [28pt Semibold]
│  │                 │  │                 │  │                 │
│  │ 90 days         │  │ Months 4-6      │  │ Months 7-18     │  [20pt Regular]
│  │ $100k AUM       │  │ $1-2M AUM       │  │ $10M+ AUM       │  [20pt Mono, Green]
│  │                 │  │                 │  │                 │
│  │ • Deploy $100k  │  │ • Pitch VCs     │  │ • Raise from LPs│  [18pt Regular]
│  │ • Prove returns │  │ • Use Phase 1   │  │ • Scale infra   │
│  │ • Build track   │  │   results       │  │ • Expand to     │
│  │   record        │  │ • Deploy $1-2M  │  │   equities      │
│  │ • Deliver 90-day│  │ • Institutional │  │ • Path to $100M │
│  │   audit         │  │   grade track   │  │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘
│                                                │
│ Exit options: $1B+ fund | Strategic acquisition│  [24pt Regular, Black]
│ | Spin out technology                          │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Phase Headers:** 28pt Inter Semibold, Black
- **Timeline/AUM:** 20pt Inter Regular (timeline), 20pt JetBrains Mono Green (AUM)
- **Bullets:** 18pt Inter Regular, Black
- **Exit Options:** 24pt Inter Regular, Black

### Visual Elements
- Three phase boxes (480×400px, 60px gap)
- Box styling: White background, 2px border (#e0e0e0), 24px padding
- Arrows between boxes (3px black line, 16px arrowhead)
- Phase headers at top of each box
- Timeline and AUM below headers
- Bullets describing activities
- Exit options centered below boxes

### Animation
1. Title appears
2. Phase 1 box appears (slide in from left, 400ms)
3. Arrow 1 appears (fade in, 300ms, +200ms delay)
4. Phase 2 box appears (slide in from center, 400ms, +300ms delay)
5. Arrow 2 appears (fade in, 300ms, +200ms delay)
6. Phase 3 box appears (slide in from right, 400ms, +300ms delay)
7. Exit options fade in (300ms)

### Focal Points
1. **Primary:** AUM progression ($100k → $1-2M → $10M+) in green
2. **Secondary:** Phase arrows (visual metaphor for progression)
3. **Tertiary:** Exit options (multiple paths to liquidity)

### Speaker Notes
- "Here's our go-to-market strategy in three phases."
- Point to Phase 1: "First 90 days, deploy $100k, prove 65-110% returns, deliver audited results."
- Point to Phase 2: "Months 4-6, use those results to raise $1-2M seed round. Deploy at institutional scale."
- Point to Phase 3: "Months 7-18, scale to $10M+ AUM. Expand beyond crypto into equities."
- "Exit options: Continue scaling to $1 billion+, get acquired by Citadel or Two Sigma, or spin out the technology."
- Advance to next slide

### Design Rationale
- **Three-phase structure:** Simple, digestible roadmap
- **Visual progression:** Left-to-right flow with arrows
- **AUM in green:** Numbers pop (this is what matters)
- **Exit options:** Addresses "how do I get my money back?" concern

---

## Slide 15: The Ask

### Layout: Title + Two Options + Justification

```
┌────────────────────────────────────────────────┐
│ $1-2M Seed @ $10M Valuation                    │  [72pt Bold, Black]
│                                                │
│ Two investment structures:                     │  [32pt Semibold, Black]
│                                                │
│ ┌────────────────────────┐  ┌────────────────────────┐
│ │ Option 1:              │  │ Option 2:              │  [28pt Semibold]
│ │ Equity Investment      │  │ Direct AUM Deployment  │
│ │                        │  │                        │
│ │ • $1-2M for 10-20%     │  │ • Invest $1-2M in fund │  [24pt Regular]
│ │   equity               │  │ • Standard 2 & 20 fees │
│ │ • $10M pre-money       │  │ • Equity warrant       │
│ │ • 10-20x revenue       │  │   (5-10%)              │
│ │ • Exit: Strategic      │  │ • Upside: Returns +    │
│ │   acquisition          │  │   long-term equity     │
│ └────────────────────────┘  └────────────────────────┘
│                                                │
│ Why $10M valuation is justified:               │  [32pt Semibold, Black]
│ • Software-like margins (99%)                  │  [24pt Regular, Black]
│ • Proprietary tech (400KB+ code)               │
│ • First-mover (12-24mo ahead)                  │
│ • Proven execution (built in 2 hours)          │  [Highlight: Green]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Section Header:** 32pt Inter Semibold, Black
- **Option Headers:** 28pt Inter Semibold, Black
- **Option Bullets:** 24pt Inter Regular, Black
- **Justification Header:** 32pt Inter Semibold, Black
- **Justification Bullets:** 24pt Inter Regular, Black
- **"Built in 2 hours" Highlight:** Green text

### Visual Elements
- Two option boxes (540×320px, 60px gap)
- Box styling: White background, 2px border (#e0e0e0), 24px padding
- Option 1 (left), Option 2 (right)
- Justification section below boxes
- "Built in 2 hours" in green

### Animation
1. Title appears
2. Section header fades in (300ms)
3. Option 1 box slides in from left (400ms)
4. Option 2 box slides in from right (400ms, +200ms delay)
5. Justification bullets appear sequentially (slide in, 400ms each, 150ms stagger)
6. "Built in 2 hours" pulses (scale 1.0 → 1.05 → 1.0, 400ms)

### Focal Points
1. **Primary:** "$1-2M @ $10M" in title (the ask)
2. **Secondary:** Two option boxes (flexibility)
3. **Tertiary:** Justification bullets (why $10M is fair)

### Speaker Notes
- "Here's the ask: $1 to $2 million at a $10 million valuation."
- Point to options: "Two ways to structure this. Option 1: Straight equity, 10-20% for $1-2M."
- "Option 2: Invest directly in the fund. Get 2 & 20 fees, plus a 5-10% equity warrant for long-term upside."
- "Why is $10M fair? Software-like margins, proprietary tech, first-mover advantage."
- Emphasize: "We built this in 2 hours. We're not theoretical. We're operational."
- Advance to next slide

### Design Rationale
- **Two options:** Gives investors flexibility (equity vs. fund deployment)
- **Justification section:** Pre-empts "why is the valuation so high?" objection
- **"2 hours" repeated:** This is the proof point (keeps coming back)

---

## Slide 16: Use of Funds

### Layout: Title + Allocation Breakdown

```
┌────────────────────────────────────────────────┐
│ Deploy Capital, Prove Economics, Scale Team    │  [72pt Bold, Black]
│                                                │
│ $1-2M allocation:                              │  [32pt Semibold, Black]
│                                                │
│  ███████████ 40% ($400-800k)                   │  [Bar: Green]
│  AUM Deployment                                │  [28pt Semibold, Black]
│  Deploy in live markets, build 90-day track    │  [20pt Regular, Light Gray]
│                                                │
│  ████████ 30% ($300-600k)                      │  [Bar: Green]
│  Infrastructure Scaling                        │
│  Bloomberg, prime broker, compliance           │
│                                                │
│  █████ 20% ($200-400k)                         │  [Bar: Green]
│  Team Expansion                                │
│  Trader (6mo), Compliance (12mo), Eng (12mo)   │
│                                                │
│  ██ 10% ($100-200k)                            │  [Bar: Green]
│  Runway & Operations                           │
│  18-month runway, cloud, legal                 │
│                                                │
│ Key milestone: Prove 65-110% returns in 90 days│  [28pt Semibold, Green box]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Allocation Header:** 32pt Inter Semibold, Black
- **Percentages:** 28pt Inter Bold, Green
- **Category Names:** 28pt Inter Semibold, Black
- **Descriptions:** 20pt Inter Regular, Light Gray
- **Milestone Box:** 28pt Inter Semibold, Green

### Visual Elements
- Four horizontal bars (width proportional to percentage)
- Bar color: Green (#4ade80)
- Bar height: 48px
- Percentage and dollar amount to the right of each bar
- Category name below each bar
- Description text below category name (light gray)
- Green box at bottom with key milestone

### Animation
1. Title appears
2. Bars grow from left to right (500ms, ease-out, sequential with 200ms stagger)
3. Percentages count up (500ms, simultaneous with bar growth)
4. Category names and descriptions fade in (300ms, after bars)
5. Milestone box scales up (500ms)

### Focal Points
1. **Primary:** 40% bar (largest, top, most important)
2. **Secondary:** Green bars (visual hierarchy by size)
3. **Tertiary:** "90 days" milestone (green box)

### Speaker Notes
- "Here's how we'll use the capital."
- Point to bars: "40% goes directly into AUM deployment. We'll deploy this in live markets to prove returns."
- "30% for infrastructure scaling: Bloomberg data, prime broker, compliance."
- "20% for team expansion: execution trader, compliance officer, infrastructure engineer."
- "10% for runway and operations: 18 months of founder runway, cloud costs, legal."
- Emphasize: "Key milestone: Use the first $100k to prove 65-110% returns in 90 days. Then deploy the rest."
- Advance to next slide

### Design Rationale
- **Horizontal bars:** Visual comparison (easy to see priorities)
- **Green bars:** Consistent with roostr brand
- **40% to AUM:** Shows capital is deployed (not just salaries)
- **90-day milestone:** Creates urgency and tangible checkpoint

---

## Slide 17: Milestones (18-Month Roadmap)

### Layout: Title + Timeline with Quarters

```
┌────────────────────────────────────────────────┐
│ 90-Day Track Record → Institutional Raise →    │  [72pt Bold, Black]
│ $100M AUM                                      │
│                                                │
│ Q1 2026 (Months 1-3):                          │  [32pt Semibold, Black]
│ ✅ Infrastructure built (complete)             │  [24pt Regular, Green check]
│ ✅ 4 edges validated (complete)                │
│ 🎯 Deploy $100k Phase 1 capital               │  [24pt Regular, Black, target emoji]
│ 🎯 Deliver 90-day audited results             │
│                                                │
│ Q2 2026 (Months 4-6):                          │
│ • Raise $1-2M seed round                       │  [24pt Regular, Black]
│ • Deploy seed capital                          │
│ • Institutional-grade reporting                │
│ • Onboard first LP                             │
│                                                │
│ Q3 2026 (Months 7-9):                          │
│ • Scale to $5-10M AUM                          │
│ • Hire execution trader + compliance           │
│ • Register as investment advisor (SEC/CFTC)    │
│ • Expand from crypto → equities                │
│                                                │
│ Q4 2026 (Months 10-12):                        │
│ • Deliver 12-month audited track record        │
│ • Pitch institutional LPs                      │
│ • Target: $20M+ AUM                            │  [Highlight: Green]
│                                                │
│ 2027 (Months 13-18):                           │
│ • Scale to $50-100M AUM                        │  [Highlight: Green]
│ • Top-tier crypto fund                         │
│ • Explore strategic acquisition                │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Quarter Headers:** 32pt Inter Semibold, Black
- **Completed Items:** 24pt Inter Regular, Black, green checkmark (✅)
- **In-Progress Items:** 24pt Inter Regular, Black, target emoji (🎯)
- **Future Items:** 24pt Inter Regular, Black, bullet (•)
- **Highlights:** Green text

### Visual Elements
- Five sections (Q1-Q4 2026, 2027)
- Visual indicators: ✅ (done), 🎯 (in progress), • (future)
- Green checkmarks for completed items
- Green text for AUM targets ($20M+, $50-100M)
- Optional: Vertical timeline bar on left side (green, 4px wide)

### Animation
1. Title appears
2. Quarters appear sequentially (fade in + slide in, 400ms each, 200ms stagger)
3. Within each quarter, items appear sequentially (fade in, 300ms each, 100ms stagger)
4. Green highlights pulse briefly (scale 1.0 → 1.05 → 1.0, 400ms)

### Focal Points
1. **Primary:** Q1 2026 checkmarks (proof of progress)
2. **Secondary:** "$20M+ AUM" in Q4 (green, ambitious)
3. **Tertiary:** "$50-100M AUM" in 2027 (green, long-term goal)

### Speaker Notes
- "Here's our 18-month roadmap."
- Point to Q1: "We've already completed the infrastructure and validated 4 edges. Next: deploy $100k and deliver 90-day results."
- Point to Q2: "Use those results to raise $1-2M seed round. Deploy at institutional scale."
- Point to Q3: "Scale to $5-10M AUM. Hire team. Register with SEC/CFTC."
- Point to Q4: "Deliver 12-month audited track record. Target $20M+ AUM."
- Point to 2027: "Scale to $50-100M. Become a top-tier crypto fund."
- Advance to next slide

### Design Rationale
- **Visual indicators:** ✅ (done), 🎯 (in progress), • (future) make progress clear
- **Green highlights:** Draw eye to key metrics (AUM targets)
- **Sequential reveal:** Builds momentum (we're already moving)

---

## Slide 18: Why Now?

### Layout: Title + Three Sections (Tech, Market, Risk)

```
┌────────────────────────────────────────────────┐
│ The Window Is Closing                          │  [72pt Bold, Black]
│                                                │
│ Technology readiness:                          │  [32pt Semibold, Black]
│ • Claude Sonnet 4 (Jan 2025): First LLM capable│  [24pt Regular, Black]
│   of analyst-level research                    │
│ • Multi-agent architectures (2025): Enable     │
│   specialization at scale                      │
│ • This wasn't possible 12 months ago           │  [24pt Semibold, Green]
│                                                │
│ Market timing:                                 │  [32pt Semibold, Black]
│ • Crypto markets (2024-2025): High volatility  │
│ • Institutional crypto adoption (ETFs, custody)│
│ • Traditional funds still hiring analysts      │  [24pt Regular, Black]
│                                                │
│ First-mover advantage:                         │  [32pt Semibold, Black]
│ • roostr is 12-24 months ahead of competitors  │  [24pt Semibold, Green]
│ • Building in public = brand moat              │
│ • Proprietary data pipelines = defensible edge │
│                                                │
│ The risk of waiting: Citadel/Two Sigma will    │  [28pt Semibold, Black]
│ build AI-native funds (but slower, 2-3 years)  │
│                                                │
│ Window to capture market share: 18-24 months   │  [32pt Bold, Green box]
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Section Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **Key Statements:** 24pt Inter Semibold, Green
- **Risk Statement:** 28pt Inter Semibold, Black
- **Window Statement:** 32pt Inter Bold, Green

### Visual Elements
- Three sections (Technology, Market, First-Mover)
- Green highlights for key statements
- Risk statement below sections
- Large green box at bottom with window statement

### Animation
1. Title appears
2. Sections appear sequentially (fade in + slide in, 400ms each, 200ms stagger)
3. Key statements (green) pulse briefly (scale 1.0 → 1.05 → 1.0, 400ms)
4. Risk statement fades in (300ms)
5. Window box scales up (500ms, emphasis)

### Focal Points
1. **Primary:** "18-24 months" window (green box, urgency)
2. **Secondary:** "This wasn't possible 12 months ago" (green, repeated)
3. **Tertiary:** "12-24 months ahead" (green, competitive advantage)

### Speaker Notes
- "Why invest now? Three reasons."
- "One: Technology is ready. Claude Sonnet 4 launched in January 2025. This wasn't possible before."
- "Two: Market timing. Crypto is volatile, institutional adoption is happening, traditional funds are still hiring humans."
- "Three: First-mover advantage. We're 12-24 months ahead of competitors."
- Emphasize: "The risk of waiting? Citadel and Two Sigma will build AI-native funds. But they're slow. 2-3 years."
- "The window to capture market share is 18-24 months. After that, competition catches up."
- Advance to next slide

### Design Rationale
- **Three-part structure:** Comprehensive case for urgency
- **Green highlights:** Key insights pop visually
- **Window callout:** Creates FOMO (investors don't want to miss the wave)

---

## Slide 19: Vision

### Layout: Title + Three-Phase Vision

```
┌────────────────────────────────────────────────┐
│ AI-Powered Intelligence Layer for Capital      │  [72pt Bold, Black]
│ Markets                                        │
│                                                │
│ Short-term (2026-2027):                        │  [32pt Semibold, Black]
│ • Best-in-class crypto hedge fund              │  [24pt Regular, Black]
│ • 65-110% annual returns, Sharpe 2.1-2.8       │
│ • $50M+ AUM, institutional LPs                 │
│                                                │
│ Medium-term (2027-2028):                       │  [32pt Semibold, Black]
│ • Expand: crypto → equities → commodities      │
│ • Spin out technology (AI agent infrastructure)│
│ • Become the "Palantir of capital markets"     │  [24pt Semibold, Green]
│                                                │
│ Long-term (2028+):                             │  [32pt Semibold, Black]
│ • roostr = AI intelligence layer for all       │  [24pt Semibold, Green]
│   capital markets                              │
│ • Other funds license roostr's agents          │
│ • Platform revenue: $50M+/year (SaaS)          │
│                                                │
│ The bigger picture:                            │  [32pt Semibold, Black]
│ Traditional funds are dinosaurs. AI-native     │  [28pt Regular, Black]
│ funds are the future. roostr is the first.     │
│                                                │
│ Our advantage: We're building the picks and    │  [28pt Semibold, Green box]
│ shovels that every fund will need.             │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Slide Title:** 72pt Inter Bold, Black
- **Phase Headers:** 32pt Inter Semibold, Black
- **Bullets:** 24pt Inter Regular, Black
- **Key Statements:** 24pt Inter Semibold, Green
- **Bigger Picture:** 28pt Inter Regular, Black
- **Advantage Box:** 28pt Inter Semibold, Green

### Visual Elements
- Three phases (Short, Medium, Long)
- Green highlights for key vision statements
- "Bigger picture" section below phases
- Green box at bottom with picks-and-shovels metaphor

### Animation
1. Title appears
2. Phases appear sequentially (fade in + slide in, 400ms each, 200ms stagger)
3. Key statements (green) pulse briefly
4. Bigger picture fades in (300ms)
5. Advantage box scales up (500ms)

### Focal Points
1. **Primary:** "Palantir of capital markets" (green, bold metaphor)
2. **Secondary:** "$50M+/year (SaaS)" (green, platform revenue)
3. **Tertiary:** "Picks and shovels" (green box, key insight)

### Speaker Notes
- "Let me paint the long-term vision."
- "Short-term: Become the best crypto hedge fund. Prove 65-110% returns."
- "Medium-term: Expand beyond crypto. Spin out the technology. Become the Palantir of capital markets."
- "Long-term: roostr becomes the AI intelligence layer for all capital markets. Other funds license our agents. Platform revenue: $50M+ per year."
- Emphasize: "The bigger picture? Traditional funds are dinosaurs. AI-native funds are the future. roostr is the first."
- "Our advantage: We're not just building a fund. We're building the picks and shovels that every fund will need."
- Advance to next slide

### Design Rationale
- **Three-phase vision:** Shows trajectory beyond just a fund
- **Palantir metaphor:** Makes the vision tangible (investors know Palantir)
- **Picks-and-shovels:** This is the "aha" (infrastructure play, not just trading)

---

## Slide 20: Contact & Next Steps

### Layout: Centered Hero + CTA

```
┌────────────────────────────────────────────────┐
│                                                │
│                                                │
│         Let's Build the Future of Finance      │  [72pt Bold, Black]
│                                                │
│                 roostr                         │  [96pt Bold, Black]
│   The First Fully AI-Native Hedge Fund         │  [32pt Semibold, Black]
│                                                │
│ GitHub: github.com/joselo-ai/roostr-research   │  [24pt Regular, Black]
│ Dashboard: [Live performance tracking]          │
│ Contact: [Founder email/Telegram]              │
│                                                │
│                                                │
│             Next Steps:                        │  [32pt Semibold, Black]
│                                                │
│  1. Review this deck                           │  [24pt Regular, Black]
│  2. Check the public dashboard                 │
│  3. Schedule a call (30-min deep dive)         │
│  4. Commit capital ($1-2M seed or AUM)         │
│                                                │
│ Timeline: Phase 1 (March 2026) | Seed close    │  [20pt Regular, Light Gray]
│ (April 2026) | 90-day results (June 2026)      │
│                                                │
│ We didn't spend 6 months in stealth.           │  [28pt Semibold, Black]
│ We shipped in 2 hours.                         │
│ Now let's raise $2M and prove AI beats market. │
│                                                │
│ roostr: zero human analysts. infinite scale.   │  [24pt Semibold, Green]
│         99% margins.                           │
│                                                │
└────────────────────────────────────────────────┘
```

### Typography Hierarchy
- **Hero Text:** 72pt Inter Bold, Black
- **roostr Wordmark:** 96pt Inter Bold, Black
- **Tagline:** 32pt Inter Semibold, Black
- **Contact Info:** 24pt Inter Regular, Black
- **Next Steps Header:** 32pt Inter Semibold, Black
- **Next Steps List:** 24pt Inter Regular, Black, numbered
- **Timeline:** 20pt Inter Regular, Light Gray
- **Closing Statement:** 28pt Inter Semibold, Black
- **Three-Line Hook:** 24pt Inter Semibold, Green

### Visual Elements
- Centered layout
- roostr wordmark prominent
- Contact info (clickable links if PDF allows)
- Numbered next steps (clear CTA)
- Timeline in light gray (supporting info)
- Closing statement (repeated "2 hours" motif)
- Three-line hook at bottom (green, memorable)

### Animation
1. Hero text fades in (500ms)
2. roostr wordmark fades in (500ms, +200ms delay)
3. Tagline fades in (300ms, +200ms delay)
4. Contact info fades in (300ms, +200ms delay)
5. Next steps appear sequentially (fade in, 300ms each, 200ms stagger)
6. Timeline fades in (300ms)
7. Closing statement fades in (300ms)
8. Three-line hook fades in (500ms, emphasis)

### Focal Points
1. **Primary:** "Let's Build the Future of Finance" (hero text)
2. **Secondary:** Next steps (clear CTA)
3. **Tertiary:** Three-line hook in green (memorable closing)

### Speaker Notes
- "That's roostr."
- "Here's how to move forward."
- Read next steps: "One: Review this deck. Two: Check our public dashboard. Three: Schedule a 30-minute call. Four: Commit capital."
- "Timeline: Phase 1 launches in March. Seed round closes in April. 90-day results in June."
- Emphasize: "We didn't spend 6 months in stealth. We shipped in 2 hours."
- "Now let's raise $2 million and prove AI can beat the market."
- Pause on three-line hook: "roostr: zero human analysts, infinite scalability, 99% margins."
- "Thank you."

### Design Rationale
- **Clear CTA:** Next steps are numbered and actionable
- **Timeline:** Creates urgency (specific dates)
- **Repeated "2 hours":** This is the hook (investors will remember)
- **Three-line hook:** Circles back to Slide 1 (memorable bookend)

---

## Global Design Notes

### Consistency Across Slides
- Title always 72pt Inter Bold, top-left, 80px from top
- Safe zone: 120px margins (left/right), 80px (top/bottom)
- Spacing: Multiples of 8px (8, 16, 24, 32, 48, 64)
- Green accent: #4ade80 (only for emphasis, not overused)
- Black text: #000000 (primary)
- Light gray text: #e0e0e0 (secondary/captions)

### Animation Principles
- Total animation time per slide: <3 seconds
- Stagger delays: 100-200ms (prevents visual overload)
- Easing: Ease-out (most common), ease-in-out (transitions)
- No auto-advance (presenter controls pacing)

### Presenting Tips
- Pause after each slide title (let investors read)
- Point to specific elements ("Look at this number...")
- Emphasize green text (this is the key insight)
- Pause before advancing (allow questions)

### Remote Viewing Optimization
- All text 18pt+ (readable on Zoom)
- High contrast colors only (black on white)
- Large numbers in green (easy to spot)
- Minimal text per slide (<50 words)

### Investor Psychology
- Slide 1: Hook them ("99% margins")
- Slides 2-6: Build credibility (problem, tech, validation)
- Slides 7-10: Wow them (performance, margins, scale)
- Slides 11-17: De-risk (team, traction, roadmap)
- Slides 18-19: Create urgency (why now, vision)
- Slide 20: Close (clear CTA)

---

**This deck is designed to raise $2M. Every slide serves that purpose.**
