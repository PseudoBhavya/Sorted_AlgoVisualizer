#!/usr/bin/env python3
"""Sorted Desktop Launcher"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Sorted.gui.main_window import main

if __name__ == "__main__":
    main()
