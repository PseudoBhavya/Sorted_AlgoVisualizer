#!/usr/bin/env python3
"""Sorted Flask REST API Server Launcher"""
import os
import sys

# Ensure project root is in sys.path even when reloaded by watchdog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Sorted.api.app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Sorted REST API on http://127.0.0.1:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
