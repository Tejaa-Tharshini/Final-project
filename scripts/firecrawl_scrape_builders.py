# scripts/firecrawl_scrape_builders.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from config import DATA_DIR, FIRECRAWL_API_KEY, USE_FIRECRAWL, USER_AGENT
import requests
from parsers import generic_builder_parser, PLUGIN_PARSERS

if not FIRECRAWL_API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not set")

firecrawl_client = Firecrawl(api_key=FIRECRAWL_API_KEY)

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
        res = firecrawl_client.scrape(url, formats=["html"])
        # Handle Document object (v1 SDK) or dict (older SDK)
        html = ""
        if hasattr(res, "html"):
            html = res.html
        elif isinstance(res, dict):
            html = res.get("html") or res.get("data", {}).get("html") or ""
        
        if not html:
            return fetch_html_fallback(url)
        return html
    except Exception as e:
        error_msg = str(e).lower()
        if "payment" in error_msg or "credit" in error_msg or "402" in error_msg or "429" in error_msg:
            print(f"[INFO] Firecrawl limit reached for {url}. Switching to fallback...")
            return fetch_html_fallback(url)
            
        print(f"[ERROR] Firecrawl scrape failed for {url}: {e}")
        return fetch_html_fallback(url)

def parser_quality(rows):
    if not rows:
        return 0.0
    filled = sum(1 for r in rows if r.get("project_name") and r.get("city"))
    return filled / len(rows)

def main():
    in_path = DATA_DIR / "builders_websites.csv"
    out_path = DATA_DIR / "raw" / "builders_raw.csv"

    if not in_path.exists():
        print(f"[ERROR] Input file not found: {in_path}")
        print("[TIP] You must successfully run 'scripts/discover_websites.py' first.")
        return

    df = pd.read_csv(in_path, dtype=str)
    all_rows = []

    for _, row in df.iterrows():
        builder_name = row["builder_name"]
        url = row["website_url"]
        city = row["city"]
        state = row["state"]
        country = row.get("country", "India")

        print(f"[SCRAPE] {builder_name} -> {url}")
        html = fetch_html_firecrawl(url)
        if not html:
            continue

        builder_row = {
            "builder_id": None,           # not using IDs here
            "builder_name": builder_name,
            "city": city,
            "state": state,
            "country": country,
        }

        rows = generic_builder_parser(html, builder_row)

        if parser_quality(rows) < 0.3 and builder_name in PLUGIN_PARSERS:
            rows = PLUGIN_PARSERS[builder_name](html, builder_row)

        all_rows.extend(rows)

    if not all_rows:
        print("[WARN] No project rows scraped.")
        return

    df_out = pd.DataFrame(all_rows)
    df_out.to_csv(out_path, index=False)
    print(f"[OK] Saved Firecrawl builder data to {out_path}")


if __name__ == "__main__":
    main()
