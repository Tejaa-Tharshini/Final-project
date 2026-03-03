import sys
from pathlib import Path

# Add root directory to sys.path to allow importing from config
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import DATA_DIR, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT}


def parse_project_cards(html, city, state, country, builder_name):
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    # Updated selectors based on MagicBricks builder profile page
    for card in soup.select("div.dev-detail__complete-proj__card"):
        # project name
        name_tag = card.select_one("a.dev-detail__complete-proj__card__info--name")
        project_name = name_tag.get_text(strip=True) if name_tag else None
        if not project_name:
            continue

        # location / locality
        loc_tag = card.select_one("div.dev-detail__complete-proj__card__info--loc")
        location_text = loc_tag.get_text(strip=True) if loc_tag else ""

        # status
        status_tag = card.select_one("div.dev-detail__complete-proj__card__info--status")
        status_text = status_tag.get_text(strip=True).lower() if status_tag else ""
        if "ongoing" in status_text or "under construction" in status_text:
            status = "ongoing"
        elif "upcoming" in status_text or "launch" in status_text:
            status = "upcoming"
        elif "ready" in status_text or "completed" in status_text:
            status = "completed"
        else:
            status = status_text if status_text else None

        # type / possession date (sometimes combined)
        type_tag = card.select_one("div.dev-detail__complete-proj__card__info--type")
        project_type = type_tag.get_text(strip=True) if type_tag else ""

        # budget / price
        price_tag = card.select_one("div.dev-detail__complete-proj__card__info--price")
        budget_raw = price_tag.get_text(strip=True) if price_tag else None

        rows.append({
            "city": city,
            "state": state,
            "country": country,
            "builder_name": builder_name,
            "project_name": project_name,
            "location_text": location_text,
            "status": status,
            "project_type": project_type,
            "budget_raw": budget_raw,
            "source": "magicbricks",
        })

    return rows


def main():
    in_path = DATA_DIR / "builders_websites.csv"
    out_path = DATA_DIR / "raw" / "magicbricks_projects_raw.csv"

    df = pd.read_csv(in_path, dtype=str)
    all_rows = []

    for _, row in df.iterrows():
        city = row["city"]
        state = row["state"]
        country = row["country"]
        builder_name = row["builder_name"]
        url = row["website_url"]   # Magicbricks builder profile

        if not url:
            continue

        print(f"[SCRAPE] {city}, {builder_name} -> {url}")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code != 200:
                print(f"[WARN] status {resp.status_code} for {url}")
                continue
        except Exception as e:
            print(f"[ERROR] fetch failed for {url}: {e}")
            continue

        rows = parse_project_cards(resp.text, city, state, country, builder_name)
        all_rows.extend(rows)

    if not all_rows:
        print("[WARN] No project rows scraped – fix selectors in parse_project_cards().")
        return

    df_out = pd.DataFrame(all_rows)
    df_out.to_csv(out_path, index=False)
    print(f"[OK] Saved Magicbricks projects to {out_path}")


if __name__ == "__main__":
    main()
