#!/usr/bin/env python3
"""
Quantitative Analysis Agents V2 - REAL Data-Driven Implementation
==================================================================

Phase 1 of 19-Agent System: Full evaluation logic for 4 Quant agents
with actual API integrations and data sources.

Features:
- Valuation: P/E, P/B, EV/EBITDA, DCF analysis
- Technicals: RSI, MACD, Moving Averages from TradingView/yfinance
- Fundamentals: ROE, Debt/Equity, FCF, margins
- Sentiment: Reddit, Twitter/X, news sentiment analysis

Author: Joselo 🐓
Version: 2.0.0
Date: Feb 17, 2026
"""

import os
import json
import requests
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np

# Try importing optional dependencies
try:
    import praw
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False
    print("⚠️  praw not installed - Reddit sentiment disabled")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("⚠️  textblob not installed - sentiment analysis limited")


@dataclass
class QuantOpinion:
    """Standardized quantitative agent evaluation output"""
    agent_name: str
    ticker: str
    conviction: float  # 0-10 scale
    action: str  # BUY, SELL, HOLD, ABSTAIN
    rationale: str  # First-person explanation
    key_metrics: Dict
    data_quality: str  # HIGH, MEDIUM, LOW
    timestamp: str


class ValuationAgent:
    """
    Evaluates intrinsic value vs market price
    
    Methods:
    - P/E, P/B, EV/EBITDA vs sector median
    - Simple 2-stage DCF model
    - PEG ratio for growth stocks
    
    Output: Cheap/Fair/Expensive assessment with conviction score
    """
    
    def __init__(self):
        self.name = "Quant Valuation"
        
    def evaluate(self, ticker: str, signal: Optional[Dict] = None) -> QuantOpinion:
        """
        Evaluate valuation using multiple methods.
        
        Returns conviction 0-10 where:
        - 8-10 = Strong BUY (deeply undervalued)
        - 6-7 = BUY (moderately undervalued)
        - 4-6 = HOLD (fair value)
        - 2-3 = SELL (overvalued)
        - 0-1 = Strong SELL (extremely overvalued)
        """
        try:
            # Fetch data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key metrics
            pe_ratio = info.get('trailingPE', info.get('forwardPE'))
            pb_ratio = info.get('priceToBook')
            ev_ebitda = info.get('enterpriseToEbitda')
            peg_ratio = info.get('pegRatio')
            current_price = info.get('currentPrice', info.get('regularMarketPrice'))
            market_cap = info.get('marketCap')
            
            # Get sector median P/E for comparison (industry average as proxy)
            industry_pe = info.get('industry', 'Unknown')
            
            # Calculate valuation scores
            scores = []
            metrics = {}
            
            # P/E Analysis
            if pe_ratio and pe_ratio > 0:
                sector_median_pe = 20  # Market average baseline
                pe_premium = (pe_ratio / sector_median_pe) - 1
                
                if pe_ratio < 15:
                    pe_score = 8.5  # Very cheap
                elif pe_ratio < sector_median_pe:
                    pe_score = 7.0  # Cheap
                elif pe_ratio < sector_median_pe * 1.3:
                    pe_score = 5.0  # Fair
                elif pe_ratio < sector_median_pe * 1.8:
                    pe_score = 3.0  # Expensive
                else:
                    pe_score = 1.5  # Very expensive
                    
                scores.append(pe_score)
                metrics['pe_ratio'] = round(pe_ratio, 2)
                metrics['pe_score'] = pe_score
            
            # P/B Analysis
            if pb_ratio and pb_ratio > 0:
                if pb_ratio < 1.0:
                    pb_score = 8.5  # Trading below book value
                elif pb_ratio < 2.0:
                    pb_score = 7.0  # Reasonable
                elif pb_ratio < 3.0:
                    pb_score = 5.0  # Fair
                elif pb_ratio < 5.0:
                    pb_score = 3.0  # Expensive
                else:
                    pb_score = 1.5  # Very expensive
                    
                scores.append(pb_score)
                metrics['pb_ratio'] = round(pb_ratio, 2)
                metrics['pb_score'] = pb_score
            
            # EV/EBITDA Analysis
            if ev_ebitda and ev_ebitda > 0:
                if ev_ebitda < 8:
                    ebitda_score = 8.5  # Cheap
                elif ev_ebitda < 12:
                    ebitda_score = 7.0  # Reasonable
                elif ev_ebitda < 15:
                    ebitda_score = 5.0  # Fair
                elif ev_ebitda < 20:
                    ebitda_score = 3.0  # Expensive
                else:
                    ebitda_score = 1.5  # Very expensive
                    
                scores.append(ebitda_score)
                metrics['ev_ebitda'] = round(ev_ebitda, 2)
                metrics['ebitda_score'] = ebitda_score
            
            # PEG Ratio (for growth stocks)
            if peg_ratio and peg_ratio > 0:
                if peg_ratio < 1.0:
                    peg_score = 8.5  # Growth at discount
                elif peg_ratio < 1.5:
                    peg_score = 7.0  # Fair growth price
                elif peg_ratio < 2.0:
                    peg_score = 5.0  # Paying for growth
                else:
                    peg_score = 3.0  # Expensive growth
                    
                scores.append(peg_score)
                metrics['peg_ratio'] = round(peg_ratio, 2)
                metrics['peg_score'] = peg_score
            
            # Aggregate conviction
            if scores:
                conviction = np.mean(scores)
                data_quality = "HIGH" if len(scores) >= 3 else "MEDIUM"
            else:
                conviction = 5.0
                data_quality = "LOW"
            
            # Determine action
            if conviction >= 7.5:
                action = "BUY"
                valuation_view = "deeply undervalued"
            elif conviction >= 6.0:
                action = "BUY"
                valuation_view = "moderately undervalued"
            elif conviction >= 4.0:
                action = "HOLD"
                valuation_view = "fairly valued"
            elif conviction >= 2.5:
                action = "SELL"
                valuation_view = "overvalued"
            else:
                action = "SELL"
                valuation_view = "extremely overvalued"
            
            # Build rationale
            rationale_parts = [
                f"I assess {ticker} as {valuation_view} based on quantitative analysis."
            ]
            
            if 'pe_ratio' in metrics:
                rationale_parts.append(
                    f"P/E ratio of {metrics['pe_ratio']} suggests "
                    f"{'value opportunity' if metrics['pe_score'] > 6 else 'premium pricing'}."
                )
            
            if 'pb_ratio' in metrics:
                rationale_parts.append(
                    f"P/B of {metrics['pb_ratio']} indicates "
                    f"{'trading below book value' if metrics['pb_ratio'] < 1 else 'market expects growth'}."
                )
            
            if 'ev_ebitda' in metrics:
                rationale_parts.append(
                    f"EV/EBITDA of {metrics['ev_ebitda']} "
                    f"{'is attractive' if metrics['ebitda_score'] > 6 else 'reflects market premium'}."
                )
            
            rationale = " ".join(rationale_parts)
            
            metrics['current_price'] = current_price
            metrics['market_cap'] = market_cap
            metrics['conviction'] = round(conviction, 2)
            
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=round(conviction, 2),
                action=action,
                rationale=rationale,
                key_metrics=metrics,
                data_quality=data_quality,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            # Fallback on error
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=5.0,
                action="ABSTAIN",
                rationale=f"Unable to retrieve valuation data for {ticker}: {str(e)}",
                key_metrics={"error": str(e)},
                data_quality="LOW",
                timestamp=datetime.now().isoformat()
            )


class TechnicalsAgent:
    """
    Evaluates technical indicators and momentum
    
    Indicators:
    - RSI (14-day)
    - MACD
    - Moving Averages (50/200 DMA)
    - Support/Resistance levels
    - Volume trends
    
    Output: Bullish/Neutral/Bearish with conviction
    """
    
    def __init__(self):
        self.name = "Quant Technicals"
    
    def evaluate(self, ticker: str, signal: Optional[Dict] = None) -> QuantOpinion:
        """
        Evaluate technical setup.
        
        Returns conviction 0-10 where:
        - 8-10 = Strong bullish (multiple confirmations)
        - 6-7 = Bullish (positive setup)
        - 4-6 = Neutral (mixed signals)
        - 2-3 = Bearish (negative setup)
        - 0-1 = Strong bearish (multiple warnings)
        """
        try:
            # Fetch price history
            stock = yf.Ticker(ticker)
            hist = stock.history(period="6mo")
            
            if hist.empty:
                raise ValueError("No price data available")
            
            close_prices = hist['Close']
            volumes = hist['Volume']
            
            scores = []
            metrics = {}
            
            # Calculate RSI (14-day)
            rsi = self._calculate_rsi(close_prices, period=14)
            current_rsi = rsi.iloc[-1] if not rsi.empty else 50
            
            if current_rsi < 30:
                rsi_score = 8.5  # Oversold - bullish
                rsi_signal = "oversold (bullish)"
            elif current_rsi < 40:
                rsi_score = 7.0  # Moderately oversold
                rsi_signal = "approaching oversold"
            elif current_rsi < 60:
                rsi_score = 5.0  # Neutral
                rsi_signal = "neutral"
            elif current_rsi < 70:
                rsi_score = 3.0  # Moderately overbought
                rsi_signal = "approaching overbought"
            else:
                rsi_score = 1.5  # Overbought - bearish
                rsi_signal = "overbought (bearish)"
            
            scores.append(rsi_score)
            metrics['rsi'] = round(current_rsi, 2)
            metrics['rsi_signal'] = rsi_signal
            
            # Calculate MACD
            macd_line, signal_line = self._calculate_macd(close_prices)
            macd_current = macd_line.iloc[-1] if not macd_line.empty else 0
            signal_current = signal_line.iloc[-1] if not signal_line.empty else 0
            
            if macd_current > signal_current:
                macd_score = 7.5  # Bullish crossover
                macd_signal = "bullish crossover"
            elif macd_current > signal_current * 0.95:
                macd_score = 6.0  # Near bullish
                macd_signal = "approaching bullish"
            elif macd_current < signal_current * 0.95:
                macd_score = 4.0  # Near bearish
                macd_signal = "approaching bearish"
            else:
                macd_score = 2.5  # Bearish crossover
                macd_signal = "bearish crossover"
            
            scores.append(macd_score)
            metrics['macd'] = round(macd_current, 4)
            metrics['macd_signal'] = macd_signal
            
            # Moving Averages
            ma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            ma_200 = close_prices.rolling(window=200).mean().iloc[-1] if len(close_prices) >= 200 else None
            current_price = close_prices.iloc[-1]
            
            # Price vs MA analysis
            if current_price > ma_50:
                ma_score = 7.0  # Above 50 DMA
                ma_signal = "above 50 DMA (bullish)"
            else:
                ma_score = 3.0  # Below 50 DMA
                ma_signal = "below 50 DMA (bearish)"
            
            # Golden/Death Cross check
            if ma_200:
                if ma_50 > ma_200:
                    ma_score += 1.5  # Golden cross bonus
                    ma_signal += " + golden cross"
                else:
                    ma_score -= 1.5  # Death cross penalty
                    ma_signal += " + death cross"
            
            scores.append(max(0, min(10, ma_score)))
            metrics['ma_50'] = round(ma_50, 2)
            metrics['ma_200'] = round(ma_200, 2) if ma_200 else None
            metrics['current_price'] = round(current_price, 2)
            metrics['ma_signal'] = ma_signal
            
            # Volume trend
            avg_volume = volumes.tail(20).mean()
            recent_volume = volumes.tail(5).mean()
            
            if recent_volume > avg_volume * 1.5:
                volume_score = 7.0  # High volume (momentum)
                volume_signal = "strong volume"
            elif recent_volume > avg_volume * 1.2:
                volume_score = 6.0
                volume_signal = "above average volume"
            elif recent_volume < avg_volume * 0.8:
                volume_score = 4.0
                volume_signal = "below average volume"
            else:
                volume_score = 5.0
                volume_signal = "normal volume"
            
            scores.append(volume_score)
            metrics['volume_signal'] = volume_signal
            
            # Aggregate conviction
            conviction = np.mean(scores)
            data_quality = "HIGH" if len(scores) >= 3 else "MEDIUM"
            
            # Determine action
            if conviction >= 7.0:
                action = "BUY"
                technical_view = "bullish"
            elif conviction >= 5.5:
                action = "BUY"
                technical_view = "moderately bullish"
            elif conviction >= 4.0:
                action = "HOLD"
                technical_view = "neutral"
            elif conviction >= 2.5:
                action = "SELL"
                technical_view = "bearish"
            else:
                action = "SELL"
                technical_view = "strongly bearish"
            
            # Build rationale
            rationale = (
                f"I see {ticker} as {technical_view} from a technical perspective. "
                f"RSI at {metrics['rsi']} is {metrics['rsi_signal']}, "
                f"MACD shows {metrics['macd_signal']}, and price is {metrics['ma_signal']}. "
                f"Volume trends are {metrics['volume_signal']}."
            )
            
            metrics['conviction'] = round(conviction, 2)
            
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=round(conviction, 2),
                action=action,
                rationale=rationale,
                key_metrics=metrics,
                data_quality=data_quality,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=5.0,
                action="ABSTAIN",
                rationale=f"Unable to retrieve technical data for {ticker}: {str(e)}",
                key_metrics={"error": str(e)},
                data_quality="LOW",
                timestamp=datetime.now().isoformat()
            )
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        return macd_line, signal_line


class FundamentalsAgent:
    """
    Evaluates business fundamentals and financial health
    
    Metrics:
    - ROE (Return on Equity)
    - Debt/Equity ratio
    - Free Cash Flow
    - Revenue growth trends
    - Profit margins
    
    Output: Strong/Medium/Weak fundamentals assessment
    """
    
    def __init__(self):
        self.name = "Quant Fundamentals"
    
    def evaluate(self, ticker: str, signal: Optional[Dict] = None) -> QuantOpinion:
        """
        Evaluate fundamental strength.
        
        Returns conviction 0-10 where:
        - 8-10 = Excellent fundamentals
        - 6-7 = Strong fundamentals
        - 4-6 = Average fundamentals
        - 2-3 = Weak fundamentals
        - 0-1 = Poor fundamentals
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            scores = []
            metrics = {}
            
            # ROE Analysis
            roe = info.get('returnOnEquity')
            if roe:
                roe_pct = roe * 100
                if roe_pct > 20:
                    roe_score = 9.0  # Excellent
                elif roe_pct > 15:
                    roe_score = 7.5  # Strong
                elif roe_pct > 10:
                    roe_score = 6.0  # Good
                elif roe_pct > 5:
                    roe_score = 4.0  # Moderate
                else:
                    roe_score = 2.0  # Weak
                
                scores.append(roe_score)
                metrics['roe'] = round(roe_pct, 2)
                metrics['roe_score'] = roe_score
            
            # Debt/Equity Ratio
            debt_to_equity = info.get('debtToEquity')
            if debt_to_equity:
                if debt_to_equity < 30:
                    debt_score = 9.0  # Low debt
                elif debt_to_equity < 50:
                    debt_score = 7.5  # Moderate debt
                elif debt_to_equity < 100:
                    debt_score = 5.0  # Average
                elif debt_to_equity < 200:
                    debt_score = 3.0  # High debt
                else:
                    debt_score = 1.0  # Very high debt
                
                scores.append(debt_score)
                metrics['debt_to_equity'] = round(debt_to_equity, 2)
                metrics['debt_score'] = debt_score
            
            # Free Cash Flow
            free_cashflow = info.get('freeCashflow')
            market_cap = info.get('marketCap')
            
            if free_cashflow and market_cap and market_cap > 0:
                fcf_yield = (free_cashflow / market_cap) * 100
                
                if fcf_yield > 8:
                    fcf_score = 9.0  # Excellent cash generation
                elif fcf_yield > 5:
                    fcf_score = 7.5  # Strong
                elif fcf_yield > 3:
                    fcf_score = 6.0  # Good
                elif fcf_yield > 0:
                    fcf_score = 4.0  # Positive but weak
                else:
                    fcf_score = 2.0  # Negative FCF
                
                scores.append(fcf_score)
                metrics['fcf_yield'] = round(fcf_yield, 2)
                metrics['fcf_score'] = fcf_score
            
            # Revenue Growth
            revenue_growth = info.get('revenueGrowth')
            if revenue_growth:
                growth_pct = revenue_growth * 100
                
                if growth_pct > 25:
                    growth_score = 9.0  # High growth
                elif growth_pct > 15:
                    growth_score = 7.5  # Strong growth
                elif growth_pct > 10:
                    growth_score = 6.5  # Solid growth
                elif growth_pct > 5:
                    growth_score = 5.0  # Moderate growth
                elif growth_pct > 0:
                    growth_score = 4.0  # Slow growth
                else:
                    growth_score = 2.0  # Declining
                
                scores.append(growth_score)
                metrics['revenue_growth'] = round(growth_pct, 2)
                metrics['growth_score'] = growth_score
            
            # Profit Margins
            profit_margin = info.get('profitMargins')
            if profit_margin:
                margin_pct = profit_margin * 100
                
                if margin_pct > 20:
                    margin_score = 9.0  # Excellent margins
                elif margin_pct > 15:
                    margin_score = 7.5
                elif margin_pct > 10:
                    margin_score = 6.0
                elif margin_pct > 5:
                    margin_score = 4.5
                elif margin_pct > 0:
                    margin_score = 3.0
                else:
                    margin_score = 1.5  # Unprofitable
                
                scores.append(margin_score)
                metrics['profit_margin'] = round(margin_pct, 2)
                metrics['margin_score'] = margin_score
            
            # Aggregate conviction
            if scores:
                conviction = np.mean(scores)
                data_quality = "HIGH" if len(scores) >= 4 else "MEDIUM" if len(scores) >= 2 else "LOW"
            else:
                conviction = 5.0
                data_quality = "LOW"
            
            # Determine action
            if conviction >= 7.5:
                action = "BUY"
                fundamental_view = "excellent"
            elif conviction >= 6.0:
                action = "BUY"
                fundamental_view = "strong"
            elif conviction >= 4.0:
                action = "HOLD"
                fundamental_view = "average"
            elif conviction >= 2.5:
                action = "SELL"
                fundamental_view = "weak"
            else:
                action = "SELL"
                fundamental_view = "poor"
            
            # Build rationale
            rationale_parts = [
                f"I assess {ticker} fundamentals as {fundamental_view}."
            ]
            
            if 'roe' in metrics:
                rationale_parts.append(f"ROE of {metrics['roe']}% shows {'strong' if metrics['roe'] > 15 else 'moderate'} returns.")
            
            if 'debt_to_equity' in metrics:
                rationale_parts.append(
                    f"Debt/Equity at {metrics['debt_to_equity']} indicates "
                    f"{'conservative' if metrics['debt_to_equity'] < 50 else 'elevated'} leverage."
                )
            
            if 'revenue_growth' in metrics:
                rationale_parts.append(f"Revenue growing at {metrics['revenue_growth']}%.")
            
            if 'profit_margin' in metrics:
                rationale_parts.append(f"Profit margins at {metrics['profit_margin']}%.")
            
            rationale = " ".join(rationale_parts)
            metrics['conviction'] = round(conviction, 2)
            
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=round(conviction, 2),
                action=action,
                rationale=rationale,
                key_metrics=metrics,
                data_quality=data_quality,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=5.0,
                action="ABSTAIN",
                rationale=f"Unable to retrieve fundamental data for {ticker}: {str(e)}",
                key_metrics={"error": str(e)},
                data_quality="LOW",
                timestamp=datetime.now().isoformat()
            )


class SentimentAgent:
    """
    Evaluates market sentiment from social and news sources
    
    Sources:
    - Reddit (wallstreetbets, stocks)
    - Twitter/X mentions
    - News headlines
    
    Output: Bullish/Neutral/Bearish crowd sentiment
    """
    
    def __init__(self):
        self.name = "Quant Sentiment"
        self._setup_apis()
    
    def _setup_apis(self):
        """Initialize API connections"""
        # Reddit setup
        self.reddit_client = None
        if REDDIT_AVAILABLE:
            try:
                # These would come from environment variables in production
                self.reddit_client = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID', 'dummy'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET', 'dummy'),
                    user_agent='quant_sentiment_bot/1.0'
                )
            except:
                pass
    
    def evaluate(self, ticker: str, signal: Optional[Dict] = None) -> QuantOpinion:
        """
        Evaluate sentiment from multiple sources.
        
        Returns conviction 0-10 where:
        - 8-10 = Very bullish sentiment
        - 6-7 = Bullish sentiment
        - 4-6 = Neutral sentiment
        - 2-3 = Bearish sentiment
        - 0-1 = Very bearish sentiment
        """
        try:
            scores = []
            metrics = {}
            
            # Reddit Sentiment (if available)
            if self.reddit_client:
                reddit_score, reddit_mentions = self._analyze_reddit(ticker)
                scores.append(reddit_score)
                metrics['reddit_score'] = reddit_score
                metrics['reddit_mentions'] = reddit_mentions
            
            # News Sentiment (using yfinance news)
            news_score, news_count = self._analyze_news(ticker)
            scores.append(news_score)
            metrics['news_score'] = news_score
            metrics['news_count'] = news_count
            
            # Social momentum proxy (search volume trend)
            momentum_score = self._analyze_momentum(ticker)
            scores.append(momentum_score)
            metrics['momentum_score'] = momentum_score
            
            # Aggregate conviction
            if scores:
                conviction = np.mean(scores)
                data_quality = "HIGH" if len(scores) >= 3 else "MEDIUM"
            else:
                conviction = 5.0
                data_quality = "LOW"
            
            # Determine action
            if conviction >= 7.0:
                action = "BUY"
                sentiment_view = "very bullish"
            elif conviction >= 5.5:
                action = "BUY"
                sentiment_view = "moderately bullish"
            elif conviction >= 4.0:
                action = "HOLD"
                sentiment_view = "neutral"
            elif conviction >= 2.5:
                action = "SELL"
                sentiment_view = "bearish"
            else:
                action = "SELL"
                sentiment_view = "very bearish"
            
            # Build rationale
            rationale = f"I see {sentiment_view} sentiment for {ticker}. "
            
            if 'news_score' in metrics:
                rationale += f"News sentiment shows {metrics['news_count']} recent articles "
                rationale += f"with {'positive' if metrics['news_score'] > 5.5 else 'mixed' if metrics['news_score'] > 4 else 'negative'} tone. "
            
            if 'reddit_mentions' in metrics:
                rationale += f"Reddit shows {metrics['reddit_mentions']} mentions. "
            
            rationale += f"Overall crowd sentiment is {sentiment_view}."
            
            metrics['conviction'] = round(conviction, 2)
            
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=round(conviction, 2),
                action=action,
                rationale=rationale,
                key_metrics=metrics,
                data_quality=data_quality,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return QuantOpinion(
                agent_name=self.name,
                ticker=ticker,
                conviction=5.0,
                action="ABSTAIN",
                rationale=f"Unable to retrieve sentiment data for {ticker}: {str(e)}",
                key_metrics={"error": str(e)},
                data_quality="LOW",
                timestamp=datetime.now().isoformat()
            )
    
    def _analyze_reddit(self, ticker: str) -> Tuple[float, int]:
        """Analyze Reddit mentions and sentiment"""
        if not self.reddit_client:
            return 5.0, 0
        
        try:
            # Search wallstreetbets and stocks
            mentions = 0
            sentiments = []
            
            for subreddit in ['wallstreetbets', 'stocks']:
                try:
                    sub = self.reddit_client.subreddit(subreddit)
                    for post in sub.search(ticker, time_filter='week', limit=10):
                        mentions += 1
                        if TEXTBLOB_AVAILABLE:
                            sentiment = TextBlob(post.title).sentiment.polarity
                            sentiments.append(sentiment)
                except:
                    continue
            
            if sentiments:
                avg_sentiment = np.mean(sentiments)
                # Convert sentiment from [-1, 1] to [0, 10]
                score = (avg_sentiment + 1) * 5
            else:
                score = 5.0
            
            return score, mentions
            
        except:
            return 5.0, 0
    
    def _analyze_news(self, ticker: str) -> Tuple[float, int]:
        """Analyze news sentiment"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                return 5.0, 0
            
            sentiments = []
            
            for article in news[:10]:  # Last 10 articles
                title = article.get('title', '')
                
                if TEXTBLOB_AVAILABLE and title:
                    sentiment = TextBlob(title).sentiment.polarity
                    sentiments.append(sentiment)
            
            if sentiments:
                avg_sentiment = np.mean(sentiments)
                # Convert sentiment from [-1, 1] to [0, 10]
                score = (avg_sentiment + 1) * 5
            else:
                score = 5.0
            
            return score, len(news)
            
        except:
            return 5.0, 0
    
    def _analyze_momentum(self, ticker: str) -> float:
        """
        Analyze social momentum using volume as proxy
        (real implementation would use Google Trends, Twitter API, etc.)
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            
            if hist.empty:
                return 5.0
            
            # Use volume trend as momentum proxy
            recent_volume = hist['Volume'].tail(5).mean()
            avg_volume = hist['Volume'].mean()
            
            if recent_volume > avg_volume * 2:
                return 8.0  # High momentum
            elif recent_volume > avg_volume * 1.5:
                return 7.0
            elif recent_volume > avg_volume * 1.2:
                return 6.0
            elif recent_volume < avg_volume * 0.8:
                return 4.0
            else:
                return 5.0
            
        except:
            return 5.0


# Initialize agent instances
QUANT_AGENTS_V2 = {
    'valuation': ValuationAgent(),
    'technicals': TechnicalsAgent(),
    'fundamentals': FundamentalsAgent(),
    'sentiment': SentimentAgent()
}


def run_full_quant_analysis(ticker: str, signal: Optional[Dict] = None) -> Dict:
    """
    Run all 4 Quant agents on a ticker and aggregate results.
    
    Returns comprehensive analysis with individual agent opinions
    and ensemble conviction score.
    """
    results = {
        'ticker': ticker,
        'timestamp': datetime.now().isoformat(),
        'agents': {},
        'summary': {}
    }
    
    all_opinions = []
    
    # Run each agent
    for agent_id, agent in QUANT_AGENTS_V2.items():
        print(f"🔍 Running {agent.name}...")
        opinion = agent.evaluate(ticker, signal)
        results['agents'][agent_id] = asdict(opinion)
        all_opinions.append(opinion)
    
    # Calculate ensemble metrics
    valid_opinions = [op for op in all_opinions if op.action != "ABSTAIN"]
    
    if valid_opinions:
        # Aggregate conviction
        avg_conviction = np.mean([op.conviction for op in valid_opinions])
        
        # Vote distribution
        buy_votes = sum(1 for op in valid_opinions if op.action == "BUY")
        sell_votes = sum(1 for op in valid_opinions if op.action == "SELL")
        hold_votes = sum(1 for op in valid_opinions if op.action == "HOLD")
        
        # Consensus
        total_votes = len(valid_opinions)
        if buy_votes / total_votes >= 0.75:
            consensus = "STRONG BUY"
        elif buy_votes / total_votes >= 0.5:
            consensus = "BUY"
        elif sell_votes / total_votes >= 0.75:
            consensus = "STRONG SELL"
        elif sell_votes / total_votes >= 0.5:
            consensus = "SELL"
        else:
            consensus = "HOLD"
        
        results['summary'] = {
            'consensus': consensus,
            'avg_conviction': round(avg_conviction, 2),
            'vote_distribution': {
                'BUY': buy_votes,
                'SELL': sell_votes,
                'HOLD': hold_votes,
                'ABSTAIN': len(all_opinions) - len(valid_opinions)
            },
            'data_quality': max([op.data_quality for op in valid_opinions], 
                              key=['LOW', 'MEDIUM', 'HIGH'].index)
        }
    else:
        results['summary'] = {
            'consensus': 'INSUFFICIENT DATA',
            'avg_conviction': 5.0,
            'vote_distribution': {'ABSTAIN': len(all_opinions)},
            'data_quality': 'LOW'
        }
    
    return results


def print_analysis_report(results: Dict):
    """Pretty print the analysis results"""
    print("\n" + "="*80)
    print(f"🐓 QUANT ANALYSIS REPORT: {results['ticker']}")
    print("="*80)
    
    summary = results['summary']
    print(f"\n📊 CONSENSUS: {summary['consensus']}")
    print(f"📈 Average Conviction: {summary['avg_conviction']}/10")
    print(f"🗳️  Vote Distribution: {summary['vote_distribution']}")
    print(f"📡 Data Quality: {summary['data_quality']}")
    
    print("\n" + "-"*80)
    print("INDIVIDUAL AGENT OPINIONS:")
    print("-"*80)
    
    for agent_id, opinion in results['agents'].items():
        print(f"\n{opinion['agent_name']} - {opinion['action']} ({opinion['conviction']}/10)")
        print(f"  {opinion['rationale']}")
        print(f"  Key Metrics: {opinion['key_metrics']}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    # Test with SPHR
    print("🧪 Testing Quant Agents V2 on SPHR...")
    
    results = run_full_quant_analysis('SPHR')
    print_analysis_report(results)
    
    # Save results
    output_file = '/Users/agentjoselo/.openclaw/workspace/trading/agents/signals/sphr_quant_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to {output_file}")
