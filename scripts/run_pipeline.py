# scripts/run_pipeline.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from config import LOCATIONS_FILE
from discovery import update_builders_master
from builder_scraper import scrape_all_builders
from secondary_scraper import scrape_secondary_portals
from preprocess import preprocess_and_fix

def load_locations():
    df = pd.read_csv(LOCATIONS_FILE, dtype=str)
    # Optional: limit for testing
    # df = df.head(50)
    return df[["city", "state", "country"]].to_dict(orient="records")

def main():
    try:
        locations = load_locations()

        print("[STEP] Discovery: update_builders_master")
        update_builders_master(locations)

        print("[STEP] Scrape builder websites (Firecrawl)")
        scrape_all_builders()

        print("[STEP] Scrape secondary portals")
        scrape_secondary_portals(locations)

        print("[STEP] Preprocess + geocode")
        preprocess_and_fix()

        print("[DONE] Pipeline finished")
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
