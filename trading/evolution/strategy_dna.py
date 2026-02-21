"""
Strategy DNA - Genetic representation of trading strategies
Each strategy has genes that define entry/exit logic
"""
import random
import json
from typing import Dict, Any, List

class StrategyDNA:
    """Represents a trading strategy as genetic code"""
    
    def __init__(self, genes: Dict[str, Any] = None):
        if genes:
            self.genes = genes
        else:
            self.genes = self._random_genes()
        
        self.fitness = 0.0
        self.backtest_results = {}
    
    def _random_genes(self) -> Dict[str, Any]:
        """Generate random strategy genes"""
        return {
            "entry": {
                "rsi_period": random.randint(7, 21),
                "rsi_oversold": random.randint(20, 40),
                "volume_spike": round(random.uniform(1.5, 3.0), 1),
                "price_above_sma": random.choice([20, 50, 100, 200]),
                "min_price": random.choice([5, 10, 20]),
            },
            "exit": {
                "profit_target": round(random.uniform(0.08, 0.25), 2),
                "stop_loss": round(random.uniform(0.05, 0.15), 2),
                "max_hold_days": random.randint(3, 30),
                "trailing_stop": random.choice([True, False]),
            },
            "position_sizing": {
                "base_size": round(random.uniform(0.02, 0.10), 2),  # 2-10% per position
                "scale_by_conviction": random.choice([True, False]),
            },
            "filters": {
                "min_market_cap": random.choice([100, 500, 1000, 2000]),  # millions
                "require_uptrend": random.choice([True, False]),
                "avoid_earnings": random.choice([True, False]),
            }
        }
    
    def mutate(self, mutation_rate: float = 0.3):
        """Mutate genes with given probability"""
        if random.random() < mutation_rate:
            # Mutate entry rules
            if random.random() < 0.5:
                self.genes["entry"]["rsi_oversold"] += random.randint(-5, 5)
                self.genes["entry"]["rsi_oversold"] = max(20, min(45, self.genes["entry"]["rsi_oversold"]))
            
            if random.random() < 0.5:
                self.genes["entry"]["volume_spike"] += random.uniform(-0.5, 0.5)
                self.genes["entry"]["volume_spike"] = max(1.2, min(5.0, self.genes["entry"]["volume_spike"]))
        
        if random.random() < mutation_rate:
            # Mutate exit rules
            if random.random() < 0.5:
                self.genes["exit"]["profit_target"] += random.uniform(-0.05, 0.05)
                self.genes["exit"]["profit_target"] = max(0.05, min(0.50, self.genes["exit"]["profit_target"]))
            
            if random.random() < 0.5:
                self.genes["exit"]["stop_loss"] += random.uniform(-0.03, 0.03)
                self.genes["exit"]["stop_loss"] = max(0.03, min(0.20, self.genes["exit"]["stop_loss"]))
        
        if random.random() < mutation_rate:
            # Mutate position sizing
            self.genes["position_sizing"]["base_size"] += random.uniform(-0.02, 0.02)
            self.genes["position_sizing"]["base_size"] = max(0.01, min(0.15, self.genes["position_sizing"]["base_size"]))
    
    @staticmethod
    def crossover(parent1: 'StrategyDNA', parent2: 'StrategyDNA') -> 'StrategyDNA':
        """Breed two strategies to create offspring"""
        child_genes = {}
        
        # Mix entry rules
        child_genes["entry"] = {}
        for key in parent1.genes["entry"]:
            child_genes["entry"][key] = random.choice([
                parent1.genes["entry"][key],
                parent2.genes["entry"][key]
            ])
        
        # Mix exit rules
        child_genes["exit"] = {}
        for key in parent1.genes["exit"]:
            child_genes["exit"][key] = random.choice([
                parent1.genes["exit"][key],
                parent2.genes["exit"][key]
            ])
        
        # Mix position sizing
        child_genes["position_sizing"] = {}
        for key in parent1.genes["position_sizing"]:
            child_genes["position_sizing"][key] = random.choice([
                parent1.genes["position_sizing"][key],
                parent2.genes["position_sizing"][key]
            ])
        
        # Mix filters
        child_genes["filters"] = {}
        for key in parent1.genes["filters"]:
            child_genes["filters"][key] = random.choice([
                parent1.genes["filters"][key],
                parent2.genes["filters"][key]
            ])
        
        return StrategyDNA(child_genes)
    
    def calculate_fitness(self, roi: float, win_rate: float, max_drawdown: float, sharpe: float):
        """Calculate fitness score from backtest results"""
        # Penalize drawdown heavily, reward ROI and consistency
        self.fitness = (
            roi * 0.4 +
            win_rate * 0.2 +
            sharpe * 0.3 -
            max_drawdown * 0.1
        )
        
        self.backtest_results = {
            "roi": roi,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "sharpe": sharpe,
            "fitness": self.fitness
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export strategy as dict"""
        return {
            "genes": self.genes,
            "fitness": self.fitness,
            "results": self.backtest_results
        }
    
    def to_json(self) -> str:
        """Export strategy as JSON"""
        return json.dumps(self.to_dict(), indent=2)
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StrategyDNA':
        """Load strategy from dict"""
        strategy = StrategyDNA(data.get("genes"))
        strategy.fitness = data.get("fitness", 0.0)
        strategy.backtest_results = data.get("results", {})
        return strategy
    
    def get_description(self) -> str:
        """Human-readable strategy description"""
        entry = self.genes["entry"]
        exit = self.genes["exit"]
        
        desc = f"""Strategy DNA:
        
Entry Rules:
- RSI({entry['rsi_period']}) < {entry['rsi_oversold']} (oversold)
- Volume spike > {entry['volume_spike']}x average
- Price above {entry['price_above_sma']}-day SMA
- Minimum price: ${entry['min_price']}

Exit Rules:
- Profit target: {exit['profit_target']*100}%
- Stop loss: -{exit['stop_loss']*100}%
- Max hold: {exit['max_hold_days']} days
- Trailing stop: {exit['trailing_stop']}

Position Size: {self.genes['position_sizing']['base_size']*100}% of portfolio

Fitness: {self.fitness:.2f}
"""
        if self.backtest_results:
            desc += f"\nBacktest Results:\n"
            desc += f"- ROI: {self.backtest_results.get('roi', 0)*100:.1f}%\n"
            desc += f"- Win Rate: {self.backtest_results.get('win_rate', 0)*100:.1f}%\n"
            desc += f"- Max Drawdown: {self.backtest_results.get('max_drawdown', 0)*100:.1f}%\n"
            desc += f"- Sharpe: {self.backtest_results.get('sharpe', 0):.2f}\n"
        
        return desc
