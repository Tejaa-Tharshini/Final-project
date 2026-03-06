# backend/db.py
import sqlite3
import sys
from pathlib import Path

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import APP_DB_FILE

def get_db_connection():
    conn = sqlite3.connect(APP_DB_FILE)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn
