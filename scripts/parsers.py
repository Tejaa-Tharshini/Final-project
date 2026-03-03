# scripts/parsers.py
from bs4 import BeautifulSoup
import re

def extract_text(elem):
    return elem.get_text(strip=True) if elem else None

def extract_project_name(container):
    for tag in ["h1", "h2", "h3", "h4"]:
        t = container.find(tag)
        if t and t.get_text(strip=True):
            return t.get_text(strip=True)
    return None

def extract_location(container):
    text = container.get_text(" ", strip=True)
    m = re.search(r"(?:Location|City)\s*[:\-]\s*([A-Za-z\s,]+)", text, re.I)
    if m:
        return m.group(1).strip()
    return None

def extract_status(container):
    text = container.get_text(" ", strip=True).lower()
    if "ongoing" in text:
        return "ongoing"
    if "upcoming" in text:
        return "upcoming"
    if "completed" in text or "possession offered" in text:
        return "completed"
    return None

def extract_completion_date(container):
    text = container.get_text(" ", strip=True)
    m = re.search(r"(?:Possession|Completion)\s*[:\-]?\s*([A-Za-z0-9\s,]+)", text, re.I)
    if m:
        return m.group(1).strip()
    return None

def extract_budget(container):
    text = container.get_text(" ", strip=True)
    m = re.search(r"(₹[\d,\.]+\s*(?:Lakh|Cr)?)", text)
    if m:
        return m.group(1).strip()
    return None

def normalise_location(location_text, builder_row):
    """
    Tries to extract city and state from location_text.
    Fallback to builder_row values if not found.
    """
    if not location_text or not isinstance(location_text, str):
        return builder_row.get("city"), builder_row.get("state")

    # Common Indian cities for extraction
    # This can be expanded or replaced with a more robust lookup if needed
    major_cities = [
        "Mumbai", "Pune", "Thane", "Nagpur", "Nashik", "Aurangabad", 
        "Delhi", "Gurgaon", "Gurugram", "Noida", "Faridabad", "Ghaziabad",
        "Bangalore", "Bengaluru", "Mysore", "Hubli", "Mangalore",
        "Chennai", "Coimbatore", "Madurai", "Trichy", "Salem",
        "Hyderabad", "Secunderabad", "Warangal", "Visakhapatnam", "Vijayawada",
        "Kolkata", "Howrah", "Durgapur", "Siliguri",
        "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar",
        "Lucknow", "Kanpur", "Agra", "Meerut", "Varanasi", "Prayagraj",
        "Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"
    ]

    location_text_clean = location_text.strip()
    
    # Try to find a major city in the text
    for city in major_cities:
        if city.lower() in location_text_clean.lower():
            # If we find a city, we might still want to check if it's the 'right' city
            # for the builder, but usually the project location is more specific.
            return city, builder_row.get("state")

    parts = [p.strip() for p in location_text_clean.split(",")]
    if len(parts) >= 2:
        # Check if the last part is a known state or city
        potential_city = parts[-1]
        if potential_city.lower() in [c.lower() for c in major_cities]:
            return potential_city, builder_row.get("state")
        
        # Often format is "Locality, City"
        potential_city = parts[-1]
        return potential_city, builder_row.get("state")

    return builder_row.get("city"), builder_row.get("state")

def generic_builder_parser(html: str, builder_row: dict):
    soup = BeautifulSoup(html, "html.parser")
    projects = []

    containers = soup.find_all(
        "div",
        class_=lambda c: c and any(
            kw in c.lower() for kw in ["project", "property", "card", "listing"]
        ),
    )

    for c in containers:
        project_name = extract_project_name(c)
        if not project_name:
            continue

        location_text = extract_location(c)
        status = extract_status(c)
        completion = extract_completion_date(c)
        budget_raw = extract_budget(c)
        city, state = normalise_location(location_text, builder_row)

        projects.append({
            "builder_id": builder_row["builder_id"],
            "builder_name": builder_row["builder_name"],
            "project_name": project_name,
            "location_text": location_text,
            "city": city,
            "state": state,
            "status": status,
            "approx_completion_date": completion,
            "budget_raw": budget_raw,
            "source": "builder_site",
        })

    return projects

# Example plugin (once you inspect a real builder site)
def parse_demo_builder(html, builder_row):
    soup = BeautifulSoup(html, "html.parser")
    projects = []
    for card in soup.select("div.project-card"):  # adjust selectors
        project_name = extract_text(card.select_one("h3.project-title"))
        if not project_name:
            continue
        location_text = extract_text(card.select_one("span.project-location"))
        status = extract_text(card.select_one("span.project-status"))
        completion = extract_text(card.select_one("span.project-possession"))
        budget_raw = extract_text(card.select_one("span.project-price"))
        city, state = normalise_location(location_text, builder_row)

        projects.append({
            "builder_id": builder_row["builder_id"],
            "builder_name": builder_row["builder_name"],
            "project_name": project_name,
            "location_text": location_text,
            "city": city,
            "state": state,
            "status": status,
            "approx_completion_date": completion,
            "budget_raw": budget_raw,
            "source": "builder_site",
        })
    return projects

PLUGIN_PARSERS = {
    "Demo Builder Thane": parse_demo_builder,
    # Add real builders here later
}
