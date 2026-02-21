#!/usr/bin/env python3
"""
Evolution Status - Check current evolution progress
"""
import json
import os
from datetime import datetime

def load_latest():
    """Load latest evolution state"""
    latest_file = "/Users/agentjoselo/.openclaw/workspace/trading/evolution/latest.json"
    
    if not os.path.exists(latest_file):
        print("❌ No evolution data found. Run runner.py first.")
        return None
    
    with open(latest_file, "r") as f:
        return json.load(f)

def print_status():
    """Print current evolution status"""
    data = load_latest()
    if not data:
        return
    
    print(f"\n🐓 roostr Evolution Engine - Status")
    print(f"{'='*60}")
    print(f"Last Update: {data.get('timestamp', 'Unknown')}")
    print(f"Generation: {data.get('generation', 0)}")
    print(f"Population Size: {data.get('population_size', 0)}")
    print(f"Elite Size: {data.get('elite_size', 0)}")
    
    if data.get('best_ever'):
        best = data['best_ever']
        results = best.get('results', {})
        
        print(f"\n🏆 Best Strategy Ever:")
        print(f"{'='*60}")
        print(f"Fitness: {best.get('fitness', 0):.2f}")
        print(f"ROI: {results.get('roi', 0)*100:.1f}%")
        print(f"Win Rate: {results.get('win_rate', 0)*100:.1f}%")
        print(f"Max Drawdown: {results.get('max_drawdown', 0)*100:.1f}%")
        print(f"Sharpe: {results.get('sharpe', 0):.2f}")
        print(f"Total Trades: {results.get('total_trades', 0)}")
    
    # Show history trend
    if data.get('history') and len(data['history']) > 0:
        print(f"\n📊 Evolution Progress (Last 10 Generations):")
        print(f"{'='*60}")
        
        history = data['history'][-10:]  # Last 10 generations
        
        print(f"{'Gen':<6} {'Avg Fitness':<15} {'Best Fitness':<15} {'Best ROI':<15}")
        print(f"{'-'*60}")
        
        for gen_data in history:
            gen = gen_data.get('generation', 0)
            avg_fit = gen_data.get('avg_fitness', 0)
            best_fit = gen_data.get('best_fitness', 0)
            best_roi = gen_data.get('best_roi', 0)
            
            print(f"{gen:<6} {avg_fit:<15.2f} {best_fit:<15.2f} {best_roi*100:<15.1f}%")
    
    # Check for high-conviction signals
    check_high_conviction()
    
    print(f"\n{'='*60}\n")

def check_high_conviction():
    """Check for any high-conviction strategy files"""
    evolution_dir = "/Users/agentjoselo/.openclaw/workspace/trading/evolution"
    
    high_conv_files = [f for f in os.listdir(evolution_dir) if f.startswith('high_conviction_')]
    
    if high_conv_files:
        print(f"\n🚨 High-Conviction Strategies Found:")
        print(f"{'='*60}")
        
        # Show most recent
        latest = sorted(high_conv_files)[-1]
        filepath = os.path.join(evolution_dir, latest)
        
        with open(filepath, "r") as f:
            data = json.load(f)
        
        print(f"File: {latest}")
        print(f"Timestamp: {data.get('timestamp', 'Unknown')}")
        print(f"Generation: {data.get('generation', 0)}")
        print(f"Number of Strategies: {len(data.get('strategies', []))}")
        
        for i, strat_data in enumerate(data.get('strategies', [])[:3]):  # Show top 3
            print(f"\n  Strategy {i+1}:")
            print(f"  Conviction: {strat_data.get('conviction', 0):.1f}/10")
            
            results = strat_data.get('strategy', {}).get('results', {})
            print(f"  ROI: {results.get('roi', 0)*100:.1f}%")
            print(f"  Win Rate: {results.get('win_rate', 0)*100:.1f}%")
            print(f"  Trades: {results.get('total_trades', 0)}")

if __name__ == "__main__":
    print_status()
