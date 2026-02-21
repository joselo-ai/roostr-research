"""
Evolution Engine - Genetic algorithm for strategy optimization
"""
import random
import json
from typing import List, Dict
from datetime import datetime
from strategy_dna import StrategyDNA
from backtester import Backtester, get_sp500_tickers

class EvolutionEngine:
    """Evolves trading strategies using genetic algorithms"""
    
    def __init__(self, 
                 population_size: int = 50,
                 elite_size: int = 10,
                 mutation_rate: float = 0.3,
                 new_blood_rate: float = 0.2):
        """
        Args:
            population_size: Total strategies per generation
            elite_size: Top N to keep + breed from
            mutation_rate: Probability of mutation (30% new traits)
            new_blood_rate: Fraction of population that's completely new each gen
        """
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.new_blood_rate = new_blood_rate
        
        self.population: List[StrategyDNA] = []
        self.generation = 0
        self.best_ever: StrategyDNA = None
        
        # Backtester setup
        self.universe = get_sp500_tickers(limit=30)  # Start with 30 stocks for speed
        self.backtester = Backtester(self.universe, lookback_days=365)
        
        # History tracking
        self.history = []
    
    def initialize_population(self):
        """Create initial random population"""
        print(f"🧬 Initializing population of {self.population_size} strategies...")
        self.population = [StrategyDNA() for _ in range(self.population_size)]
        print(f"✅ Population initialized")
    
    def evaluate_population(self):
        """Backtest all strategies in current population"""
        print(f"\n📊 Evaluating Generation {self.generation}...")
        
        for i, strategy in enumerate(self.population):
            print(f"   Testing strategy {i+1}/{len(self.population)}...", end='\r')
            results = self.backtester.backtest_strategy(strategy)
            strategy.backtest_results = results
        
        print(f"\n✅ Generation {self.generation} evaluated")
    
    def select_elite(self) -> List[StrategyDNA]:
        """Select top performers"""
        sorted_pop = sorted(self.population, key=lambda s: s.fitness, reverse=True)
        elite = sorted_pop[:self.elite_size]
        
        # Track best ever
        if not self.best_ever or elite[0].fitness > self.best_ever.fitness:
            self.best_ever = elite[0]
        
        return elite
    
    def breed_next_generation(self, elite: List[StrategyDNA]) -> List[StrategyDNA]:
        """Create next generation from elite"""
        next_gen = []
        
        # Keep elite (elitism)
        next_gen.extend(elite)
        
        # Breed offspring
        num_offspring = self.population_size - len(elite)
        num_new_blood = int(num_offspring * self.new_blood_rate)
        num_bred = num_offspring - num_new_blood
        
        # Crossover + mutation
        for _ in range(num_bred):
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child = StrategyDNA.crossover(parent1, parent2)
            child.mutate(self.mutation_rate)
            next_gen.append(child)
        
        # Fresh blood (completely new strategies)
        for _ in range(num_new_blood):
            next_gen.append(StrategyDNA())
        
        return next_gen
    
    def evolve_generation(self):
        """Run one full generation cycle"""
        # Evaluate current population
        self.evaluate_population()
        
        # Select elite
        elite = self.select_elite()
        
        # Log generation stats
        self.log_generation_stats(elite)
        
        # Breed next generation
        self.population = self.breed_next_generation(elite)
        
        # Increment generation counter
        self.generation += 1
    
    def log_generation_stats(self, elite: List[StrategyDNA]):
        """Log and save generation statistics"""
        top_5 = elite[:5]
        
        avg_fitness = sum(s.fitness for s in self.population) / len(self.population)
        best_fitness = elite[0].fitness
        
        stats = {
            "generation": self.generation,
            "timestamp": datetime.now().isoformat(),
            "avg_fitness": avg_fitness,
            "best_fitness": best_fitness,
            "best_roi": elite[0].backtest_results.get("roi", 0),
            "best_trades": elite[0].backtest_results.get("total_trades", 0),
            "top_5": [s.to_dict() for s in top_5]
        }
        
        self.history.append(stats)
        
        # Print summary
        print(f"\n🏆 Generation {self.generation} Results:")
        print(f"   Best Fitness: {best_fitness:.2f}")
        print(f"   Best ROI: {elite[0].backtest_results.get('roi', 0)*100:.1f}%")
        print(f"   Best Win Rate: {elite[0].backtest_results.get('win_rate', 0)*100:.1f}%")
        print(f"   Avg Population Fitness: {avg_fitness:.2f}")
        print(f"   Total Trades: {elite[0].backtest_results.get('total_trades', 0)}")
        
        # Save to file
        self.save_generation()
    
    def save_generation(self):
        """Save current generation data"""
        data = {
            "generation": self.generation,
            "timestamp": datetime.now().isoformat(),
            "population_size": len(self.population),
            "elite_size": self.elite_size,
            "best_ever": self.best_ever.to_dict() if self.best_ever else None,
            "history": self.history
        }
        
        with open(f"/Users/agentjoselo/.openclaw/workspace/trading/evolution/generation_{self.generation}.json", "w") as f:
            json.dump(data, f, indent=2)
        
        # Also update latest.json
        with open(f"/Users/agentjoselo/.openclaw/workspace/trading/evolution/latest.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def get_top_strategies(self, n: int = 10) -> List[StrategyDNA]:
        """Get top N strategies from current generation"""
        return sorted(self.population, key=lambda s: s.fitness, reverse=True)[:n]
    
    def run_evolution(self, num_generations: int = 10):
        """Run multiple generations"""
        print(f"\n🚀 Starting evolution for {num_generations} generations...")
        
        if not self.population:
            self.initialize_population()
        
        for i in range(num_generations):
            print(f"\n{'='*60}")
            print(f"Generation {self.generation + 1}/{self.generation + num_generations}")
            print(f"{'='*60}")
            
            self.evolve_generation()
        
        print(f"\n✅ Evolution complete!")
        print(f"\n🏆 Best Strategy Ever:")
        print(self.best_ever.get_description())

if __name__ == "__main__":
    # Test run
    engine = EvolutionEngine(
        population_size=20,  # Small for testing
        elite_size=5,
        mutation_rate=0.3,
        new_blood_rate=0.2
    )
    
    engine.run_evolution(num_generations=3)
