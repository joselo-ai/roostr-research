#!/usr/bin/env python3
"""
Simple HTTP server for roostr Trading Dashboard
Serves dashboard.html on localhost:8080
"""

import http.server
import socketserver
import os
from pathlib import Path

# Change to trading directory
TRADING_DIR = Path(__file__).parent.parent
os.chdir(TRADING_DIR)

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve dashboard.html for root path
        if self.path == '/':
            self.path = '/dashboard.html'
        return super().do_GET()

Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🐓 roostr Dashboard Server")
    print(f"📊 Serving at: http://localhost:{PORT}")
    print(f"📱 Access from your network: http://<your-ip>:{PORT}")
    print(f"⏹️  Press Ctrl+C to stop")
    httpd.serve_forever()
