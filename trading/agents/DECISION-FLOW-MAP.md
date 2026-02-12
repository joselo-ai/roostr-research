# 18-Agent Decision Flow - Mind Map
**How Each Agent Makes Trading Decisions**

---

## 🎯 OVERVIEW: Signal → 18 Agents → Final Decision

```
INPUT SIGNAL
   ├─ Ticker: PGR
   ├─ Price: $245.50
   ├─ Catalyst: "Strong moat, P/E 15.2, ROE 24.3%..."
   ├─ Source: Value Screener
   └─ Asset Class: Stock
         ↓
    [18 AGENTS PARALLEL EVALUATION]
         ↓
    FINAL DECISION (BUY/SELL/HOLD)
```

---

## 🏛️ LEGENDARY INVESTOR AGENTS (12)

Each agent has **Philosophy → Keywords → Scoring Logic → Vote**

### 1. Warren Buffett - "Wonderful companies at fair prices"

**What Buffett looks for:**
```
INPUT: Catalyst text
  ↓
SCAN FOR KEYWORDS:
  ✅ Positive: "moat", "competitive advantage", "consistent earnings", 
               "quality management", "brand", "pricing power"
  ❌ Negative: "speculation", "hype", "momentum"
  
  ↓
SCORING:
  Start: 5.5/10
  + Moat found: +1.0 → 6.5
  + Consistent earnings: +1.0 → 7.5
  + Quality management: +1.0 → 8.5
  - Speculation mentioned: -0.75
  
  Final: 8.5/10
  
  ↓
VOTE LOGIC:
  IF score >= 6.0 → BUY
  IF score <= 4.0 → SELL
  ELSE → HOLD
  
  ↓
OUTPUT: BUY (8.5/10)
```

### 2. Charlie Munger - "Avoid stupidity, multidisciplinary thinking"

**What Munger looks for:**
```
SCAN FOR KEYWORDS:
  ✅ Positive: "profitable", "cash flow", "sustainable",
               "long-term", "fundamentals"
  ❌ Red Flags: "fomo", "pump", "meme", "moon", "quick gains"
  
SCORING:
  Start: 5.5/10
  + Strong fundamentals: +1.0
  + Long-term focus: +1.0
  - FOMO/hype language: -0.75 per instance
  
VOTE:
  IF score >= 6.0 → BUY
  ELSE IF score <= 4.0 → SELL
  ELSE → HOLD
```

### 3. Michael Burry - "Contrarian deep value"

**What Burry looks for:**
```
SCAN FOR KEYWORDS:
  ✅ Positive: "undervalued", "oversold", "contrarian", 
               "distressed", "mispriced", "overlooked"
  ❌ Negative: "momentum", "trending", "viral", "following herd"
  
SPECIAL CHECK:
  IF (Reddit + viral) → -1.0 (not contrarian enough)
  IF (fundamental research mentioned) → +1.0
  
VOTE:
  Contrarian setup (score >= 6.0) → BUY
  Following crowd (score < 6.0) → HOLD/SELL
```

### 4. Ben Graham - "Margin of safety"

**What Graham looks for:**
```
SCAN FOR KEYWORDS:
  ✅ Positive: "undervalued", "cheap", "discount", "bargain",
               "margin of safety", "book value", "assets"
  ❌ Negative: "growth story", "no book value", "crypto"
  
SCORING:
  Start: 5.5/10
  + Margin of safety: +1.0
  + Asset backing: +1.0
  - Growth-only story: -0.75
  - Crypto (no tangible assets): -0.75
```

### 5. Mohnish Pabrai - "Asymmetric risk/reward"

**What Pabrai looks for:**
```
SCAN FOR KEYWORDS:
  ✅ Positive: "upside", "asymmetric", "limited downside",
               "stop loss", "protect", "heads I win"
  ❌ Negative: "speculative", "high risk"
  
SPECIAL:
  IF (stop loss mentioned) → +1.0 (downside protection)
  IF (following proven investors) → +1.0 (cloning)
```

### 6. Cathie Wood - "Innovation and disruption"

**What Cathie looks for:**
```
SCAN FOR KEYWORDS:
  ✅ Positive: "innovation", "disrupt", "AI", "blockchain",
               "genomics", "fintech", "exponential", "5-year"
  ❌ Negative: "value", "traditional", "old economy"
  
SCORING:
  Start: 5.5/10
  + Innovation mentioned: +1.0
  + Exponential growth: +1.0
  + 5-year thesis: +1.0
  - Traditional/value play: -0.75
```

### 7-12. Other Legendary Investors

**Phil Fisher:** Looks for "research", "competitive advantage", "scuttlebutt"  
**Peter Lynch:** Looks for "consumer", "everyday business", "growth"  
**Bill Ackman:** Looks for "high conviction" (9+/10), "catalyst", "activist"  
**Stanley Druckenmiller:** Looks for "macro", "asymmetric", "stop loss"  
**Aswath Damodaran:** Looks for "valuation", "DCF", "cash flow", "numbers"  
**Rakesh Jhunjhunwala:** Looks for "growth", "long-term", "emerging"

---

## 📊 QUANTITATIVE AGENTS (4)

Data-driven, less narrative-focused.

### 1. Valuation Agent

**Decision Logic:**
```
SCAN FOR:
  ✅ "undervalued", "cheap", "discount", "bargain" → Score: 8.0 → BUY
  ❌ "overvalued", "expensive", "rich" → Score: 3.0 → SELL
  ⚖️  "fair value" → Score: 5.5 → HOLD
  
OUTPUT:
  Score: 8.0/10
  Recommendation: BUY
  Reasoning: "PGR appears undervalued relative to intrinsic value"
```

### 2. Sentiment Agent

**Decision Logic:**
```
CHECK SIGNAL SOURCE:
  Reddit → Check for: "🚀", "moon", "apes", "yolo"
    IF high engagement → Score: 7.0 → BUY
    ELSE → Score: 5.0 → HOLD
  
  Discord/Yieldschool → Check for: "conviction"
    IF mentioned → Score: 7.0
    ELSE → Score: 5.0
  
  No social signals → Score: 5.0 → HOLD
```

### 3. Fundamentals Agent

**Decision Logic:**
```
SCAN FOR:
  ✅ Strong: "profitable", "cash flow", "revenue growth",
            "earnings", "margin"
  ❌ Weak: "unprofitable", "burning cash", "losses"
  🎯 Catalyst: "product launch", "partnership", "contract"
  
SCORING:
  Start: 5.0
  + Strong fundamentals: +2.0
  + Catalyst: +1.0
  - Weak fundamentals: -2.0
  
  Range: 0-10
```

### 4. Technicals Agent

**Decision Logic:**
```
SCAN FOR:
  ✅ Bullish: "breakout", "golden cross", "support", 
              "oversold", "bounce"
  ❌ Bearish: "breakdown", "death cross", "resistance",
              "overbought"
  📈 Momentum: "momentum", "trending"
  
SCORING:
  Start: 5.0
  + Bullish signals: +2.0
  + Momentum: +1.0
  - Bearish signals: -2.0
```

---

## ⚠️ RISK MANAGER (Joselo 🐓)

**Validation Logic:**
```
INPUT: Combined conviction from 16 agents
  ↓
CHECK 1: Is conviction high enough?
  IF conviction < 6.0 → Flag: "Below deployment threshold"
  
CHECK 2: Asset class risk
  IF crypto AND conviction < 8.0 → Adjust: -1.0
  
CHECK 3: Catalyst clarity
  IF catalyst.length < 30 chars → Adjust: -0.5
  
CHECK 4: Stop loss defined?
  IF "stop" NOT in catalyst → Flag: "No stop mentioned"
  
  ↓
OUTPUT:
  Adjusted Conviction: 6.5/10
  Concerns: ["Crypto requires 8.0+"]
  Approved: YES/NO
```

---

## 🎲 PORTFOLIO MANAGER

**Final Decision Logic:**
```
INPUT:
  - 12 Legendary opinions (avg: 6.75/10)
  - 4 Quant opinions (avg: 6.25/10)
  - Risk Manager adjustment
  
  ↓
COMBINE (WEIGHTED):
  Final = (Legendary × 60%) + (Quant × 40%)
  Final = (6.75 × 0.6) + (6.25 × 0.4)
  Final = 6.55/10
  
  ↓
APPLY RISK MANAGER:
  IF concerns exist → may adjust down
  Final = 6.55/10 (no adjustments)
  
  ↓
MAKE DECISION:
  IF conviction >= 6.0 → BUY
  ELSE IF conviction <= 4.0 → SELL
  ELSE → HOLD
  
  ↓
CALCULATE POSITION SIZE:
  IF conviction >= 9.5 → 20% allocation
  ELSE IF conviction >= 9.0 → 15%
  ELSE IF conviction >= 7.5 → 10%
  ELSE IF conviction >= 6.5 → 7.5%
  ELSE → 5%
  
  For PGR (6.55/10) → 7.5% = $75,000
  
  ↓
OUTPUT:
  Decision: BUY
  Position: $75,000
  Stop: $220.95 (-10%)
  Max Risk: $7,500
```

---

## 📊 EXAMPLE: PGR DECISION FLOW

```
SIGNAL: PGR @ $245.50
Catalyst: "Strong moat, P/E 15.2, ROE 24.3%, consistent earnings"

┌─────────────────────────────────────────────────────────────┐
│                    12 LEGENDARY INVESTORS                    │
├─────────────────────────────────────────────────────────────┤
│ Buffett:       8.5/10 BUY  (moat + quality)                │
│ Munger:        7.5/10 BUY  (fundamentals + long-term)      │
│ Burry:         6.5/10 HOLD (contrarian but not deep value) │
│ Graham:        6.5/10 HOLD (margin of safety present)      │
│ Pabrai:        7.5/10 BUY  (asymmetric + stop mentioned)   │
│ Cathie:        6.5/10 HOLD (not innovative enough)         │
│ Fisher:        6.5/10 HOLD (competitive advantage found)   │
│ Lynch:         6.5/10 HOLD (growth story)                  │
│ Ackman:        5.5/10 HOLD (not bold enough)               │
│ Druckenmiller: 5.5/10 HOLD (no macro edge)                 │
│ Damodaran:     6.5/10 HOLD (numbers back story)            │
│ Jhunjhunwala:  7.5/10 BUY  (long-term growth)              │
├─────────────────────────────────────────────────────────────┤
│ CONSENSUS: HOLD (4 BUY, 0 SELL, 8 HOLD)                    │
│ AVG CONVICTION: 6.75/10                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      4 QUANT AGENTS                          │
├─────────────────────────────────────────────────────────────┤
│ Valuation:     8.0/10 BUY  (undervalued signal)            │
│ Sentiment:     5.0/10 HOLD (no social buzz)                │
│ Fundamentals:  7.0/10 BUY  (strong fundamentals)           │
│ Technicals:    5.0/10 HOLD (neutral chart)                 │
├─────────────────────────────────────────────────────────────┤
│ CONSENSUS: HOLD (2 BUY, 0 SELL, 2 HOLD)                    │
│ AVG SCORE: 6.25/10                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      SYNTHESIS                               │
├─────────────────────────────────────────────────────────────┤
│ Combined: (6.75 × 60%) + (6.25 × 40%) = 6.55/10            │
│ Risk Manager: ✅ No concerns                                 │
│ Final Conviction: 6.55/10                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   FINAL DECISION                             │
├─────────────────────────────────────────────────────────────┤
│ ✅ BUY (conviction >= 6.0)                                   │
│ Position: $75,000 (7.5% allocation)                         │
│ Entry: $245.50                                              │
│ Stop: $220.95 (-10%)                                        │
│ Max Risk: $7,500 (0.75% of portfolio)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 KEY TAKEAWAYS

**Decision Logic:**
1. **Each agent scans catalyst for keywords** (moat, growth, value, etc.)
2. **Starts at 5.5/10, adjusts up/down** based on matches
3. **Votes BUY (≥6.0), SELL (≤4.0), or HOLD** (between)
4. **Portfolio Manager combines** all votes (60% legendary, 40% quant)
5. **Risk Manager validates** (flags concerns, may adjust)
6. **Final decision:** ≥6.0 = BUY, ≤4.0 = SELL

**Conviction → Position Size:**
- 9.5-10.0: 20% ($200k)
- 9.0-9.5: 15% ($150k)
- 7.5-9.0: 10% ($100k)
- 6.5-7.5: 7.5% ($75k)
- 6.0-6.5: 5% ($50k)
- <6.0: HOLD (no deployment)

**Why it works:**
- Diversity of opinion (12 philosophies)
- Data validation (4 quant checks)
- Human oversight (risk manager + final approval)
- Transparent scoring (every decision documented)
