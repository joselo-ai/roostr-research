# roostr Pitch Deck Design System
**Version 1.0 | February 2026**

A complete visual design guide for roostr's investor pitch deck.

---

## Design Philosophy

**Minimal but Impactful**
- Every element serves a purpose
- White space is a design element, not empty space
- Bold typography does the heavy lifting
- Data visualization over decoration

**Professional but Modern**
- Technical confidence, not corporate boredom
- Slightly edgy, never flashy
- roostr voice: lowercase, direct, transparent
- Show don't tell (charts > bullet points)

**Optimized for Remote**
- High contrast for Zoom/small screens
- Readable at thumbnail sizes
- Minimal text per slide (visuals tell the story)
- Fast cognitive processing (investors scan in 3 seconds)

---

## Color System

### Primary Palette

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **roostr black** | `#000000` | `0, 0, 0` | Headlines, primary text, data labels |
| **roostr white** | `#FFFFFF` | `255, 255, 255` | Backgrounds, negative space, contrast |
| **roostr green** | `#4ade80` | `74, 222, 128` | Accent, CTAs, positive metrics, growth |
| **deep black** | `#0a0a0a` | `10, 10, 10` | Secondary backgrounds, depth, cards |
| **light gray** | `#e0e0e0` | `224, 224, 224` | Secondary text, captions, metadata |

### Extended Palette (Data Visualization)

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **signal green** | `#22c55e` | `34, 197, 94` | Positive returns, validation, success |
| **dark green** | `#166534` | `22, 101, 52` | Bar charts (dark mode), secondary accents |
| **neutral gray** | `#525252` | `82, 82, 82` | Grid lines, borders, dividers |
| **warning red** | `#ef4444` | `239, 68, 68` | Risk indicators, drawdowns (use sparingly) |
| **info blue** | `#3b82f6` | `59, 130, 246` | Secondary data series (avoid if possible) |

### Color Psychology

- **Black:** Authority, precision, technical confidence
- **Green:** Growth, validation, alpha (crypto-native color)
- **White:** Clarity, transparency, simplicity
- **Gray:** Supporting information, not distracting

### Usage Rules

✅ **DO:**
- Use black for all headlines (100% contrast)
- Use green for positive metrics, CTAs, key highlights
- Use white backgrounds for maximum readability
- Use gray for supporting text (never as primary)

❌ **DON'T:**
- Mix green with blue (confusing color semantics)
- Use gradients (too flashy for roostr brand)
- Use low-contrast colors (fails remote viewing test)
- Use more than 3 colors per slide

---

## Typography System

### Typeface Hierarchy

**Primary:** **Inter** (Google Fonts, free, excellent at all sizes)
- Modern, clean, technical
- Excellent readability on screens
- Variable font (one file, all weights)

**Fallback:** **Helvetica Neue** (system font)
- Universal availability
- Professional, neutral
- Safe choice for compatibility

**Monospace:** **JetBrains Mono** (for code/data)
- Technical, slightly edgy
- Excellent for numbers and data
- Crypto-native aesthetic

### Type Scale (16:9 slides, 1920x1080)

| Element | Font | Size | Weight | Line Height | Letter Spacing | Color |
|---------|------|------|--------|-------------|----------------|-------|
| **Slide Title** | Inter | 72pt | Bold (700) | 1.1 | -0.02em | Black |
| **Section Heading** | Inter | 48pt | Bold (700) | 1.2 | -0.01em | Black |
| **Subheading** | Inter | 32pt | Semibold (600) | 1.3 | 0em | Black |
| **Body Text** | Inter | 24pt | Regular (400) | 1.5 | 0em | Black |
| **Caption** | Inter | 18pt | Regular (400) | 1.4 | 0em | Light Gray |
| **Data Label** | JetBrains Mono | 20pt | Medium (500) | 1.2 | 0em | Black |
| **Large Number** | Inter | 64pt | Bold (700) | 1.0 | -0.02em | Black or Green |
| **Small Print** | Inter | 16pt | Regular (400) | 1.4 | 0em | Light Gray |

### Typography Rules

✅ **DO:**
- Use bold weights for headlines (700+)
- Keep body text 24pt+ (readable on Zoom)
- Use monospace for numbers, percentages, code
- Limit to 2-3 font sizes per slide
- Use negative letter-spacing for large headlines (-0.02em)

❌ **DON'T:**
- Use italic (looks weak, hard to read)
- Mix more than 2 font families per slide
- Use serif fonts (too traditional for roostr)
- Set body text below 20pt (fails readability test)
- Use ALL CAPS except for emphasis (e.g., "AUM", "AI")

### Hierarchy Examples

**Good:**
```
roostr                          [72pt Bold, Black]
The First Fully AI-Native       [32pt Semibold, Black]
Hedge Fund

99% margins                     [64pt Bold, Green]
```

**Bad (too many sizes):**
```
roostr                          [72pt Bold]
The First Fully                 [40pt Regular]
AI-Native                       [36pt Semibold]
Hedge Fund                      [28pt Light]
```

---

## Spacing & Grid System

### Grid Structure (1920x1080 canvas)

**Safe Zone:**
- Top margin: 80px
- Bottom margin: 80px
- Left margin: 120px
- Right margin: 120px
- Content area: 1680px × 920px

**Grid Columns:**
- 12-column grid
- Column width: 120px
- Gutter: 20px
- Total: 1680px

**Vertical Rhythm:**
- Base unit: 8px
- All spacing in multiples of 8 (8, 16, 24, 32, 40, 48, 64, 80, 96, 120)

### Spacing Scale

| Token | Size | Usage |
|-------|------|-------|
| `xs` | 8px | Tight spacing (chart labels) |
| `sm` | 16px | Element padding, icon gaps |
| `md` | 24px | Paragraph spacing |
| `lg` | 32px | Section spacing |
| `xl` | 48px | Major section breaks |
| `2xl` | 64px | Slide title to content |
| `3xl` | 96px | Vertical centering offset |
| `4xl` | 120px | Maximum breathing room |

### Layout Patterns

**Pattern 1: Title + Content (80% of slides)**
```
[120px margin]
  [Slide Title - 72pt]
  [64px space]
  [Content area - body text, charts, bullets]
[120px margin]
```

**Pattern 2: Centered Hero (Cover, Section Breaks)**
```
[Vertical center]
  [Hero Text - 72pt]
  [24px space]
  [Subtext - 32pt]
  [48px space]
  [CTA or supporting text - 24pt]
```

**Pattern 3: Two-Column (Comparison Slides)**
```
[Left Column - 6 cols]    [Right Column - 6 cols]
    [Content]                 [Content]
   [1680px × 920px split 50/50]
```

**Pattern 4: Chart-Dominant (Data Slides)**
```
[Slide Title - 72pt, top-left]
[32px space]
[Chart fills 80% of canvas]
[Caption below - 18pt]
```

---

## Iconography

### Style Guidelines

**Aesthetic:**
- Outline style (2px stroke weight)
- Rounded corners (2px radius)
- Minimal detail (geometric, not illustrative)
- Consistent optical sizing (24×24 or 32×32 base)

**Color:**
- Primary: Black (`#000000`)
- Accent: Green (`#4ade80`) for active/selected states
- Never use gray icons on white backgrounds (low contrast)

### Icon Scale

| Size | Usage |
|------|-------|
| 24×24 | Inline icons (bullet points, list items) |
| 32×32 | Section headers, chart legends |
| 48×48 | Feature highlights, key callouts |
| 64×64 | Hero icons (cover slide, section breaks) |

### Icon Recommendations

**Use Lucide Icons (https://lucide.dev):**
- Open source, consistent style
- 2px stroke weight (matches roostr aesthetic)
- Comprehensive library (1000+ icons)
- Available as React, Vue, SVG exports

**Key Icons Needed:**
- `activity` — Agent workflows, real-time monitoring
- `bar-chart-2` — Data visualization, performance
- `zap` — Speed, execution, automation
- `shield-check` — Risk management, validation
- `trending-up` — Growth, returns, alpha
- `cpu` — AI/ML infrastructure
- `users` — Team, human oversight
- `target` — Strategy, focus
- `clock` — 24/7 operation
- `check-circle` — Validation, completed milestones

### Icon Usage Rules

✅ **DO:**
- Use icons to reinforce concepts (not decoration)
- Keep stroke weight consistent (2px)
- Align icons to text baseline
- Use sparingly (3-5 icons per slide max)

❌ **DON'T:**
- Mix icon styles (outline + solid)
- Use emoji (unprofessional for VC pitch)
- Use 3D or shadowed icons (too decorative)
- Scale icons disproportionately (maintain aspect ratio)

---

## Data Visualization

### Chart Types & When to Use

| Chart Type | Use Case | roostr Example |
|------------|----------|----------------|
| **Bar Chart** | Compare discrete values | Slide 9: Operating Margins (Traditional vs roostr) |
| **Line Chart** | Show trends over time | Slide 8: Performance curve (65-110% annual) |
| **Table** | Precise numbers, comparison | Slide 7: The Edges (strategy performance) |
| **Comparison Card** | Side-by-side metrics | Slide 10: Cost structure at different AUM levels |
| **Flow Diagram** | Process visualization | Slide 4: Scraper → Atlas → Edge workflow |
| **Number + Label** | Single key metric | Slide 1: "99% margins" |

### Chart Design Principles

**Minimal Chrome:**
- Remove gridlines (or make very subtle, `#e0e0e0`)
- No borders on chart area
- No background fills
- No drop shadows or 3D effects

**High Data-Ink Ratio:**
- Maximize data, minimize decoration
- Direct labels (not legends when possible)
- Remove axes if values are labeled
- Use white space to separate elements

**Color Strategy:**
- Single color (green) for primary data
- Black for comparison/baseline data
- Red sparingly (only for risk/negative)
- No rainbow charts (confusing, distracting)

### Chart Specifications

**Bar Chart:**
```
Bar color: #4ade80 (green)
Bar spacing: 8px gap between bars
Bar width: 32-48px
Value labels: 20pt JetBrains Mono, black, centered above bar
Y-axis: Remove (use direct labels)
X-axis: 18pt Inter Regular, light gray
Grid: None (or subtle horizontal at 25%, 50%, 75%)
```

**Line Chart:**
```
Line color: #4ade80 (green), 3px stroke
Point markers: 8px circles, green fill
Area fill: Optional gradient (green 20% opacity)
Y-axis: Right-aligned, 18pt Inter Regular, light gray
X-axis: Bottom-aligned, 18pt Inter Regular, light gray
Grid: Horizontal only, 1px, #e0e0e0, 25% intervals
```

**Table:**
```
Header row: 20pt Inter Semibold, black, 16px padding
Data rows: 20pt JetBrains Mono Regular, black, 12px padding
Row dividers: 1px solid #e0e0e0
Column alignment: Left (text), Right (numbers)
Hover state: Subtle gray background (#f5f5f5)
Highlight: Green text for positive values
```

### Number Formatting

**Currencies:**
- `$1M` (not `$1,000,000`)
- `$10M+` (ranges)
- `$1-2M` (seed round size)

**Percentages:**
- `99%` (whole numbers preferred)
- `65-110%` (ranges)
- `+77%` (returns, always include sign)

**Multipliers:**
- `1000x` (not `1,000×`)
- `10-20x` (valuation multiples)

**Dates:**
- `Q1 2026` (quarters)
- `Feb 2026` (months)
- `90 days` (durations)

---

## Animation Principles

### Motion Philosophy

**Purposeful, Not Decorative:**
- Animations guide attention (not distraction)
- Slow is smooth, smooth is fast
- Respect cognitive load (one animation at a time)

**Performance:**
- 60fps minimum (no jank on Zoom screen share)
- GPU-accelerated (transform/opacity only)
- Preload all assets (no mid-presentation loading)

### Animation Timing

| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| **Fade In** | 300ms | Ease-out | Text reveals, slide entry |
| **Slide In** | 400ms | Ease-out | Charts, diagrams entering |
| **Scale Up** | 250ms | Ease-out | Number highlights, emphasis |
| **Morph** | 500ms | Ease-in-out | Chart transitions (bar → line) |
| **Stagger** | +100ms | Ease-out | List items, sequential reveals |

### Easing Functions

- **Ease-out:** Fast start, slow end (most common, feels responsive)
- **Ease-in-out:** Smooth acceleration/deceleration (transitions between states)
- **Linear:** No easing (data visualization, mechanical feel)

### Animation Patterns

**Pattern 1: Build Sequence (Bullet Lists)**
```
1. Title appears (fade in, 300ms)
2. Wait 200ms
3. Bullet 1 appears (slide in from left, 400ms)
4. Wait 100ms (stagger delay)
5. Bullet 2 appears (slide in from left, 400ms)
6. Repeat for all bullets
```

**Pattern 2: Chart Reveal**
```
1. Chart axes appear (fade in, 300ms)
2. Wait 200ms
3. Data bars grow from zero (scale up, 500ms, ease-out)
4. Wait 100ms
5. Value labels appear (fade in, 300ms)
```

**Pattern 3: Number Emphasis**
```
1. Number starts at 0
2. Count up to final value (800ms, ease-out)
3. Scale up 1.0 → 1.1 → 1.0 (bounce, 400ms)
4. Color shift to green (200ms)
```

**Pattern 4: Slide Transition**
```
1. Current slide fades out (300ms)
2. Wait 100ms (avoid overlap)
3. Next slide fades in (300ms)
Total: 700ms per transition
```

### Animation Don'ts

❌ **Avoid:**
- Auto-advancing slides (presenter should control pacing)
- Looping animations (distracting, unprofessional)
- Sound effects (cringe in investor pitch)
- Parallax/3D effects (gimmicky, hard to follow on Zoom)
- Spinning/rotating elements (nauseating)
- More than 3 animated elements per slide

---

## Component Library

### 1. Slide Title

**Specifications:**
- Font: Inter Bold, 72pt
- Color: Black
- Position: 120px from left, 80px from top
- Max width: 1200px (wrap if needed)
- Letter spacing: -0.02em

**Usage:** Every slide except cover and section breaks

---

### 2. Hero Number

**Specifications:**
- Font: Inter Bold, 96pt (or JetBrains Mono for data)
- Color: Green (`#4ade80`) or Black
- Position: Vertically centered
- Letter spacing: -0.03em
- Optional: Count-up animation on reveal

**Usage:** Key metrics (99% margins, 1000x return, $10M valuation)

**Example:**
```
      99%
   margins
```

---

### 3. Data Table

**Structure:**
```
┌─────────────┬──────────┬──────────┬──────────┐
│ Header 1    │ Header 2 │ Header 3 │ Header 4 │  [20pt Semibold, Black]
├─────────────┼──────────┼──────────┼──────────┤
│ Row 1 Data  │   $10M   │   +77%   │    ✓     │  [20pt Regular/Mono, Black]
│ Row 2 Data  │   $50M   │  +120%   │    ✓     │
│ Row 3 Data  │  $100M   │  1000x   │    ✓     │
└─────────────┴──────────┴──────────┴──────────┘
```

**Specifications:**
- Row height: 48px
- Cell padding: 12px (left/right), 16px (top/bottom)
- Dividers: 1px solid `#e0e0e0`
- Alternating row background: White / `#f9fafb` (very subtle)
- Number alignment: Right-aligned
- Text alignment: Left-aligned

---

### 4. Comparison Card (Side-by-Side)

**Layout:**
```
┌────────────────────┐  ┌────────────────────┐
│  Traditional Fund  │  │      roostr        │
│                    │  │                    │
│  40-60% margins    │  │   99% margins      │
│  50+ analysts      │  │   3 AI agents      │
│  $15M costs        │  │   $200k costs      │
└────────────────────┘  └────────────────────┘
```

**Specifications:**
- Card width: 780px each (40px gap between)
- Card background: `#f9fafb` (left), `#0a0a0a` (right, dark mode)
- Card padding: 40px
- Border: None or 1px `#e0e0e0`
- Text color: Black (left), White (right)
- Accent: Green for roostr card numbers

---

### 5. Workflow Diagram (Agent Flow)

**Structure:**
```
┌───────────┐      ┌───────────┐      ┌───────────┐
│  Scraper  │  →   │   Atlas   │  →   │   Edge    │
│  (Data)   │      │ (Validate)│      │  (Execute)│
└───────────┘      └───────────┘      └───────────┘
```

**Specifications:**
- Box size: 240px × 120px
- Box background: White
- Box border: 2px solid Black
- Box padding: 24px
- Arrow: 3px black line, 16px arrowhead
- Text: 24pt Inter Semibold (agent name), 18pt Inter Regular (description)
- Spacing: 60px between boxes

**Animation:**
- Boxes appear sequentially (fade in + slide in, 400ms each, 200ms stagger)
- Arrows appear after boxes (fade in, 300ms)

---

### 6. Bullet List

**Structure:**
```
• First bullet point here
• Second bullet point here
• Third bullet point here
```

**Specifications:**
- Bullet character: `•` (U+2022)
- Bullet color: Green (`#4ade80`)
- Bullet size: 16pt (smaller than text)
- Text: 24pt Inter Regular, Black
- Line height: 1.6
- Left indent: 40px (bullet), 60px (text)
- Spacing between bullets: 16px

**Best Practice:**
- Max 5 bullets per slide
- Max 10 words per bullet
- Use icons instead of bullets when possible

---

### 7. Quote/Callout Box

**Structure:**
```
┌─────────────────────────────────────────┐
│ "This wasn't possible 12 months ago."   │
│                                          │
│ — Joselo, roostr founder                │
└─────────────────────────────────────────┘
```

**Specifications:**
- Background: `#f9fafb`
- Border-left: 4px solid Green (`#4ade80`)
- Padding: 32px
- Quote text: 28pt Inter Regular, Black
- Attribution: 20pt Inter Regular, Light Gray (`#e0e0e0`)
- Max width: 1000px

---

## Slide Templates

### Template A: Title Slide
- Centered hero text
- No header/footer
- Minimal chrome

### Template B: Content Slide (Default)
- Top-left title (72pt)
- Content area below
- Optional footer (slide number, confidential notice)

### Template C: Section Break
- Centered large text
- Full-bleed background (optional: `#0a0a0a` dark)
- White text on dark background

### Template D: Data Slide
- Small title (48pt, top-left)
- Chart dominates (80% of canvas)
- Caption/source at bottom

### Template E: Two-Column
- Title spans full width
- Content split 50/50
- Useful for comparisons

---

## Accessibility

### Color Contrast (WCAG AA)

All text meets 4.5:1 contrast ratio:
- Black on white: 21:1 ✅
- Green on white: 4.6:1 ✅ (barely passes, use for accent only)
- Light gray on white: 2.9:1 ❌ (captions only, not body text)

### Readability

- Minimum font size: 18pt (captions)
- Body text: 24pt+ (readable on Zoom)
- High contrast colors only
- No italics (harder to read)
- No light font weights (<400)

### Remote Viewing

**Zoom Test:**
- View deck at 50% size
- Can you read all text? ✅
- Can you see all chart labels? ✅
- Are colors distinguishable? ✅

---

## Export Settings

### Google Slides
- Canvas: 16:9 (1920×1080)
- Fonts: Inter (Google Fonts), fallback Helvetica
- Export as PDF: 300 DPI, embed fonts

### Keynote
- Canvas: 1920×1080 (HD)
- Fonts: Inter (download from Google Fonts), fallback SF Pro
- Export as PDF: Best Quality, embed fonts

### PowerPoint
- Canvas: 16:9 (1920×1080)
- Fonts: Inter (install locally), fallback Arial
- Export as PDF: High Quality, embed fonts

### Figma
- Frame: 1920×1080
- Export: PNG @2x, PDF (vector)
- Fonts: Inter (auto-loads from Google Fonts)

---

## File Naming Conventions

```
roostr-pitch-deck-v1.0.pdf          [Final PDF for distribution]
roostr-pitch-deck-v1.0.key          [Keynote source]
roostr-pitch-deck-v1.0.gslides      [Google Slides link]
roostr-pitch-deck-v1.0.fig          [Figma file]

roostr-deck-slide-01-cover.png      [Individual slide exports]
roostr-deck-slide-02-problem.png
...

roostr-deck-assets/                 [Asset folder]
  icons/                            [Icon exports]
  charts/                           [Chart images]
  logos/                            [roostr logo variants]
```

---

## Brand Voice (Visual)

**roostr is:**
- Lowercase (roostr, not ROOSTR or Roostr)
- Minimal (no logo needed, wordmark is enough)
- Direct (data > fluff)
- Transparent (show the numbers)
- Confident (we shipped, they didn't)
- Slightly edgy (AI-native, not AI-assisted)

**roostr is NOT:**
- Corporate (blue suits, stock photos)
- Crypto-flashy (gradients, 3D coins, rocket emojis)
- Academic (too much text, footnotes)
- Timid (small fonts, hedged language)

---

## Design Checklist

Before finalizing any slide:

- [ ] Title is 72pt Inter Bold, black
- [ ] No more than 3 colors used
- [ ] All text is 18pt+ (readable on Zoom)
- [ ] White space is generous (not cramped)
- [ ] Charts have direct labels (no legends)
- [ ] Icons are 2px stroke, black or green
- [ ] Animations are purposeful (not decorative)
- [ ] Slide passes 50% size test (readable when small)
- [ ] No gradients, drop shadows, or 3D effects
- [ ] Confidential notice on footer (if needed)

---

## Version History

**v1.0 (Feb 2026):** Initial design system for seed raise

---

**This design system is living documentation. Update as the brand evolves.**
