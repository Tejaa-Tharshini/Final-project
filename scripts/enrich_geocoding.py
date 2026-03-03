import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
from pathlib import Path
import sys

# Add root directory to sys.path to allow importing from config
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from config import DATA_DIR, USER_AGENT

def geocode_locations(in_file, out_file):
    print(f"[GEO] Loading data from {in_file}")
    df = pd.read_csv(in_file)
    
    # Create address string for geocoding
    # Use location_text directly as it usually includes "Locality, City"
    # Appending the discovery city/state can be incorrect for builders with national presence.
    df['full_address'] = df['location_text'] + ", " + df['country']
    
    unique_addresses = df['full_address'].unique()
    print(f"[GEO] Found {len(unique_addresses)} unique locations for {len(df)} rows.")

    geolocator = Nominatim(user_agent=USER_AGENT)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1)

    location_map = {}
    
    # Optional: Load existing cache if available to resume
    cache_file = DATA_DIR / "geocoding_cache.csv"
    if cache_file.exists():
        print(f"[GEO] Loading cache from {cache_file}")
        cache_df = pd.read_csv(cache_file)
        location_map = dict(zip(cache_df['address'], zip(cache_df['lat'], cache_df['lon'])))

    count = 0
    new_geocodes = 0
    
    print("[GEO] Starting geocoding (this may take a while)...")
    try:
        for addr in unique_addresses:
            if addr in location_map:
                continue
            
            try:
                location = geocode(addr)
                if location:
                    location_map[addr] = (location.latitude, location.longitude)
                    new_geocodes += 1
                else:
                    # Try fallback to just Locality + City
                    fallback_addr = ", ".join(addr.split(",")[:2])
                    location = geocode(fallback_addr)
                    if location:
                        location_map[addr] = (location.latitude, location.longitude)
                        new_geocodes += 1
                    else:
                        location_map[addr] = (None, None)
            except Exception as e:
                print(f"[WARN] Error geocoding {addr}: {e}")
                location_map[addr] = (None, None)
            
            count += 1
            if count % 10 == 0:
                print(f"[GEO] Processed {count}/{len(unique_addresses)} unique locations...")
                # Save cache periodically
                temp_cache = pd.DataFrame([{'address': k, 'lat': v[0], 'lon': v[1]} for k, v in location_map.items()])
                temp_cache.to_csv(cache_file, index=False)
                
    except KeyboardInterrupt:
        print("[GEO] Interrupted. Saving current progress...")

    # Map back to original dataframe
    df['latitude'] = df['full_address'].map(lambda x: location_map.get(x, (None, None))[0])
    df['longitude'] = df['full_address'].map(lambda x: location_map.get(x, (None, None))[1])
    
    # Drop the temporary full_address column
    df = df.drop(columns=['full_address'])
    
    df.to_csv(out_file, index=False)
    print(f"[OK] Saved enriched data to {out_file}")
    
    # Save final cache
    final_cache = pd.DataFrame([{'address': k, 'lat': v[0], 'lon': v[1]} for k, v in location_map.items()])
    final_cache.to_csv(cache_file, index=False)

def main():
    in_path = DATA_DIR / "raw" / "magicbricks_projects_raw.csv"
    out_path = DATA_DIR / "raw" / "magicbricks_projects_raw_enriched.csv"
    
    if not in_path.exists():
        print(f"[ERROR] Input file {in_path} not found.")
        return
        
    geocode_locations(in_path, out_path)

if __name__ == "__main__":
    main()
