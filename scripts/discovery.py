# scripts/discover_websites.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import DATA_DIR, USER_AGENT, BUILDERS_MASTER_FILE, LOCATIONS_FILE, BUILDERS_WEBSITES_FILE

HEADERS = {"User-Agent": USER_AGENT}

def extract_builders_from_magicbricks(url: str, city: str, state: str, country: str):
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"[WARN] status {resp.status_code} for {url}")
            return results
    except Exception as e:
        print(f"[ERROR] fetch failed for {url}: {e}")
        return results

    soup = BeautifulSoup(resp.text, "html.parser")

    for card in soup.select("div.card"):
        # The builder name is inside h3.builder__name a
        name_tag = card.select_one("h3.builder__name a")
        if not name_tag:
            continue

        builder_name = name_tag.get_text(strip=True)
        # The link_tag is the name_tag itself or we can grab href from it
        website_url = (
            name_tag["href"].strip()
            if name_tag and name_tag.has_attr("href")
            else ""
        )

        results.append({
            "city": city,
            "state": state,
            "country": country,
            "builder_name": builder_name,
            "website_url": website_url,  # likely Magicbricks profile URL
        })
    return results


def update_builders_master(locations):
    """
    Discovery step:
    1. Runs build_magicbricks_city_urls logic (simplified)
    2. Runs extract_builders_from_magicbricks for each city
    3. Saves to builders_websites.csv
    4. Initializes builders_master.csv if missing
    """
    all_rows = []
    for loc in locations:
        city = loc["city"]
        state = loc["state"]
        country = loc["country"]
        
        # Build URL
        slug = city.strip().lower().replace(" ", "-")
        url = f"https://www.magicbricks.com/builders-in-{slug}"
        
        print(f"[DISCOVERY] {city}, {state} -> {url}")
        rows = extract_builders_from_magicbricks(url, city, state, country)
        all_rows.extend(rows)

    if not all_rows:
        print("[WARN] No builder websites found – fix CSS selectors in extract_builders_from_magicbricks().")
        return

    df_out = pd.DataFrame(all_rows)
    df_out.drop_duplicates(subset=["builder_name", "website_url"], inplace=True)
    df_out.to_csv(BUILDERS_WEBSITES_FILE, index=False)
    print(f"[OK] Saved builder websites to {BUILDERS_WEBSITES_FILE}")

    # Initialize builders_master.csv if it doesn't exist
    if not BUILDERS_MASTER_FILE.exists():
        print(f"[INIT] Creating {BUILDERS_MASTER_FILE}")
        master_df = df_out.copy()
        master_df["active_flag"] = "1"
        master_df.to_csv(BUILDERS_MASTER_FILE, index=False)
    else:
        # Update existing master logic could go here if needed
        print(f"[INFO] {BUILDERS_MASTER_FILE} already exists. Skipping initialization.")
def main():
    in_path = DATA_DIR / "magicbricks_city_urls.csv"
    out_path = DATA_DIR / "builders_websites.csv"

    df = pd.read_csv(in_path, dtype=str)
    all_rows = []

    for _, row in df.iterrows():
        city = row["city"]
        state = row["state"]
        country = row["country"]
        url = row["magicbricks_url"]
        print(f"[DISCOVERY] {city}, {state} -> {url}")

        rows = extract_builders_from_magicbricks(url, city, state, country)
        all_rows.extend(rows)

    if not all_rows:
        print("[WARN] No builder websites found – fix CSS selectors in extract_builders_from_magicbricks().")
        return

    df_out = pd.DataFrame(all_rows)
    df_out.drop_duplicates(subset=["builder_name", "website_url"], inplace=True)
    df_out.to_csv(out_path, index=False)
    print(f"[OK] Saved builder websites to {out_path}")


if __name__ == "__main__":
    main()
