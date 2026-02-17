#!/usr/bin/env python3
"""
OpenClaw Integration Runner
This script is called by OpenClaw agents to run the pipeline with web_search
"""

import sys
import json
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent))

import run_pipeline
import agent_research


def openclaw_search_wrapper(query: str, count: int = 5):
    """
    Wrapper for web_search that gets injected by OpenClaw.
    When running from OpenClaw, this will be replaced with actual web_search.
    """
    # This is a placeholder - OpenClaw will inject the real web_search
    print(f"[MOCK] Would search for: {query} (count={count})")
    return []


def run_research_only():
    """Run just the research agent with web_search."""
    print("🔍 Running Research Agent with OpenClaw web_search integration...\n")
    
    # OpenClaw agents can inject search_fn here
    stories = agent_research.run_research_agent(
        openclaw_search_fn=openclaw_search_wrapper,
        top_n=7
    )
    
    agent_research.post_to_discord(stories)
    
    print(f"\n✅ Research complete: {len(stories)} stories posted to Discord")
    return stories


def run_full_pipeline_with_search():
    """Run full pipeline with web_search."""
    print("🏭 Running Full Pipeline with OpenClaw web_search integration...\n")
    
    run_pipeline.run_full_pipeline(
        search_fn=openclaw_search_wrapper,
        delay_between_agents=10  # Longer delay for production
    )


if __name__ == "__main__":
    # Default: run full pipeline
    if len(sys.argv) > 1 and sys.argv[1] == 'research-only':
        run_research_only()
    else:
        run_full_pipeline_with_search()
