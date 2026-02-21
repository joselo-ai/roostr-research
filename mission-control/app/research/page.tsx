export default function ResearchPage() {
  const todayOpportunities = [
    { ticker: "CRWD", score: 78.5, price: 423.97, source: "analyst_upgrade", catalyst: "Analyst target $545.62 (78.5% upside)" },
    { ticker: "SNOW", score: 52.5, price: 178.21, source: "analyst_upgrade", catalyst: "Analyst target $271.72 (52.5% upside)" },
    { ticker: "DDOG", score: 51.0, price: 120.82, source: "analyst_upgrade", catalyst: "Analyst target $182.43 (51.0% upside)" },
    { ticker: "MSFT", score: 49.9, price: 397.60, source: "analyst_upgrade", catalyst: "Analyst target $596.00 (49.9% upside)" },
    { ticker: "AMD", score: 44.0, price: 199.62, source: "analyst_upgrade", catalyst: "Analyst target $287.52 (44.0% upside)" },
    { ticker: "PLTR", score: 41.4, price: 134.29, source: "analyst_upgrade", catalyst: "Analyst target $189.92 (41.4% upside)" },
    { ticker: "JNJ", score: 32.4, price: 242.81, source: "insider_proxy", catalyst: "Insider confidence proxy: 76% institutional" },
    { ticker: "PG", score: 20.1, price: 160.15, source: "insider_proxy", catalyst: "Insider confidence proxy: 70% institutional" },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <a href="/" className="text-4xl">🐓</a>
              <div>
                <h1 className="text-2xl font-bold text-white">Research Pipeline</h1>
                <p className="text-slate-400 text-sm">Daily opportunity scanner + nightly research</p>
              </div>
            </div>
            <a href="/" className="text-slate-400 hover:text-white transition">← Back</a>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Scanner Status */}
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold text-white">Today's Scan</h2>
              <p className="text-slate-400 text-sm">Feb 20, 2026 - Last run: 12:41 PM EST</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 bg-green-400 rounded-full"></span>
              <span className="text-green-400 font-semibold">COMPLETE</span>
            </div>
          </div>
          
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Opportunities Found</p>
              <p className="text-white text-3xl font-bold">25</p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Evaluated by Agents</p>
              <p className="text-white text-3xl font-bold">8</p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Deployed</p>
              <p className="text-white text-3xl font-bold">1</p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-1">Next Scan</p>
              <p className="text-white text-xl font-bold">2:00 AM</p>
            </div>
          </div>
        </div>

        {/* Today's Opportunities */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-white mb-4">Top Opportunities (Today)</h2>
          <div className="space-y-3">
            {todayOpportunities.map((opp) => (
              <div key={opp.ticker} className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 hover:border-slate-600 transition">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4 mb-2">
                      <h3 className="text-white font-bold text-lg">${opp.ticker}</h3>
                      <span className="bg-orange-500/20 text-orange-400 px-3 py-1 rounded-full text-sm font-semibold">
                        {opp.score.toFixed(1)} score
                      </span>
                      <span className="text-slate-400 text-sm">{opp.source.replace('_', ' ')}</span>
                    </div>
                    <p className="text-slate-300 text-sm">{opp.catalyst}</p>
                  </div>
                  <div className="text-right ml-6">
                    <p className="text-white font-mono text-xl">${opp.price.toFixed(2)}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Scanner Sources */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-white mb-4">Active Scanner Sources</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">📊</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Unusual Volume</h3>
              <p className="text-slate-400 text-xs">3x+ average volume spikes</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">💰</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Value Stocks</h3>
              <p className="text-slate-400 text-xs">Low P/E + high dividends</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">📈</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Growth Stocks</h3>
              <p className="text-slate-400 text-xs">Revenue + earnings growth</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">🎯</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Earnings Surprises</h3>
              <p className="text-slate-400 text-xs">Beat + raised guidance</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">💼</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Insider Buying</h3>
              <p className="text-slate-400 text-xs">High institutional holdings</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">📊</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Analyst Upgrades</h3>
              <p className="text-slate-400 text-xs">Price target raises</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">🚀</span>
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Momentum Breakouts</h3>
              <p className="text-slate-400 text-xs">Price &gt; MA20 &amp; MA50</p>
            </div>
            
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">🌐</span>
                <span className="w-2 h-2 bg-amber-400 rounded-full"></span>
              </div>
              <h3 className="text-white font-semibold mb-1">Social Sentiment</h3>
              <p className="text-slate-400 text-xs">Reddit WSB tracking</p>
            </div>
          </div>
        </div>

        {/* Nightly Research Preview */}
        <div>
          <h2 className="text-xl font-bold text-white mb-4">Nightly Research (2 AM)</h2>
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-white font-semibold text-lg mb-2">Next Run: Tonight @ 2:00 AM EST</h3>
                <p className="text-slate-400 text-sm">Automated deployment plan generation</p>
              </div>
              <span className="text-3xl">🌙</span>
            </div>
            
            <div className="bg-slate-900/50 rounded-lg p-4 mb-4">
              <h4 className="text-white font-semibold mb-3">What Happens:</h4>
              <ol className="space-y-2 text-slate-300 text-sm">
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">1.</span>
                  Scans global markets (base + enhanced scanners)
                </li>
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">2.</span>
                  Generates top 10 unique opportunities
                </li>
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">3.</span>
                  Evaluates top 5 with 18-agent system
                </li>
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">4.</span>
                  Creates deployment plan (saved to next-day-deployment-plan.md)
                </li>
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">5.</span>
                  Sends Telegram alert with summary
                </li>
              </ol>
            </div>
            
            <div className="border-t border-slate-700 pt-4">
              <p className="text-slate-400 text-sm">
                <strong className="text-white">Result:</strong> Wake up to tomorrow's best trades already researched, 
                evaluated by 18 agents, and ready for 9:30 AM deployment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
