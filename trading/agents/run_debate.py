#!/usr/bin/env python3
"""
Run 18-Agent Debate

Simple script to launch a multi-agent debate on a trading signal.
"""

import json
import sys
from pathlib import Path
from debate_orchestrator import DebateOrchestrator


def load_signal_from_file(filepath: str) -> dict:
    """Load signal from JSON or markdown file"""
    path = Path(filepath)
    
    if path.suffix == '.json':
        with open(path, 'r') as f:
            return json.load(f)
    
    elif path.suffix == '.md':
        # Parse markdown file for signal details
        # Simplified parser - looks for key fields
        with open(path, 'r') as f:
            content = f.read()
        
        # Extract ticker, price, catalyst from markdown
        signal = {
            'ticker': 'UNKNOWN',
            'price': 0,
            'catalyst': 'General Analysis',
            'description': content[:500]  # First 500 chars
        }
        
        # Try to find ticker
        for line in content.split('\n'):
            if 'ticker:' in line.lower():
                signal['ticker'] = line.split(':')[1].strip().replace('*', '').replace('$', '')
            elif 'price:' in line.lower():
                try:
                    price_str = line.split(':')[1].strip().replace('$', '').replace(',', '')
                    signal['price'] = float(price_str)
                except:
                    pass
            elif 'catalyst' in line.lower():
                signal['catalyst'] = line.split(':')[1].strip()
        
        return signal
    
    else:
        raise ValueError("Signal file must be .json or .md")


def create_asts_signal() -> dict:
    """Create the ASTS signal for testing"""
    return {
        "ticker": "ASTS",
        "price": 4.20,
        "catalyst": "FCC Approval Expected Q1 2026",
        "description": """**AST SpaceMobile** - Space-based cellular broadband network enabling standard phones to connect directly to satellites.

**The Bull Case:**
• Direct-to-device satellite connectivity (massive TAM)
• Strategic partnerships: AT&T, Vodafone, Rakuten (~2.8B subscribers)
• Technology proven with BlueBird test satellite
• FCC approval is binary catalyst that could unlock commercial operations

**The Bear Case:**
• Pre-revenue, cash-burning business
• FCC approval carries binary risk (could delay or deny)
• SpaceX/Starlink competition (better capitalized)
• Execution risk on global constellation buildout
• No earnings, no moat clarity yet

**The Key Question:**
Is FCC approval probability underpriced by the market? This is a classic binary catalyst setup."""
    }


def main():
    """Main entry point"""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           🎭  18 LEGENDARY INVESTORS DEBATE SYSTEM  🎭        ║
║                                                               ║
║  Where Warren Buffett, Michael Burry, Cathie Wood, and       ║
║  15 other legendary minds battle over trading signals        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    # Check for signal file argument
    if len(sys.argv) > 1:
        signal_file = sys.argv[1]
        print(f"📂 Loading signal from: {signal_file}")
        signal = load_signal_from_file(signal_file)
    else:
        print("📊 Using default signal: ASTS")
        signal = create_asts_signal()
    
    # Display signal
    print(f"\n{'='*60}")
    print(f"📊 SIGNAL: {signal['ticker']} @ ${signal['price']}")
    print(f"⚡ CATALYST: {signal['catalyst']}")
    print(f"{'='*60}\n")
    
    # Ask for confirmation
    print("This will spawn 18 sub-agents who will debate in Discord #18-agents-debate")
    confirm = input("\n🎭 Ready to unleash the debate? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("❌ Debate cancelled.")
        return
    
    # Run the debate!
    print("\n🚀 Launching debate orchestrator...\n")
    
    orchestrator = DebateOrchestrator(signal)
    
    # Choose debate mode
    print("Select debate mode:")
    print("  1. Quick debate (1 round, ~2 minutes)")
    print("  2. Standard debate (2 rounds, ~5 minutes)")
    print("  3. Deep debate (3 rounds, ~10 minutes)")
    
    mode = input("\nMode (1/2/3): ").strip() or "2"
    
    rounds = {
        "1": 1,
        "2": 2,
        "3": 3
    }.get(mode, 2)
    
    print(f"\n🎭 Starting {rounds}-round debate...")
    print(f"⏰ Estimated time: ~{rounds * 2.5:.0f} minutes\n")
    
    # Run it!
    result = orchestrator.run_full_debate(rounds=rounds)
    
    print("\n" + "="*60)
    print("✅ DEBATE COMPLETE!")
    print("="*60)
    print(f"\n📊 Final Tally:")
    print(f"   BUY:  {result.get('buy_votes', 0)} votes")
    print(f"   HOLD: {result.get('hold_votes', 0)} votes")
    print(f"   SELL: {result.get('sell_votes', 0)} votes")
    print(f"\n🎯 Consensus: {result.get('consensus', 'N/A')}")
    print(f"💪 Avg Conviction: {result.get('avg_conviction', 0)}/10\n")
    
    print("📢 Full report posted to Discord #research")
    print(f"🔗 View debate: discord://channels/1469016615718924349/1472692185106481417\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Debate interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
