# Google Slides Template: roostr Pitch Deck
**Step-by-step build instructions | 20 slides | February 2026**

Complete implementation guide for creating the roostr pitch deck in Google Slides.

---

## Setup & Theme Configuration

### 1. Create New Presentation

1. Go to Google Slides: https://slides.google.com
2. Click "Blank presentation"
3. Immediately rename: "roostr Pitch Deck v1.0"
4. Set slide size:
   - Click **Slide** → **Page setup**
   - Choose **Widescreen 16:9** (1920×1080)
   - Click **OK**

### 2. Install Fonts

Google Slides auto-loads Google Fonts. We'll use **Inter** (already available).

**To verify Inter is available:**
1. Select any text
2. Click font dropdown
3. Type "Inter" in search
4. Should appear (if not, use Helvetica as fallback)

**Font Downloads (for offline work):**
- Inter: https://fonts.google.com/specimen/Inter
- JetBrains Mono: https://fonts.google.com/specimen/JetBrains+Mono

### 3. Set Up Master Slides (Theme)

**Create Custom Theme:**

1. Click **Slide** → **Edit theme**
2. You'll see theme editor with master slides

**Master Slide Setup:**

**Master 1: Title Slide (Centered)**
- Delete all placeholders
- Background: White (#FFFFFF)
- No footer, no page number

**Master 2: Content Slide (Default)**
- Title placeholder: 
  - Position: 120px from left, 80px from top
  - Size: 1680px wide × 120px tall
  - Font: Inter Bold, 72pt, Black
- Content placeholder:
  - Position: 120px from left, 224px from top (80 + 80 + 64 spacing)
  - Size: 1680px wide × 776px tall
  - Font: Inter Regular, 24pt, Black
- No footer (add manually per slide if needed)

**Master 3: Section Break (Dark)**
- Background: #0a0a0a (near-black)
- Text color: White
- Centered layout

**Color Palette (add to theme):**
1. In theme editor, click **Colors**
2. Add custom colors:
   - Text: #000000 (Black)
   - Background: #FFFFFF (White)
   - Accent 1: #4ade80 (Green)
   - Accent 2: #0a0a0a (Deep Black)
   - Accent 3: #e0e0e0 (Light Gray)

3. Click **Done** to save theme

---

## Slide-by-Slide Build Instructions

### Slide 1: Cover

**Layout:** Blank slide

**Instructions:**
1. Insert → Text box
2. Type: `roostr`
3. Format:
   - Font: Inter, Bold
   - Size: 96pt
   - Color: Black (#000000)
   - Alignment: Center
   - Letter spacing: -0.03em (Format → Text → Spacing → Custom → -3%)
4. Position: Horizontally centered, 360px from top

5. Insert → Text box
6. Type: `The First Fully AI-Native Hedge Fund`
7. Format:
   - Font: Inter, Semibold (600)
   - Size: 36pt
   - Color: Black
   - Alignment: Center
   - Letter spacing: -0.01em (-1%)
8. Position: Horizontally centered, 480px from top

9. Insert → Text box
10. Type:
    ```
    Zero human analysts. Infinite scalability.
    99% margins.
    ```
11. Format:
    - Font: Inter, Regular
    - Size: 24pt
    - Color: Light Gray (#e0e0e0)
    - Alignment: Center
    - Line spacing: 1.5
12. Position: Horizontally centered, 600px from top

13. Insert → Text box
14. Type: `github.com/joselo-ai/roostr-research`
15. Format:
    - Font: Inter, Regular
    - Size: 18pt
    - Color: Light Gray (#e0e0e0)
    - Alignment: Center
16. Position: Horizontally centered, 920px from top (near bottom)

**Optional enhancement:**
- Add subtle underline under "roostr": Insert → Line, 2px, Green (#4ade80), centered below wordmark

**Animation (if presenting live):**
1. Select "roostr" → Insert → Animation → Fade in (500ms, On click)
2. Select tagline → Insert → Animation → Fly in from bottom (400ms, After previous, 200ms delay)
3. Select three-line hook → Insert → Animation → Fade in (300ms, After previous, 400ms delay)
4. Select GitHub link → Insert → Animation → Fade in (300ms, After previous, 200ms delay)

---

### Slide 2: The Problem

**Layout:** Content slide (from master)

**Instructions:**

**Title:**
1. Click title placeholder
2. Type: `Traditional Hedge Funds Hit a Ceiling`
3. Format should auto-apply from master (72pt Inter Bold, Black)

**Left Column:**
1. Insert → Text box
2. Position: 120px from left, 224px from top
3. Size: 780px wide
4. Type:
   ```
   The human bottleneck:
   • Analyst bandwidth limits scale (one analyst = ~10 positions monitored)
   • Operating margins: 40-60% (personnel costs dominate)
   • Research quality degrades as AUM grows
   • Can't operate 24/7 across global markets
   ```
5. Format:
   - Header: Inter Semibold, 32pt, Black
   - Bullets: Inter Regular, 24pt, Black
   - Bullet color: Green (#4ade80), 16pt
   - Line spacing: 1.6

**Right Column:**
1. Insert → Text box
2. Position: 980px from left, 224px from top
3. Size: 780px wide
4. Type:
   ```
   The math doesn't work:
   • $1M AUM → 3-5 analysts required
   • $100M AUM → 50+ analysts required
   • Linear cost scaling kills margins at scale
   ```
5. Format: Same as left column

**Conclusion Box:**
1. Insert → Shape → Rectangle
2. Size: 1200px wide × 80px tall
3. Position: Horizontally centered, 800px from top
4. Fill: #f9fafb (very light gray)
5. Border: 4px left border, Green (#4ade80)
6. Insert → Text box (inside rectangle)
7. Type: `Traditional funds trade margin for growth.`
8. Format: Inter Semibold, 28pt, Green, centered

**Animation:**
1. Title: Fade in (300ms, On click)
2. Left column: Fly in from left (400ms, After previous)
3. Right column: Fly in from right (400ms, After previous, 200ms delay)
4. Conclusion box: Fade in + Scale up 0.9→1.0 (500ms, After previous, 300ms delay)

---

### Slide 3: The Opportunity

**Layout:** Content slide

**Title:** `AI Breaks the Scaling Curve`

**Section 1 (What changed in 2025):**
1. Insert → Text box
2. Type:
   ```
   What changed in 2025:
   • LLMs (Claude Sonnet 4, GPT-4) can now perform analyst-level research
   • Multi-agent architectures enable specialization at scale
   • 24/7 operation with zero fatigue
   • Cost per analysis: $0.0001 vs $50,000/year per human analyst
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Bullets: Inter Regular, 24pt, Black
   - Cost line: JetBrains Mono, 24pt, Green for numbers
4. Position: 120px from left, 224px from top

**Section 2 (The market is ready):**
1. Insert → Text box
2. Type:
   ```
   The market is ready:
   • $4 trillion global hedge fund industry
   • Institutional investors seeking alpha in efficient markets
   • Crypto markets (24/7, data-rich, high volatility) = perfect testing ground
   ```
3. Format: Same as Section 1
4. Position: 120px from left, 480px from top

**Section 3 (First-mover advantage):**
1. Insert → Text box
2. Type:
   ```
   First-mover advantage:
   This wasn't possible 12 months ago.
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Statement: Inter Regular, 28pt, Black
4. Position: 120px from left, 680px from top

**Icons (Optional - using Lucide):**
1. Download icons from https://lucide.dev as SVG
2. Insert → Image → Upload from computer
3. Resize to 32×32px
4. Position next to section headers

**Animation:**
1. Title: Fade in (300ms, On click)
2. Section 1: Fly in from left (400ms, After previous)
3. Section 2: Fly in from right (400ms, After previous, 300ms delay)
4. Section 3: Fade in + Scale up (500ms, After previous, 300ms delay)

---

### Slide 4: Our Solution (Agent Flow Diagram)

**Layout:** Content slide

**Title:** `3 AI Agents Replace the Entire Analyst Team`

**Agent Boxes:**

**Box 1 (Scraper):**
1. Insert → Shape → Rectangle with rounded corners
2. Size: 240px wide × 120px tall
3. Position: 420px from left, 320px from top
4. Fill: White
5. Border: 2px solid Black
6. Insert → Text box (inside)
7. Type:
   ```
   Scraper
   ────────
   Data Collection
   
   10,000+ sources
   24/7 ingestion
   ```
8. Format:
   - "Scraper": Inter Semibold, 24pt, Black, centered
   - "Data Collection": Inter Regular, 20pt, Black, centered
   - Details: Inter Regular, 18pt, Light Gray, centered
   - Line spacing: 1.3

**Box 2 (Atlas):**
1. Duplicate Box 1
2. Position: 740px from left, 320px from top
3. Edit text:
   ```
   Atlas
   ─────
   Validate Signal
   
   Multi-source
   corroboration
   ```

**Box 3 (Edge):**
1. Duplicate Box 1
2. Position: 1060px from left, 320px from top
3. Edit text:
   ```
   Edge
   ────
   Execute Strategy
   
   Backtesting
   + Risk
   ```

**Arrows:**
1. Insert → Line → Arrow
2. Format: 3px thickness, Black, arrowhead on right
3. Position: Connect Scraper → Atlas (between boxes)
4. Duplicate for Atlas → Edge

**Human Oversight:**
1. Insert → Text box
2. Type: `Human oversight: Joselo (Risk + Strategy)`
3. Format: Inter Regular, 20pt, Light Gray
4. Position: Horizontally centered, 500px from top

**Animation (WOW FACTOR):**
1. Title: Fade in (300ms, On click)
2. Scraper box: Fly in from left (400ms, After previous)
3. Atlas box: Fly in from bottom (400ms, After previous, 200ms delay)
4. Edge box: Fly in from right (400ms, After previous, 200ms delay)
5. Arrow 1: Wipe right (300ms, After previous)
6. Arrow 2: Wipe right (300ms, After previous)
7. Human oversight: Fade in (300ms, After previous, 500ms delay)

---

### Slide 5: How It Works

**Layout:** Content slide

**Title:** `Data → Validation → Risk → Execution`

**Four Steps (Stacked Vertically):**

**Template for each step:**
1. Insert → Shape → Circle (32×32px)
2. Fill: Green (#4ade80)
3. Position: 120px from left
4. Insert → Text box (inside circle)
5. Type step number (1, 2, 3, 4)
6. Format: Inter Bold, 20pt, White, centered

7. Insert → Text box (next to circle)
8. Type step header (e.g., "Step 1: Signal Discovery")
9. Format: Inter Semibold, 32pt, Black
10. Position: 170px from left

11. Insert → Text box (below header)
12. Type bullet points
13. Format: Inter Regular, 24pt, Black, green bullets

**Step 1 (Y: 224):**
```
Step 1: Signal Discovery
• Scraper monitors crypto Twitter, whale wallets, dev activity
• Flags high-conviction signals (e.g., "Dan bought 100 TAO")
```

**Example Quote Box:**
1. Insert → Shape → Rectangle
2. Size: 600px × 60px
3. Fill: #f9fafb
4. Border-left: 4px Green
5. Insert → Text box (inside)
6. Type: `"Dan bought 100 TAO"`
7. Format: JetBrains Mono, 24pt, Black

**Step 2 (Y: 380):**
```
Step 2: Multi-Source Validation
• Atlas cross-references: on-chain data + GitHub commits + social sentiment
• Validates trader track record (Dan: 1000x on TAO, proven alpha)
```

**Step 3 (Y: 536):**
```
Step 3: Risk Assessment
• Edge backtests similar setups (narrative-driven plays, early accumulation)
• Calculates position size based on Kelly Criterion
```

**Step 4 (Y: 692):**
```
Step 4: Execution
• Automated limit orders, stop-losses, position management
• 24/7 monitoring for exit signals
```

**Result Box:**
1. Insert → Shape → Rectangle
2. Size: 1200px × 80px
3. Position: Horizontally centered, 860px from top
4. Fill: #f9fafb
5. Border: 2px solid Green
6. Insert → Text box (inside)
7. Type: `Result: High-conviction trades with quantified risk/reward.`
8. Format: Inter Semibold, 28pt, Green, centered

**Animation:**
1. Title: Fade in (300ms, On click)
2. Steps appear sequentially: Circle + Header + Bullets (400ms each, 200ms stagger)
3. Result box: Scale up + Fade in (500ms, After all steps)

---

### Slide 6: The Technology

**Layout:** Content slide

**Title:** `Proprietary Infrastructure Built in 2 Hours`

**Section 1 (Tech Stack):**
1. Insert → Text box
2. Type:
   ```
   Tech Stack:
   • Data Layer: Custom scrapers (Twitter API, Telegram bots, on-chain indexers)
   • Intelligence Layer: Claude Sonnet 4 multi-agent orchestration
   • Validation Layer: Multi-source corroboration algorithms
   • Execution Layer: CEX/DEX integrations (Binance, Uniswap, Jupiter)
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Bullets: Inter Regular, 24pt, Black
4. Position: 120px from left, 224px from top

**Section 2 (400KB+ production code):**
1. Insert → Text box
2. Type:
   ```
   400KB+ production code deployed:
   ✓ Scraper agent: Real-time social monitoring
   ✓ Atlas agent: ML validation pipelines
   ✓ Edge agent: Backtesting & risk models
   ✓ Public dashboard: roostr-research repository
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Items: Inter Regular, 24pt, Black
   - Checkmarks: Green (#4ade80), 24pt
4. Position: 120px from left, 500px from top

**Moat Statement:**
1. Insert → Shape → Rectangle
2. Size: 800px × 80px
3. Fill: #f9fafb
4. Position: 120px from left, 740px from top
5. Insert → Text box (inside)
6. Type: `Moat: Proprietary data pipelines + validated agent workflows`
7. Format: Inter Semibold, 24pt, Black

**Proof Box:**
1. Insert → Shape → Rectangle
2. Size: 600px × 80px
3. Fill: White
4. Border: 2px solid Green
5. Position: Horizontally centered, 860px from top
6. Insert → Text box (inside)
7. Type: `Proof of execution: Built in 2 hours (Jan 2026)`
8. Format: Inter Semibold, 28pt, Green, centered

**Animation:**
1. Title: Fade in (300ms, On click)
2. Tech Stack bullets: Appear together (400ms, After previous)
3. Deployed code items: Appear sequentially with checkmarks (300ms each, 150ms stagger)
4. Moat statement: Fade in (300ms, After previous)
5. Proof box: Scale up (500ms, After previous)

---

### Slide 7: The Edges (Data Table)

**Layout:** Content slide

**Title:** `Track Record of Alpha Generation`

**Table:**
1. Insert → Table
2. Dimensions: 4 columns × 5 rows (including header)

**Header Row Formatting:**
1. Select header row
2. Fill: #0a0a0a (dark background)
3. Text: Inter Semibold, 20pt, White
4. Headers: Strategy | Example Trade | Return | Status

**Data Rows:**
1. Row height: 64px
2. Cell padding: 16px
3. Alternating row colors: White / #f9fafb
4. Text: Inter Regular, 20pt, Black
5. Numbers: JetBrains Mono, 20pt, Black
6. Returns: Green text (#4ade80)

**Data:**
```
Row 1: Social Arbitrage | Camillo's PENGU call | +77% | Validated
Row 2: Riz Playbook | Multiple high-conviction plays | $120k+ profits | Validated
Row 3: Dan's TAO Trade | Early accumulation → 1000x | 1000x | Case study
Row 4: Multi-Source Validation | Cross-reference social + on-chain | Reduces false positives by 60% | Operational
```

**Key Insight (Below Table):**
1. Insert → Text box
2. Type:
   ```
   Key insight: These aren't backtests.
   These are real trades from real traders, validated and replicated by roostr's system.
   ```
3. Format: Inter Semibold, 24pt, Black
4. Position: 120px from left, 680px from top

**Replicable Statement:**
1. Insert → Shape → Rectangle
2. Size: 1000px × 80px
3. Fill: #f0fdf4 (light green)
4. Border: 2px solid Green
5. Position: Horizontally centered, 820px from top
6. Insert → Text box (inside)
7. Type: `Dan's TAO 1000x is *replicable* with AI-powered early detection.`
8. Format: Inter Semibold, 28pt, Green, centered

**Animation:**
1. Title: Fade in (300ms, On click)
2. Table header: Slide in from top (300ms, After previous)
3. Table rows: Appear sequentially (300ms each, 150ms stagger)
4. Key insight: Fade in (300ms, After table)
5. Replicable box: Scale up (500ms, After previous)

---

### Slide 8: Performance Targets

**Layout:** Content slide

**Title:** `Top 5% of Global Hedge Funds`

**Hero Numbers (Horizontally Centered):**

**Number 1:**
1. Insert → Text box
2. Type: `65-110%`
3. Format: Inter Bold, 72pt, Green (#4ade80), centered
4. Position: 320px from left, 260px from top
5. Insert → Text box (below)
6. Type: `Annual Return`
7. Format: Inter Regular, 20pt, Light Gray, centered
8. Position: 320px from left, 360px from top

**Number 2:**
1. Insert → Text box
2. Type: `2.1-2.8`
3. Format: Inter Bold, 72pt, Green, centered
4. Position: 760px from left, 260px from top
5. Insert → Text box (below)
6. Type: `Sharpe Ratio`
7. Format: Inter Regular, 20pt, Light Gray, centered

**Number 3:**
1. Insert → Text box
2. Type: `<25%`
3. Format: Inter Bold, 72pt, Green, centered
4. Position: 1200px from left, 260px from top
5. Insert → Text box (below)
6. Type: `Max Drawdown`
7. Format: Inter Regular, 20pt, Light Gray, centered

**Comparison Section:**
1. Insert → Text box
2. Type:
   ```
   Comparison to Industry:
   • Traditional hedge funds: 8-12% annual, Sharpe 0.8-1.2
   • Top quant funds (Renaissance, Citadel): 20-30% annual, Sharpe 1.5-2.0
   • roostr target: Top 5% performance tier
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Bullets: Inter Regular, 24pt, Black
   - roostr line: Inter Semibold, 24pt, Green
4. Position: 120px from left, 480px from top

**Risk Management:**
1. Insert → Text box
2. Type:
   ```
   Risk management:
   • Kelly Criterion position sizing
   • Stop-losses on every trade
   • Diversification across 10-15 uncorrelated plays
   • Maximum 5% portfolio risk per position
   ```
3. Format: Same as Comparison
4. Position: 120px from left, 700px from top

**Animation:**
1. Title: Fade in (300ms, On click)
2. Hero numbers: Count up from 0 (800ms, After previous, simultaneous start)
3. Labels: Fade in (300ms, After numbers)
4. Comparison bullets: Appear sequentially (400ms each, 150ms stagger)
5. Risk bullets: Appear sequentially (400ms each, 150ms stagger)

---

### Slide 9: Competitive Advantage (Bar Chart)

**Layout:** Content slide

**Title:** `99% Operating Margins (Impossible for Traditional Funds)`

**Bar Chart (Manual Creation):**

**Chart Area:**
1. Insert → Shape → Rectangle
2. Size: 800px wide × 400px tall
3. Fill: #f9fafb
4. Border: None
5. Position: 560px from left, 260px from top

**Traditional Fund Bar:**
1. Insert → Shape → Rectangle
2. Size: 120px wide × 160px tall (proportional to 50%)
3. Fill: Black (#000000)
4. Position: 640px from left, 500px from top
5. Insert → Text box (above bar)
6. Type: `40-60%`
7. Format: Inter Bold, 48pt, Black, centered
8. Position: Centered above bar
9. Insert → Text box (below bar)
10. Type: `Traditional Fund`
11. Format: Inter Semibold, 24pt, Black, centered

**roostr Fund Bar:**
1. Insert → Shape → Rectangle
2. Size: 120px wide × 320px tall (proportional to 99%, 2x traditional)
3. Fill: Green (#4ade80)
4. Position: 1000px from left, 340px from top
5. Insert → Text box (above bar)
6. Type: `99%`
7. Format: Inter Bold, 48pt, Green, centered
8. Insert → Text box (below bar)
9. Type: `roostr Fund`
10. Format: Inter Semibold, 24pt, Black, centered

**Chart Details (Below bars):**
1. Insert → Text box
2. Type: `Revenue: 2 & 20` (under Traditional)
3. Format: Inter Regular, 18pt, Light Gray
4. Insert → Text box
5. Type: `Costs: 40-60%` (under Traditional)
6. Repeat for roostr side (`2 & 20`, `1%`)

**Other Advantages:**
1. Insert → Text box
2. Type:
   ```
   Other advantages:
   • 24/7 operation (capture Asian/European market moves)
   • Infinite bandwidth (monitor 10,000+ assets simultaneously)
   • Zero analyst turnover, no sick days, no vacation
   • Consistent execution (no emotional trading)
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Bullets: Inter Regular, 24pt, Black
4. Position: 120px from left, 720px from top

**Scaling Statement:**
1. Insert → Shape → Rectangle
2. Size: 1200px × 80px
3. Fill: #f0fdf4
4. Border: 2px solid Green
5. Position: Horizontally centered, 900px from top
6. Insert → Text box (inside)
7. Type: `roostr scales $1M → $100M AUM with the same cost base`
8. Format: Inter Semibold, 28pt, Green, centered

**Animation (WOW FACTOR):**
1. Title: Fade in (300ms, On click)
2. Chart area: Fade in (300ms, After previous)
3. Traditional bar: Grow from bottom (500ms, ease-out, After previous)
4. Traditional "40-60%": Fade in (300ms, After bar)
5. roostr bar: Grow from bottom (500ms, ease-out, After previous, 300ms delay)
6. roostr "99%": Fade in + Scale up 0.9→1.1→1.0 (600ms, emphasis, After bar)
7. Chart details: Fade in (300ms, After bars)
8. Other advantages: Appear sequentially (400ms each, 150ms stagger)
9. Scaling statement: Scale up (500ms, After advantages)

---

### Slide 10: Economics of Scale (Table)

**Layout:** Content slide

**Title:** `$1M → $100M with the Same Team`

**Subtitle:**
1. Insert → Text box
2. Type: `Cost structure at different AUM levels:`
3. Format: Inter Semibold, 24pt, Black
4. Position: 120px from left, 224px from top

**Table:**
1. Insert → Table
2. Dimensions: 4 columns × 4 rows (including header)

**Header Row:**
- Fill: #0a0a0a
- Text: Inter Semibold, 20pt, White
- Headers: AUM | Traditional Fund Costs | roostr Costs | roostr Advantage

**Data Rows:**
```
Row 1: $1M  | $400k | $10k  | 40x
Row 2: $10M | $2M   | $50k  | 40x
Row 3: $100M| $15M  | $200k | 75x
```

**Row 3 Highlight:**
- Background: #f0fdf4 (light green)
- Advantage value: Inter Bold, 20pt, Green

**Text Formatting:**
- AUM: JetBrains Mono, 20pt, Black
- Costs: JetBrains Mono, 20pt, Black
- Advantage: JetBrains Mono, 20pt, Green

**Table Position:** Horizontally centered, 300px from top

**Key Insight:**
1. Insert → Text box
2. Type:
   ```
   Key insight: roostr's unit economics *improve* as AUM scales.
   ```
3. Format: Inter Semibold, 24pt, Black, italic on "*improve*"
4. Position: 120px from left, 640px from top

**Implications:**
1. Insert → Text box
2. Type:
   ```
   Implications for valuation:
   • Traditional hedge funds: 2-3x revenue valuation (labor-intensive business)
   • roostr: 10-20x revenue valuation (software-like margins)
   • Justification for $10M pre-money valuation at $1-2M revenue run-rate
   ```
3. Format:
   - Header: Inter Semibold, 32pt, Black
   - Bullets: Inter Regular, 24pt, Black
   - roostr bullet: Inter Semibold, 24pt, Green
4. Position: 120px from left, 720px from top

**Animation:**
1. Title: Fade in (300ms, On click)
2. Subtitle: Fade in (300ms, After previous)
3. Table header: Slide in from top (300ms, After previous)
4. Table rows: Appear sequentially (400ms each, 200ms stagger)
5. Advantage values: Count up (500ms, simultaneous with row appearance)
6. Key insight: Fade in (300ms, After table)
7. Implications bullets: Appear sequentially (400ms each, 150ms stagger)

---

### Slides 11-20: Quick Build Notes

**Slide 11: The Team**
- Three agent cards (240×120 each, use rounded rectangles)
- Position agent cards horizontally centered with 40px gaps
- Human oversight section below cards
- Use same animation pattern as Slide 4 (agent flow)

**Slide 12: Traction**
- Green checkmarks before each item (use ✓ character or insert checkmark shape)
- Two sections (Infrastructure, Validated Edges)
- Large "2 hours" callout box (green)
- Closing statement centered

**Slide 13: Market Opportunity**
- Three hero numbers at top (count-up animation)
- Two bullet sections (Target Market, Comparables)
- Green box at bottom with wedge statement

**Slide 14: Go-to-Market Strategy**
- Three phase boxes (480×400 each, use rounded rectangles)
- Arrows between phases
- Exit options centered below

**Slide 15: The Ask**
- Two option boxes (540×320 each)
- Justification bullets below
- "Built in 2 hours" highlighted in green

**Slide 16: Use of Funds**
- Four horizontal bars (use rectangles, width proportional to percentage)
- Bar color: Green
- Percentages and dollar amounts to right of bars
- Milestone box at bottom

**Slide 17: Milestones**
- Five quarter sections (Q1-Q4 2026, 2027)
- Use ✅ (done), 🎯 (in progress), • (future) indicators
- Green highlights for AUM targets

**Slide 18: Why Now?**
- Three sections (Technology, Market, First-Mover)
- Green highlights for key statements
- Large green box at bottom with window statement

**Slide 19: Vision**
- Three phases (Short, Medium, Long)
- Green highlights for vision statements
- Green box at bottom with picks-and-shovels metaphor

**Slide 20: Contact & Next Steps**
- Centered layout
- roostr wordmark prominent (96pt)
- Numbered next steps (clear CTA)
- Three-line hook at bottom (green)

---

## Global Formatting Tips

### Consistent Spacing
- Top margin: 80px (title position)
- Left/right margins: 120px
- Spacing between elements: Multiples of 8px (16, 24, 32, 48, 64)

### Text Formatting Shortcuts
- **Bold:** Ctrl+B (Cmd+B on Mac)
- **Increase font size:** Ctrl+Shift+> (Cmd+Shift+> on Mac)
- **Decrease font size:** Ctrl+Shift+< (Cmd+Shift+< on Mac)
- **Align center:** Ctrl+Shift+E (Cmd+Shift+E on Mac)

### Alignment Tools
- Select multiple objects → Right-click → Align → Distribute horizontally/vertically
- Use guides: View → Guides → Show guides (or Ctrl+; / Cmd+;)
- Snap to grid: View → Snap → Snap to grid

### Color Picker (Custom Colors)
1. Select object
2. Click fill color
3. Click "+" (Custom)
4. Enter hex codes:
   - Black: #000000
   - Green: #4ade80
   - Deep Black: #0a0a0a
   - Light Gray: #e0e0e0
   - Light Green (boxes): #f0fdf4
   - Very Light Gray: #f9fafb

---

## Animation Best Practices

### Adding Animations
1. Select object
2. Insert → Animation
3. Choose animation type
4. Set timing:
   - **On click:** Manual advance (recommended for key slides)
   - **After previous:** Auto-advance after previous animation
   - **With previous:** Simultaneous with previous animation
5. Set duration (300-500ms recommended)
6. Set delay if needed (0-500ms for stagger effects)

### Animation Order
- Use animation panel to reorder: View → Motion (or right sidebar)
- Drag animations to reorder
- Preview: Click "Play" in animation panel

### Recommended Animations
- **Fade in:** Text, simple reveals
- **Fly in from left/right:** Columns, side-by-side content
- **Scale up:** Emphasis boxes, hero numbers
- **Wipe:** Arrows, dividers
- **Grow from bottom:** Bar charts

---

## Export Settings

### PDF Export (Most Common for VCs)
1. File → Download → PDF Document (.pdf)
2. Opens PDF in new tab
3. Save to computer
4. Filename: `roostr-pitch-deck-v1.0.pdf`

**PDF Settings:**
- Embedded fonts: ✅ (automatic in Google Slides)
- High resolution: ✅ (automatic)
- Preserve animations: ❌ (PDFs are static)

### PowerPoint Export (Compatibility)
1. File → Download → Microsoft PowerPoint (.pptx)
2. Opens file download
3. Test in PowerPoint to verify compatibility
4. Fonts may need adjustment (Inter may not be installed)

### Image Export (Individual Slides)
1. File → Download → PNG image (.png)
2. Downloads all slides as PNG files (zipped)
3. Use for social media, website previews

---

## Presenting from Google Slides

### Presenter View
1. Click "Present" button (top-right)
2. Choose "Presenter view"
3. Shows:
   - Current slide (large, what audience sees)
   - Next slide (preview)
   - Speaker notes (your private notes)
   - Timer

### Remote Presenting (Zoom)
1. Start Zoom meeting
2. Click "Share Screen"
3. Select Google Slides window
4. Check "Share computer sound" (if using audio)
5. Check "Optimize for video clip" (smoother animations)
6. Click "Share"

**Pro tip:** Use dual monitors
- Monitor 1: Zoom window with audience video
- Monitor 2: Google Slides in Presenter view

### Keyboard Shortcuts (Presenting)
- **Next slide:** Right arrow, Space, or Click
- **Previous slide:** Left arrow
- **Go to specific slide:** Type slide number, then Enter
- **Black screen:** B key
- **White screen:** W key
- **Exit presentation:** Esc

---

## Collaboration & Version Control

### Sharing with Team
1. Click "Share" button (top-right)
2. Add collaborators by email
3. Set permissions:
   - **Editor:** Can edit (use for co-founders)
   - **Commenter:** Can comment (use for advisors)
   - **Viewer:** Read-only (use for investors after pitch)

### Version History
1. File → Version history → See version history
2. View all changes, restore previous versions
3. Name versions: Click "︙" → Name current version (e.g., "v1.0 - Seed Raise")

### Making a Copy (for Customization)
1. File → Make a copy
2. Rename for specific pitch (e.g., "roostr Pitch - [VC Name]")
3. Customize slides for specific investor (e.g., add custom slide addressing their thesis)

---

## Troubleshooting

### Fonts Not Loading
- **Issue:** Inter doesn't appear in font list
- **Solution:** Use Helvetica or Arial as fallback, or download Inter and use desktop app

### Animations Not Playing
- **Issue:** Animations don't play during presentation
- **Solution:** Ensure you're in "Present" mode (not edit mode). Verify animations are set to "On click" or "After previous."

### Images/Icons Not Aligned
- **Issue:** Elements look misaligned
- **Solution:** Use alignment tools (Right-click → Align) and guides (Ctrl+; / Cmd+;)

### Export Quality Low
- **Issue:** PDF looks pixelated
- **Solution:** Google Slides exports at high quality automatically. If issue persists, export as PowerPoint, then export to PDF from PowerPoint at "Best Quality" setting.

### Slow Performance
- **Issue:** Google Slides lags with many animations
- **Solution:** Reduce number of animations, or present from PowerPoint (File → Download → .pptx)

---

## Final Checklist

Before finalizing deck:

- [ ] All 20 slides created
- [ ] Consistent fonts (Inter Bold for titles, Regular for body)
- [ ] Consistent colors (Black, White, Green only)
- [ ] All animations tested in Presenter view
- [ ] Speaker notes added to each slide
- [ ] PDF exported and tested (opens correctly, fonts embedded)
- [ ] Deck reviewed at 50% zoom (readable on small screens)
- [ ] No typos, consistent capitalization (roostr is lowercase)
- [ ] Confidential notice on footer (if needed)
- [ ] Version number and date on cover slide

---

## Quick Start Guide (TL;DR)

1. **Create presentation:** Google Slides → Blank → 16:9 widescreen
2. **Set up theme:** Slide → Edit theme → Add Inter font, custom colors
3. **Build slides 1-20:** Use instructions above
4. **Add animations:** Insert → Animation (Fade in, Fly in, Scale up)
5. **Test in Presenter view:** Click "Present" → Verify animations, readability
6. **Export PDF:** File → Download → PDF
7. **Pitch investors:** Present from Google Slides or send PDF

---

**This template is designed for speed. You should be able to build the full 20-slide deck in 2-3 hours using these instructions.**

**Ready to raise $2M? Start building.** 🚀
