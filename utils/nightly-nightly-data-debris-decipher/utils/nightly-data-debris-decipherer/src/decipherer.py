import re
import json
import sys

def decipher_debris(text: str) -> dict:
    """
    Scans the input text for common data patterns and extracts them.

    Args:
        text: The input string to scan.

    Returns:
        A dictionary where keys are pattern types and values are lists of found items.
    """
    extracted_data = {
        "urls": [],
        "emails": [],
        "ipv4_addresses": [],
        "iso_dates": [],
        "numbers": []
    }

    # Regex patterns
    # URL pattern: https://stackoverflow.com/questions/5710204/what-is-a-good-regex-to-match-a-url
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    # Email pattern: https://emailregex.com/
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    # IPv4 pattern
    ipv4_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    # ISO 8601 Date/Datetime pattern (simplified for common cases)
    iso_date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?)?')
    # Number pattern (integers and floats)
    number_pattern = re.compile(r'\b-?\d+(?:\.\d+)?\b')

    # Find all matches
    extracted_data["urls"] = list(set(url_pattern.findall(text)))
    extracted_data["emails"] = list(set(email_pattern.findall(text)))
    extracted_data["ipv4_addresses"] = list(set(ipv4_pattern.findall(text)))
    extracted_data["iso_dates"] = list(set(iso_date_pattern.findall(text)))
    extracted_data["numbers"] = list(set(number_pattern.findall(text)))

    # Remove duplicates and sort for deterministic output (lexicographical for strings)
    for key in extracted_data:
        extracted_data[key].sort()

    return extracted_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m utils.nightly-data-debris-decipherer.src.decipherer <text_to_decipher>", file=sys.stderr)
        sys.exit(1)

    input_text = sys.argv[1]
    result = decipher_debris(input_text)
    print(json.dumps(result, indent=2))
