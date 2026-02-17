#!/usr/bin/env python3
"""
Phase 1 Test Script - Quant Agents V2
======================================

Validates that all 4 Quant agents:
1. Return data-driven scores (not ABSTAIN 5.0)
2. Connect to actual data sources
3. Provide proper output format (conviction 0-10, BUY/SELL/HOLD, rationale)

Author: Joselo 🐓
Date: Feb 17, 2026
"""

import sys
import json
from quant_agents_v2 import (
    run_full_quant_analysis,
    print_analysis_report,
    QUANT_AGENTS_V2
)


def test_phase1_requirements(ticker: str = "SPHR") -> bool:
    """
    Test Phase 1 success criteria:
    - All 4 agents return data-driven scores
    - No ABSTAIN with default 5.0 conviction
    - Proper output format
    """
    print("="*80)
    print("PHASE 1 TEST - 4 QUANT AGENTS")
    print("="*80)
    print(f"\nTesting on: {ticker}\n")
    
    # Run analysis
    results = run_full_quant_analysis(ticker)
    
    # Validate results
    all_passed = True
    test_results = {
        'ticker': ticker,
        'tests': {},
        'summary': {}
    }
    
    print("\n📋 VALIDATION CHECKS:")
    print("-"*80)
    
    # Test 1: All agents returned opinions
    agents_count = len(results['agents'])
    test_results['tests']['agent_count'] = {
        'expected': 4,
        'actual': agents_count,
        'passed': agents_count == 4
    }
    print(f"✓ Agent count: {agents_count}/4 {'✅' if agents_count == 4 else '❌'}")
    
    # Test 2: No ABSTAIN votes
    abstain_count = results['summary']['vote_distribution'].get('ABSTAIN', 0)
    test_results['tests']['no_abstain'] = {
        'expected': 0,
        'actual': abstain_count,
        'passed': abstain_count == 0
    }
    print(f"✓ ABSTAIN votes: {abstain_count} {'✅' if abstain_count == 0 else '❌'}")
    
    # Test 3: All agents have valid conviction scores (not default 5.0)
    non_default_scores = []
    for agent_id, opinion in results['agents'].items():
        conviction = opinion['conviction']
        is_not_default = conviction != 5.0
        non_default_scores.append(is_not_default)
        
        status = '✅' if is_not_default else '❌'
        print(f"  - {opinion['agent_name']}: {conviction}/10 {status}")
    
    all_non_default = all(non_default_scores)
    test_results['tests']['data_driven_scores'] = {
        'expected': 'All agents with non-default scores',
        'actual': f"{sum(non_default_scores)}/4 agents",
        'passed': all_non_default
    }
    print(f"✓ Data-driven scores: {sum(non_default_scores)}/4 {'✅' if all_non_default else '❌'}")
    
    # Test 4: Data quality check
    data_quality = results['summary']['data_quality']
    quality_acceptable = data_quality in ['HIGH', 'MEDIUM']
    test_results['tests']['data_quality'] = {
        'expected': 'HIGH or MEDIUM',
        'actual': data_quality,
        'passed': quality_acceptable
    }
    print(f"✓ Data quality: {data_quality} {'✅' if quality_acceptable else '❌'}")
    
    # Test 5: Output format validation
    format_valid = True
    for agent_id, opinion in results['agents'].items():
        required_fields = ['agent_name', 'ticker', 'conviction', 'action', 
                          'rationale', 'key_metrics', 'data_quality', 'timestamp']
        
        for field in required_fields:
            if field not in opinion:
                format_valid = False
                print(f"  ❌ Missing field '{field}' in {agent_id}")
    
    test_results['tests']['output_format'] = {
        'expected': 'All required fields present',
        'passed': format_valid
    }
    print(f"✓ Output format: {'✅' if format_valid else '❌'}")
    
    # Test 6: Valid actions (BUY/SELL/HOLD/ABSTAIN)
    valid_actions = all(
        opinion['action'] in ['BUY', 'SELL', 'HOLD', 'ABSTAIN']
        for opinion in results['agents'].values()
    )
    test_results['tests']['valid_actions'] = {
        'expected': 'All actions in [BUY, SELL, HOLD, ABSTAIN]',
        'passed': valid_actions
    }
    print(f"✓ Valid actions: {'✅' if valid_actions else '❌'}")
    
    # Overall pass/fail
    all_tests = [
        test_results['tests']['agent_count']['passed'],
        test_results['tests']['no_abstain']['passed'],
        test_results['tests']['data_driven_scores']['passed'],
        test_results['tests']['data_quality']['passed'],
        test_results['tests']['output_format']['passed'],
        test_results['tests']['valid_actions']['passed']
    ]
    
    phase1_passed = all(all_tests)
    test_results['summary'] = {
        'phase1_passed': phase1_passed,
        'tests_passed': sum(all_tests),
        'tests_total': len(all_tests),
        'consensus': results['summary']['consensus'],
        'avg_conviction': results['summary']['avg_conviction']
    }
    
    print("\n" + "="*80)
    if phase1_passed:
        print("🎉 PHASE 1 COMPLETE - ALL TESTS PASSED")
    else:
        print("❌ PHASE 1 INCOMPLETE - SOME TESTS FAILED")
    print("="*80)
    
    # Save test results
    output_file = f'/Users/agentjoselo/.openclaw/workspace/trading/agents/signals/{ticker.lower()}_phase1_test.json'
    with open(output_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📄 Test results saved to {output_file}")
    
    # Print full analysis
    print_analysis_report(results)
    
    return phase1_passed


def test_multiple_tickers():
    """Test agents on multiple tickers to verify robustness"""
    print("\n" + "="*80)
    print("TESTING MULTIPLE TICKERS")
    print("="*80)
    
    test_tickers = ['SPHR', 'AAPL', 'TSLA']
    
    for ticker in test_tickers:
        try:
            print(f"\n🧪 Testing {ticker}...")
            results = run_full_quant_analysis(ticker)
            
            abstain_count = results['summary']['vote_distribution'].get('ABSTAIN', 0)
            consensus = results['summary']['consensus']
            avg_conviction = results['summary']['avg_conviction']
            
            print(f"  Consensus: {consensus}")
            print(f"  Avg Conviction: {avg_conviction}/10")
            print(f"  ABSTAIN votes: {abstain_count}")
            print(f"  Status: {'✅ PASS' if abstain_count == 0 else '❌ FAIL'}")
            
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")


if __name__ == "__main__":
    # Run Phase 1 test on SPHR
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPHR"
    
    phase1_passed = test_phase1_requirements(ticker)
    
    # Optional: Test multiple tickers
    if '--multi' in sys.argv:
        test_multiple_tickers()
    
    # Exit with appropriate code
    sys.exit(0 if phase1_passed else 1)
