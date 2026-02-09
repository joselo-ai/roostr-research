#!/usr/bin/env python3
"""
Test script for Quant Agent
Validates all components are working correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from backtest import Backtester, BacktestConfig, Trade
        print("  ✅ backtest.py")
    except ImportError as e:
        print(f"  ❌ backtest.py: {e}")
        return False
    
    try:
        from validation import SignalValidator, generate_validation_report
        print("  ✅ validation.py")
    except ImportError as e:
        print(f"  ❌ validation.py: {e}")
        return False
    
    try:
        from agents.quant_agent import QuantAgent
        print("  ✅ quant_agent.py")
    except ImportError as e:
        print(f"  ❌ quant_agent.py: {e}")
        return False
    
    return True

def test_dependencies():
    """Test that required packages are installed"""
    print("\n🔍 Testing dependencies...")
    
    deps = ['pandas', 'numpy', 'yfinance', 'scipy']
    all_ok = True
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def test_backtest_config():
    """Test BacktestConfig creation"""
    print("\n🔍 Testing BacktestConfig...")
    
    try:
        from backtest import BacktestConfig
        
        config = BacktestConfig(
            starting_capital=100000,
            position_size_pct=0.10,
            stop_loss_pct=0.20
        )
        
        assert config.starting_capital == 100000
        assert config.position_size_pct == 0.10
        
        print("  ✅ BacktestConfig initialization")
        return True
    except Exception as e:
        print(f"  ❌ BacktestConfig: {e}")
        return False

def test_quant_agent_init():
    """Test QuantAgent initialization"""
    print("\n🔍 Testing QuantAgent initialization...")
    
    try:
        from agents.quant_agent import QuantAgent
        
        agent = QuantAgent()
        
        assert agent.config is not None
        assert agent.backtester is not None
        assert agent.validator is not None
        
        print("  ✅ QuantAgent initialization")
        return True
    except Exception as e:
        print(f"  ❌ QuantAgent: {e}")
        return False

def test_signal_loading():
    """Test loading signals from database"""
    print("\n🔍 Testing signal loading...")
    
    try:
        from agents.quant_agent import QuantAgent
        import os
        
        agent = QuantAgent()
        
        # Check if signals database exists
        signals_path = Path(__file__).parent.parent / 'signals-database.csv'
        
        if signals_path.exists():
            signals = agent.load_signals('database')
            print(f"  ✅ Loaded {len(signals)} signals")
            return True
        else:
            print(f"  ⚠️  Signal database not found at {signals_path}")
            return True  # Not a failure, just missing data
    except Exception as e:
        print(f"  ❌ Signal loading: {e}")
        return False

def test_validation_functions():
    """Test statistical validation functions"""
    print("\n🔍 Testing validation functions...")
    
    try:
        from validation import SignalValidator
        import numpy as np
        
        validator = SignalValidator()
        
        # Test IC calculation
        predictions = np.array([1, 2, 3, 4, 5])
        actuals = np.array([1.1, 2.2, 2.9, 4.1, 5.2])
        
        ic_result = validator.calculate_information_coefficient(predictions, actuals)
        
        assert 'pearson_ic' in ic_result
        assert 'spearman_ic' in ic_result
        
        print("  ✅ Information Coefficient calculation")
        
        # Test significance test
        returns = np.array([1.5, -0.5, 2.0, -1.0, 3.0])
        sig_result = validator.test_signal_vs_random(returns)
        
        assert 't_statistic' in sig_result
        assert 'p_value' in sig_result
        
        print("  ✅ Significance testing")
        
        return True
    except Exception as e:
        print(f"  ❌ Validation functions: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("QUANT AGENT - SYSTEM TESTS")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_dependencies,
        test_backtest_config,
        test_quant_agent_init,
        test_signal_loading,
        test_validation_functions
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print(f"⚠️  {total - passed} tests failed")
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
