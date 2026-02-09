#!/usr/bin/env python3
"""
Simple HTTP server for Command Center dashboard
"""

import http.server
import socketserver
import os

PORT = 8001
DIRECTORY = "/Users/agentjoselo/.openclaw/workspace/command-center"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🐓 Joselo Command Center")
        print(f"📊 Dashboard: http://localhost:{PORT}/dashboard.html")
        print(f"🔄 Auto-refresh: Every 5 seconds")
        print(f"\nPress Ctrl+C to stop")
        httpd.serve_forever()
