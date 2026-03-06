# scripts/load_to_db.py
import sys
from pathlib import Path
import pandas as pd
import sqlite3
import re

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import PROJECTS_CLEAN_FIXED_FILE, APP_DB_FILE

def parse_budget_numeric(text):
    """
    Converts budgets like '?4.19 Cr - ?9.77 Cr' to numeric value in INR.
    Uses the minimum value of a range.
    """
    if not text or not isinstance(text, str) or text.strip() == "":
        return None
    
    # Remove common clutter
    text = text.replace('?', '').replace('₹', '').replace(',', '').strip()
    text = text.replace('Onwards', '').strip()
    
    # Handle ranges: split by '-' or 'to' and take the first (minimum) part
    # Example: '4.19 Cr - 9.77 Cr' -> '4.19 Cr'
    # Example: '95 Lac - 3.75 Cr' -> '95 Lac'
    parts = re.split(r'[-\s]to[-\s]|[-]', text)
    first_part = parts[0].strip()
    
    # Extract number and unit
    # Matches '4.19', '95', etc. and optionally 'Cr', 'Lac', etc.
    match = re.search(r'([\d\.]+)\s*(Lac|Lakh|Cr|Crore)?', first_part, re.I)
    if not match:
        return None
        
    try:
        val = float(match.group(1))
        unit = match.group(2)
        
        if unit:
            unit = unit.lower()
            if 'lac' in unit or 'lakh' in unit:
                val *= 100_000
            elif 'cr' in unit or 'crore' in unit:
                val *= 10_000_000
        return val
    except (ValueError, TypeError):
        return None

def load_data():
    print(f"[ETL] Loading data from {PROJECTS_CLEAN_FIXED_FILE}...")
    try:
        df = pd.read_csv(PROJECTS_CLEAN_FIXED_FILE)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return

    print(f"[ETL] Processing {len(df)} rows...")
    
    # Parse numeric budget
    df['budget_num'] = df['budget_raw'].apply(parse_budget_numeric)
    
    # Connect to SQLite
    print(f"[ETL] Syncing to {APP_DB_FILE}...")
    conn = sqlite3.connect(APP_DB_FILE)
    
    try:
        # We'll replace the table every time for now as per user spec
        df.to_sql('projects', conn, if_exists='replace', index=True, index_label='id')
        
        # Create an index on common filter columns for performance
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_city ON projects(city)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON projects(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_builder ON projects(builder_name)")
        
        print(f"[OK] Successfully loaded {len(df)} projects into database.")
        
        # Quick check
        res = cursor.execute("SELECT COUNT(*) FROM projects WHERE budget_num IS NOT NULL").fetchone()
        print(f"[INFO] Rows with numeric budget: {res[0]}")
        
    except Exception as e:
        print(f"[ERROR] Database sync failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    load_data()
