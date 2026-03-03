# scripts/builder_scraper.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from config import BUILDERS_MASTER_FILE, RAW_BUILDERS_FILE, FIRECRAWL_API_KEY, USE_FIRECRAWL, USER_AGENT
from firecrawl import Firecrawl
import requests
from parsers import generic_builder_parser, PLUGIN_PARSERS

if not FIRECRAWL_API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not set. Configure it in config.py or env.")

firecrawl_client = Firecrawl(api_key=FIRECRAWL_API_KEY)

if not FIRECRAWL_API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not set. Configure it in config.py or env.")

def load_active_builders():
    """Load builders with active_flag='1' from builders_master.csv."""
    if not BUILDERS_MASTER_FILE.exists():
        print(f"[ERROR] Builders master file not found: {BUILDERS_MASTER_FILE}")
        return []
    df = pd.read_csv(BUILDERS_MASTER_FILE, dtype=str)
    if "active_flag" not in df.columns:
        # If active_flag is missing, assume all are active for now or fix master
        df["active_flag"] = "1"
    df = df[df["active_flag"] == "1"].copy()
    return df.to_dict(orient="records")

def fetch_html_fallback(url: str) -> str:
    """Standard requests fallback if Firecrawl fails or is disabled."""
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.text
        print(f"[WARN] Fallback failed for {url}: Status {resp.status_code}")
        return ""
    except Exception as e:
        print(f"[ERROR] Fallback error for {url}: {e}")
        return ""

def fetch_html_firecrawl(url: str) -> str:
    if not USE_FIRECRAWL:
        return fetch_html_fallback(url)
        
    try:
        result = firecrawl_client.scrape(
            url,
            formats=["html"],
        )
        # Handle Document object (v1 SDK) or dict (older SDK)
        html = ""
        if hasattr(result, "html"):
            html = result.html
        elif isinstance(result, dict):
            html = result.get("html") or result.get("data", {}).get("html") or ""
        
        if not html:
            # If Firecrawl returns empty, try fallback
            return fetch_html_fallback(url)
        return html
    except Exception as e:
        error_msg = str(e).lower()
        if "payment" in error_msg or "credit" in error_msg or "402" in error_msg or "429" in error_msg:
            print(f"[INFO] Firecrawl limit reached for {url}. Switching to fallback...")
            return fetch_html_fallback(url)
            
        print(f"[ERROR] Firecrawl scrape failed for {url}: {e}")
        return fetch_html_fallback(url) # Fallback anyway for robustness

def parser_quality(rows):
    if not rows:
        return 0.0
    filled = 0
    for r in rows:
        if r.get("project_name") and r.get("city"):
            filled += 1
    return filled / len(rows)

def scrape_all_builders():
    builders = load_active_builders()
    all_rows = []

    for b in builders:
        url = b["website_url"]
        if not url:
            continue

        print(f"[INFO] Scraping builder with Firecrawl: {b['builder_name']} -> {url}")
        html = fetch_html_firecrawl(url)
        if not html:
            continue

        rows = generic_builder_parser(html, b)

        key = b["builder_name"]
        if parser_quality(rows) < 0.3 and key in PLUGIN_PARSERS:
            plugin = PLUGIN_PARSERS[key]
            rows = plugin(html, b)

        all_rows.extend(rows)

    if all_rows:
        df_out = pd.DataFrame(all_rows)
        df_out.to_csv(RAW_BUILDERS_FILE, index=False)
        print(f"[OK] Saved builder raw data to {RAW_BUILDERS_FILE}")
    else:
        print("[WARN] No rows scraped from builder sites.")
 