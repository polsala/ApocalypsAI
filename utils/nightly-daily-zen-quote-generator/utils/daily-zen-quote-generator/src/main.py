import json
import sys
import hashlib
from datetime import date
from pathlib import Path

QUOTES_PATH = Path(__file__).with_name('quotes.json')

def load_quotes() -> list[str]:
    """Load the bundled quotes JSON file.

    Returns:
        List of quote strings.
    """
    try:
        with QUOTES_PATH.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError('Quotes JSON must be a list')
            return [str(q) for q in data]
    except FileNotFoundError:
        sys.stderr.write('Quotes file not found.\n')
        return []

def deterministic_index(quotes: list[str], today: date) -> int:
    """Return an index into ``quotes`` that is deterministic for a given date.

    The algorithm hashes the ISO string of the date and maps it into the range.
    """
    if not quotes:
        return -1
    # Use SHA256 for stable hashing across Python versions
    hash_bytes = hashlib.sha256(today.isoformat().encode('utf-8')).digest()
    # Convert first 8 bytes to int
    hash_int = int.from_bytes(hash_bytes[:8], 'big')
    return hash_int % len(quotes)

def get_quote(today: date | None = None) -> str:
    """Get the quote for *today* (or supplied date).

    Args:
        today: Optional date to override the current day (useful for testing).
    Returns:
        Selected quote string, or a fallback message.
    """
    quotes = load_quotes()
    if not quotes:
        return 'No quotes available.'
    if today is None:
        today = date.today()
    idx = deterministic_index(quotes, today)
    return quotes[idx]

def main() -> None:
    quote = get_quote()
    print(quote)

if __name__ == '__main__':
    main()
