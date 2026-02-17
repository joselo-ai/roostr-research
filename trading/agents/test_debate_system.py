#!/usr/bin/env python3
"""
Test the 18-agent debate system components
"""

import json
import sys
from pathlib import Path

# Test imports
try:
    from debate_orchestrator import DebateOrchestrator, AGENT_ORDER, DNA_CARDS_DIR
    from discord_utils import DiscordClient, VoteParser
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_dna_cards():
    """Test that all DNA cards exist and are valid"""
    print("\n" + "="*60)
    print("TEST 1: DNA Cards")
    print("="*60)
    
    missing = []
    invalid = []
    valid = []
    
    for agent_id in AGENT_ORDER:
        dna_file = DNA_CARDS_DIR / f"{agent_id}.json"
        
        if not dna_file.exists():
            missing.append(agent_id)
            print(f"❌ Missing: {agent_id}")
            continue
        
        try:
            with open(dna_file, 'r') as f:
                data = json.load(f)
            
            # Validate required fields
            required = ['agent_id', 'display_name', 'emoji']
            for field in required:
                if field not in data:
                    raise ValueError(f"Missing field: {field}")
            
            valid.append(agent_id)
            print(f"✅ {data['display_name']} {data['emoji']}")
            
        except Exception as e:
            invalid.append(agent_id)
            print(f"❌ Invalid {agent_id}: {e}")
    
    print(f"\n📊 Results:")
    print(f"   Valid: {len(valid)}/18")
    print(f"   Missing: {len(missing)}/18")
    print(f"   Invalid: {len(invalid)}/18")
    
    return len(valid) == 18


def test_vote_parser():
    """Test vote parsing logic"""
    print("\n" + "="*60)
    print("TEST 2: Vote Parser")
    print("="*60)
    
    test_cases = [
        {
            "name": "Valid BUY vote",
            "post": """🎩 **Warren Buffett**

This is a quality business with a strong moat.

**Vote:** BUY
**Conviction:** 8/10
**Risk:** Medium""",
            "expected": {
                "vote": "BUY",
                "conviction": 8,
                "risk": "Medium"
            }
        },
        {
            "name": "Valid SELL vote",
            "post": """🔍 **Michael Burry**

Overvalued with asymmetric downside risk.

**Vote:** SELL
**Conviction:** 9/10
**Risk:** High""",
            "expected": {
                "vote": "SELL",
                "conviction": 9,
                "risk": "High"
            }
        },
        {
            "name": "Valid HOLD vote",
            "post": """📊 **Benjamin Graham**

Fair value, no margin of safety.

**Vote:** HOLD
**Conviction:** 5/10
**Risk:** Low""",
            "expected": {
                "vote": "HOLD",
                "conviction": 5,
                "risk": "Low"
            }
        }
    ]
    
    parser = VoteParser()
    passed = 0
    failed = 0
    
    for test in test_cases:
        parsed = parser.parse_agent_post(test['post'])
        
        if parsed:
            match = (
                parsed['vote'] == test['expected']['vote'] and
                parsed['conviction'] == test['expected']['conviction'] and
                parsed['risk'] == test['expected']['risk']
            )
            
            if match:
                print(f"✅ {test['name']}")
                passed += 1
            else:
                print(f"❌ {test['name']}: Parse mismatch")
                print(f"   Expected: {test['expected']}")
                print(f"   Got: {parsed}")
                failed += 1
        else:
            print(f"❌ {test['name']}: Failed to parse")
            failed += 1
    
    print(f"\n📊 Results: {passed}/{len(test_cases)} passed")
    
    return failed == 0


def test_orchestrator_init():
    """Test orchestrator initialization"""
    print("\n" + "="*60)
    print("TEST 3: Orchestrator Initialization")
    print("="*60)
    
    test_signal = {
        "ticker": "TEST",
        "price": 100.0,
        "catalyst": "Test Catalyst",
        "description": "Test description"
    }
    
    try:
        orchestrator = DebateOrchestrator(test_signal)
        print(f"✅ Orchestrator created")
        print(f"✅ Loaded {len(orchestrator.agents)} agents")
        
        # Test prompt building
        if orchestrator.agents:
            agent_id = list(orchestrator.agents.keys())[0]
            prompt = orchestrator.build_agent_prompt(agent_id, 1)
            
            if "TEST" in prompt and "100.0" in prompt:
                print(f"✅ Prompt building works")
                return True
            else:
                print(f"❌ Prompt missing signal data")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator init failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_discord_client():
    """Test Discord client (without actually sending)"""
    print("\n" + "="*60)
    print("TEST 4: Discord Client")
    print("="*60)
    
    try:
        client = DiscordClient("1472692185106481417")
        print("✅ Discord client created")
        
        # Don't actually send, just verify the client exists
        print("⚠️  Skipping actual Discord send (dry run)")
        
        return True
        
    except Exception as e:
        print(f"❌ Discord client error: {e}")
        return False


def test_vote_tallying():
    """Test vote tallying logic"""
    print("\n" + "="*60)
    print("TEST 5: Vote Tallying")
    print("="*60)
    
    mock_votes = [
        {"vote": "BUY", "conviction": 8},
        {"vote": "BUY", "conviction": 9},
        {"vote": "BUY", "conviction": 7},
        {"vote": "HOLD", "conviction": 5},
        {"vote": "HOLD", "conviction": 6},
        {"vote": "SELL", "conviction": 9},
    ]
    
    parser = VoteParser()
    tally = parser.tally_votes(mock_votes)
    
    print(f"   BUY: {tally['buy_votes']}")
    print(f"   HOLD: {tally['hold_votes']}")
    print(f"   SELL: {tally['sell_votes']}")
    print(f"   Avg Conviction: {tally['avg_conviction']}/10")
    print(f"   Consensus: {tally['consensus']}")
    
    expected_buy = 3
    expected_hold = 2
    expected_sell = 1
    
    if (tally['buy_votes'] == expected_buy and 
        tally['hold_votes'] == expected_hold and
        tally['sell_votes'] == expected_sell):
        print("✅ Vote tallying correct")
        return True
    else:
        print("❌ Vote tallying incorrect")
        return False


def main():
    """Run all tests"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🧪  18-AGENT DEBATE SYSTEM - TEST SUITE  🧪           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    tests = [
        ("DNA Cards", test_dna_cards),
        ("Vote Parser", test_vote_parser),
        ("Orchestrator", test_orchestrator_init),
        ("Discord Client", test_discord_client),
        ("Vote Tallying", test_vote_tallying)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System ready for debate.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
