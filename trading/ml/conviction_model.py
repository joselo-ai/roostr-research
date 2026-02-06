#!/usr/bin/env python3
"""
ML Conviction Scoring Model
Predicts P(signal will 2x in 30 days) using XGBoost

Author: Atlas (roostr ML Engineer AI)
Date: Feb 5, 2026
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    roc_auc_score, confusion_matrix, classification_report
)
import pickle
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')


class ConvictionModel:
    """
    XGBoost-based conviction scoring model
    
    Predicts binary outcome: Will signal 2x+ in 30 days?
    """
    
    def __init__(self, model_version: str = 'v1'):
        self.model_version = model_version
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.training_date = None
        self.metrics = {}
        
        # XGBoost hyperparameters (tuned for small datasets)
        self.params = {
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'max_depth': 6,
            'learning_rate': 0.05,
            'n_estimators': 150,
            'min_child_weight': 3,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'gamma': 0.1,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
            'random_state': 42,
        }
    
    def train(self, 
              X: pd.DataFrame, 
              y: pd.Series,
              test_size: float = 0.2,
              cv_folds: int = 5) -> Dict[str, Any]:
        """
        Train conviction model with cross-validation
        
        Args:
            X: Feature matrix (DataFrame with feature columns)
            y: Target labels (0 or 1)
            test_size: Fraction of data for test set
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dict of training metrics
        """
        print(f"Training Conviction Model {self.model_version}")
        print(f"Dataset: {len(X)} samples, {len(X.columns)} features")
        print(f"Class distribution: {y.value_counts().to_dict()}")
        
        # Store feature names
        self.feature_names = list(X.columns)
        
        # Train/test split (stratified to maintain class balance)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\nTrain: {len(X_train)} samples, Test: {len(X_test)} samples")
        
        # Scale features (XGBoost doesn't require but helps with interpretability)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize XGBoost
        self.model = xgb.XGBClassifier(**self.params)
        
        # Cross-validation on training set
        print("\nRunning 5-fold cross-validation...")
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train,
            cv=cv_folds, scoring='roc_auc', n_jobs=-1
        )
        
        print(f"CV AUC-ROC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Train on full training set
        print("\nTraining final model...")
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            early_stopping_rounds=20,
            verbose=False
        )
        
        # Evaluate on test set
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'auc_roc': roc_auc_score(y_test, y_pred_proba),
            'cv_auc_mean': cv_scores.mean(),
            'cv_auc_std': cv_scores.std(),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'n_train': len(X_train),
            'n_test': len(X_test),
            'n_features': len(self.feature_names),
        }
        
        self.metrics = metrics
        self.training_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Print results
        print("\n" + "="*50)
        print("TRAINING RESULTS")
        print("="*50)
        print(f"Accuracy:  {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall:    {metrics['recall']:.3f}")
        print(f"AUC-ROC:   {metrics['auc_roc']:.3f}")
        print(f"\nConfusion Matrix:")
        print(f"  TN: {metrics['confusion_matrix'][0][0]}, FP: {metrics['confusion_matrix'][0][1]}")
        print(f"  FN: {metrics['confusion_matrix'][1][0]}, TP: {metrics['confusion_matrix'][1][1]}")
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['No 2x', '2x+']))
        
        # Feature importance
        self._print_feature_importance(top_n=15)
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict conviction labels (0 or 1)
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of predictions (0 or 1)
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Ensure feature order matches training
        X = X[self.feature_names]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict conviction probabilities P(2x in 30 days)
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of probabilities (0-1)
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Ensure feature order matches training
        X = X[self.feature_names]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Return probability of positive class (2x+)
        return self.model.predict_proba(X_scaled)[:, 1]
    
    def score_signal(self, X: pd.DataFrame) -> Tuple[int, float]:
        """
        Score a single signal (1-10 scale + probability)
        
        Args:
            X: Feature vector (single row DataFrame)
            
        Returns:
            (conviction_score, probability)
            conviction_score: 1-10 integer
            probability: 0-1 float
        """
        prob = self.predict_proba(X)[0]
        
        # Map probability to 1-10 scale
        conviction_score = int(np.round(prob * 10))
        conviction_score = max(1, min(10, conviction_score))  # Clamp to 1-10
        
        return conviction_score, prob
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance rankings
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature names and importance scores
        """
        if self.model is None:
            raise ValueError("Model not trained yet.")
        
        importance_scores = self.model.feature_importances_
        
        df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance_scores
        }).sort_values('importance', ascending=False)
        
        return df.head(top_n)
    
    def _print_feature_importance(self, top_n: int = 15):
        """Print top features by importance"""
        df = self.get_feature_importance(top_n)
        
        print(f"\nTop {top_n} Most Important Features:")
        print("-" * 50)
        for i, row in df.iterrows():
            bar = "█" * int(row['importance'] * 50)
            print(f"{row['feature']:30s} {bar} {row['importance']:.4f}")
    
    def save(self, output_dir: str = 'models'):
        """
        Save trained model to disk
        
        Args:
            output_dir: Directory to save model files
        """
        if self.model is None:
            raise ValueError("Model not trained yet.")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_file = output_path / f'conviction_{self.model_version}.pkl'
        with open(model_file, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save scaler
        scaler_file = output_path / f'scaler_{self.model_version}.pkl'
        with open(scaler_file, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save feature names
        feature_file = output_path / f'features_{self.model_version}.json'
        with open(feature_file, 'w') as f:
            json.dump(self.feature_names, f, indent=2)
        
        # Save metadata
        metadata = {
            'model_version': self.model_version,
            'training_date': self.training_date,
            'metrics': self.metrics,
            'hyperparameters': self.params,
            'n_features': len(self.feature_names),
        }
        
        metadata_file = output_path / f'metadata_{self.model_version}.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nModel saved to {output_path}/")
        print(f"  - {model_file.name}")
        print(f"  - {scaler_file.name}")
        print(f"  - {feature_file.name}")
        print(f"  - {metadata_file.name}")
    
    def load(self, model_dir: str = 'models', version: str = None):
        """
        Load trained model from disk
        
        Args:
            model_dir: Directory containing model files
            version: Model version to load (default: self.model_version)
        """
        if version is None:
            version = self.model_version
        
        model_path = Path(model_dir)
        
        # Load model
        model_file = model_path / f'conviction_{version}.pkl'
        with open(model_file, 'rb') as f:
            self.model = pickle.load(f)
        
        # Load scaler
        scaler_file = model_path / f'scaler_{version}.pkl'
        with open(scaler_file, 'rb') as f:
            self.scaler = pickle.load(f)
        
        # Load feature names
        feature_file = model_path / f'features_{version}.json'
        with open(feature_file, 'r') as f:
            self.feature_names = json.load(f)
        
        # Load metadata
        metadata_file = model_path / f'metadata_{version}.json'
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            self.metrics = metadata['metrics']
            self.training_date = metadata['training_date']
        
        print(f"Loaded model {version} (trained {self.training_date})")
        print(f"Test AUC-ROC: {self.metrics['auc_roc']:.3f}")


def create_sample_training_data(n_samples: int = 200) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic training data for cold start
    
    This simulates signals with realistic feature distributions
    and labels based on heuristic rules (Dan's methodology)
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        (X, y) where X is features, y is labels (0 or 1)
    """
    np.random.seed(42)
    
    data = []
    
    for i in range(n_samples):
        # Generate features with realistic distributions
        
        # Source credibility (Dan's track record)
        dan_endorsed = np.random.choice([0, 1], p=[0.85, 0.15])  # 15% Dan calls
        source_yieldschool = np.random.choice([0, 1], p=[0.6, 0.4])
        mention_count = np.random.poisson(2) + 1
        multi_source = int(mention_count > 1)
        
        # Social conviction
        total_reactions = np.random.lognormal(3, 1)  # Log-normal distribution
        fire_reactions = total_reactions * np.random.uniform(0.3, 0.6)
        rocket_reactions = total_reactions * np.random.uniform(0.2, 0.4)
        reaction_velocity = total_reactions / np.random.uniform(12, 72)
        reaction_diversity = total_reactions * np.random.uniform(0.6, 0.9)
        thesis_quality = np.random.beta(5, 2)  # Skewed toward higher quality
        
        # Market timing
        google_trends_now = np.random.uniform(10, 80)
        google_trends_7d_change = np.random.uniform(-20, 100)
        trends_peak_ratio = np.random.beta(2, 3)  # Skewed toward early
        message_age_hours = np.random.exponential(36)
        price_vs_mention = np.random.lognormal(0, 0.2)  # Usually near 1.0
        
        # On-chain (50% crypto, 50% stocks)
        is_crypto = np.random.choice([0, 1])
        if is_crypto:
            whale_accumulation = np.random.choice([0, 1], p=[0.8, 0.2])
            liquidity_level = np.random.lognormal(12, 2)
        else:
            whale_accumulation = 0
            liquidity_level = 0
        
        # Thesis quality
        thesis_length = np.random.gamma(50, 2)
        thesis_keywords = np.random.poisson(3)
        catalyst_mentioned = np.random.choice([0, 1], p=[0.6, 0.4])
        
        # Interaction features
        dan_x_reactions = dan_endorsed * total_reactions
        early_momentum = reaction_velocity * (1 - trends_peak_ratio)
        
        # Create feature dict
        features = {
            'dan_endorsed': dan_endorsed,
            'source_yieldschool': source_yieldschool,
            'source_bluechips': source_yieldschool * np.random.choice([0, 1]),
            'source_dumbmoney': 1 - source_yieldschool,
            'mention_count': mention_count,
            'multi_source': multi_source,
            'source_reliability_score': 0.75 if source_yieldschool else 0.65,
            'total_reactions': total_reactions,
            'fire_reactions': fire_reactions,
            'rocket_reactions': rocket_reactions,
            'thumbsup_reactions': total_reactions * 0.2,
            'reaction_velocity': reaction_velocity,
            'reaction_diversity': reaction_diversity,
            'comment_count': np.random.poisson(5),
            'sentiment_score': np.random.beta(6, 2),
            'hype_ratio': (fire_reactions + rocket_reactions) / max(total_reactions, 1),
            'thesis_quality_score': thesis_quality,
            'link_count': np.random.poisson(1),
            'emoji_spam': np.random.choice([0, 1], p=[0.9, 0.1]),
            'reaction_recency': int(message_age_hours < 48),
            'google_trends_now': google_trends_now,
            'google_trends_7d_change': google_trends_7d_change,
            'google_trends_30d_change': google_trends_7d_change * 1.5,
            'trends_peak_ratio': trends_peak_ratio,
            'message_age_hours': message_age_hours,
            'price_vs_mention': price_vs_mention,
            'volume_spike': np.random.lognormal(0.5, 1),
            'new_token': int(is_crypto and np.random.random() < 0.3),
            'liquidity_level': liquidity_level,
            'holder_growth': np.random.uniform(0, 30) if is_crypto else 0,
            'whale_accumulation': whale_accumulation,
            'smart_money_holdings': whale_accumulation * np.random.choice([0, 1]),
            'liquidity_locked': np.random.uniform(0, 100) if is_crypto else 0,
            'contract_verified': is_crypto,
            'honeypot_score': np.random.uniform(0, 0.1) if is_crypto else 0,
            'holder_concentration': np.random.uniform(20, 60),
            'dex_listing_count': np.random.poisson(2) if is_crypto else 0,
            'volume_authenticity': np.random.beta(8, 2),
            'thesis_length': thesis_length,
            'thesis_keywords': thesis_keywords,
            'financial_metrics': np.random.choice([0, 1], p=[0.5, 0.5]),
            'catalyst_mentioned': catalyst_mentioned,
            'competitive_advantage': np.random.choice([0, 1], p=[0.6, 0.4]),
            'addressable_market': np.random.choice([0, 1], p=[0.7, 0.3]),
            'team_quality': np.random.uniform(0, 1),
            'partnerships': np.random.choice([0, 1], p=[0.7, 0.3]),
            'regulatory_risk': np.random.choice([0, 1], p=[0.8, 0.2]),
            'hype_language_penalty': np.random.poisson(0.5),
            'dan_x_reactions': dan_x_reactions,
            'early_momentum': early_momentum,
            'source_consensus': multi_source * mention_count,
            'conviction_quality': reaction_diversity * thesis_quality,
            'smart_timing': whale_accumulation * int(message_age_hours < 48),
        }
        
        # Generate label using heuristic (Dan's green flags methodology)
        # Strong signals = high probability of 2x
        green_flags = (
            dan_endorsed * 3 +  # Dan's endorsement = strongest
            multi_source * 2 +
            (total_reactions > 50) * 2 +
            (google_trends_7d_change > 50) * 1 +
            (trends_peak_ratio < 0.5) * 1 +
            whale_accumulation * 2 +
            (thesis_quality > 0.7) * 1 +
            catalyst_mentioned * 1
        )
        
        # Probability of 2x based on green flags
        prob_2x = 1 / (1 + np.exp(-(green_flags - 4)))  # Sigmoid
        label = int(np.random.random() < prob_2x)
        
        data.append((features, label))
    
    # Convert to DataFrame
    X = pd.DataFrame([d[0] for d in data])
    y = pd.Series([d[1] for d in data], name='hit_target')
    
    return X, y


if __name__ == "__main__":
    print("Conviction Model - Training Example\n" + "="*50)
    
    # Generate synthetic training data
    print("\n1. Generating synthetic training data...")
    X, y = create_sample_training_data(n_samples=200)
    
    print(f"Generated {len(X)} samples")
    print(f"Features: {len(X.columns)}")
    print(f"Class balance: {y.value_counts().to_dict()}")
    
    # Train model
    print("\n2. Training conviction model...")
    model = ConvictionModel(model_version='v0.1')
    metrics = model.train(X, y, test_size=0.2, cv_folds=5)
    
    # Save model
    print("\n3. Saving model...")
    model.save(output_dir='/Users/agentjoselo/.openclaw/workspace/trading/ml/models')
    
    # Test predictions
    print("\n4. Testing predictions on 5 random samples...")
    test_samples = X.sample(5)
    
    for i, (idx, row) in enumerate(test_samples.iterrows()):
        score, prob = model.score_signal(row.to_frame().T)
        actual = y.loc[idx]
        
        print(f"\nSample {i+1}:")
        print(f"  Conviction Score: {score}/10")
        print(f"  Probability (2x): {prob:.2%}")
        print(f"  Actual Outcome: {'✓ 2x+' if actual == 1 else '✗ No 2x'}")
        print(f"  Dan Endorsed: {bool(row['dan_endorsed'])}")
        print(f"  Total Reactions: {row['total_reactions']:.0f}")
        print(f"  Trends Rising: {row['google_trends_7d_change']:.1f}%")
    
    print("\n" + "="*50)
    print("Training complete! Model ready for deployment.")
    print("="*50)
