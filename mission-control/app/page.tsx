import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-5xl">🐓</span>
              <div>
                <h1 className="text-3xl font-bold text-white">roostr Capital</h1>
                <p className="text-slate-400 text-sm">Mission Control</p>
              </div>
            </div>
            <div className="flex space-x-4">
              <Link href="/agents" className="text-slate-300 hover:text-white transition">Agents</Link>
              <Link href="/research" className="text-slate-300 hover:text-white transition">Research</Link>
              <Link href="/portfolio" className="text-slate-300 hover:text-white transition">Portfolio</Link>
            </div>
          </div>
        </div>
      </header>

      {/* Mission Statement */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-gradient-to-r from-orange-500/10 to-amber-500/10 border border-orange-500/20 rounded-2xl p-8 mb-8">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-orange-500/20 rounded-full flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
            </div>
            <div className="flex-1">
              <h2 className="text-sm font-semibold text-orange-400 uppercase tracking-wider mb-2">
                Mission Statement
              </h2>
              <p className="text-2xl font-bold text-white leading-relaxed">
                Autonomous AI hedge fund that compounds capital 24/7 through systematic, disciplined, transparent execution.
              </p>
              <p className="text-slate-400 mt-4">
                Every tool, every decision, every line of code serves this mission.
              </p>
            </div>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Portfolio Status */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Portfolio</h3>
              <span className="text-2xl">💰</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Total Value</span>
                <span className="text-white font-mono">$50,000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">P&L Today</span>
                <span className="text-green-400 font-mono">+$33 (+0.07%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Positions</span>
                <span className="text-white font-mono">4 active</span>
              </div>
            </div>
            <Link href="/portfolio" className="block mt-4 text-sm text-orange-400 hover:text-orange-300 transition">
              View Details →
            </Link>
          </div>

          {/* 18-Agent System */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">18-Agent System</h3>
              <span className="text-2xl">🤖</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Status</span>
                <span className="text-green-400 font-semibold">● Operational</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Today's Signals</span>
                <span className="text-white font-mono">10 evaluated</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Deployed</span>
                <span className="text-white font-mono">1 position</span>
              </div>
            </div>
            <Link href="/agents" className="block mt-4 text-sm text-orange-400 hover:text-orange-300 transition">
              View Agents →
            </Link>
          </div>

          {/* Recent Activity */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Recent Activity</h3>
              <span className="text-2xl">📊</span>
            </div>
            <div className="space-y-3">
              <div className="flex items-start space-x-2">
                <span className="text-xs text-slate-500 mt-1">13:05</span>
                <div>
                  <p className="text-sm text-white">PG deployed</p>
                  <p className="text-xs text-slate-400">$160.15, 5.2/10 conviction</p>
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <span className="text-xs text-slate-500 mt-1">12:20</span>
                <div>
                  <p className="text-sm text-white">3 tickers evaluated</p>
                  <p className="text-xs text-slate-400">HOOD, NEM, PYPL</p>
                </div>
              </div>
            </div>
            <Link href="/research" className="block mt-4 text-sm text-orange-400 hover:text-orange-300 transition">
              View Research →
            </Link>
          </div>

          {/* Risk Status */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Risk Monitor</h3>
              <span className="text-2xl">🛡️</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">All Stops</span>
                <span className="text-green-400 font-semibold">✓ Intact</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Max Drawdown</span>
                <span className="text-white font-mono">-1.83%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Portfolio Risk</span>
                <span className="text-green-400 font-mono">4.5% / 10%</span>
              </div>
            </div>
          </div>

          {/* Nightly Research */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Nightly Research</h3>
              <span className="text-2xl">🌙</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Next Run</span>
                <span className="text-white font-mono">2:00 AM</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Last Run</span>
                <span className="text-slate-400 font-mono">Not yet</span>
              </div>
              <p className="text-xs text-slate-500 mt-3">
                Auto-generates deployment plan for next market open
              </p>
            </div>
          </div>

          {/* Social/Marketing */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">roostr Social</h3>
              <span className="text-2xl">🐦</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Twitter</span>
                <span className="text-white font-mono">@roostrcapital</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Followers</span>
                <span className="text-white font-mono">Building...</span>
              </div>
              <p className="text-xs text-slate-500 mt-3">
                Full transparency: wins AND losses
              </p>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-1">Phase 1 Capital</p>
            <p className="text-white text-2xl font-bold">$1M</p>
            <p className="text-xs text-slate-500 mt-1">Paper trading</p>
          </div>
          <div className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-1">Win Rate</p>
            <p className="text-white text-2xl font-bold">33%</p>
            <p className="text-xs text-slate-500 mt-1">1 of 3 green</p>
          </div>
          <div className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-1">Deployed</p>
            <p className="text-white text-2xl font-bold">4.5%</p>
            <p className="text-xs text-slate-500 mt-1">$45k of $1M</p>
          </div>
          <div className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-1">Days Active</p>
            <p className="text-white text-2xl font-bold">11</p>
            <p className="text-xs text-slate-500 mt-1">Since Feb 9</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-700 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between text-sm">
            <p className="text-slate-400">
              🐓 roostr Capital - Built by Joselo AI
            </p>
            <div className="flex space-x-4">
              <a href="https://github.com/joselo-ai/roostr-research" className="text-slate-400 hover:text-white transition">
                GitHub
              </a>
              <a href="https://twitter.com/roostrcapital" className="text-slate-400 hover:text-white transition">
                Twitter
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
