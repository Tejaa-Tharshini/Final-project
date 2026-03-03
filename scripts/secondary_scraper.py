# scripts/secondary_scraper.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import RAW_SECONDARY_FILE, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT}

def scrape_99acres_for_location(loc):
    city = loc["city"]
    state = loc["state"]
    rows = []

    # TODO: replace with real URL and selectors
    url = "https://www.magicbricks.com/builders-in-" + city.lower().replace(" ", "-")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"[WARN] 99acres-like URL {url} status {resp.status_code}")
            return rows
    except Exception as e:
        print(f"[ERROR] 99acres-like fetch {url}: {e}")
        return rows

    soup = BeautifulSoup(resp.text, "html.parser")

    for card in soup.select("div.project-card"):  # adjust
        project_name = card.select_one("h2.project-title").get_text(strip=True) if card.select_one("h2.project-title") else None
        builder_name = card.select_one("span.builder-name").get_text(strip=True) if card.select_one("span.builder-name") else None
        location_text = card.select_one("span.project-location").get_text(strip=True) if card.select_one("span.project-location") else None
        possession = card.select_one("span.possession").get_text(strip=True) if card.select_one("span.possession") else None
        price = card.select_one("span.price").get_text(strip=True) if card.select_one("span.price") else None

        if not project_name:
            continue

        rows.append({
            "builder_name": builder_name,
            "project_name": project_name,
            "location_text": location_text,
            "city": city,
            "state": state,
            "status": None,
            "approx_completion_date": possession,
            "budget_raw": price,
            "source": "secondary_portal",
        })

    return rows

def scrape_secondary_portals(locations):
    all_rows = []
    for loc in locations:
        print(f"[INFO] Scraping secondary portals for {loc['city']}")
        rows_99 = scrape_99acres_for_location(loc)
        all_rows.extend(rows_99)

    if all_rows:
        df = pd.DataFrame(all_rows)
        df.to_csv(RAW_SECONDARY_FILE, index=False)
        print(f"[OK] Saved secondary raw data to {RAW_SECONDARY_FILE}")
    else:
        print("[WARN] No rows scraped from secondary portals.")
