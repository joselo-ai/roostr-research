#!/usr/bin/env python3
"""
Feature Engineering for Conviction Scoring ML Model
Transforms raw signals into 45+ features for XGBoost training

Author: Atlas (roostr ML Engineer AI)
Date: Feb 5, 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')


class FeatureEngineer:
    """Extract ML features from raw trading signals"""
    
    def __init__(self):
        # Dan's green flag weights
        self.dan_weight = 3.0
        self.multi_source_weight = 2.0
        self.fire_emoji_weight = 0.15
        self.rocket_emoji_weight = 0.15
        
        # Thesis quality keywords
        self.quality_keywords = [
            'revenue', 'growth', 'earnings', 'profit', 'market share',
            'moat', 'competitive advantage', 'addressable market', 'tam',
            'partnership', 'patent', 'first mover', 'network effect'
        ]
        
        # Hype spam keywords (penalty)
        self.hype_keywords = [
            'moon', 'lambo', 'to the moon', '100x', '1000x', 'life changing'
        ]
        
        # Catalyst keywords
        self.catalyst_keywords = [
            'approval', 'fda', 'fcc', 'earnings', 'launch', 'release',
            'partnership announced', 'acquisition', 'merger'
        ]
    
    def extract_features(self, signal: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract all features from a raw signal
        
        Args:
            signal: Dict with keys like ticker, source, message, reactions, etc.
            
        Returns:
            Dict of 45+ engineered features
        """
        features = {}
        
        # 1. Source credibility features
        features.update(self._extract_source_features(signal))
        
        # 2. Social conviction features
        features.update(self._extract_social_features(signal))
        
        # 3. Market timing features
        features.update(self._extract_timing_features(signal))
        
        # 4. On-chain features (crypto only)
        if signal.get('asset_type') == 'crypto':
            features.update(self._extract_onchain_features(signal))
        else:
            # Fill with zeros for stocks
            features.update(self._onchain_zeros())
        
        # 5. Fundamental quality features
        features.update(self._extract_thesis_features(signal))
        
        # 6. Interaction features
        features.update(self._extract_interactions(features, signal))
        
        return features
    
    def _extract_source_features(self, signal: Dict[str, Any]) -> Dict[str, float]:
        """Extract source credibility features"""
        source = signal.get('source', '')
        
        return {
            'dan_endorsed': float(signal.get('dan_endorsed', False)),
            'source_yieldschool': float('yieldschool' in source.lower()),
            'source_bluechips': float('bluechip' in source.lower()),
            'source_dumbmoney': float('dumbmoney' in source.lower()),
            'mention_count': float(signal.get('mention_count', 1)),
            'multi_source': float(signal.get('mention_count', 1) > 1),
            'source_reliability_score': self._get_source_reliability(source),
        }
    
    def _extract_social_features(self, signal: Dict[str, Any]) -> Dict[str, float]:
        """Extract social conviction features"""
        reactions = signal.get('reactions', {})
        message = signal.get('message', '')
        
        # Count reactions
        total_reactions = signal.get('total_reactions', sum(reactions.values()))
        fire_reactions = reactions.get('🔥', 0) + reactions.get('fire', 0)
        rocket_reactions = reactions.get('🚀', 0) + reactions.get('rocket', 0)
        thumbsup_reactions = reactions.get('👍', 0) + reactions.get('thumbsup', 0)
        
        # Reaction velocity (reactions per hour)
        message_age_hours = signal.get('message_age_hours', 24)
        reaction_velocity = total_reactions / max(message_age_hours, 1)
        
        # Reaction diversity (unique reactors)
        reaction_diversity = signal.get('unique_reactors', int(total_reactions * 0.7))  # Estimate
        
        # Hype ratio
        hype_reactions = fire_reactions + rocket_reactions
        hype_ratio = hype_reactions / max(total_reactions, 1)
        
        # Emoji spam detection
        emoji_spam = self._detect_emoji_spam(message)
        
        # Sentiment score (simple heuristic)
        sentiment_score = self._calculate_sentiment(message)
        
        # Thesis quality
        thesis_quality = self._calculate_thesis_quality(message)
        
        return {
            'total_reactions': float(total_reactions),
            'fire_reactions': float(fire_reactions),
            'rocket_reactions': float(rocket_reactions),
            'thumbsup_reactions': float(thumbsup_reactions),
            'reaction_velocity': float(reaction_velocity),
            'reaction_diversity': float(reaction_diversity),
            'comment_count': float(signal.get('comment_count', 0)),
            'sentiment_score': sentiment_score,
            'hype_ratio': hype_ratio,
            'thesis_quality_score': thesis_quality,
            'link_count': float(len(re.findall(r'http\S+', message))),
            'emoji_spam': float(emoji_spam),
            'reaction_recency': float(message_age_hours < 48),
        }
    
    def _extract_timing_features(self, signal: Dict[str, Any]) -> Dict[str, float]:
        """Extract market timing features"""
        google_trends = signal.get('google_trends', {})
        
        # Google Trends metrics
        trends_now = google_trends.get('current', 50)
        trends_7d_ago = google_trends.get('7d_ago', 40)
        trends_30d_ago = google_trends.get('30d_ago', 30)
        trends_peak = google_trends.get('peak', 100)
        
        # Calculate changes
        trends_7d_change = ((trends_now - trends_7d_ago) / max(trends_7d_ago, 1)) * 100
        trends_30d_change = ((trends_now - trends_30d_ago) / max(trends_30d_ago, 1)) * 100
        trends_peak_ratio = trends_now / max(trends_peak, 1)
        
        # Price metrics
        price_at_mention = signal.get('price_at_mention', 1.0)
        current_price = signal.get('current_price', price_at_mention)
        price_vs_mention = current_price / max(price_at_mention, 0.01)
        
        # Volume
        volume_now = signal.get('volume_24h', 0)
        volume_avg = signal.get('volume_30d_avg', volume_now)
        volume_spike = volume_now / max(volume_avg, 1)
        
        # Age metrics
        message_age_hours = signal.get('message_age_hours', 24)
        token_age_days = signal.get('token_age_days', 365)
        
        return {
            'google_trends_now': float(trends_now),
            'google_trends_7d_change': float(trends_7d_change),
            'google_trends_30d_change': float(trends_30d_change),
            'trends_peak_ratio': float(trends_peak_ratio),
            'message_age_hours': float(message_age_hours),
            'price_vs_mention': float(price_vs_mention),
            'volume_spike': float(volume_spike),
            'new_token': float(token_age_days < 30),
        }
    
    def _extract_onchain_features(self, signal: Dict[str, Any]) -> Dict[str, float]:
        """Extract on-chain features (crypto only)"""
        onchain = signal.get('onchain_data', {})
        
        return {
            'liquidity_level': float(onchain.get('liquidity', 0)),
            'holder_growth': float(onchain.get('holder_growth_7d', 0)),
            'whale_accumulation': float(onchain.get('whale_buying', False)),
            'smart_money_holdings': float(onchain.get('smart_money_holds', False)),
            'liquidity_locked': float(onchain.get('liquidity_locked_pct', 0)),
            'contract_verified': float(onchain.get('verified', False)),
            'honeypot_score': float(onchain.get('honeypot_score', 0)),
            'holder_concentration': float(onchain.get('top10_pct', 50)),
            'dex_listing_count': float(onchain.get('dex_count', 0)),
            'volume_authenticity': float(onchain.get('volume_authenticity', 0.5)),
        }
    
    def _onchain_zeros(self) -> Dict[str, float]:
        """Return zeros for on-chain features (when not crypto)"""
        return {
            'liquidity_level': 0.0,
            'holder_growth': 0.0,
            'whale_accumulation': 0.0,
            'smart_money_holdings': 0.0,
            'liquidity_locked': 0.0,
            'contract_verified': 0.0,
            'honeypot_score': 0.0,
            'holder_concentration': 0.0,
            'dex_listing_count': 0.0,
            'volume_authenticity': 0.0,
        }
    
    def _extract_thesis_features(self, signal: Dict[str, Any]) -> Dict[str, float]:
        """Extract fundamental/thesis quality features"""
        message = signal.get('message', '')
        message_lower = message.lower()
        
        # Thesis length
        thesis_length = len(message.split())
        
        # Count quality keywords
        thesis_keywords = sum(1 for kw in self.quality_keywords if kw in message_lower)
        
        # Financial metrics mentioned
        financial_metrics = float(any(word in message_lower for word in 
                                     ['p/e', 'revenue', 'earnings', 'ebitda', 'market cap']))
        
        # Catalyst mentioned
        catalyst_mentioned = float(any(word in message_lower for word in self.catalyst_keywords))
        
        # Competitive advantage
        competitive_advantage = float(any(word in message_lower for word in 
                                         ['moat', 'first mover', 'patent', 'network effect']))
        
        # Addressable market
        addressable_market = float('tam' in message_lower or 'addressable market' in message_lower)
        
        # Team quality
        team_quality = float(any(word in message_lower for word in 
                                ['experienced team', 'y combinator', 'yc', 'founded']))
        
        # Partnerships
        partnerships = float(any(word in message_lower for word in 
                                ['partnership', 'partner with', 'partnered']))
        
        # Regulatory risk
        regulatory_risk = float(any(word in message_lower for word in 
                                   ['fda', 'fcc', 'sec', 'regulatory', 'approval pending']))
        
        # Hype language penalty
        hype_language_penalty = sum(1 for kw in self.hype_keywords if kw in message_lower)
        
        return {
            'thesis_length': float(thesis_length),
            'thesis_keywords': float(thesis_keywords),
            'financial_metrics': financial_metrics,
            'catalyst_mentioned': catalyst_mentioned,
            'competitive_advantage': competitive_advantage,
            'addressable_market': addressable_market,
            'team_quality': team_quality,
            'partnerships': partnerships,
            'regulatory_risk': regulatory_risk,
            'hype_language_penalty': float(hype_language_penalty),
        }
    
    def _extract_interactions(self, features: Dict[str, float], signal: Dict[str, Any]) -> Dict[str, float]:
        """Extract interaction features (non-linear combinations)"""
        return {
            'dan_x_reactions': features['dan_endorsed'] * features['total_reactions'],
            'early_momentum': features['reaction_velocity'] * (1 - features['trends_peak_ratio']),
            'source_consensus': features['multi_source'] * features['mention_count'],
            'conviction_quality': features['reaction_diversity'] * features['thesis_quality_score'],
            'smart_timing': features.get('whale_accumulation', 0) * (1 if features['message_age_hours'] < 48 else 0),
        }
    
    def _get_source_reliability(self, source: str) -> float:
        """
        Get historical reliability score for source
        
        TODO: Track actual win rates per source over time
        For now, use heuristic weights based on Dan's track record
        """
        source_lower = source.lower()
        
        if 'yieldschool' in source_lower and 'yield hub' in source_lower:
            return 0.85  # Dan's track record
        elif 'yieldschool' in source_lower:
            return 0.75
        elif 'dumbmoney' in source_lower:
            return 0.70  # Social arb
        else:
            return 0.50  # Unknown source
    
    def _detect_emoji_spam(self, message: str) -> bool:
        """Detect if message has excessive emoji spam"""
        # Count rocket/fire emojis
        rocket_count = message.count('🚀')
        fire_count = message.count('🔥')
        
        # If more than 3 repeated emojis = spam
        return rocket_count > 3 or fire_count > 3
    
    def _calculate_sentiment(self, message: str) -> float:
        """
        Calculate sentiment score (0-1)
        
        Simple heuristic: count positive vs negative words
        TODO: Use proper NLP (TextBlob, VADER) in production
        """
        positive_words = ['bullish', 'great', 'strong', 'buying', 'accumulating', 
                         'undervalued', 'opportunity', 'conviction']
        negative_words = ['bearish', 'weak', 'risky', 'overvalued', 'dump', 'scam']
        
        message_lower = message.lower()
        
        pos_count = sum(1 for word in positive_words if word in message_lower)
        neg_count = sum(1 for word in negative_words if word in message_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.5  # Neutral
        
        return pos_count / total
    
    def _calculate_thesis_quality(self, message: str) -> float:
        """
        Calculate thesis quality score (0-1)
        
        Based on length + keyword richness + structure
        """
        word_count = len(message.split())
        message_lower = message.lower()
        
        # Base score from length
        if word_count < 20:
            length_score = 0.2
        elif word_count < 50:
            length_score = 0.4
        elif word_count < 100:
            length_score = 0.6
        else:
            length_score = 0.8
        
        # Keyword richness
        keyword_count = sum(1 for kw in self.quality_keywords if kw in message_lower)
        keyword_score = min(keyword_count / 5, 1.0)  # Max 1.0 at 5+ keywords
        
        # Has links (research)
        link_score = 0.2 if 'http' in message else 0.0
        
        # Combined (weighted average)
        quality = 0.5 * length_score + 0.3 * keyword_score + 0.2 * link_score
        
        return min(quality, 1.0)
    
    def batch_extract(self, signals: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Extract features for multiple signals
        
        Args:
            signals: List of signal dicts
            
        Returns:
            DataFrame with rows=signals, columns=features
        """
        feature_dicts = []
        
        for signal in signals:
            features = self.extract_features(signal)
            
            # Add metadata (not used in training but useful for tracking)
            features['ticker'] = signal.get('ticker', 'UNKNOWN')
            features['source'] = signal.get('source', 'UNKNOWN')
            features['date_found'] = signal.get('date_found', datetime.now().strftime('%Y-%m-%d'))
            
            feature_dicts.append(features)
        
        df = pd.DataFrame(feature_dicts)
        
        # Reorder columns (metadata first, then features)
        metadata_cols = ['ticker', 'source', 'date_found']
        feature_cols = [col for col in df.columns if col not in metadata_cols]
        
        df = df[metadata_cols + feature_cols]
        
        return df
    
    def get_feature_names(self) -> List[str]:
        """
        Get list of all feature names (for model training)
        
        Returns:
            List of feature column names (excludes metadata)
        """
        # Generate dummy signal to get all features
        dummy_signal = {
            'ticker': 'DUMMY',
            'source': 'test',
            'message': 'test message',
            'reactions': {},
            'asset_type': 'crypto',
            'onchain_data': {},
        }
        
        features = self.extract_features(dummy_signal)
        
        # Exclude metadata
        return [k for k in features.keys() if k not in ['ticker', 'source', 'date_found']]


def test_feature_engineering():
    """Test feature extraction with sample signals"""
    
    # Sample signal: Dan's $TAO call (historical)
    tao_signal = {
        'ticker': 'TAO',
        'source': 'Yieldschool-YieldHub',
        'date_found': '2025-09-15',
        'message': '$TAO (Bittensor) is the most undervalued AI play in crypto. Dan has been accumulating. Real working product, decentralized AI inference. Partnership with Foundry. This is a 10-100x. Not financial advice but high conviction. 🔥',
        'reactions': {'🔥': 34, '🚀': 18, '👍': 15},
        'total_reactions': 67,
        'unique_reactors': 45,
        'comment_count': 12,
        'dan_endorsed': True,
        'mention_count': 5,
        'message_age_hours': 18,
        'price_at_mention': 12.50,
        'current_price': 13.00,
        'volume_24h': 4200000,
        'volume_30d_avg': 1000000,
        'token_age_days': 180,
        'google_trends': {
            'current': 23,
            '7d_ago': 14,
            '30d_ago': 8,
            'peak': 75,
        },
        'asset_type': 'crypto',
        'onchain_data': {
            'liquidity': 850000,
            'holder_growth_7d': 18,
            'whale_buying': True,
            'smart_money_holds': True,
            'liquidity_locked_pct': 65,
            'verified': True,
            'honeypot_score': 0,
            'top10_pct': 38,
            'dex_count': 3,
            'volume_authenticity': 0.88,
        }
    }
    
    # Sample signal: $ASTS from Dumb Money
    asts_signal = {
        'ticker': 'ASTS',
        'source': 'DumbMoney',
        'date_found': '2025-11-20',
        'message': '$ASTS SpaceMobile is first-mover in satellite-to-cell. Partnerships with AT&T, Verizon. Waiting on FCC approval. Market cap $3B but TAM is $38B (global mobile). Could 3x on approval.',
        'reactions': {'🔥': 28, '🚀': 14, '👍': 10},
        'total_reactions': 52,
        'unique_reactors': 38,
        'comment_count': 8,
        'dan_endorsed': False,
        'mention_count': 2,
        'message_age_hours': 24,
        'price_at_mention': 8.20,
        'current_price': 9.18,
        'volume_24h': 0,
        'volume_30d_avg': 0,
        'token_age_days': 365,
        'google_trends': {
            'current': 45,
            '7d_ago': 28,
            '30d_ago': 18,
            'peak': 85,
        },
        'asset_type': 'stock',
    }
    
    # Test feature extraction
    engineer = FeatureEngineer()
    
    print("Testing Feature Engineering\n" + "="*50)
    
    # Test single signal
    print("\n1. $TAO Signal Features:")
    tao_features = engineer.extract_features(tao_signal)
    for key, value in tao_features.items():
        print(f"  {key}: {value:.3f}" if isinstance(value, float) else f"  {key}: {value}")
    
    print("\n2. $ASTS Signal Features:")
    asts_features = engineer.extract_features(asts_signal)
    for key, value in asts_features.items():
        print(f"  {key}: {value:.3f}" if isinstance(value, float) else f"  {key}: {value}")
    
    # Test batch extraction
    print("\n3. Batch Extraction:")
    signals = [tao_signal, asts_signal]
    df = engineer.batch_extract(signals)
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"Feature count: {len(engineer.get_feature_names())}")
    
    # Save sample data
    df.to_csv('/Users/agentjoselo/.openclaw/workspace/trading/ml/data/sample_features.csv', index=False)
    print("\nSaved sample features to ml/data/sample_features.csv")


if __name__ == "__main__":
    test_feature_engineering()
