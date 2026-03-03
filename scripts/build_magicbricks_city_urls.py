# scripts/build_magicbricks_city_urls.py
import pandas as pd
from pathlib import Path

# Adjust this path if needed
LOCATIONS_FILE = Path("data/locations.csv")
OUT_FILE = Path("data/magicbricks_city_urls.csv")


def city_to_slug(city: str) -> str:
    """
    Convert city name to Magicbricks slug.
    Example: 'New Delhi' -> 'new-delhi'
    """
    return city.strip().lower().replace(" ", "-")


def main():
    df = pd.read_csv(LOCATIONS_FILE, dtype=str)

    # Ensure columns exist
    for col in ["city", "state", "country"]:
        if col not in df.columns:
            raise ValueError(f"locations.csv missing column: {col}")

    df["city_slug"] = df["city"].apply(city_to_slug)
    df["magicbricks_url"] = (
        "https://www.magicbricks.com/builders-in-" + df["city_slug"]
    )

    # Keep useful columns
    df_out = df[["city", "state", "country", "magicbricks_url"]].copy()
    df_out.to_csv(OUT_FILE, index=False)
    print(f"[OK] Saved city → Magicbricks URLs to {OUT_FILE}")


if __name__ == "__main__":
    main()
