"""Pytest configuration."""
import os
import sys

# Add the parent directory to the path so we can import stockalert
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
