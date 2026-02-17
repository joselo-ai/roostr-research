#!/usr/bin/env python3
"""
Content Factory Pipeline Orchestrator
Runs the full pipeline: Research → Scripts → Thumbnails → Packages
"""

import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import agent_research
import agent_script_writer
import agent_thumbnail
import agent_assembler


def run_full_pipeline(search_fn=None, delay_between_agents: int = 5):
    """
    Run the complete content factory pipeline.
    
    Args:
        search_fn: Optional web_search function for research agent
        delay_between_agents: Seconds to wait between agent runs
    
    Pipeline Flow:
        1. Research Agent: Find trending stories
        2. Script Writer: Generate scripts for stories
        3. Thumbnail Generator: Create thumbnails for scripts
        4. Package Assembler: Combine into publish-ready packages
    """
    print("=" * 70)
    print("🏭 CONTENT FACTORY PIPELINE")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}\n")
    
    # Step 1: Research Agent
    print("🔍 STEP 1: RESEARCH AGENT")
    print("-" * 70)
    try:
        stories = agent_research.run_research_agent(openclaw_search_fn=search_fn, top_n=7)
        agent_research.post_to_discord(stories)
        print(f"✅ Research complete: {len(stories)} trending stories posted\n")
    except Exception as e:
        print(f"❌ Research agent failed: {e}\n")
        return
    
    # Delay to let Discord API settle
    print(f"⏳ Waiting {delay_between_agents} seconds...")
    time.sleep(delay_between_agents)
    
    # Step 2: Script Writer Agent
    print("\n📝 STEP 2: SCRIPT WRITER AGENT")
    print("-" * 70)
    try:
        agent_script_writer.monitor_and_generate(limit=15)
        print("✅ Script writing complete\n")
    except Exception as e:
        print(f"❌ Script writer agent failed: {e}\n")
        return
    
    # Delay for Discord + image generation time
    print(f"⏳ Waiting {delay_between_agents} seconds...")
    time.sleep(delay_between_agents)
    
    # Step 3: Thumbnail Generator Agent
    print("\n🎨 STEP 3: THUMBNAIL GENERATOR AGENT")
    print("-" * 70)
    try:
        agent_thumbnail.monitor_and_generate(limit=10)
        print("✅ Thumbnail generation complete\n")
    except Exception as e:
        print(f"❌ Thumbnail generator agent failed: {e}\n")
        return
    
    # Delay for Discord to process uploads
    print(f"⏳ Waiting {delay_between_agents} seconds...")
    time.sleep(delay_between_agents)
    
    # Step 4: Package Assembler Agent
    print("\n📦 STEP 4: PACKAGE ASSEMBLER AGENT")
    print("-" * 70)
    try:
        agent_assembler.monitor_and_assemble(limit=20)
        print("✅ Package assembly complete\n")
    except Exception as e:
        print(f"❌ Package assembler agent failed: {e}\n")
        return
    
    # Summary
    print("=" * 70)
    print("🎉 PIPELINE COMPLETE!")
    print("=" * 70)
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    print("\nCheck Discord channels:")
    print("  • #trending-stories - Research output")
    print("  • #scripts - Video scripts")
    print("  • #thumbnails - Generated thumbnails")
    print("  • #ready-to-publish - Complete packages")
    print("=" * 70)


def run_individual_agent(agent_name: str, search_fn=None):
    """Run a single agent."""
    print(f"🤖 Running {agent_name} agent...\n")
    
    if agent_name == 'research':
        stories = agent_research.run_research_agent(openclaw_search_fn=search_fn, top_n=7)
        agent_research.post_to_discord(stories)
    
    elif agent_name == 'script':
        agent_script_writer.monitor_and_generate(limit=10)
    
    elif agent_name == 'thumbnail':
        agent_thumbnail.monitor_and_generate(limit=5)
    
    elif agent_name == 'assembler':
        agent_assembler.monitor_and_assemble(limit=15)
    
    else:
        print(f"❌ Unknown agent: {agent_name}")
        print("Available agents: research, script, thumbnail, assembler")
        return
    
    print(f"\n✅ {agent_name.title()} agent complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Content Factory Pipeline')
    parser.add_argument(
        '--agent',
        choices=['research', 'script', 'thumbnail', 'assembler', 'full'],
        default='full',
        help='Which agent to run (default: full pipeline)'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=5,
        help='Seconds to wait between agents (default: 5)'
    )
    
    args = parser.parse_args()
    
    if args.agent == 'full':
        run_full_pipeline(search_fn=None, delay_between_agents=args.delay)
    else:
        run_individual_agent(args.agent, search_fn=None)
