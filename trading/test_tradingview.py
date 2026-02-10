#!/usr/bin/env python3
"""Test TradingView integration"""

from tradingview_ta import TA_Handler, Interval

# Test TAO
print("Testing TAO...")
tao = TA_Handler(
    symbol='TAOUSD',
    exchange='BINANCE',
    screener='crypto',
    interval=Interval.INTERVAL_1_HOUR
)
tao_data = tao.get_analysis()
print(f'TAO: ${tao_data.indicators["close"]:.2f}')
print(f'RSI: {tao_data.indicators["RSI"]:.1f}')
print(f'Recommendation: {tao_data.summary["RECOMMENDATION"]}')
print()

# Test SOL
print("Testing SOL...")
sol = TA_Handler(
    symbol='SOLUSD',
    exchange='BINANCE',
    screener='crypto',
    interval=Interval.INTERVAL_1_HOUR
)
sol_data = sol.get_analysis()
print(f'SOL: ${sol_data.indicators["close"]:.2f}')
print(f'RSI: {sol_data.indicators["RSI"]:.1f}')
print(f'Recommendation: {sol_data.summary["RECOMMENDATION"]}')
