#!/usr/bin/env python3
"""
19-Agent System - Comprehensive Test Script
============================================

Tests complete 19-agent deliberation system:
- 4 Quant Agents (Valuation, Technicals, Fundamentals, Sentiment)
- 12 Legendary Investors (Phases 2-5)
- Synthesizer (aggregates all 16 votes)
- Risk Manager (Joselo - position sizing)
- John Hull (quantitative risk)

Author: Joselo 🐓
Date: Feb 17, 2026
"""

import sys
import json
from datetime import datetime
from typing import Dict, List
import numpy as np

# Import agent modules
from quant_agents_v2 import QUANT_AGENTS_V2, run_full_quant_analysis
from legendary_investors_v2 import LEGENDARY_INVESTORS_V2, run_legendary_analysis


def run_19_agent_deliberation(ticker: str) -> Dict:
    """
    Run complete 19-agent deliberation on a ticker.
    
    Returns:
        Dict with all agent opinions and synthesized recommendation
    """
    print("\n" + "="*80)
    print(f"🎯 19-AGENT DELIBERATION SYSTEM - {ticker}")
    print("="*80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*80 + "\n")
    
    results = {
        'ticker': ticker,
        'timestamp': datetime.now().isoformat(),
        'agents': {
            'quant': {},
            'legendary': {}
        },
        'synthesis': {},
        'risk': {},
        'recommendation': {}
    }
    
    # ========================================================================
    # PHASE 1: Run 4 Quant Agents
    # ========================================================================
    print("\n📊 PHASE 1: QUANTITATIVE ANALYSIS (4 agents)")
    print("-" * 80)
    
    quant_results = run_full_quant_analysis(ticker)
    results['agents']['quant'] = quant_results['agents']
    
    for agent_id, opinion in quant_results['agents'].items():
        print(f"✓ {opinion['agent_name']}: {opinion['action']} ({opinion['conviction']}/10)")
    
    # ========================================================================
    # PHASE 2-5: Run 12 Legendary Investors
    # ========================================================================
    print("\n🏛️  PHASES 2-5: LEGENDARY INVESTORS (12 agents)")
    print("-" * 80)
    
    legendary_results = run_legendary_analysis(ticker)
    results['agents']['legendary'] = legendary_results['agents']
    
    for agent_id, opinion in legendary_results['agents'].items():
        print(f"✓ {opinion['agent_name']}: {opinion['action']} ({opinion['conviction']}/10)")
    
    # ========================================================================
    # SYNTHESIZE: Aggregate all 16 votes
    # ========================================================================
    print("\n🔄 SYNTHESIS: Aggregating 16 Agent Votes")
    print("-" * 80)
    
    all_opinions = []
    all_opinions.extend(quant_results['agents'].values())
    all_opinions.extend(legendary_results['agents'].values())
    
    # Vote counts
    vote_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0, 'ABSTAIN': 0}
    for opinion in all_opinions:
        vote_counts[opinion['action']] += 1
    
    # Average conviction
    avg_conviction = np.mean([op['conviction'] for op in all_opinions])
    
    # Weighted average (could weight by specialty)
    # For now, equal weight
    
    # Consensus logic
    total_votes = len(all_opinions)
    buy_pct = vote_counts['BUY'] / total_votes
    sell_pct = vote_counts['SELL'] / total_votes
    
    if buy_pct > 0.5:
        consensus = 'BUY'
        consensus_strength = 'STRONG'
    elif buy_pct > 0.4:
        consensus = 'BUY'
        consensus_strength = 'MODERATE'
    elif sell_pct > 0.5:
        consensus = 'SELL'
        consensus_strength = 'STRONG'
    elif sell_pct > 0.4:
        consensus = 'SELL'
        consensus_strength = 'MODERATE'
    else:
        consensus = 'HOLD'
        consensus_strength = 'NEUTRAL'
    
    # Data quality
    quality_scores = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    avg_quality = np.mean([quality_scores.get(op['data_quality'], 1) for op in all_opinions])
    
    if avg_quality >= 2.5:
        data_quality = 'HIGH'
    elif avg_quality >= 1.5:
        data_quality = 'MEDIUM'
    else:
        data_quality = 'LOW'
    
    synthesis = {
        'consensus': consensus,
        'consensus_strength': consensus_strength,
        'avg_conviction': round(avg_conviction, 2),
        'vote_distribution': vote_counts,
        'data_quality': data_quality,
        'total_agents': total_votes,
        'buy_percentage': round(buy_pct * 100, 1),
        'sell_percentage': round(sell_pct * 100, 1)
    }
    
    results['synthesis'] = synthesis
    
    print(f"Consensus: {consensus} ({consensus_strength})")
    print(f"Avg Conviction: {avg_conviction:.2f}/10")
    print(f"Vote Distribution: {vote_counts}")
    print(f"BUY: {buy_pct*100:.1f}% | SELL: {sell_pct*100:.1f}%")
    print(f"Data Quality: {data_quality}")
    
    # ========================================================================
    # RISK MANAGEMENT: Position Sizing (Joselo + Hull)
    # ========================================================================
    print("\n⚖️  RISK MANAGEMENT")
    print("-" * 80)
    
    # Risk Manager (Joselo) - Position sizing based on conviction
    if consensus == 'BUY':
        if avg_conviction >= 8:
            position_size_pct = 15  # Large position
            stop_loss_pct = 15
        elif avg_conviction >= 7:
            position_size_pct = 10  # Medium position
            stop_loss_pct = 12
        elif avg_conviction >= 6:
            position_size_pct = 5   # Small position
            stop_loss_pct = 10
        else:
            position_size_pct = 2   # Tiny position
            stop_loss_pct = 8
    elif consensus == 'SELL':
        position_size_pct = 0
        stop_loss_pct = 0
    else:  # HOLD
        position_size_pct = 3  # Minimal position
        stop_loss_pct = 10
    
    risk_assessment = {
        'position_size_pct': position_size_pct,
        'stop_loss_pct': stop_loss_pct,
        'risk_level': 'LOW' if avg_conviction >= 7 else 'MEDIUM' if avg_conviction >= 5 else 'HIGH',
        'max_portfolio_exposure': min(position_size_pct * 2, 25)  # Cap at 25%
    }
    
    # John Hull - Quantitative risk metrics
    # (Simplified - would normally calculate VaR, stress tests)
    hull_metrics = {
        'conviction_variance': round(np.var([op['conviction'] for op in all_opinions]), 2),
        'agent_disagreement': round(abs(buy_pct - sell_pct), 2),
        'data_reliability': data_quality,
        'recommendation': 'PROCEED' if avg_conviction >= 6 and data_quality in ['HIGH', 'MEDIUM'] else 'CAUTION'
    }
    
    results['risk'] = {
        'risk_manager': risk_assessment,
        'john_hull': hull_metrics
    }
    
    print(f"Risk Manager (Joselo): {position_size_pct}% position, {stop_loss_pct}% stop-loss")
    print(f"John Hull: {hull_metrics['recommendation']} (variance: {hull_metrics['conviction_variance']})")
    
    # ========================================================================
    # FINAL RECOMMENDATION
    # ========================================================================
    print("\n🎯 FINAL RECOMMENDATION")
    print("=" * 80)
    
    final_recommendation = {
        'action': consensus,
        'conviction': avg_conviction,
        'position_size_pct': position_size_pct,
        'stop_loss_pct': stop_loss_pct,
        'reasoning': generate_recommendation_rationale(
            consensus, avg_conviction, vote_counts, buy_pct, sell_pct, data_quality
        ),
        'key_supporters': get_top_supporters(all_opinions, consensus, n=3),
        'key_critics': get_top_critics(all_opinions, consensus, n=3)
    }
    
    results['recommendation'] = final_recommendation
    
    print(f"ACTION: {final_recommendation['action']}")
    print(f"CONVICTION: {final_recommendation['conviction']:.2f}/10")
    print(f"POSITION SIZE: {final_recommendation['position_size_pct']}%")
    print(f"STOP LOSS: {final_recommendation['stop_loss_pct']}%")
    print(f"\nREASONING: {final_recommendation['reasoning']}")
    
    print(f"\nKEY SUPPORTERS:")
    for supporter in final_recommendation['key_supporters']:
        print(f"  • {supporter['name']} ({supporter['conviction']}/10): {supporter['rationale'][:100]}...")
    
    print(f"\nKEY CRITICS:")
    for critic in final_recommendation['key_critics']:
        print(f"  • {critic['name']} ({critic['conviction']}/10): {critic['rationale'][:100]}...")
    
    return results


def generate_recommendation_rationale(consensus: str, avg_conviction: float, 
                                     vote_counts: Dict, buy_pct: float, 
                                     sell_pct: float, data_quality: str) -> str:
    """Generate human-readable rationale for final recommendation"""
    
    rationale = f"After deliberation among 16 specialized agents, "
    
    if consensus == 'BUY':
        rationale += f"{buy_pct*100:.0f}% recommend BUY with average conviction {avg_conviction:.1f}/10. "
        if avg_conviction >= 7:
            rationale += "This is a high-conviction opportunity. "
        elif avg_conviction >= 6:
            rationale += "Moderate conviction - proceed with standard position sizing. "
        else:
            rationale += "Lower conviction - consider small position only. "
    elif consensus == 'SELL':
        rationale += f"{sell_pct*100:.0f}% recommend SELL with average conviction {avg_conviction:.1f}/10. "
        rationale += "Majority sees limited upside or significant risks. "
    else:
        rationale += f"mixed signals (BUY: {vote_counts['BUY']}, SELL: {vote_counts['SELL']}, HOLD: {vote_counts['HOLD']}). "
        rationale += "Recommend HOLD or pass until clearer picture emerges. "
    
    rationale += f"Data quality is {data_quality}."
    
    return rationale


def get_top_supporters(opinions: List[Dict], consensus: str, n: int = 3) -> List[Dict]:
    """Get top N agents supporting the consensus"""
    if consensus == 'BUY':
        supporters = [op for op in opinions if op['action'] == 'BUY']
    elif consensus == 'SELL':
        supporters = [op for op in opinions if op['action'] == 'SELL']
    else:
        supporters = [op for op in opinions if op['action'] in ['BUY', 'HOLD']]
    
    supporters.sort(key=lambda x: x['conviction'], reverse=True)
    
    return [
        {
            'name': op['agent_name'],
            'conviction': op['conviction'],
            'rationale': op['rationale']
        }
        for op in supporters[:n]
    ]


def get_top_critics(opinions: List[Dict], consensus: str, n: int = 3) -> List[Dict]:
    """Get top N agents opposing the consensus"""
    if consensus == 'BUY':
        critics = [op for op in opinions if op['action'] in ['SELL', 'HOLD']]
    elif consensus == 'SELL':
        critics = [op for op in opinions if op['action'] in ['BUY', 'HOLD']]
    else:
        critics = [op for op in opinions if op['action'] in ['BUY', 'SELL']]
    
    critics.sort(key=lambda x: x['conviction'], reverse=True)
    
    return [
        {
            'name': op['agent_name'],
            'conviction': op['conviction'],
            'rationale': op['rationale']
        }
        for op in critics[:n]
    ]


def save_deliberation_report(results: Dict, ticker: str):
    """Save comprehensive deliberation report"""
    
    # Save JSON
    json_file = f'/Users/agentjoselo/.openclaw/workspace/trading/agents/signals/{ticker.lower()}_19agent_deliberation.json'
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Full deliberation saved to {json_file}")
    
    # Save markdown summary
    md_file = f'/Users/agentjoselo/.openclaw/workspace/trading/agents/signals/{ticker.upper()}_DELIBERATION_REPORT.md'
    
    with open(md_file, 'w') as f:
        f.write(f"# 19-Agent Deliberation Report: {ticker.upper()}\n\n")
        f.write(f"**Timestamp:** {results['timestamp']}\n\n")
        f.write("---\n\n")
        
        f.write("## 🎯 Final Recommendation\n\n")
        rec = results['recommendation']
        f.write(f"- **Action:** {rec['action']}\n")
        f.write(f"- **Conviction:** {rec['conviction']:.2f}/10\n")
        f.write(f"- **Position Size:** {rec['position_size_pct']}%\n")
        f.write(f"- **Stop Loss:** {rec['stop_loss_pct']}%\n\n")
        f.write(f"**Reasoning:** {rec['reasoning']}\n\n")
        
        f.write("---\n\n")
        
        f.write("## 📊 Synthesis\n\n")
        syn = results['synthesis']
        f.write(f"- **Consensus:** {syn['consensus']} ({syn['consensus_strength']})\n")
        f.write(f"- **Average Conviction:** {syn['avg_conviction']}/10\n")
        f.write(f"- **Vote Distribution:** {syn['vote_distribution']}\n")
        f.write(f"- **BUY:** {syn['buy_percentage']}% | **SELL:** {syn['sell_percentage']}%\n")
        f.write(f"- **Data Quality:** {syn['data_quality']}\n\n")
        
        f.write("---\n\n")
        
        f.write("## 👥 Agent Opinions\n\n")
        
        f.write("### 📊 Quant Agents (4)\n\n")
        for agent_id, opinion in results['agents']['quant'].items():
            f.write(f"**{opinion['agent_name']}** - {opinion['action']} ({opinion['conviction']}/10)\n")
            f.write(f"> {opinion['rationale'][:200]}...\n\n")
        
        f.write("### 🏛️ Legendary Investors (12)\n\n")
        for agent_id, opinion in results['agents']['legendary'].items():
            f.write(f"**{opinion['agent_name']}** - {opinion['action']} ({opinion['conviction']}/10)\n")
            f.write(f"> {opinion['rationale'][:200]}...\n\n")
        
        f.write("---\n\n")
        f.write(f"*Generated by 19-Agent Deliberation System | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print(f"📄 Summary report saved to {md_file}")


def test_success_criteria(results: Dict) -> bool:
    """
    Test if the 19-agent system meets success criteria:
    - All agents return data-driven scores (not ABSTAIN)
    - Conviction score ≥7.0 or ≤4.0 (clear signal, not 5.0 neutral)
    - Data quality HIGH or MEDIUM
    """
    
    print("\n" + "="*80)
    print("✅ SUCCESS CRITERIA VALIDATION")
    print("="*80)
    
    all_passed = True
    
    # Test 1: No ABSTAIN votes
    abstain_count = results['synthesis']['vote_distribution'].get('ABSTAIN', 0)
    test1_passed = abstain_count == 0
    print(f"1. No ABSTAIN votes: {'✅ PASS' if test1_passed else '❌ FAIL'} ({abstain_count} abstain)")
    all_passed = all_passed and test1_passed
    
    # Test 2: Clear conviction signal (not neutral 5.0)
    avg_conviction = results['synthesis']['avg_conviction']
    test2_passed = avg_conviction >= 7.0 or avg_conviction <= 4.0
    print(f"2. Clear signal (≥7.0 or ≤4.0): {'✅ PASS' if test2_passed else '❌ FAIL'} ({avg_conviction:.2f})")
    all_passed = all_passed and test2_passed
    
    # Test 3: Data quality
    data_quality = results['synthesis']['data_quality']
    test3_passed = data_quality in ['HIGH', 'MEDIUM']
    print(f"3. Data quality HIGH/MEDIUM: {'✅ PASS' if test3_passed else '❌ FAIL'} ({data_quality})")
    all_passed = all_passed and test3_passed
    
    # Test 4: All 16 agents voted
    total_agents = results['synthesis']['total_agents']
    test4_passed = total_agents == 16
    print(f"4. All 16 agents voted: {'✅ PASS' if test4_passed else '❌ FAIL'} ({total_agents}/16)")
    all_passed = all_passed and test4_passed
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL SUCCESS CRITERIA MET - SYSTEM OPERATIONAL")
    else:
        print("⚠️  SOME CRITERIA NOT MET - REVIEW REQUIRED")
    print("="*80)
    
    return all_passed


if __name__ == "__main__":
    # Get ticker from command line
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPHR"
    
    # Run 19-agent deliberation
    results = run_19_agent_deliberation(ticker)
    
    # Save reports
    save_deliberation_report(results, ticker)
    
    # Test success criteria
    success = test_success_criteria(results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
