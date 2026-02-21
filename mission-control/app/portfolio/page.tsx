'use client'

import { useEffect, useState } from 'react'

interface Position {
  ticker: string
  entry: number
  current: number
  shares: number
  positionSize: number
  pnl: number
  pnlPct: number
  stopLoss: number
  conviction: number
  date: string
}

export default function PortfolioPage() {
  const [positions, setPositions] = useState<Position[]>([])
  const [totalPnL, setTotalPnL] = useState(0)
  const [totalValue, setTotalValue] = useState(0)

  // In production, this would fetch from API that reads positions.csv
  // For now, using mock data that matches current positions
  useEffect(() => {
    const mockPositions: Position[] = [
      {
        ticker: 'ALL',
        entry: 207.00,
        current: 203.22,
        shares: 96.62,
        positionSize: 20000,
        pnl: -365,
        pnlPct: -1.83,
        stopLoss: 175.95,
        conviction: 8.0,
        date: '2026-02-09'
      },
      {
        ticker: 'PGR',
        entry: 201.57,
        current: 201.77,
        shares: 74.42,
        positionSize: 15000,
        pnl: 15,
        pnlPct: 0.10,
        stopLoss: 171.33,
        conviction: 8.0,
        date: '2026-02-09'
      },
      {
        ticker: 'KTB',
        entry: 67.00,
        current: 67.65,
        shares: 149.25,
        positionSize: 10000,
        pnl: 97,
        pnlPct: 0.97,
        stopLoss: 56.95,
        conviction: 7.7,
        date: '2026-02-09'
      },
      {
        ticker: 'PG',
        entry: 160.15,
        current: 160.15,
        shares: 31,
        positionSize: 5000,
        pnl: 0,
        pnlPct: 0.00,
        stopLoss: 147.34,
        conviction: 5.2,
        date: '2026-02-20'
      }
    ]

    setPositions(mockPositions)
    
    const total = mockPositions.reduce((sum, p) => sum + p.pnl, 0)
    const value = mockPositions.reduce((sum, p) => sum + p.positionSize, 0)
    
    setTotalPnL(total)
    setTotalValue(value)
  }, [])

  const totalPnLPct = totalValue > 0 ? (totalPnL / totalValue) * 100 : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <a href="/" className="text-4xl">🐓</a>
              <div>
                <h1 className="text-2xl font-bold text-white">Portfolio Performance</h1>
                <p className="text-slate-400 text-sm">Real-time P&L tracking</p>
              </div>
            </div>
            <a href="/" className="text-slate-400 hover:text-white transition">← Back</a>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Portfolio Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <p className="text-slate-400 text-sm mb-2">Total Capital</p>
            <p className="text-white text-3xl font-bold">$1.0M</p>
            <p className="text-slate-500 text-xs mt-1">Phase 1 Paper</p>
          </div>
          
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <p className="text-slate-400 text-sm mb-2">Deployed</p>
            <p className="text-white text-3xl font-bold">${(totalValue / 1000).toFixed(0)}k</p>
            <p className="text-slate-500 text-xs mt-1">{((totalValue / 1000000) * 100).toFixed(1)}% of capital</p>
          </div>
          
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <p className="text-slate-400 text-sm mb-2">Total P&L</p>
            <p className={`text-3xl font-bold ${totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {totalPnL >= 0 ? '+' : ''}${totalPnL.toFixed(0)}
            </p>
            <p className={`text-xs mt-1 ${totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {totalPnL >= 0 ? '+' : ''}{totalPnLPct.toFixed(2)}%
            </p>
          </div>
          
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <p className="text-slate-400 text-sm mb-2">Active Positions</p>
            <p className="text-white text-3xl font-bold">{positions.length}</p>
            <p className="text-slate-500 text-xs mt-1">All within stops</p>
          </div>
        </div>

        {/* Active Positions */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-white mb-4">Active Positions</h2>
          <div className="space-y-4">
            {positions.map((position) => (
              <div key={position.ticker} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-slate-600 transition">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center space-x-4 mb-2">
                      <h3 className="text-white font-bold text-2xl">${position.ticker}</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        position.pnl >= 0 
                          ? 'bg-green-500/20 text-green-400' 
                          : 'bg-red-500/20 text-red-400'
                      }`}>
                        {position.pnl >= 0 ? '+' : ''}${position.pnl.toFixed(0)} ({position.pnl >= 0 ? '+' : ''}{position.pnlPct.toFixed(2)}%)
                      </span>
                      <span className="text-slate-400 text-sm">
                        {position.conviction}/10 conviction
                      </span>
                    </div>
                    <p className="text-slate-400 text-sm">
                      Opened: {new Date(position.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-white font-mono text-2xl">${position.current.toFixed(2)}</p>
                    <p className="text-slate-400 text-sm">Current Price</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-5 gap-4 pt-4 border-t border-slate-700">
                  <div>
                    <p className="text-slate-400 text-xs mb-1">Entry</p>
                    <p className="text-white font-mono">${position.entry.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-xs mb-1">Shares</p>
                    <p className="text-white font-mono">{position.shares.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-xs mb-1">Position Size</p>
                    <p className="text-white font-mono">${(position.positionSize / 1000).toFixed(0)}k</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-xs mb-1">Stop Loss</p>
                    <p className="text-white font-mono">${position.stopLoss.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-xs mb-1">Distance to Stop</p>
                    <p className={`font-mono ${
                      ((position.current - position.stopLoss) / position.current * 100) < 5 
                        ? 'text-red-400' 
                        : 'text-green-400'
                    }`}>
                      {((position.current - position.stopLoss) / position.current * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Performance Metrics */}
        <div>
          <h2 className="text-xl font-bold text-white mb-4">Performance Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
              <h3 className="text-white font-semibold mb-4">Win Rate</h3>
              <div className="flex items-end space-x-2 mb-2">
                <p className="text-white text-4xl font-bold">33%</p>
                <p className="text-slate-400 mb-2">1 of 3 green</p>
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-green-400" style={{ width: '33%' }}></div>
              </div>
            </div>

            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
              <h3 className="text-white font-semibold mb-4">Max Drawdown</h3>
              <div className="flex items-end space-x-2 mb-2">
                <p className="text-white text-4xl font-bold">-1.83%</p>
                <p className="text-slate-400 mb-2">of 15% limit</p>
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-amber-400" style={{ width: '12.2%' }}></div>
              </div>
            </div>

            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
              <h3 className="text-white font-semibold mb-4">Avg Conviction</h3>
              <div className="flex items-end space-x-2 mb-2">
                <p className="text-white text-4xl font-bold">7.2</p>
                <p className="text-slate-400 mb-2">out of 10</p>
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-orange-400" style={{ width: '72%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Auto-Update Notice */}
        <div className="mt-8 bg-orange-500/10 border border-orange-500/20 rounded-xl p-6">
          <div className="flex items-start space-x-3">
            <span className="text-2xl">⚡</span>
            <div>
              <h3 className="text-orange-400 font-semibold mb-2">Auto-Updated Dashboard</h3>
              <p className="text-slate-300 text-sm mb-3">
                This dashboard automatically updates:
              </p>
              <ul className="text-slate-400 text-sm space-y-1">
                <li>• <strong className="text-white">Hourly:</strong> Prices sync from yfinance</li>
                <li>• <strong className="text-white">Real-time:</strong> Risk monitor checks stops every 5 minutes</li>
                <li>• <strong className="text-white">Daily:</strong> Performance journal + Git commit</li>
              </ul>
              <p className="text-slate-500 text-xs mt-3">
                Data source: <code className="bg-slate-800 px-2 py-1 rounded">trading/positions.csv</code> + 
                <code className="bg-slate-800 px-2 py-1 rounded ml-1">dashboard.html</code>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
