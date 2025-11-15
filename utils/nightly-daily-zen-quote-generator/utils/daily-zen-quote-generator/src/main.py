import datetime
import json
import pathlib
from typing import List

_QUOTE_FILE = pathlib.Path(__file__).with_name('quotes.json')

def _load_quotes() -> List[str]:
    """Load the list of quotes from the bundled JSON file.

    Returns:
        List of quote strings.
    """
    with _QUOTE_FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('quotes', [])

_QUOTES = _load_quotes()

def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date.

    The quote is selected by hashing the ISO‑format date and taking the
    modulus with the number of available quotes.

    Args:
        date: Optional date; defaults to today in UTC.
    Returns:
        A quote string.
    """
    if date is None:
        date = datetime.datetime.utcnow().date()
    # Simple deterministic index based on date string hash
    idx = hash(date.isoformat()) % len(_QUOTES)
    return __QUOTES[idx]

def main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    print(get_quote())

if __name__ == "__main__":
    main()
