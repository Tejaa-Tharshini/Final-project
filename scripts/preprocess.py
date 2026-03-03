# scripts/preprocess.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

from config import (
    RAW_MAGICBRICKS_ENRICHED_FILE,
    BUILDERS_WEBSITES_FILE,
    RAW_CITIES_SOURCE_FILE,
    PROJECTS_CLEAN_FIXED_FILE,
    GEOCODER_USER_AGENT,
    GEOCODER_CACHE_FILE,
)

# ---------- LOAD DATA ----------

def load_data():
    try:
        # Load enriched projects
        df_projects = pd.read_csv(RAW_MAGICBRICKS_ENRICHED_FILE, dtype=str)
        print(f"[LOAD] Loaded {len(df_projects)} enriched projects.")
    except FileNotFoundError:
        print(f"[ERROR] Enriched projects file not found: {RAW_MAGICBRICKS_ENRICHED_FILE}")
        df_projects = pd.DataFrame()

    try:
        # Load builder info
        df_builders = pd.read_csv(BUILDERS_WEBSITES_FILE, dtype=str)
        # Rename builder columns to prevent collision
        builder_rename = {
            "city": "builder_city",
            "state": "builder_state",
            "country": "builder_country",
            "website_url": "builder_website",
            "city_latitude": "builder_city_latitude",
            "city_longitude": "builder_city_longitude"
        }
        df_builders = df_builders.rename(columns=builder_rename)
        print(f"[LOAD] Loaded {len(df_builders)} builders.")
    except FileNotFoundError:
        print(f"[WARN] Builders file not found: {BUILDERS_WEBSITES_FILE}")
        df_builders = pd.DataFrame()

    try:
        # Load city source for state mapping
        df_cities = pd.read_csv(RAW_CITIES_SOURCE_FILE, dtype=str)
        # Strip whitespace from city and state names
        df_cities['City'] = df_cities['City'].str.strip()
        df_cities['State'] = df_cities['State'].str.strip()
        
        # Use only unique City -> State mapping
        city_to_state = df_cities[['City', 'State']].drop_duplicates('City').set_index('City')['State'].to_dict()
        
        # Add common aliases and missing major cities
        aliases = {
            "Bangalore": "Karnataka",
            "Gurgaon": "Haryana",
            "Noida": "Uttar Pradesh",
            "Greater Noida": "Uttar Pradesh",
            "Navi Mumbai": "Maharashtra",
            "Thane": "Maharashtra",
            "Trivandrum": "Kerala",
            "Mohali": "Punjab",
            "Zirakpur": "Punjab",
            "Panchkula": "Haryana",
            "Kharar": "Punjab",
        }
        for city, state in aliases.items():
            if city not in city_to_state:
                city_to_state[city] = state
                
        print(f"[LOAD] Loaded city-to-state mapping for {len(city_to_state)} cities (with aliases).")
    except FileNotFoundError:
        print(f"[WARN] City source file not found: {RAW_CITIES_SOURCE_FILE}")
        city_to_state = {}

    return df_projects, df_builders, city_to_state

# ---------- PROCESSING ----------

def recover_project_location(df, city_to_state):
    """
    Recovers the true project city and state from location_text.
    Most MagicBricks location_text is "Locality, City".
    """
    def extract_city(loc_text):
        if not loc_text or "," not in loc_text:
            return ""
        parts = [p.strip() for p in loc_text.split(",")]
        return parts[-1] if parts else ""

    print("[PROC] Recovering project-level cities and states...")
    # Extract city from location_text if the current 'city' is suspect (e.g. builder HQ)
    df['project_city'] = df['location_text'].apply(extract_city)
    
    # Map to state
    df['project_state'] = df['project_city'].map(city_to_state).fillna("Unknown")
    df['project_country'] = "India"
    
    return df

def rebuild_geo_key(df):
    """
    Rebuilds geo_key as "{location_text}, {project_city}, {project_state}, India"
    """
    print("[PROC] Rebuilding geo_keys...")
    df["geo_key"] = df.apply(
        lambda r: (
            (r.get("location_text") or "").strip() + ", "
            + (r.get("project_city") or "").strip() + ", "
            + (r.get("project_state") or "").strip() + ", India"
        ).strip(", "),
        axis=1,
    )
    return df

def clean_and_merge(df_projects, df_builders, city_to_state):
    if df_projects.empty:
        return pd.DataFrame()

    # 1. Recover locations
    df = recover_project_location(df_projects, city_to_state)

    # 2. Merge with builder info
    # We use builder_name as the link
    if not df_builders.empty:
        print("[PROC] Merging with builder info...")
        df = df.merge(df_builders, on="builder_name", how="left")

    # 3. Rebuild geo_key
    df = rebuild_geo_key(df)

    # 4. Final cleaning
    for col in df.columns:
        df[col] = df[col].fillna("").str.strip()
    
    # Remove empty rows
    df = df[df["project_name"] != ""]
    
    # Deduplicate based on project details
    subset = ["builder_name", "project_name", "project_city", "location_text"]
    df = df.drop_duplicates(subset=subset)

    return df

# ---------- MAIN ----------

def preprocess_and_fix():
    df_projects, df_builders, city_to_state = load_data()
    
    if df_projects.empty:
        return

    df_final = clean_and_merge(df_projects, df_builders, city_to_state)

    # Reorder columns for final output
    cols_order = [
        "project_city",
        "project_state",
        "project_country",
        "builder_name",
        "project_name",
        "location_text",
        "status",
        "latitude",
        "longitude",
        "budget_raw",
        "builder_city",
        "builder_state",
        "builder_website",
        "geo_key",
        "source",
    ]
    
    # Include all columns that actually exist
    existing_cols = [c for c in cols_order if c in df_final.columns]
    remaining = [c for c in df_final.columns if c not in existing_cols]
    df_final = df_final[existing_cols + remaining]

    # Rename project_city/state back to city/state for final clean output if desired
    # We drop the original 'city', 'state', 'country' columns first to avoid conflict
    df_final = df_final.drop(columns=["city", "state", "country"], errors="ignore")
    df_final = df_final.rename(columns={
        "project_city": "city",
        "project_state": "state",
        "project_country": "country"
    })

    df_final.to_csv(PROJECTS_CLEAN_FIXED_FILE, index=False)
    print(f"[OK] Saved fixed projects to {PROJECTS_CLEAN_FIXED_FILE}")
    print(f"[OK] Total projects: {len(df_final)}")

if __name__ == "__main__":
    preprocess_and_fix()
