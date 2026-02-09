# Figma Handoff: roostr Pitch Deck
**Design specifications for Figma | 20 slides | February 2026**

Complete Figma setup guide for creating a pixel-perfect pitch deck with maximum design control.

---

## Why Figma?

**Advantages over Google Slides/Keynote:**
- Pixel-perfect precision (exact positioning, spacing)
- Component library (reusable elements across slides)
- Auto-layout (responsive spacing, consistent padding)
- Version control (branches, history, comments)
- Easy export (PNG, PDF, SVG, video)
- Collaboration (real-time co-editing, handoff to engineers)

**When to use Figma:**
- High-stakes pitch (flagship investors, demo day)
- Custom illustrations needed (agent diagrams, custom charts)
- Print materials (one-pagers, leave-behinds)
- Web version of deck (export to HTML/animation)

---

## File Setup

### 1. Create New Figma File

1. Go to Figma: https://figma.com
2. Click "New design file"
3. Rename: "roostr Pitch Deck v1.0"

### 2. Canvas Setup

**Frame Dimensions:**
- Width: 1920px
- Height: 1080px
- Aspect ratio: 16:9

**Create Master Frame:**
1. Press `F` (Frame tool)
2. Click "Presentation" in right sidebar
3. Select "Slide 16:9" (1920×1080)
4. Rename frame: "Slide 01 - Cover"
5. Duplicate for all 20 slides (Cmd+D / Ctrl+D, 19 times)

**Frame Organization:**
1. Arrange frames in 4×5 grid on canvas
2. Spacing between frames: 200px (for visibility)
3. Name frames sequentially:
   - Slide 01 - Cover
   - Slide 02 - Problem
   - Slide 03 - Opportunity
   - ... (etc.)

### 3. Page Organization

Create separate pages in Figma for organization:

**Page 1: "🎨 Design System"**
- Color palette
- Typography styles
- Component library
- Spacing system

**Page 2: "📊 Slides (Final)"**
- All 20 final slides
- Presentation-ready

**Page 3: "🔧 Components"**
- Reusable components (buttons, boxes, icons)
- Master components (use across slides)

**Page 4: "📝 Drafts & Explorations"**
- Experimental layouts
- Iterations
- Archive old versions

---

## Design System Setup

### Colors (Create Styles)

1. Go to "🎨 Design System" page
2. Create color swatches:
   - Draw rectangle (100×100px)
   - Fill with color
   - Right-click → "Selection colors" → "+" (create style)
   - Name style

**Color Styles to Create:**

| Style Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| `roostr/black` | #000000 | 0,0,0 | Primary text, headlines |
| `roostr/white` | #FFFFFF | 255,255,255 | Backgrounds, negative space |
| `roostr/green` | #4ade80 | 74,222,128 | Accent, CTAs, positive metrics |
| `roostr/deep-black` | #0a0a0a | 10,10,10 | Secondary backgrounds |
| `roostr/light-gray` | #e0e0e0 | 224,224,224 | Secondary text, captions |
| `roostr/neutral-gray` | #525252 | 82,82,82 | Grid lines, dividers |
| `roostr/bg-light-gray` | #f9fafb | 249,250,251 | Box backgrounds |
| `roostr/bg-light-green` | #f0fdf4 | 240,253,244 | Green box backgrounds |
| `roostr/warning-red` | #ef4444 | 239,68,68 | Risk indicators (use sparingly) |

### Typography (Create Text Styles)

**Install Fonts:**
1. Download Inter: https://fonts.google.com/specimen/Inter
2. Download JetBrains Mono: https://fonts.google.com/specimen/JetBrains+Mono
3. Install on your system (Figma auto-detects local fonts)

**Text Styles to Create:**

| Style Name | Font | Size | Weight | Line Height | Letter Spacing | Color |
|------------|------|------|--------|-------------|----------------|-------|
| `H1 - Slide Title` | Inter | 72pt | Bold (700) | 79px (110%) | -1.44px (-2%) | Black |
| `H2 - Section Header` | Inter | 48pt | Bold (700) | 58px (120%) | -0.48px (-1%) | Black |
| `H3 - Subheading` | Inter | 32pt | Semibold (600) | 42px (130%) | 0px | Black |
| `Body - Regular` | Inter | 24pt | Regular (400) | 36px (150%) | 0px | Black |
| `Body - Emphasis` | Inter | 24pt | Semibold (600) | 36px (150%) | 0px | Green |
| `Caption` | Inter | 18pt | Regular (400) | 25px (140%) | 0px | Light Gray |
| `Data Label` | JetBrains Mono | 20pt | Medium (500) | 24px (120%) | 0px | Black |
| `Hero Number` | Inter | 96pt | Bold (700) | 96px (100%) | -2.88px (-3%) | Green |
| `Large Number` | Inter | 64pt | Bold (700) | 64px (100%) | -1.28px (-2%) | Green |
| `Small Print` | Inter | 16pt | Regular (400) | 22px (140%) | 0px | Light Gray |

**How to Create Text Styles:**
1. Create text layer (press `T`)
2. Type sample text
3. Format with font, size, weight, line height, letter spacing, color
4. Right-click → "Text styles" → "+" (create style)
5. Name style (use naming convention above)
6. Delete sample text (styles are saved)

### Spacing System (Grid & Layout)

**Grid Setup (apply to each slide frame):**
1. Select slide frame
2. Right sidebar → Layout grid
3. Click "+" to add grid

**Grid Configuration:**

**Columns:**
- Count: 12
- Type: Stretch
- Margin: 120px (left/right safe zone)
- Gutter: 20px
- Color: Green (#4ade80, 10% opacity)

**Rows:**
- Count: 12
- Type: Stretch
- Margin: 80px (top/bottom safe zone)
- Gutter: 20px
- Color: Green (#4ade80, 10% opacity)

**8px Base Grid:**
- Type: Grid
- Size: 8px
- Color: Light Gray (#e0e0e0, 5% opacity)

**Toggle Grid Visibility:** Cmd+' (Ctrl+' on Windows)

### Auto-Layout (Spacing Tokens)

Create reusable spacing components:

1. Create frame
2. Right-click → "Add auto layout" (or Shift+A)
3. Set spacing (8, 16, 24, 32, 48, 64, 96, 120)
4. Save as component (Cmd+Option+K / Ctrl+Alt+K)
5. Name: `Spacing/8px`, `Spacing/16px`, etc.

**Use these components to maintain consistent spacing across slides.**

---

## Component Library

### Base Components (Create on "🔧 Components" page)

#### 1. Slide Background

**Master Component: `slide/background`**
1. Frame: 1920×1080px
2. Fill: White (#FFFFFF)
3. Create component (Cmd+Option+K)

**Variant: `slide/background-dark`**
1. Duplicate background component
2. Fill: Deep Black (#0a0a0a)
3. Add variant (right sidebar → Variants → "+")

#### 2. Slide Title

**Master Component: `slide/title`**
1. Text layer: "Slide Title Here"
2. Style: `H1 - Slide Title`
3. Position: 120px from left, 80px from top
4. Width: 1680px (auto-width, max 1680)
5. Create component

#### 3. Bullet List

**Master Component: `content/bullet-list`**
1. Frame: 800px wide, auto-height
2. Auto-layout: Vertical, 16px spacing
3. Bullet item:
   - Text: "• Bullet point text"
   - Bullet character: Green (#4ade80), 16pt
   - Text: Body Regular, 24pt, Black
4. Duplicate bullet item 4 times
5. Create component

**Usage:** Drag component onto slide, edit text

#### 4. Data Table

**Master Component: `data/table-row`**
1. Frame: 1440px wide × 64px tall
2. Auto-layout: Horizontal, 0px spacing
3. Cells: 4 columns (360px each, or custom widths)
4. Cell padding: 16px
5. Background: White (alternates with light gray)
6. Border-bottom: 1px, Light Gray (#e0e0e0)
7. Create component

**Variant: `data/table-header`**
1. Duplicate table-row component
2. Background: Deep Black (#0a0a0a)
3. Text color: White
4. Font: Inter Semibold, 20pt
5. Add variant

**Usage:** Stack header + multiple rows, alternate row backgrounds

#### 5. Callout Box

**Master Component: `content/callout-box`**
1. Frame: 1000px wide × 80px tall
2. Auto-layout: Horizontal, 24px padding
3. Background: Light Gray (#f9fafb)
4. Border-left: 4px, Green (#4ade80)
5. Text: Body Emphasis, 28pt, centered
6. Create component

**Variant: `content/callout-box-green`**
1. Duplicate callout box
2. Background: Light Green (#f0fdf4)
3. Border: 2px, all sides, Green
4. Text color: Green
5. Add variant

#### 6. Agent Card (for Slide 4)

**Master Component: `agent/card`**
1. Frame: 240px wide × 120px tall
2. Auto-layout: Vertical, 8px spacing, 24px padding
3. Background: White
4. Border: 2px, Black
5. Border radius: 8px (optional, for rounded corners)
6. Text layers:
   - Agent name: Inter Semibold, 24pt, Black, centered
   - Agent role: Inter Regular, 20pt, Black, centered
   - Agent details: Inter Regular, 18pt, Light Gray, centered
7. Create component

**Variants: `agent/scraper`, `agent/atlas`, `agent/edge`**
1. Duplicate agent card component
2. Edit text for each agent
3. Add variants

#### 7. Arrow Connector

**Master Component: `diagram/arrow`**
1. Line tool (L)
2. Stroke: 3px, Black (#000000)
3. Stroke cap: Arrow (right side only)
4. Length: 80px (horizontal)
5. Create component

**Usage:** Connect agent cards, workflow diagrams

#### 8. Icon (from Lucide)

**Import Icons:**
1. Go to https://lucide.dev
2. Search for icon (e.g., "activity", "trending-up")
3. Click "Copy SVG"
4. Paste into Figma (Cmd+V)
5. Resize to 32×32px
6. Stroke: 2px, Black
7. Create component
8. Name: `icon/activity`, `icon/trending-up`, etc.

**Create Icon Library:**
- Import 10-15 key icons (see DESIGN_SYSTEM.md for list)
- Save as components
- Use instances across slides

---

## Slide Templates

### Template A: Title Slide (Centered Hero)

**Structure:**
1. Use `slide/background` component
2. Create auto-layout frame (vertical, centered)
3. Add text layers:
   - "roostr" (Hero Number style, 96pt)
   - Tagline (H3, 36pt)
   - Three-line hook (Body Regular, 24pt)
   - GitHub link (Caption, 18pt)
4. Spacing between elements: 24-48px
5. Vertically center entire group (use auto-layout)

**Save as Component:** `template/title-slide`

### Template B: Content Slide (Default)

**Structure:**
1. Use `slide/background` component
2. Use `slide/title` component (top-left)
3. Content area: Frame below title (120px left margin, 224px top)
4. Add content (text, bullets, charts, etc.)

**Save as Component:** `template/content-slide`

### Template C: Section Break (Dark)

**Structure:**
1. Use `slide/background-dark` component
2. Create auto-layout frame (vertical, centered)
3. Add text layers (white text on dark background)
4. Vertically center entire group

**Save as Component:** `template/section-break`

### Template D: Data Slide (Chart-Dominant)

**Structure:**
1. Use `slide/background` component
2. Title: H2 style, 48pt (smaller than default), top-left
3. Chart area: 80% of canvas height
4. Caption: Small Print, bottom-center

**Save as Component:** `template/data-slide`

---

## Building Slides (Efficient Workflow)

### Workflow Steps

1. **Duplicate template:** Select template component → Duplicate (Cmd+D)
2. **Detach instance:** Right-click → Detach instance (allows editing)
3. **Edit content:** Replace placeholder text, add visuals
4. **Apply components:** Drag components from library (bullets, boxes, icons)
5. **Fine-tune spacing:** Use grid (Cmd+'), align tools (Option+A / Alt+A)
6. **Review:** Zoom out (Cmd+0), check consistency

### Slide-by-Slide Quick Guide

**Slide 1: Cover**
- Use `template/title-slide`
- Edit text layers (roostr, tagline, hook, GitHub link)
- Optional: Add subtle line under "roostr" (2px, Green)

**Slide 2: Problem**
- Use `template/content-slide`
- Title: "Traditional Hedge Funds Hit a Ceiling"
- Left column: Bullet list (use `content/bullet-list` component)
- Right column: Duplicate bullet list
- Bottom: Callout box (use `content/callout-box-green` component)

**Slide 3: Opportunity**
- Use `template/content-slide`
- Three sections stacked vertically
- Each section: Header + bullet list
- Use auto-layout frames for consistent spacing (48px between sections)

**Slide 4: Our Solution (Agent Flow)**
- Use `template/content-slide`
- Title: "3 AI Agents Replace the Entire Analyst Team"
- Agent cards: Use `agent/scraper`, `agent/atlas`, `agent/edge` components
- Arrows: Use `diagram/arrow` component between cards
- Human oversight: Caption text below cards

**Slide 5: How It Works**
- Use `template/content-slide`
- Four steps: Use auto-layout frame, 32px spacing
- Step indicators: Circle (32×32px, Green fill, white text)
- Result box: Use `content/callout-box-green` component

**Slide 6: Technology**
- Use `template/content-slide`
- Two sections (Tech Stack, Deployed Code)
- Checkmarks: Use text character (✓) in Green, or custom checkmark icon
- Proof box: Use `content/callout-box-green` component

**Slide 7: The Edges (Table)**
- Use `template/data-slide`
- Table: Use `data/table-header` + multiple `data/table-row` components
- Stack rows, alternate backgrounds (white, light gray)
- Return values: Green text
- Key insight: Text below table
- Replicable statement: Use `content/callout-box-green` component

**Slide 8: Performance Targets**
- Use `template/content-slide`
- Hero numbers: Three text layers (Large Number style, 72pt, Green)
- Labels below numbers (Caption style)
- Two sections: Comparison + Risk Management (bullet lists)

**Slide 9: Competitive Advantage (Bar Chart)**
- Use `template/data-slide`
- Chart area: Rectangle background (#f9fafb)
- Bars: Rectangles (Traditional: Black, roostr: Green)
  - Traditional: 160px tall (proportional to 50%)
  - roostr: 320px tall (proportional to 99%)
- Values above bars (48pt Bold)
- Chart labels below bars
- Other advantages: Bullet list
- Scaling statement: Use `content/callout-box-green` component

**Slide 10: Economics of Scale (Table)**
- Use `template/data-slide`
- Cost comparison table (use table components)
- Highlight row 3 ($100M) with light green background
- Key insight below table
- Implications: Bullet list with roostr line in green

**Slides 11-20:**
- Follow same pattern: Use appropriate template, add components
- Maintain consistent spacing (8px base, 16-64px between sections)
- Use green strategically (emphasis only, not overused)

---

## Advanced Techniques

### Prototyping (Interactive Deck)

**Add Slide Navigation:**
1. Select all slide frames
2. Click "Prototype" tab (right sidebar)
3. Add interaction: "On click" → "Navigate to" → "Next slide"
4. Transition: "Instant" or "Dissolve" (300ms)
5. Click "Present" (▶️ button, top-right) to test

**Add Animations (Build Sequence):**
1. Duplicate slide frame (before and after states)
2. Create variants (e.g., "Step 1", "Step 2", "Step 3")
3. Link variants in Prototype mode
4. Use "Smart Animate" transition (detects changes, animates automatically)

**Example: Slide 9 Bar Chart Animation**
- Variant 1: Bars at 0px height
- Variant 2: Bars at full height
- Prototype: Variant 1 → Variant 2, Smart Animate, 500ms

### Custom Charts (Data Visualization)

**Bar Chart:**
1. Rectangles for bars (width/height proportional to data)
2. Auto-layout frame for multiple bars (horizontal, 8px spacing)
3. Text labels above/below bars (Data Label style)
4. Grid lines: Horizontal lines, 1px, Light Gray, 25% opacity

**Line Chart:**
1. Pen tool (P) to draw line path
2. Stroke: 3px, Green
3. Points: Circles (8px diameter, Green fill)
4. Area fill: Duplicate line path, close path, fill with Green (20% opacity)
5. Axes: Lines (1px, Light Gray)
6. Labels: Data Label style

**Table:**
- Use `data/table-row` components (stack vertically)
- Auto-layout for rows (0px spacing)
- Alternate row backgrounds (white, light gray)

### Exporting Assets

**Export Settings:**
1. Select frame/layer
2. Right sidebar → Export
3. Click "+" to add export setting

**Export Configurations:**

**Full Slides (for presentation):**
- Format: PDF
- Scale: 1x
- Select all 20 slide frames → Export

**Individual Slides (for social media):**
- Format: PNG
- Scale: 2x (@2x for retina)
- Select specific slide → Export

**Vector Assets (for print):**
- Format: SVG
- Select specific elements (icons, logos) → Export

**Thumbnails (for preview):**
- Format: JPG
- Quality: 80%
- Scale: 0.5x
- Select all slides → Export

---

## Collaboration & Handoff

### Sharing with Team

**Share Link:**
1. Click "Share" button (top-right)
2. Copy link
3. Set permissions:
   - **Can edit:** Full design control (co-founders)
   - **Can view:** Read-only, can comment (advisors, investors)

**Comments:**
- Click "Comment" tool (C)
- Click on canvas to add comment
- Tag collaborators: @username
- Resolve comments when addressed

### Developer Handoff (if building web version)

**Inspect Mode:**
1. Share link with developer
2. Developer opens in "Inspect" mode (automatic for developers)
3. Developer can:
   - View CSS (copy exact spacing, colors, fonts)
   - Export assets (icons, images)
   - Measure distances

**Export Code:**
- Use plugins: "Figma to HTML" or "Anima" for automatic code export
- Export CSS variables for design tokens (colors, spacing, typography)

---

## Version Control

### Branching (for Experimentation)

1. Click file name dropdown (top-left)
2. Click "Create branch"
3. Name branch: "experiment-charts" (or specific task)
4. Make changes in branch (won't affect main)
5. Merge branch: "Review and merge to main" (if changes approved)

### Version History

1. File name dropdown → "Show version history"
2. View all changes, restore previous versions
3. Name versions: Click version → "Name this version" (e.g., "v1.0 - Seed Raise")

### Duplicating File (for Customization)

1. File name dropdown → "Duplicate"
2. Rename: "roostr Pitch - [VC Name]"
3. Customize for specific investor

---

## Plugins (Recommended)

### Design Efficiency

**Iconify** (Free)
- Search and insert 100,000+ icons (Lucide, Feather, etc.)
- Install: Plugins → Browse plugins → Search "Iconify" → Install
- Usage: Plugins → Iconify → Search "trending-up" → Insert

**Unsplash** (Free)
- Insert high-quality stock photos
- Usage: Plugins → Unsplash → Search → Insert

**Charts** (Free)
- Generate editable charts (bar, line, pie)
- Usage: Plugins → Charts → Select type → Configure data → Insert

### Content Population

**Content Reel** (Free)
- Populate text with realistic content
- Usage: Select text layer → Plugins → Content Reel → Choose content type

**Google Sheets Sync** (Free)
- Sync data from Google Sheets to Figma tables
- Usage: Link Google Sheet → Auto-update table data

### Export & Presentation

**Pitchdeck** (Free)
- Export Figma slides as PDF presentation
- Usage: Plugins → Pitchdeck → Select slides → Export PDF

**Figmotion** (Paid, $12/mo)
- Add animations (fade, slide, scale)
- Export as video (MP4) or animated GIF
- Usage: Plugins → Figmotion → Add keyframes → Export

---

## Performance Optimization

### Keep File Size Small

- **Flatten layers:** Merge unnecessary layers (Cmd+E / Ctrl+E)
- **Outline text:** Convert text to vector paths (right-click → Outline stroke) for final export
- **Optimize images:** Compress images before importing (use TinyPNG.com)
- **Remove unused components:** Clean up component library

### Faster Rendering

- **Hide unnecessary layers:** Toggle visibility (Cmd+Shift+H / Ctrl+Shift+H)
- **Reduce effects:** Avoid excessive shadows, blurs
- **Simplify complex paths:** Use fewer vector points

---

## Quality Checklist

Before finalizing deck:

- [ ] All 20 slides created on "📊 Slides (Final)" page
- [ ] Consistent use of text styles (no custom formatting outside styles)
- [ ] Consistent use of color styles (no hard-coded colors)
- [ ] All components used (no duplicated elements that should be components)
- [ ] Grid alignment (all elements snap to 8px grid)
- [ ] Margins consistent (120px left/right, 80px top/bottom)
- [ ] Animations tested in Prototype mode (if applicable)
- [ ] Exported PDF tested (fonts embedded, colors correct)
- [ ] Zoomed out view (Cmd+0) - all slides visually consistent
- [ ] Mobile/small screen test (zoom to 25%) - readable?
- [ ] Version named ("v1.0 - Seed Raise")
- [ ] File shared with team (appropriate permissions)

---

## Export Checklist

### For Presentation

**PDF (Standard):**
- [ ] Select all 20 slide frames
- [ ] Export → PDF, 1x scale
- [ ] Test PDF (open in Adobe Reader, fonts embedded?)
- [ ] Filename: `roostr-pitch-deck-v1.0.pdf`

**PDF (Print-Quality):**
- [ ] Export → PDF, 2x scale
- [ ] For print materials, leave-behinds
- [ ] Filename: `roostr-pitch-deck-v1.0-print.pdf`

### For Social Media

**PNG (Individual Slides):**
- [ ] Select specific slides (e.g., Slide 1 Cover, Slide 9 Margins)
- [ ] Export → PNG, 2x scale
- [ ] For Twitter, LinkedIn posts
- [ ] Filenames: `roostr-slide-01-cover@2x.png`

### For Web

**SVG (Vector Assets):**
- [ ] Select icons, logos, diagrams
- [ ] Export → SVG
- [ ] For web developers (scalable, crisp on any screen)

---

## Presentation Tips (Using Figma)

### Full-Screen Presentation

1. Click "Present" button (▶️, top-right)
2. Full-screen mode opens
3. Navigation:
   - **Next slide:** Right arrow, Space, Click
   - **Previous slide:** Left arrow
   - **Exit:** Esc

### Remote Presenting (Zoom + Figma)

1. Start Zoom meeting
2. Share screen → Select Figma window
3. Enter Figma Presentation mode
4. Zoom settings:
   - ✅ Optimize for video clip (smoother)
   - ✅ Share computer sound (if using audio)

**Pro tip:** Use dual monitors
- Monitor 1: Zoom (audience view)
- Monitor 2: Figma in edit mode (see notes, next slide)

---

## Advanced: Animated Deck (Video Export)

### Using Figmotion Plugin (Optional)

**Create Animated Slides:**
1. Install Figmotion plugin
2. Select slide frame
3. Add keyframes:
   - Keyframe 1 (0s): Initial state (e.g., bar at 0px height)
   - Keyframe 2 (0.5s): Final state (e.g., bar at full height)
4. Set easing (ease-out)
5. Repeat for all animated elements

**Export as Video:**
1. Plugins → Figmotion → Export
2. Format: MP4 (H.264)
3. Resolution: 1920×1080 (Full HD)
4. Frame rate: 30fps
5. Export

**Usage:**
- Auto-playing demo (website, email)
- YouTube/Vimeo upload (public pitch deck)
- Investor portal (self-serve viewing)

---

## Troubleshooting

### Fonts Not Loading
- **Issue:** Inter or JetBrains Mono missing
- **Solution:** Download fonts, install on system, restart Figma

### Components Not Syncing
- **Issue:** Changes to master component don't update instances
- **Solution:** Ensure instance is not detached. Right-click instance → "Reset instance" to sync.

### Export Quality Low
- **Issue:** PDF/PNG looks pixelated
- **Solution:** Export at 2x scale. Check "Include bleed" for print exports.

### File Too Large
- **Issue:** Figma file slow to load
- **Solution:** Flatten complex layers, compress images, remove unused components.

### Animations Not Playing
- **Issue:** Prototype mode animations don't work
- **Solution:** Verify interactions added in Prototype tab. Use "Smart Animate" for smooth transitions.

---

## Resources

### Learning Figma
- **Figma Basics:** https://help.figma.com/hc/en-us/categories/360002051613
- **Auto-layout Guide:** https://help.figma.com/hc/en-us/articles/360040451373
- **Components Guide:** https://help.figma.com/hc/en-us/articles/360038662654

### Design Inspiration
- **Pitch Deck Templates:** Search Figma Community for "pitch deck"
- **Data Visualization:** Search for "charts" or "infographics"
- **Icon Libraries:** Iconify plugin (Lucide icons recommended)

### Figma Community
- **roostr Template (if created):** Share on Figma Community for others to use
- **Pitch Deck Templates:** Browse community for inspiration

---

## Final Notes

**Figma vs. Google Slides:**
- **Figma:** Pixel-perfect, custom visuals, design handoff
- **Google Slides:** Speed, collaboration, investor familiarity

**Recommendation:**
1. Build deck in Google Slides first (fast iteration)
2. Recreate in Figma for final polish (high-stakes pitches)
3. Export Figma → PDF for presentation

**Time Estimate:**
- Google Slides build: 2-3 hours
- Figma build (from scratch): 4-6 hours
- Figma build (from Google Slides): 6-8 hours (pixel-perfect recreation)

---

**This Figma guide enables maximum design control. Use it for flagship investor pitches where visual perfection matters.**

**Ready to design? Open Figma and start building.** 🎨
