# roostr Pitch Deck Design Guide
## Visual Design Recommendations for Keynote/PowerPoint

---

## Brand Identity

### roostr Brand Principles
- **Lowercase everything** — roostr, not ROOSTR or Roostr
- **Minimal, not corporate** — Clean lines, no gradients, no stock photos
- **Data-driven** — Numbers speak louder than buzzwords
- **Transparent** — Building in public, nothing to hide
- **Confident, not hype** — We shipped. Competitors are still talking.

---

## Color Palette

### Primary Colors
- **Black (#000000)** — Primary text, headers, logos
- **White (#FFFFFF)** — Backgrounds, negative space
- **Green (#00FF00 or #00D100)** — Accent color for wins, key metrics, CTAs

### Secondary Colors (use sparingly)
- **Red (#FF0000)** — Only for negative comparisons (traditional fund margins)
- **Gray (#F5F5F5)** — Background variation, subtle sections
- **Dark Gray (#666666)** — Secondary text, captions

### Color Usage Rules
- 80% black/white (dominant)
- 15% green (highlights, wins)
- 5% red (contrast, competitors)
- Never use blue (generic finance color — we're different)

---

## Typography

### Font Hierarchy
**Primary font: Inter** (modern, clean, works at all sizes)
- Download: https://rsms.me/inter/

**Alternative: Helvetica Neue** (if Inter unavailable)

### Font Sizes
- **Slide titles:** 48-72pt (bold)
- **Section headers:** 36-48pt (bold)
- **Body text:** 24-28pt (regular)
- **Captions/footnotes:** 18-20pt (light)
- **Key metrics:** 72-96pt (bold, green)

### Font Weight Usage
- **Bold (700):** Titles, headers, key stats
- **Regular (400):** Body text, bullet points
- **Light (300):** Captions, footnotes

### Line Spacing
- Headers: 1.1x
- Body text: 1.4x
- Bullet points: 1.5x spacing between items

---

## Layout System

### Grid Structure
- Use a **12-column grid** for consistency
- 80px margin on all sides (more whitespace = cleaner)
- Align all elements to grid (no random placement)

### Slide Layouts (4 templates)

**1. Title Slide**
- Center-aligned
- Large title (72pt)
- Subtitle (36pt)
- Minimal background (solid white or subtle gray)

**2. Two-Column Layout**
- 60/40 split (text left, visual right)
- Vertical center alignment
- Use for comparisons, problem/solution

**3. Centered Content**
- Single-column, centered
- Use for key stats, big reveals
- Maximum visual impact

**4. Data/Table Slide**
- Full-width table or chart
- Title at top (48pt)
- Minimal borders (1px, gray)

### Whitespace Rules
- **Minimum 80px margins** on all sides
- **100-120px between sections** (vertical spacing)
- **40-60px between elements** (headers → body)
- When in doubt, add more whitespace

---

## Visual Elements

### Icons
**Style:** Line icons (not filled, not 3D)
**Size:** 64-80px
**Color:** Black or green (match text)
**Sources:**
- Noun Project (https://thenounproject.com)
- Feather Icons (https://feathericons.com)
- Heroicons (https://heroicons.com)

**Recommended icons:**
- Scraper agent: Magnifying glass 🔍
- Atlas agent: Shield 🛡️
- Edge agent: Line chart 📈
- 24/7: Clock ⏰
- Scalability: Arrow up 📊
- Margins: Dollar sign 💰

### Charts & Graphs
**Style:** Minimal, no 3D, no drop shadows
**Colors:** Black lines, green highlights
**Grid:** Light gray (subtle, 0.5px lines)

**Chart types to use:**
- **Line charts:** Growth, performance over time
- **Bar charts:** Comparisons (roostr vs traditional)
- **Tables:** Data-heavy slides (edges, milestones)
- **Flow diagrams:** Process (How It Works)

**Avoid:**
- Pie charts (too corporate, hard to read)
- 3D charts (looks dated)
- Too many data points (keep it simple)

### Architecture Diagrams
**Style:** Boxes + arrows (no complex flowcharts)
**Layout:** Horizontal flow (left → right) or vertical layers
**Colors:** Black boxes, green arrows, white text

**Example (AI agent architecture):**
```
[Data Layer] → [Intelligence Layer] → [Validation Layer] → [Execution Layer]
```

Each layer: Black box (rounded corners), white text, green connectors

---

## Slide-Specific Design Notes

### Slide 1: Cover
- **Background:** Solid black with white text (inverted for impact)
- **roostr logo:** White, lowercase, 72pt
- **Tagline:** Green, 36pt
- **Optional:** Subtle animated gradient (black → dark green)

### Slide 2: The Problem
- **Left column:** Text (black background, white text for contrast)
- **Right column:** Line chart (traditional fund costs scaling linearly)
- **Key stat:** Red text box — "Linear cost scaling kills margins"

### Slide 3: The Opportunity
- **Background:** White
- **3 columns:** Icons at top, text below
- **Market stat:** 72pt green — "$4 Trillion"
- **Callout box:** Green border, white background

### Slide 7: The Edges (Table)
- **Table design:** Minimal borders (1px gray)
- **Header row:** Black background, white text
- **Data rows:** White background, black text
- **Returns column:** Green text (highlight wins)
- **Status column:** Checkmarks (green) or icons

### Slide 8: Performance Targets
- **3 key metrics:** 96pt green, centered
- **Comparison table below:** roostr row highlighted (green background)
- **Visual:** Optional line chart showing roostr vs competitors

### Slide 9: Competitive Advantage
- **Two boxes:** Side-by-side comparison
- **roostr box:** Green border, 99% margin in large text
- **Traditional box:** Red border, 40-60% margin
- **Icons below:** 4 icons in a row (24/7, bandwidth, etc.)

### Slide 15: The Ask
- **Two options:** Side-by-side boxes
- **Left box (equity):** Green border
- **Right box (AUM):** Green border
- **CTA button:** Green background, white text — "Let's Talk"

### Slide 20: Contact
- **Background:** Black (inverted again for impact)
- **roostr logo:** White, large (96pt)
- **Contact info:** White text
- **CTA:** Green button — "Schedule a Call"

---

## Animation & Transitions

### Transition Rules
- **Between slides:** Fade (0.3s duration)
- **Within slides:** Fade in (0.5s delay)
- **No:** Fly-ins, bounces, spins (too cheesy)

### Animation Sequence (for complex slides)
1. Title fades in (0s)
2. Section 1 fades in (0.3s)
3. Section 2 fades in (0.6s)
4. Section 3 fades in (0.9s)

**Use animations sparingly** — only for slides with 3+ sections

---

## Image & Media Guidelines

### Photos
**Style:** Black & white or desaturated (no vibrant colors)
**Subject:** Abstract tech imagery (networks, data, code)
**Placement:** Background (subtle opacity: 20-30%) or right column

**Avoid:**
- Stock photos of people in suits (too corporate)
- Generic "handshake" or "office" photos
- Colorful, distracting images

### Screenshots (if showing dashboard)
**Treatment:** 
- Border: 2px black
- Drop shadow: Subtle (10px blur, 20% opacity)
- Placement: Right column or full-slide

### Code Snippets (if showing infrastructure)
**Style:** Dark terminal theme (black background, green text)
**Font:** Monospace (JetBrains Mono or Courier New)
**Size:** 18-20pt (readable but not dominant)

---

## Presentation Tips

### Slide Timing
- **Cover slide:** 5 seconds (let it sink in)
- **Problem/Opportunity:** 60 seconds each (build tension)
- **Solution/Technology:** 90 seconds (this is the meat)
- **Performance/Edges:** 60 seconds (data speaks for itself)
- **The Ask:** 120 seconds (most important slide)

**Total deck time:** 15-20 minutes (leave 10 min for Q&A)

### Presenter Notes (what to say, not on slides)

**Slide 7 (Edges):**
"Notice these aren't backtests. Dan's TAO trade was real — he posted it publicly in April 2023, and rode it to 1000x. Our system can detect these patterns early."

**Slide 9 (Competitive Advantage):**
"Traditional funds can't get to 99% margins. They have to pay analysts $200k/year. We don't. This is a software business disguised as a hedge fund."

**Slide 15 (The Ask):**
"We're offering two structures. If you want equity exposure, we're raising at a $10M valuation. If you want immediate returns, invest directly into the fund and get a warrant. Either way, you're early."

**Slide 18 (Why Now):**
"This couldn't have been built 12 months ago. Claude Sonnet 4 launched in January 2025. We built this in 2 hours. Citadel will take 2 years. First-mover advantage is everything."

---

## Export Settings

### PDF Export (for email)
- Resolution: 300 DPI
- Embed fonts: Yes
- Compress images: No (keep quality high)
- File size target: <10 MB

### PowerPoint (.pptx) Export
- Compatibility: Office 2016 or later
- Embed fonts: Yes
- Include animations: Optional (some investors hate animations)

### Print Settings (if printing)
- Paper: 16:9 aspect ratio (not 4:3)
- Size: Tabloid (11x17) or A3
- Color: Full color (not B&W)

---

## Quality Checklist (Before Sending)

### Content
- [ ] All numbers accurate (65-110%, Sharpe 2.1-2.8, etc.)
- [ ] No typos (spell-check + manual review)
- [ ] Consistent terminology (AI-native, not AI-driven or AI-powered)
- [ ] roostr always lowercase

### Design
- [ ] All slides use consistent fonts (Inter or Helvetica)
- [ ] Color palette: Black/white/green only
- [ ] 80px margins on all slides
- [ ] Icons are consistent style (line icons, not mixed)
- [ ] Charts have minimal styling (no 3D, no excessive colors)

### Technical
- [ ] PDF exports correctly (fonts embedded)
- [ ] File size <10 MB
- [ ] All links work (GitHub, dashboard)
- [ ] Animations are subtle (if included)

---

## Platform-Specific Notes

### Keynote (Mac)
- Use "Bold" theme as starting point (minimal, clean)
- Custom color palette: Create swatches for black/white/green
- Master slides: Create 4 templates (title, two-column, centered, data)
- Export: File → Export To → PDF (Best Quality)

### PowerPoint (Windows/Mac)
- Use "Facet" or "Ion" theme (closest to roostr style)
- Custom colors: Design → Colors → Customize Colors
- Slide master: View → Slide Master (create templates)
- Export: File → Export → Create PDF

### Google Slides
- Use "Simple Light" theme
- Custom colors: Slide → Edit Theme → Colors
- Fonts: Format → Theme → Font pairing (use Roboto or Arial)
- Export: File → Download → PDF Document

---

## Inspiration & References

### Design Style Similar To:
- **Stripe pitch decks** — Minimal, data-driven
- **Linear product pages** — Clean typography, lots of whitespace
- **Apple keynotes** — Bold statements, simple visuals

### What NOT to Emulate:
- Traditional finance decks (too corporate, boring)
- SaaS pitch decks (too colorful, too many icons)
- VC-style decks (too much text, too dense)

---

## Final Notes

**roostr's design philosophy:**
- Less is more (fewer words, more impact)
- Data > buzzwords (show the 77%, 1000x, 99% margins)
- Confidence > hype (we shipped in 2 hours, that's the flex)

**The deck should feel like:**
- A technical product demo (not a sales pitch)
- A proven track record (not a future vision)
- A no-brainer investment (not a risky bet)

**Remember:**
You're not asking for money. You're offering an opportunity to get in early on the first AI-native hedge fund. Act like it.

---

**Good luck. Go raise $2M. 🚀**
