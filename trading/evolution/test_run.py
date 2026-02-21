#!/usr/bin/env python3
"""
Quick test to verify evolution engine works
"""
from evolution_engine import EvolutionEngine

print("🧪 Running quick test of evolution engine...")
print("This will test 2 generations with 10 strategies")
print("Should take ~2-3 minutes\n")

engine = EvolutionEngine(
    population_size=10,  # Very small for quick test
    elite_size=3,
    mutation_rate=0.3,
    new_blood_rate=0.2
)

try:
    engine.run_evolution(num_generations=2)
    print("\n✅ TEST PASSED - Evolution engine is operational!")
    print("\nYou can now run:")
    print("  python3 runner.py    # For continuous evolution")
    print("  python3 status.py    # To check progress")
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
