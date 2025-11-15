import json
import pathlib
import datetime
import hashlib
from typing import List

_QUOTE_FILE = pathlib.Path(__file__).with_name('quotes.json')


def _load_quotes() -> List[str]:
    """Load the static list of quotes from the bundled JSON file."""
    with _QUOTE_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def _date_hash(date: datetime.date) -> int:
    """Create a stable integer hash from a date.

    Uses SHA‑256 of the ISO formatted date string and returns an int.
    This is deterministic across Python runs and platforms.
    """
    digest = hashlib.sha256(date.isoformat().encode('utf-8')).hexdigest()
    return int(digest, 16)


def get_today_quote(today: datetime.date | None = None) -> str:
    """Return the quote for *today* (or a supplied date).

    Parameters
    ----------
    today: datetime.date, optional
        Override the date for testing or custom use. Defaults to ``datetime.date.today()``.
    """
    if today is None:
        today = datetime.date.today()
    quotes = _load_quotes()
    if not quotes:
        raise ValueError("Quote list is empty.")
    idx = _date_hash(today) % len(quotes)
    return quotes[idx]


def main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    print(get_today_quote())


if __name__ == "__main__":
    main()
