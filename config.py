# config.py
from pathlib import Path
import os

# ---------- BASE PATHS ----------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

DATA_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# ---------- INPUT / MASTER FILES ----------

LOCATIONS_FILE = DATA_DIR / "locations.csv"
BUILDERS_MASTER_FILE = DATA_DIR / "builders_master.csv"
BUILDERS_WEBSITES_FILE = DATA_DIR / "builders_websites.csv"  # used by scrapers

RAW_BUILDERS_FILE = RAW_DIR / "builders_raw.csv"
RAW_SECONDARY_FILE = RAW_DIR / "secondary_raw.csv"
RAW_CITIES_SOURCE_FILE = DATA_DIR / "raw_cities_source.csv"

# ---------- PROJECT RAW FILES (BY SOURCE) ----------

RAW_MAGICBRICKS_FILE = RAW_DIR / "magicbricks_projects_raw.csv"
RAW_MAGICBRICKS_ENRICHED_FILE = RAW_DIR / "magicbricks_projects_raw_enriched.csv"

# merged Magicbricks + other raw
RAW_MERGED_FILE = RAW_DIR / "projects_merged_raw.csv"

# ---------- CLEAN / PROCESSED OUTPUTS ----------

PROJECTS_CLEAN_FILE = PROCESSED_DIR / "projects_clean.csv"
PROJECTS_CLEAN_FIXED_FILE = PROCESSED_DIR / "projects_clean_fixed.csv"
BUILDERS_CLEAN_FILE = PROCESSED_DIR / "builders_clean.csv"
APP_DB_FILE = DATA_DIR / "app.db"

# ---------- GEOCODER / CACHE ----------

GEOCODER_CACHE_FILE = DATA_DIR / "geocode_cache.csv"
GEOCODER_USER_AGENT = "sgb_builder_monitor"

# ---------- USER AGENT ----------

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

# ---------- FIRECRAWL (UNCHANGED) ----------

FIRECRAWL_API_KEY = "fc-60997b6351ed4069a9e7a18f72285c21"
USE_FIRECRAWL = True
