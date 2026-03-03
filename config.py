# config.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

DATA_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

LOCATIONS_FILE = DATA_DIR / "locations.csv"
BUILDERS_MASTER_FILE = DATA_DIR / "builders_master.csv"
RAW_BUILDERS_FILE = RAW_DIR / "builders_raw.csv"
RAW_SECONDARY_FILE = RAW_DIR / "secondary_raw.csv"
PROJECTS_CLEAN_FILE = PROCESSED_DIR / "projects_clean.csv"
BUILDERS_CLEAN_FILE = PROCESSED_DIR / "builders_clean.csv"
GEOCODER_CACHE_FILE = DATA_DIR / "geocode_cache.csv"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

GEOCODER_USER_AGENT = "sgb_builder_monitor"

# Firecrawl API key: best via environment variable
FIRECRAWL_API_KEY = "fc-48f7936afbfa40b9adede20edfc343e1" 
USE_FIRECRAWL = True

# in config.py
RAW_MAGICBRICKS_FILE = DATA_DIR / "raw" / "magicbricks_projects_raw.csv"
RAW_MAGICBRICKS_ENRICHED_FILE = DATA_DIR / "raw" / "magicbricks_projects_raw_enriched.csv"
BUILDERS_WEBSITES_FILE = DATA_DIR / "builders_websites.csv"
RAW_CITIES_SOURCE_FILE = DATA_DIR / "raw_cities_source.csv"
PROJECTS_CLEAN_FILE = PROCESSED_DIR / "projects_clean.csv"
PROJECTS_CLEAN_FIXED_FILE = PROCESSED_DIR / "projects_clean_fixed.csv"
GEOCODER_CACHE_FILE = DATA_DIR / "geocode_cache.csv"
GEOCODER_USER_AGENT = "sgb_builder_monitor"
