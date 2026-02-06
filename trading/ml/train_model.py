#!/usr/bin/env python3
"""
Training Pipeline for Conviction Model
Orchestrates data loading, feature engineering, training, and validation

Author: Atlas (roostr ML Engineer AI)
Date: Feb 5, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import sys

# Import our modules
from feature_engineering import FeatureEngineer
from conviction_model import ConvictionModel


class TrainingPipeline:
    """End-to-end training pipeline"""
    
    def __init__(self, 
                 data_path: str,
                 output_dir: str = 'models',
                 model_version: str = None):
        """
        Initialize training pipeline
        
        Args:
            data_path: Path to training data CSV
            output_dir: Directory to save trained model
            model_version: Model version string (auto-generated if None)
        """
        self.data_path = data_path
        self.output_dir = output_dir
        
        if model_version is None:
            # Auto-generate version: v1_YYYYMMDD
            date_str = datetime.now().strftime('%Y%m%d')
            self.model_version = f'v1_{date_str}'
        else:
            self.model_version = model_version
        
        self.engineer = FeatureEngineer()
        self.model = ConvictionModel(model_version=self.model_version)
        
        self.training_report = {}
    
    def load_data(self) -> pd.DataFrame:
        """
        Load training data from CSV
        
        Expected format: ml_training_data.csv with features + hit_target column
        
        Returns:
            DataFrame with training data
        """
        print(f"Loading data from {self.data_path}...")
        
        df = pd.read_csv(self.data_path)
        
        print(f"Loaded {len(df)} samples")
        print(f"Columns: {list(df.columns)}")
        
        # Validate required columns
        if 'hit_target' not in df.columns:
            raise ValueError("Training data must have 'hit_target' column")
        
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """
        Prepare features and target from raw data
        
        If data has raw signal columns (message, reactions, etc),
        run feature engineering. Otherwise, assume features already extracted.
        
        Args:
            df: Raw or feature-engineered DataFrame
            
        Returns:
            (X, y) where X is features, y is target
        """
        print("\nPreparing features...")
        
        # Check if data has raw signal columns or engineered features
        if 'message' in df.columns:
            # Raw signals - need feature engineering
            print("Detected raw signals, running feature engineering...")
            
            # Convert to list of signal dicts
            signals = df.to_dict('records')
            
            # Extract features
            feature_df = self.engineer.batch_extract(signals)
            
            # Get target
            y = df['hit_target']
            
            # Get feature columns (exclude metadata)
            metadata_cols = ['ticker', 'source', 'date_found']
            feature_cols = [col for col in feature_df.columns if col not in metadata_cols]
            
            X = feature_df[feature_cols]
            
        else:
            # Already feature-engineered
            print("Detected engineered features, using as-is...")
            
            # Separate features from target
            y = df['hit_target']
            
            # Remove metadata and target columns
            exclude_cols = ['ticker', 'source', 'date_found', 'hit_target']
            feature_cols = [col for col in df.columns if col not in exclude_cols]
            
            X = df[feature_cols]
        
        print(f"Features: {len(X.columns)} columns, {len(X)} samples")
        print(f"Target distribution: {y.value_counts().to_dict()}")
        
        return X, y
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """
        Train model and collect metrics
        
        Args:
            X: Feature matrix
            y: Target labels
            
        Returns:
            Dict of training metrics
        """
        print(f"\n{'='*60}")
        print(f"TRAINING MODEL {self.model_version}")
        print(f"{'='*60}")
        
        # Train model
        metrics = self.model.train(X, y, test_size=0.2, cv_folds=5)
        
        # Store in report
        self.training_report = {
            'model_version': self.model_version,
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset_size': len(X),
            'n_features': len(X.columns),
            'class_distribution': y.value_counts().to_dict(),
            'metrics': metrics,
            'feature_importance': self.model.get_feature_importance(top_n=20).to_dict('records'),
        }
        
        return metrics
    
    def save_model(self):
        """Save trained model and generate report"""
        # Save model files
        self.model.save(output_dir=self.output_dir)
        
        # Save training report
        report_path = Path(self.output_dir) / f'training_report_{self.model_version}.json'
        with open(report_path, 'w') as f:
            json.dump(self.training_report, f, indent=2)
        
        print(f"\nTraining report saved to {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report()
    
    def _generate_markdown_report(self):
        """Generate human-readable training report"""
        report_path = Path(self.output_dir) / f'training_report_{self.model_version}.md'
        
        metrics = self.training_report['metrics']
        
        report = f"""# Conviction Model Training Report
**Model Version:** {self.model_version}  
**Training Date:** {self.training_report['training_date']}  
**Dataset Size:** {self.training_report['dataset_size']} samples  
**Features:** {self.training_report['n_features']}

---

## 📊 Performance Metrics

### Test Set Performance
- **Accuracy:** {metrics['accuracy']:.3f}
- **Precision:** {metrics['precision']:.3f} (% of predicted winners that actually win)
- **Recall:** {metrics['recall']:.3f} (% of actual winners we caught)
- **AUC-ROC:** {metrics['auc_roc']:.3f}

### Cross-Validation
- **CV AUC Mean:** {metrics['cv_auc_mean']:.4f}
- **CV AUC Std:** {metrics['cv_auc_std']:.4f}

### Confusion Matrix
```
                Predicted No 2x    Predicted 2x+
Actual No 2x         {metrics['confusion_matrix'][0][0]}                {metrics['confusion_matrix'][0][1]}
Actual 2x+           {metrics['confusion_matrix'][1][0]}                {metrics['confusion_matrix'][1][1]}
```

**Interpretation:**
- True Negatives (TN): {metrics['confusion_matrix'][0][0]} - Correctly predicted non-winners
- False Positives (FP): {metrics['confusion_matrix'][0][1]} - False alarms (predicted win, didn't)
- False Negatives (FN): {metrics['confusion_matrix'][1][0]} - Missed winners
- True Positives (TP): {metrics['confusion_matrix'][1][1]} - Correctly predicted winners

---

## 🎯 Model Evaluation

### ✅ Success Criteria
- Minimum Precision: 60% {'✓' if metrics['precision'] >= 0.60 else '✗'}
- Minimum Recall: 50% {'✓' if metrics['recall'] >= 0.50 else '✗'}
- Minimum AUC-ROC: 0.70 {'✓' if metrics['auc_roc'] >= 0.70 else '✗'}

### 📈 Production Readiness
{'🟢 **READY FOR PRODUCTION**' if metrics['precision'] >= 0.60 and metrics['auc_roc'] >= 0.70 else '🟡 **NEEDS IMPROVEMENT**'}

---

## 🔥 Top Features (by Importance)

"""
        # Add feature importance table
        for i, feat in enumerate(self.training_report['feature_importance'][:15], 1):
            bar = "█" * int(feat['importance'] * 30)
            report += f"{i}. **{feat['feature']}** {bar} {feat['importance']:.4f}\n"
        
        report += f"""
---

## 📝 Next Steps

### If Performance is Good (Precision >60%, AUC >0.70):
1. Deploy model to production (integrate with scrapers)
2. Run A/B test (rule-based vs ML scoring)
3. Collect live data for 7 days
4. Retrain with real outcomes

### If Performance Needs Improvement:
1. Collect more training data (need 500+ samples)
2. Feature engineering: Add new features (e.g., macro trends, sector rotation)
3. Hyperparameter tuning: Grid search on XGBoost params
4. Try ensemble: Combine multiple models

---

## 🔄 Retraining Schedule

**Recommended:** Retrain weekly as new data comes in

```bash
# Weekly retraining (Sundays)
python3 train_model.py --data ml_training_data.csv --version v1_$(date +%Y%m%d)
```

Monitor for:
- Accuracy drop >5% → Immediate retrain
- Feature drift >20% → Collect more data
- Precision <55% for 2 weeks → Model failure, investigate

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"Markdown report saved to {report_path}")
    
    def run_full_pipeline(self):
        """
        Run complete training pipeline
        
        Steps:
        1. Load data
        2. Prepare features
        3. Train model
        4. Save model and report
        """
        # Load data
        df = self.load_data()
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Train model
        metrics = self.train(X, y)
        
        # Save everything
        self.save_model()
        
        # Final summary
        print(f"\n{'='*60}")
        print("TRAINING COMPLETE")
        print(f"{'='*60}")
        print(f"Model: {self.model_version}")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"AUC-ROC: {metrics['auc_roc']:.3f}")
        print(f"\nModel saved to {self.output_dir}/")
        print(f"Ready for deployment: {'YES ✓' if metrics['precision'] >= 0.60 else 'NO - needs more data'}")


def main():
    """Main training script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Conviction Model')
    parser.add_argument('--data', type=str, required=True,
                       help='Path to training data CSV')
    parser.add_argument('--output', type=str, default='models',
                       help='Output directory for model files')
    parser.add_argument('--version', type=str, default=None,
                       help='Model version (auto-generated if not specified)')
    parser.add_argument('--test-size', type=float, default=0.2,
                       help='Test set fraction (default: 0.2)')
    
    args = parser.parse_args()
    
    # Run training pipeline
    pipeline = TrainingPipeline(
        data_path=args.data,
        output_dir=args.output,
        model_version=args.version
    )
    
    pipeline.run_full_pipeline()


if __name__ == "__main__":
    # For demo, create synthetic data and train
    print("Creating synthetic training data for demo...")
    
    from conviction_model import create_sample_training_data
    
    X, y = create_sample_training_data(n_samples=200)
    
    # Combine into DataFrame
    df = X.copy()
    df['hit_target'] = y
    
    # Save to CSV
    data_path = '/Users/agentjoselo/.openclaw/workspace/trading/ml/data/ml_training_data.csv'
    Path(data_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_path, index=False)
    
    print(f"Saved synthetic data to {data_path}")
    
    # Run training pipeline
    pipeline = TrainingPipeline(
        data_path=data_path,
        output_dir='/Users/agentjoselo/.openclaw/workspace/trading/ml/models',
        model_version='v0.1_bootstrap'
    )
    
    pipeline.run_full_pipeline()
