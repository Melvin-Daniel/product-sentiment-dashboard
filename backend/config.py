"""
Backend configuration.

DEBUG / HOST / PORT are kept for backwards compatibility.
DATA_FILE and API_PORT make it explicit where data lives and which port the API uses.
"""
import os

DEBUG = True
HOST = "127.0.0.1"
PORT = 5000  # legacy name used by app.py

# New explicit settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "sample_reviews.json")
API_PORT = PORT
