
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import pandas as pd
from firecrawl import Firecrawl
from config import FIRECRAWL_API_KEY

if not FIRECRAWL_API_KEY or "******" in FIRECRAWL_API_KEY:
    print("FIRECRAWL_API_KEY is not set or is masked!")
    sys.exit(1)

firecrawl_client = Firecrawl(api_key=FIRECRAWL_API_KEY)

url = "https://www.google.com" # Just a test URL
print(f"Testing Firecrawl with URL: {url}")
try:
    result = firecrawl_client.scrape(url, formats=["html"])
    print("Success!")
    html = result.html if hasattr(result, "html") else result.get("html", "")
    print(f"HTML Length: {len(html)}")
except Exception as e:
    print(f"Failed: {e}")
