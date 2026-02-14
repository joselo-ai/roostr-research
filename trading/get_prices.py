#!/usr/bin/env python3
import requests
import json

tickers = ['ASTS', 'PGR', 'ALL', 'KTB']

for ticker in tickers:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
        resp = requests.get(url)
        data = resp.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        print(f"{ticker}: ${price:.2f}")
    except Exception as e:
        print(f"{ticker}: Error - {e}")
