"""Daily Quote Generator utility.

Provides a function to retrieve a deterministic quote for the current day.
"""

import json
import datetime
import pathlib
from typing import List


def _load_quotes() -> List[str]:
    """Load the list of quotes from the bundled JSON file."""
    quotes_path = pathlib.Path(__file__).with_name('quotes.json')
    with open(quotes_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_daily_quote() -> str:
    """Return the quote for today, deterministic across runs."""
    quotes = _load_quotes()
    if not quotes:
        raise ValueError("Quote list is empty.")
    today = datetime.date.today()
    index = today.toordinal() % len(quotes)
    return quotes[index]


def main() -> None:
    """CLI entry point."""
    print(get_daily_quote())


if __name__ == "__main__":
    main()
