import { NextResponse } from 'next/server'
import { readFileSync } from 'fs'
import { join } from 'path'

export async function GET() {
  try {
    // Read positions from CSV
    const tradingPath = join(process.cwd(), '..', 'trading', 'positions.csv')
    const csvData = readFileSync(tradingPath, 'utf-8')
    
    const lines = csvData.trim().split('\n')
    const headers = lines[0].split(',')
    
    const positions = lines.slice(1).map(line => {
      const values = line.split(',')
      const position: any = {}
      
      headers.forEach((header, index) => {
        position[header.trim()] = values[index]?.trim()
      })
      
      return {
        ticker: position.Ticker,
        entry: parseFloat(position.Entry),
        shares: parseFloat(position.Shares),
        positionSize: parseFloat(position.Position_Size),
        stopLoss: parseFloat(position.Stop_Loss),
        conviction: parseFloat(position.Conviction),
        date: position.Date,
        status: position.Status
      }
    }).filter(p => p.status === 'OPEN')
    
    // TODO: Fetch current prices from yfinance or dashboard.html
    // For now, returning static data
    
    return NextResponse.json({
      positions,
      totalValue: positions.reduce((sum, p) => sum + p.positionSize, 0),
      lastUpdated: new Date().toISOString()
    })
  } catch (error) {
    console.error('Error reading positions:', error)
    return NextResponse.json({ error: 'Failed to load positions' }, { status: 500 })
  }
}
