# scripts/discover_websites.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import DATA_DIR, USER_AGENT   # or from config import ...

HEADERS = {"User-Agent": USER_AGENT}

def search_builder_websites_for_city(city: str, state: str, country: str = "India"):
    """
    Return a list of dicts: [{city, state, country, builder_name, website_url}, ...]
    You must customise the search logic.
    """
    results = []

    # EXAMPLE STRATEGY (placeholder): call a directory / search engine endpoint
    # TODO: replace this with a real source you are allowed to use.
    slug = city.strip().lower().replace(" ", "-")
    url = f"https://www.magicbricks.com/builders-in-{slug}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"[WARN] status {resp.status_code} for {url}")
            return results
    except Exception as e:
        print(f"[ERROR] fetch failed for {url}: {e}")
        return results

    soup = BeautifulSoup(resp.text, "html.parser")

    # TODO: change selectors based on real site structure
    for card in soup.select("div.builder-result"):
        name_tag = card.select_one("h2.builder-name")
        link_tag = card.select_one("a.builder-website")

        if not name_tag or not link_tag or not link_tag.has_attr("href"):
            continue

        builder_name = name_tag.get_text(strip=True)
        website_url = link_tag["href"].strip()

        results.append({
            "city": city,
            "state": state,
            "country": country,
            "builder_name": builder_name,
            "website_url": website_url,
        })

    return results


def main():
    loc_path = DATA_DIR / "locations.csv"
    out_path = DATA_DIR / "builders_websites.csv"

    df_loc = pd.read_csv(loc_path, dtype=str)
    all_rows = []

    for _, row in df_loc.iterrows():
        city = row["city"]
        state = row["state"]
        country = row.get("country", "India")
        print(f"[DISCOVERY] {city}, {state}")

        rows = search_builder_websites_for_city(city, state, country)
        all_rows.extend(rows)

    if not all_rows:
        print("[WARN] No builder websites found. (Using placeholder search logic, customize it in the script!)")
        return

    df_out = pd.DataFrame(all_rows)
    df_out.drop_duplicates(subset=["builder_name", "website_url"], inplace=True)
    df_out.to_csv(out_path, index=False)
    print(f"[OK] Saved builder websites to {out_path}")


if __name__ == "__main__":
    main()
