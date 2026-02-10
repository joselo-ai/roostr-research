#!/usr/bin/env python3
"""
Smooth.sh API Client - Browser Agent Automation
"""

import json
import time
import requests
from pathlib import Path

class SmoothClient:
    def __init__(self, api_key=None):
        if not api_key:
            key_file = Path(__file__).parent.parent.parent / ".smooth-api-key"
            with open(key_file) as f:
                api_key = f.read().strip()
        
        self.api_key = api_key
        self.base_url = "https://api.smooth.sh/api/v1"
    
    def run_task(self, task_description, wait_for_result=True, timeout=120):
        """Submit a task to Smooth.sh and optionally wait for result"""
        
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {"task": task_description}
        
        # Submit task
        response = requests.post(
            f"{self.base_url}/task",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        result = response.json()
        
        task_id = result["r"]["id"]
        print(f"🔮 Task submitted: {task_id}")
        print(f"📺 Live URL: https://app.smooth.sh/live (check Activity Log)")
        
        if not wait_for_result:
            return {"task_id": task_id, "status": "submitted"}
        
        # Poll for result
        start_time = time.time()
        while time.time() - start_time < timeout:
            status_response = requests.get(
                f"{self.base_url}/task/{task_id}",
                headers={"apikey": self.api_key}
            )
            status_response.raise_for_status()
            status_data = status_response.json()["r"]
            
            status = status_data.get("status")
            print(f"   Status: {status}")
            
            if status == "completed":
                return {
                    "task_id": task_id,
                    "status": "completed",
                    "result": status_data.get("result"),
                    "live_url": status_data.get("live_url")
                }
            elif status == "failed":
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "error": status_data.get("error")
                }
            
            time.sleep(5)
        
        return {
            "task_id": task_id,
            "status": "timeout",
            "message": f"Task did not complete within {timeout}s"
        }

if __name__ == "__main__":
    client = SmoothClient()
    
    # Test task
    result = client.run_task("Go to x.com and tell me the #1 trending topic")
    
    print("\n" + "="*60)
    print(json.dumps(result, indent=2))
