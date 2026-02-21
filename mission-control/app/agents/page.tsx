export default function AgentsPage() {
  const agents = {
    legendary: [
      { 
        name: "Warren Buffett", 
        focus: "Quality Owner", 
        status: "active",
        philosophy: "Buy wonderful companies at fair prices. Hold forever. Circle of competence. Strong moats, predictable earnings, honest management. Patient capital.",
        soul: "The Oracle - Patient, disciplined, folksy wisdom. Sees through hype to true value."
      },
      { 
        name: "Charlie Munger", 
        focus: "Inversion & Mental Models", 
        status: "active",
        philosophy: "Invert, always invert. Multi-disciplinary thinking. Avoid stupidity over seeking brilliance. Latticework of mental models from psychology, economics, physics.",
        soul: "The Sage - Brutally honest, intellectually rigorous, no patience for nonsense."
      },
      { 
        name: "Michael Burry", 
        focus: "Contrarian Math", 
        status: "active",
        philosophy: "Deep value through exhaustive research. Bet big when others panic. Subprime crisis prediction through reading prospectuses. Math over narratives.",
        soul: "The Contrarian - Socially awkward genius. Sees what others miss. Comfortable being early and alone."
      },
      { 
        name: "Benjamin Graham", 
        focus: "Margin of Safety", 
        status: "active",
        philosophy: "Father of value investing. Price vs. intrinsic value. Margin of safety is paramount. Mr. Market's mood swings create opportunities. Quantitative screens.",
        soul: "The Professor - Methodical, academic, risk-averse. Teaches others to be rational when markets aren't."
      },
      { 
        name: "Peter Lynch", 
        focus: "Simplicity", 
        status: "active",
        philosophy: "Invest in what you know. 10-baggers come from obvious places. PEG ratio. Visit stores, talk to customers. Growth at reasonable price (GARP).",
        soul: "The Detective - Curious, observant, loves the hunt. Finds winners in everyday life."
      },
      { 
        name: "Phil Fisher", 
        focus: "Scuttlebutt", 
        status: "active",
        philosophy: "Quality growth investing. Talk to customers, suppliers, competitors. 15-point checklist. Superior management is key. Hold concentrated positions for decades.",
        soul: "The Investigator - Thorough researcher. Values people over numbers. Long-term compounder."
      },
      { 
        name: "Mohnish Pabrai", 
        focus: "Asymmetry", 
        status: "active",
        philosophy: "Heads I win big, tails I don't lose much. Copy great investors (cloning). Low-risk, high-uncertainty bets. Concentrated portfolio. Patient capital.",
        soul: "The Opportunist - Shameless cloner. Seeks asymmetric payoffs. Margin of safety fanatic."
      },
      { 
        name: "Bill Ackman", 
        focus: "Catalyst", 
        status: "active",
        philosophy: "Activist investing. Catalyst-driven. Deep value + corporate change. Large, concentrated bets. Push management for shareholder value. Public campaigns.",
        soul: "The Activist - Confident, aggressive, vocal. Forces change rather than waiting for it."
      },
      { 
        name: "Stan Druckenmiller", 
        focus: "Macro", 
        status: "active",
        philosophy: "Top-down macro + bottom-up stock picking. Reflexivity. Big position sizing when conviction high. Risk management through position sizing, not stops.",
        soul: "The Macro Trader - Intellectually flexible. Sees big picture trends. Bets big when right."
      },
      { 
        name: "Aswath Damodaran", 
        focus: "Valuation", 
        status: "active",
        philosophy: "Everything has a price. DCF modeling. Cost of capital. Growth vs. value. Numbers tell the story. Academic rigor meets market reality.",
        soul: "The Valuation Dean - Analytical, precise, educational. Believes markets can be wrong but models are honest."
      },
      { 
        name: "Rakesh Jhunjhunwala", 
        focus: "Growth", 
        status: "active",
        philosophy: "Big Bull of India. Growth investing. Long-term conviction. Spot secular trends early. Hold through volatility. Position sizing on conviction.",
        soul: "The Bull - Optimistic, bold, passionate. Sees opportunity where others see risk."
      },
      { 
        name: "Cathie Wood", 
        focus: "Innovation", 
        status: "active",
        philosophy: "Disruptive innovation investing. 5-year time horizon. Genomics, AI, blockchain, robotics. Exponential growth potential. Price targets based on addressable market.",
        soul: "The Futurist - Visionary, tech-obsessed, conviction-driven. Bets on tomorrow, not yesterday."
      },
    ],
    quant: [
      { 
        name: "Quant Valuation", 
        focus: "P/E, DCF, Fair Value", 
        status: "active",
        philosophy: "Numbers don't lie. Discounted cash flow analysis. P/E ratios vs. sector averages. Fair value computation. Statistical arbitrage.",
        soul: "The Calculator - Cold, logical, emotionless. Only cares about mathematical truth."
      },
      { 
        name: "Quant Sentiment", 
        focus: "Social Signals", 
        status: "active",
        philosophy: "Crowd psychology drives short-term moves. Reddit engagement, Twitter mentions, Discord conviction levels. Viral stock detection.",
        soul: "The Listener - Monitors the hive mind. Detects emotional extremes. Contrarian when crowd is euphoric."
      },
      { 
        name: "Quant Fundamentals", 
        focus: "Revenue, Earnings", 
        status: "active",
        philosophy: "Revenue growth trajectory. Earnings quality. Operating margins. Cash flow generation. Catalyst-driven fundamental shifts.",
        soul: "The Accountant - Digs through 10-Ks. Spots inflection points in financial statements."
      },
      { 
        name: "Quant Technicals", 
        focus: "Charts, Momentum", 
        status: "active",
        philosophy: "Price action reveals all. Moving averages. Breakouts. Volume surges. Trend following. Support/resistance levels.",
        soul: "The Chartist - Sees patterns in chaos. Believes charts discount all known information."
      },
    ],
    risk: [
      { 
        name: "Risk Manager (Joselo)", 
        focus: "Governance Gatekeeper", 
        status: "active",
        philosophy: "Protect capital first. Every position must have a stop-loss. Conviction-weighted sizing. Portfolio heat limits. Kill bad positions fast.",
        soul: "The Rooster 🐓 - Vigilant guardian. Alerts when it matters. Discipline over hope. No exceptions to risk rules."
      },
      { 
        name: "John C. Hull", 
        focus: "Derivatives & Risk Quantification", 
        status: "active",
        philosophy: "VaR, Expected Shortfall, Greeks, correlation matrices. Quantify tail risk. Stress test every position under 5 macro scenarios. Fat-tail awareness.",
        soul: "The Quantitative Risk Officer - Academic rigor meets market reality. Measures what others fear."
      },
    ]
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <a href="/" className="text-4xl">🐓</a>
              <div>
                <h1 className="text-2xl font-bold text-white">18-Agent System</h1>
                <p className="text-slate-400 text-sm">Legendary Investors + Quants + Risk</p>
              </div>
            </div>
            <a href="/" className="text-slate-400 hover:text-white transition">← Back</a>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Status Overview */}
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white mb-2">System Status</h2>
              <p className="text-slate-400">All 18 agents operational and deliberating</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></span>
              <span className="text-green-400 font-semibold">ACTIVE</span>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Signals Today</p>
              <p className="text-white text-3xl font-bold">10</p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Avg Conviction</p>
              <p className="text-white text-3xl font-bold">5.2/10</p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Deployed</p>
              <p className="text-white text-3xl font-bold">1</p>
            </div>
          </div>
        </div>

        {/* Legendary Investors */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-2">🏛️</span>
            Legendary Investors (12)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {agents.legendary.map((agent) => (
              <div key={agent.name} className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 hover:border-slate-600 transition">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-white font-bold text-lg mb-1">{agent.name}</h3>
                    <p className="text-orange-400 text-sm font-semibold">{agent.focus}</p>
                  </div>
                  <span className="w-2 h-2 bg-green-400 rounded-full mt-2"></span>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Soul</p>
                    <p className="text-slate-300 text-sm italic">{agent.soul}</p>
                  </div>
                  
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Philosophy</p>
                    <p className="text-slate-400 text-sm">{agent.philosophy}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quant Agents */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-2">📊</span>
            Quantitative Agents (4)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {agents.quant.map((agent) => (
              <div key={agent.name} className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 hover:border-slate-600 transition">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-white font-bold text-lg mb-1">{agent.name}</h3>
                    <p className="text-blue-400 text-sm font-semibold">{agent.focus}</p>
                  </div>
                  <span className="w-2 h-2 bg-green-400 rounded-full mt-2"></span>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Soul</p>
                    <p className="text-slate-300 text-sm italic">{agent.soul}</p>
                  </div>
                  
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Philosophy</p>
                    <p className="text-slate-400 text-sm">{agent.philosophy}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Management */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-2">🛡️</span>
            Risk Management (2)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {agents.risk.map((agent) => (
              <div key={agent.name} className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 hover:border-slate-600 transition">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-white font-bold text-lg mb-1">{agent.name}</h3>
                    <p className="text-red-400 text-sm font-semibold">{agent.focus}</p>
                  </div>
                  <span className="w-2 h-2 bg-green-400 rounded-full mt-2"></span>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Soul</p>
                    <p className="text-slate-300 text-sm italic">{agent.soul}</p>
                  </div>
                  
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Philosophy</p>
                    <p className="text-slate-400 text-sm">{agent.philosophy}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Deliberations */}
        <div>
          <h2 className="text-xl font-bold text-white mb-4">Recent Deliberations</h2>
          <div className="space-y-4">
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-white font-semibold text-lg">$PG (Procter & Gamble)</h3>
                  <p className="text-slate-400 text-sm">Feb 20, 2026 1:00 PM EST</p>
                </div>
                <span className="bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full text-sm font-semibold">
                  5.2/10
                </span>
              </div>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-slate-400 text-xs mb-1">Legendary</p>
                  <p className="text-white font-mono">5.2/10</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs mb-1">Quant</p>
                  <p className="text-white font-mono">4.0/10</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs mb-1">Decision</p>
                  <p className="text-white font-semibold">HOLD → DEPLOY</p>
                </div>
              </div>
              <p className="text-slate-300 text-sm">
                Low-medium conviction. Consumer defensive, strong brand moat, 2.67% dividend. 
                Deployed at reduced size ($5k, 8% stop) per updated risk framework.
              </p>
            </div>

            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-white font-semibold text-lg">$HOOD, $NEM, $PYPL</h3>
                  <p className="text-slate-400 text-sm">Feb 20, 2026 12:20 PM EST</p>
                </div>
                <span className="bg-slate-500/20 text-slate-400 px-3 py-1 rounded-full text-sm font-semibold">
                  ~5.2/10
                </span>
              </div>
              <p className="text-slate-300 text-sm">
                All three evaluated by 18-agent system. Consensus: HOLD (below 6.0 threshold). 
                No clear edge identified. Skipped deployment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
