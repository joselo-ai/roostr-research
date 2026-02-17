#!/usr/bin/env python3
"""
Discord utilities for multi-agent debate system
"""

import json
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path


class DiscordClient:
    """Simple Discord client using OpenClaw message tool"""
    
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
    
    def send_message(self, content: str, silent: bool = False) -> bool:
        """Send a message to the Discord channel"""
        try:
            cmd = [
                'openclaw', 'message',
                '--action', 'send',
                '--target', self.channel_id,
                '--message', content
            ]
            
            if silent:
                cmd.append('--silent')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def search_messages(self, query: str = None, limit: int = 50) -> List[Dict]:
        """Search messages in the channel"""
        try:
            cmd = [
                'openclaw', 'message',
                '--action', 'search',
                '--channel-id', self.channel_id,
                '--limit', str(limit)
            ]
            
            if query:
                cmd.extend(['--query', query])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse the output
            if result.returncode == 0:
                # The output format depends on OpenClaw's implementation
                # This is a placeholder
                return []
            
            return []
            
        except Exception as e:
            print(f"❌ Error searching messages: {e}")
            return []
    
    def get_recent_messages(self, limit: int = 50) -> List[str]:
        """Get recent message contents as strings"""
        messages = self.search_messages(limit=limit)
        return [msg.get('content', '') for msg in messages]


class VoteParser:
    """Parse agent votes from Discord messages"""
    
    @staticmethod
    def parse_agent_post(content: str) -> Optional[Dict[str, Any]]:
        """
        Parse a formatted agent post to extract vote, conviction, and risk.
        
        Expected format:
        🎭 **Warren Buffett**
        
        [Analysis text]
        
        **Vote:** BUY
        **Conviction:** 7/10
        **Risk:** Medium
        """
        
        result = {
            'agent_name': None,
            'vote': None,
            'conviction': None,
            'risk': None,
            'analysis': None
        }
        
        lines = content.strip().split('\n')
        
        # Extract agent name from first line (emoji + **Name**)
        if lines:
            first_line = lines[0]
            if '**' in first_line:
                # Extract text between ** **
                parts = first_line.split('**')
                if len(parts) >= 2:
                    result['agent_name'] = parts[1].strip()
        
        # Extract vote, conviction, risk
        for line in lines:
            line = line.strip()
            
            if line.startswith('**Vote:**'):
                vote = line.replace('**Vote:**', '').strip().upper()
                if vote in ['BUY', 'HOLD', 'SELL']:
                    result['vote'] = vote
            
            elif line.startswith('**Conviction:**'):
                conv_str = line.replace('**Conviction:**', '').strip()
                # Extract number (e.g., "7/10" -> 7)
                try:
                    if '/' in conv_str:
                        result['conviction'] = int(conv_str.split('/')[0])
                    else:
                        result['conviction'] = int(conv_str)
                except:
                    pass
            
            elif line.startswith('**Risk:**'):
                risk = line.replace('**Risk:**', '').strip().capitalize()
                if risk in ['Low', 'Medium', 'High']:
                    result['risk'] = risk
        
        # Extract analysis (everything between agent name and vote lines)
        analysis_lines = []
        in_analysis = False
        for line in lines[1:]:  # Skip first line (agent name)
            if line.startswith('**Vote:**'):
                break
            if line.strip():
                analysis_lines.append(line)
        
        result['analysis'] = '\n'.join(analysis_lines).strip()
        
        return result if result['vote'] else None
    
    @staticmethod
    def tally_votes(parsed_votes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tally votes and calculate consensus"""
        
        buy_votes = sum(1 for v in parsed_votes if v['vote'] == 'BUY')
        hold_votes = sum(1 for v in parsed_votes if v['vote'] == 'HOLD')
        sell_votes = sum(1 for v in parsed_votes if v['vote'] == 'SELL')
        
        total_votes = len(parsed_votes)
        
        # Calculate average conviction
        convictions = [v['conviction'] for v in parsed_votes if v.get('conviction')]
        avg_conviction = sum(convictions) / len(convictions) if convictions else 0
        
        # Determine consensus
        if total_votes == 0:
            consensus = "NO VOTES"
        elif buy_votes > hold_votes and buy_votes > sell_votes:
            pct = (buy_votes / total_votes) * 100
            consensus = f"BUY ({pct:.0f}%)"
        elif sell_votes > buy_votes and sell_votes > hold_votes:
            pct = (sell_votes / total_votes) * 100
            consensus = f"SELL ({pct:.0f}%)"
        elif hold_votes > buy_votes and hold_votes > sell_votes:
            pct = (hold_votes / total_votes) * 100
            consensus = f"HOLD ({pct:.0f}%)"
        else:
            consensus = "MIXED (No Clear Consensus)"
        
        return {
            'buy_votes': buy_votes,
            'hold_votes': hold_votes,
            'sell_votes': sell_votes,
            'total_votes': total_votes,
            'avg_conviction': round(avg_conviction, 1),
            'consensus': consensus,
            'parsed_votes': parsed_votes
        }


def format_agent_prompt_for_discord(agent_id: str, signal: Dict, round_num: int = 1) -> str:
    """
    Format the prompt that will be given to spawned sub-agents.
    Each agent should post to Discord using the message tool.
    """
    
    prompt = f"""You are analyzing a trading signal and must post your analysis to Discord.

**Your Task:**
1. Read the signal details below
2. Analyze it according to your investment philosophy
3. Post your analysis to Discord channel ID: 1472692185106481417

**Signal:**
{json.dumps(signal, indent=2)}

**Your Analysis Format (EXACT FORMAT REQUIRED):**

Post to Discord with this format:

[YOUR_EMOJI] **[YOUR_NAME]**

[3-5 sentences of your unique analysis based on your investment philosophy]

**Vote:** BUY / HOLD / SELL
**Conviction:** X/10
**Risk:** Low / Medium / High

**Instructions:**
- Use the `message` tool with action=send, target=1472692185106481417
- Be authentic to your investment style
- Keep analysis concise (3-5 sentences)
- Must include Vote, Conviction, and Risk in the exact format shown
"""
    
    return prompt


if __name__ == "__main__":
    # Test vote parsing
    test_post = """🎩 **Warren Buffett**
    
This is a speculative pre-revenue business. I don't understand satellite technology well enough to invest confidently. Without earnings, moat evidence, or clear path to profitability, this violates my core principles.

**Vote:** SELL
**Conviction:** 8/10
**Risk:** High
"""
    
    parser = VoteParser()
    parsed = parser.parse_agent_post(test_post)
    print("Parsed vote:", json.dumps(parsed, indent=2))
