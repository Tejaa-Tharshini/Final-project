import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from firecrawl import Firecrawl
from config import FIRECRAWL_API_KEY

if not FIRECRAWL_API_KEY:
    print("FIRECRAWL_API_KEY not set")
    sys.exit(1)

client = Firecrawl(api_key=FIRECRAWL_API_KEY)
url = "https://example.com"
print(f"Testing URL: {url}")

try:
    res = client.scrape(url, formats=["html"])
    print(f"Result type: {type(res)}")
    print(f"Result attributes: {dir(res)}")
    
    # Try dict access
    try:
        html = res.get("html")
        print("Dict access (.get) worked")
    except Exception as e:
        print(f"Dict access (.get) failed: {e}")
        
    # Try attribute access
    try:
        html = res.html
        print(f"Attribute access (.html) works, length: {len(html)}")
    except Exception as e:
        print(f"Attribute access (.html) failed: {e}")

except Exception as e:
    print(f"Scrape failed: {e}")
