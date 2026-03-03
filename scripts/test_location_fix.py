import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from scripts.parsers import normalise_location

def test_location_normalization():
    builder_row = {
        "city": "Port Blair",
        "state": "Andaman and Nicobar Islands",
        "builder_name": "Emaar India"
    }

    test_cases = [
        ("Sector 62, Gurgaon", "Gurgaon"),
        ("Golf Course Extension, Gurugram", "Gurugram"),
        ("Whitefield, Bangalore", "Bangalore"),
        ("New Town, Kolkata", "Kolkata"),
        ("Banjara Hills, Hyderabad", "Hyderabad"),
        ("Just Some Locality", "Port Blair"), # Fallback to builder city
        (None, "Port Blair"),
        ("Mumbai", "Mumbai"),
    ]

    print("Testing Location Normalization:")
    print("-" * 30)
    
    passed = 0
    for input_text, expected_city in test_cases:
        actual_city, actual_state = normalise_location(input_text, builder_row)
        if actual_city == expected_city:
            print(f"[PASS] '{input_text}' -> {actual_city}")
            passed += 1
        else:
            print(f"[FAIL] '{input_text}' -> Expected: {expected_city}, Actual: {actual_city}")

    print("-" * 30)
    print(f"Result: {passed}/{len(test_cases)} passed")
    
    if passed == len(test_cases):
        print("\nAll location tests passed!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    test_location_normalization()
