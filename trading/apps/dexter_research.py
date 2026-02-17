#!/usr/bin/env python3
"""
Dexter Research API Wrapper

Bridge between roostr's Python trading system and Dexter (TypeScript/Bun).
Spawns Dexter subprocess for deep financial research.
"""

import subprocess
import json
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Path to Dexter installation
DEXTER_PATH = Path(__file__).parent.parent.parent / "dexter-research"
BUN_PATH = Path.home() / ".bun" / "bin" / "bun"


class DexterResearchEngine:
    """
    Autonomous financial research agent wrapper.
    
    Uses Dexter (TypeScript) to perform deep fundamental analysis:
    - Income statements, balance sheets, cash flow
    - SEC filings analysis
    - DCF valuation
    - Competitive analysis
    - News sentiment
    """
    
    def __init__(self, timeout: int = 180):
        """
        Initialize Dexter research engine.
        
        Args:
            timeout: Maximum time (seconds) for Dexter to complete research
        """
        self.timeout = timeout
        self.dexter_path = DEXTER_PATH
        self.bun_path = BUN_PATH
        
        # Verify Dexter installation
        if not self.dexter_path.exists():
            raise FileNotFoundError(f"Dexter not found at {self.dexter_path}")
        
        if not self.bun_path.exists():
            raise FileNotFoundError(f"Bun runtime not found at {self.bun_path}")
    
    def research_ticker(
        self, 
        ticker: str, 
        question: Optional[str] = None,
        focus_areas: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Run deep research on a ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'ASTS', 'PGR')
            question: Specific question to answer (optional)
            focus_areas: List of areas to focus on (optional)
                Examples: 'fundamentals', 'valuation', 'competition', 
                          'filings', 'news', 'moat'
        
        Returns:
            {
                'ticker': str,
                'summary': str,           # Executive summary
                'conviction': float,      # 0-10 conviction score
                'recommendation': str,    # BUY/HOLD/SELL
                'financials': dict,       # Key financial metrics
                'valuation': dict,        # Valuation analysis
                'risks': list,            # Identified risks
                'catalysts': list,        # Upcoming catalysts
                'research_notes': str,    # Full research output
                'timestamp': str,
                'research_time': float    # Seconds taken
            }
        
        Raises:
            TimeoutError: If research exceeds timeout
            subprocess.CalledProcessError: If Dexter fails
        """
        
        # Build research query
        if question is None:
            question = self._build_default_query(ticker, focus_areas)
        
        print(f"🔍 Starting Dexter research on {ticker}...")
        print(f"📋 Query: {question}")
        
        start_time = time.time()
        
        try:
            # Run Dexter via subprocess
            result = self._run_dexter(ticker, question)
            
            # Parse output
            research_data = self._parse_dexter_output(result.stdout, ticker)
            
            # Add metadata
            research_data['timestamp'] = datetime.now().isoformat()
            research_data['research_time'] = time.time() - start_time
            research_data['query'] = question
            
            print(f"✅ Research complete in {research_data['research_time']:.1f}s")
            
            return research_data
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(
                f"Dexter research on {ticker} exceeded {self.timeout}s timeout"
            )
        except Exception as e:
            raise RuntimeError(f"Dexter research failed: {str(e)}")
    
    def _build_default_query(self, ticker: str, focus_areas: Optional[list]) -> str:
        """Build a comprehensive default research query"""
        
        base_query = f"Analyze {ticker}."
        
        if focus_areas:
            focus_str = ", ".join(focus_areas)
            query = f"{base_query} Focus on: {focus_str}."
        else:
            # Comprehensive default analysis
            query = f"""{base_query} Provide:
1. Fundamentals: Revenue/earnings growth, margins, ROIC
2. Financial health: Balance sheet strength, cash flow, debt levels
3. Valuation: P/E, P/FCF vs peers, DCF estimate if possible
4. Competitive moat: Sustainable advantages vs competitors
5. Key risks: What could go wrong?
6. Catalysts: Upcoming events that could move the stock
7. Investment thesis: Why buy/hold/sell?"""
        
        return query
    
    def _run_dexter(self, ticker: str, question: str) -> subprocess.CompletedProcess:
        """
        Execute Dexter as subprocess.
        
        Uses run-research.ts script for programmatic access.
        """
        
        # Build command - use our programmatic runner
        cmd = [
            str(self.bun_path),
            "run",
            "run-research.ts",
            ticker,
            question
        ]
        
        # Execute with timeout
        result = subprocess.run(
            cmd,
            cwd=str(self.dexter_path),
            capture_output=True,
            text=True,
            timeout=self.timeout,
            env=self._get_env()
        )
        
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, 
                cmd, 
                result.stdout, 
                result.stderr
            )
        
        return result
    
    def _get_env(self) -> Dict[str, str]:
        """Get environment variables for Dexter (includes API keys)"""
        env = os.environ.copy()
        
        # Load .env from Dexter directory
        env_file = self.dexter_path / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env[key] = value
        
        return env
    
    def _parse_dexter_output(self, output: str, ticker: str) -> Dict[str, Any]:
        """
        Parse Dexter's output into structured data.
        
        Dexter's run-research.ts outputs JSON, so we parse it directly.
        """
        
        try:
            # Try to parse as JSON first
            parsed = json.loads(output)
            
            # Ensure all required fields exist
            parsed.setdefault('ticker', ticker)
            parsed.setdefault('summary', 'No summary available')
            parsed.setdefault('conviction', 5.0)
            parsed.setdefault('recommendation', 'HOLD')
            parsed.setdefault('financials', {})
            parsed.setdefault('valuation', {})
            parsed.setdefault('risks', [])
            parsed.setdefault('catalysts', [])
            parsed.setdefault('research_notes', output)
            
            return parsed
            
        except json.JSONDecodeError:
            # Fallback: if not JSON, try to parse as text
            print("⚠️  Dexter output is not JSON, using fallback parser...")
            
            parsed = {
                'ticker': ticker,
                'summary': '',
                'conviction': 5.0,
                'recommendation': 'HOLD',
                'financials': {},
                'valuation': {},
                'risks': [],
                'catalysts': [],
                'research_notes': output
            }
            
            lines = output.strip().split('\n')
            
            for line in lines:
                line_lower = line.lower().strip()
                
                # Extract recommendation keywords
                if any(word in line_lower for word in ['buy', 'strong buy', 'accumulate']):
                    parsed['recommendation'] = 'BUY'
                    parsed['conviction'] = 7.5
                elif any(word in line_lower for word in ['sell', 'avoid']):
                    parsed['recommendation'] = 'SELL'
                    parsed['conviction'] = 3.0
            
            # Extract summary (first substantial paragraph)
            paragraphs = [p.strip() for p in output.split('\n\n') if len(p.strip()) > 100]
            if paragraphs:
                parsed['summary'] = paragraphs[0][:500]
            
            return parsed
    
    def save_research(self, research_data: Dict[str, Any], output_dir: Path = None):
        """
        Save research output to file.
        
        Args:
            research_data: Research results from research_ticker()
            output_dir: Directory to save to (default: trading/research/)
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "research"
        
        output_dir.mkdir(exist_ok=True)
        
        ticker = research_data['ticker']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ticker}_dexter_{timestamp}.json"
        
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(research_data, f, indent=2)
        
        print(f"💾 Research saved to {filepath}")
        
        return filepath


def test_dexter():
    """Test Dexter with a sample query"""
    
    engine = DexterResearchEngine(timeout=180)
    
    # Test with ASTS
    result = engine.research_ticker(
        ticker="ASTS",
        focus_areas=['fundamentals', 'valuation', 'risks', 'catalysts']
    )
    
    print("\n" + "="*60)
    print("DEXTER RESEARCH RESULTS")
    print("="*60)
    print(f"\nTicker: {result['ticker']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Conviction: {result['conviction']}/10")
    print(f"\nSummary:\n{result['summary']}")
    print(f"\nResearch time: {result['research_time']:.1f}s")
    print("="*60)
    
    # Save to file
    engine.save_research(result)
    
    return result


if __name__ == "__main__":
    test_dexter()
