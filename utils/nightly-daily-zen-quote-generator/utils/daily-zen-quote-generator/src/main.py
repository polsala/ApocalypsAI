"""
Daily Zen Quote Generator – deterministic daily Zen quote.

Reads a bundled JSON list of quotes and selects one based on the
current UTC date. The selection algorithm is simple: (day_of_year) % len(quotes).
"""

import json
import pathlib
import sys
from datetime import datetime, timezone


def load_quotes() -> list[str]:
    """Load quotes from the bundled JSON file."""
    quotes_path = pathlib.Path(__file__).with_name("quotes.json")
    with quotes_path.open(encoding="utf-8") as f:
        return json.load(f)


def quote_of_the_day(date: datetime | None = None) -> str:
    """Return the quote for the given date (UTC). If date is None, use now()."""
    if date is None:
        date = datetime.now(timezone.utc)
    quotes = load_quotes()
    if not quotes:
        raise ValueError("Quote list is empty")
    day_index = date.timetuple().tm_yday - 1  # tm_yday is 1‑based
    return quotes[day_index % len(quotes)]


def main() -> None:
    """CLI entry point – prints the quote of today."""
    try:
        print(quote_of_the_day())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
