#!/usr/bin/env python3
"""
Daily Zen Quote Generator

Provides a deterministic quote of the day from a static list.
"""

import datetime
import sys
from typing import Dict, List

# Built‑in list of quotes
_QUOTES: List[Dict[str, str]] = [
    {"text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde"},
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"text": "What we think, we become.", "author": "Buddha"},
]


def get_quote_of_the_day(date: datetime.date | None = None) -> Dict[str, str]:
    """
    Return a quote dict for the given date.
    If date is None, uses today's date.
    """
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    index = day_of_year % len(_QUOTES)
    return _QUOTES[index]


def format_quote(quote: Dict[str, str]) -> str:
    """Format a quote dict as a printable string."""
    return f'"{quote["text"]}" — {quote["author"]}'


def main() -> None:
    quote = get_quote_of_the_day()
    print(format_quote(quote))

if __name__ == "__main__":
    # Allow optional date argument for debugging: YYYY-MM-DD
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
            quote = get_quote_of_the_day(custom_date)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        else:
            print(format_quote(quote))
    else:
        main()
