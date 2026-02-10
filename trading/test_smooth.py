#!/usr/bin/env python3
"""Test Smooth.sh API"""

from smooth import SmoothClient

smooth_client = SmoothClient(api_key="cmzr-pcjmPhGKTxLKO2z_XqH4fLg9JLN7_oWyuFn6J0R7SkDCuLRVHVGQqARsSLfvRYExA41lLfWEzkqs0zOHEqOpyqJbgVNn3L6TF07b5pGLofsJT-TYrDJAYG9r")

# Test with simple task
task = smooth_client.run("Go to google.com and tell me what you see")

print(f"Live URL: {task.live_url()}")
print(f"Agent response: {task.result()}")
