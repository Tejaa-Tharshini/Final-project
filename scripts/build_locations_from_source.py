# scripts/build_locations_from_source.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from config import DATA_DIR, LOCATIONS_FILE

SOURCE_FILE = DATA_DIR / "raw_cities_source.csv"

def main():
    df = pd.read_csv(SOURCE_FILE, dtype=str)

    # Pick source columns (change names according to your file)
    possible_city_cols = ["city", "City", "name"]
    possible_state_cols = ["state", "state_name", "State"]
    possible_country_cols = ["country", "Country"]

    def pick_col(possible, cols):
        for c in possible:
            if c in cols:
                return c
        return None

    city_col = pick_col(possible_city_cols, df.columns)
    state_col = pick_col(possible_state_cols, df.columns)
    country_col = pick_col(possible_country_cols, df.columns)

    if not city_col or not state_col:
        raise ValueError("Cannot find city/state columns in raw_cities_source.csv")

    if not country_col:
        df["country"] = "India"
        country_col = "country"

    df_out = df[[city_col, state_col, country_col]].copy()
    df_out.columns = ["city", "state", "country"]

    df_out["city"] = df_out["city"].str.strip()
    df_out["state"] = df_out["state"].str.strip()
    df_out["country"] = df_out["country"].str.strip()

    df_out = df_out.drop_duplicates(subset=["city", "state", "country"])
    df_out = df_out.reset_index(drop=True)
    df_out.insert(0, "location_id", df_out.index + 1)

    df_out.to_csv(LOCATIONS_FILE, index=False)
    print(f"[OK] locations.csv created with {len(df_out)} rows at {LOCATIONS_FILE}")

if __name__ == "__main__":
    main()
