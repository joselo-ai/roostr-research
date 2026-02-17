# 19-Agent System Build Plan
**Goal:** Implement full evaluation logic for all 16 placeholder agents  
**Timeline:** 8-16 hours (parallel work possible)  
**Status:** 7/19 operational (Buffett, Burry, Munger + 4 Quant agents)  
**Phase 1 Status:** ✅ **COMPLETE** (Feb 17, 2026)

---

## Priority Order (Implementation Sequence)

### Phase 1: Quant Agents (Data-Driven) - ✅ **COMPLETE** (Feb 17, 2026)
**Why first:** Objective, data-driven, reusable across all signals  
**Status:** All 4 agents operational with real API integrations

1. **✅ Valuation Agent** (COMPLETE)
   - ✅ Pulls P/E, P/B, EV/EBITDA, PEG from yfinance API
   - ✅ Compares to sector median (20x baseline)
   - ✅ Multi-method valuation scoring
   - **Output:** Intrinsic value estimate, cheap/fair/expensive (0-10 conviction)
   - **Test:** SPHR = 3.33/10 SELL (overvalued)

2. **✅ Technical Agent** (COMPLETE)
   - ✅ RSI (14-day), MACD (12/26/9), Moving Averages (50/200 DMA)
   - ✅ Volume trend analysis
   - ✅ Golden/death cross detection
   - **Output:** Bullish/neutral/bearish technicals (0-10 conviction)
   - **Test:** SPHR = 5.5/10 BUY (moderately bullish)

3. **✅ Fundamentals Agent** (COMPLETE)
   - ✅ ROE, Debt/Equity, Free Cash Flow yield
   - ✅ Revenue growth (27.9% for SPHR), margin trends
   - ✅ Balance sheet health scoring
   - **Output:** Strong/medium/weak fundamentals (0-10 conviction)
   - **Test:** SPHR = 6.1/10 BUY (strong growth)

4. **✅ Sentiment Agent** (COMPLETE)
   - ✅ News sentiment analysis (TextBlob on yfinance news)
   - ✅ Reddit API ready (optional, disabled if not configured)
   - ✅ Social momentum proxy via volume trends
   - **Output:** Bullish/neutral/bearish crowd sentiment (0-10 conviction)
   - **Test:** SPHR = 5.5/10 BUY (moderately bullish)

**Deliverables:**
- `quant_agents_v2.py` (850+ lines, full implementation)
- `test_phase1.py` (automated validation suite)
- Updated JSON configs (quant_valuation.json, etc.)
- `PHASE1_COMPLETION_REPORT.md` (detailed documentation)
- Test results: SPHR, AAPL, TSLA (100% success, 0 ABSTAIN votes)

---

### Phase 2: Valuation Specialists - 3 agents, 2-3 hours
**Why next:** Critical for Citi-style comp analysis

5. **✅ Aswath Damodaran** (1.5 hours)
   - DCF valuation (WACC, terminal value, growth assumptions)
   - Comp analysis (peer multiples)
   - Story-to-numbers framework
   - **Output:** Intrinsic value range, margin of safety

6. **✅ Benjamin Graham** (1 hour)
   - Net-net working capital
   - P/B < 0.67, P/E < 15 screens
   - Margin of safety calculation
   - **Output:** Value score, buy/pass based on safety margin

7. **✅ Peter Lynch** (1 hour)
   - PEG ratio analysis (growth at reasonable price)
   - 10-bagger screening (high growth + reasonable P/E)
   - Simplicity check (can you explain the business?)
   - **Output:** 10-bagger score, conviction on growth

---

### Phase 3: Growth & Innovation - 3 agents, 2-3 hours

8. **✅ Cathie Wood** (1 hour)
   - Innovation score (AI, biotech, fintech, disruption)
   - 5-year growth potential (ignore current P/E)
   - TAM expansion (addressable market growing?)
   - **Output:** Disruptive innovation score, 5-year price target

9. **✅ Phil Fisher** (1 hour)
   - Scuttlebutt research (customer/employee feedback)
   - Long-term growth quality (sustainable advantages)
   - Management quality proxy
   - **Output:** Quality growth score, hold forever conviction

10. **✅ Rakesh Jhunjhunwala** (45 min)
    - Emerging market exposure (India, LatAm, SEA)
    - Long-term growth + compounding
    - Risk appetite for high-growth names
    - **Output:** Growth conviction, multi-year hold score

---

### Phase 4: Catalyst & Macro - 3 agents, 2 hours

11. **✅ Bill Ackman** (1 hour)
    - Activist catalyst (management change, asset sales, spinoffs)
    - Bold concentrated bet logic
    - Value unlock potential
    - **Output:** Catalyst score, position size recommendation

12. **✅ Stanley Druckenmiller** (1 hour)
    - Macro overlay (rates, inflation, GDP, consumer trends)
    - Asymmetric bet sizing (high conviction = big bet)
    - Cut losers fast logic
    - **Output:** Macro score, position size based on conviction

13. **✅ Mohnish Pabrai** (45 min)
    - Dhandho framework (heads I win, tails I don't lose much)
    - Asymmetric risk/reward calculation
    - Downside protection focus
    - **Output:** Asymmetry score, risk/reward ratio

---

### Phase 5: Specialty & Synthesis - 3 agents, 1-2 hours

14. **✅ Charlie Munger** (ALREADY BUILT)
    - Inversion & mental models
    - Multidisciplinary thinking
    - "Wonderful business at fair price"

15. **✅ Warren Buffett** (ALREADY BUILT)
    - Quality moat analysis
    - Owner earnings, durable competitive advantage
    - Long-term hold conviction

16. **✅ Michael Burry** (ALREADY BUILT)
    - Contrarian deep value
    - Downside math, margin of safety
    - Bet against consensus

17. **✅ Synthesizer** (45 min)
    - Aggregate all 18 agent votes
    - Identify consensus vs outliers
    - Weight by agent specialty (e.g., Damodaran heavy on valuation questions)
    - **Output:** Ensemble conviction score

18. **✅ Risk Manager (Joselo)** (ALREADY BUILT)
    - Governance gatekeeper
    - Position sizing, stop-loss enforcement
    - Portfolio exposure limits

19. **✅ John C. Hull** (FIXED)
    - VaR, tail risk, stress testing
    - Quantitative risk overlay

---

## Implementation Strategy

### Code Structure
Each agent needs:
1. **evaluate(signal, data) method** - Core logic
2. **Data fetching** - Pull from APIs/databases
3. **Scoring logic** - Return conviction 0-10 + BUY/SELL/HOLD/PASS
4. **Rationale generation** - First-person explanation of vote
5. **Key factors dict** - Metrics used in decision

### Data Sources to Integrate
- **Financial Datasets API** (Dexter integration) - Income statements, balance sheets, SEC filings
- **TradingView API** - Price, RSI, MACD, volume
- **Reddit API** - wallstreetbets, stocks mentions + sentiment
- **Twitter/X API** - Ticker mentions + sentiment
- **News APIs** - Headlines, sentiment analysis

### Testing Approach
- Start with SPHR (current signal)
- Test each agent individually on SPHR
- Verify output format matches expected template
- Run full 19-agent deliberation
- Compare to manual analysis (this Citi comp doc)

---

## Success Criteria

**Phase 1 Complete:** All 4 Quant agents return data-driven scores (not ABSTAIN)  
**Phase 2 Complete:** Damodaran, Graham, Lynch provide valuation/value scores  
**Phase 3 Complete:** Wood, Fisher, Jhunjhunwala provide growth scores  
**Phase 4 Complete:** Ackman, Druckenmiller, Pabrai provide catalyst/macro scores  
**Phase 5 Complete:** Synthesizer aggregates all votes, Risk layers approve  

**Final Test:** Run SPHR through all 19 agents, get conviction score ≥7.0 or ≤4.0 (not 5.0 ABSTAIN)

---

## Time Estimates

- Phase 1 (Quants): 2-3 hours
- Phase 2 (Valuation): 2-3 hours
- Phase 3 (Growth): 2-3 hours
- Phase 4 (Catalyst/Macro): 2 hours
- Phase 5 (Synthesis): 1 hour
- Testing & Integration: 2 hours

**Total: 11-14 hours of focused work**

With parallel execution (multiple agents at once), could compress to 8-10 hours.

---

**Next Steps:**
1. Start with Phase 1 (Quant Agents) - highest leverage
2. Test each agent on SPHR immediately after building
3. Iterate to Phase 2-5
4. Run full deliberation on SPHR when complete
5. Post results to Discord #research

