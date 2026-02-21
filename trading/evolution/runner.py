#!/usr/bin/env python3
"""
Evolution Runner - Runs strategy evolution continuously
"""
import time
import signal
import sys
from datetime import datetime
from evolution_engine import EvolutionEngine

class ContinuousEvolution:
    """Manages continuous strategy evolution"""
    
    def __init__(self):
        self.engine = EvolutionEngine(
            population_size=50,
            elite_size=10,
            mutation_rate=0.30,  # 30% new traits
            new_blood_rate=0.20  # 20% completely new strategies
        )
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
    
    def shutdown(self, signum, frame):
        """Handle shutdown gracefully"""
        print(f"\n\n🛑 Shutdown signal received. Saving state...")
        self.running = False
        self.engine.save_generation()
        print("✅ State saved. Exiting.")
        sys.exit(0)
    
    def run(self, generations_per_cycle: int = 5, sleep_between_cycles: int = 300):
        """
        Run evolution continuously
        
        Args:
            generations_per_cycle: How many generations to run before pausing
            sleep_between_cycles: Seconds to wait between cycles (default 5min)
        """
        print(f"🐓 roostr Strategy Evolution Engine")
        print(f"{'='*60}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Population: {self.engine.population_size}")
        print(f"Elite: {self.engine.elite_size}")
        print(f"Mutation Rate: {self.engine.mutation_rate*100}%")
        print(f"New Blood: {self.engine.new_blood_rate*100}%")
        print(f"{'='*60}\n")
        
        # Initialize population
        self.engine.initialize_population()
        
        cycle = 0
        while self.running:
            cycle += 1
            print(f"\n🔄 Cycle {cycle} starting...")
            
            try:
                # Run N generations
                self.engine.run_evolution(num_generations=generations_per_cycle)
                
                # Check for high-conviction strategies
                self.check_for_signals()
                
                # Sleep before next cycle
                if self.running:
                    print(f"\n😴 Sleeping for {sleep_between_cycles}s before next cycle...")
                    time.sleep(sleep_between_cycles)
                
            except Exception as e:
                print(f"❌ Error in cycle {cycle}: {e}")
                print(f"Saving state and continuing...")
                self.engine.save_generation()
                time.sleep(60)  # Wait a bit before retrying
    
    def check_for_signals(self):
        """Check if any strategies are high-conviction (8.0+)"""
        top_strategies = self.engine.get_top_strategies(n=5)
        
        high_conviction = []
        for strategy in top_strategies:
            # Convert fitness to conviction score (0-10 scale)
            # Fitness is roughly -1 to 2, map to 0-10
            conviction = min(10, max(0, (strategy.fitness + 1) * 3.33))
            
            if conviction >= 8.0:
                high_conviction.append((strategy, conviction))
        
        if high_conviction:
            print(f"\n🚨 HIGH-CONVICTION STRATEGIES FOUND!")
            print(f"{'='*60}")
            
            for strategy, conviction in high_conviction:
                print(f"\n🎯 Conviction: {conviction:.1f}/10")
                print(strategy.get_description())
                print(f"\nBacktest Results:")
                for key, value in strategy.backtest_results.items():
                    if key != 'trades':
                        print(f"  {key}: {value}")
                print(f"{'='*60}")
            
            # Save high-conviction strategies separately
            self.save_high_conviction(high_conviction)
    
    def save_high_conviction(self, strategies: list):
        """Save high-conviction strategies for review"""
        import json
        
        output = {
            "timestamp": datetime.now().isoformat(),
            "generation": self.engine.generation,
            "strategies": [
                {
                    "conviction": conv,
                    "strategy": strat.to_dict()
                }
                for strat, conv in strategies
            ]
        }
        
        filename = f"/Users/agentjoselo/.openclaw/workspace/trading/evolution/high_conviction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Saved to: {filename}")

if __name__ == "__main__":
    runner = ContinuousEvolution()
    
    # Run with 5 generations per cycle, 5 min between cycles
    runner.run(generations_per_cycle=5, sleep_between_cycles=300)
