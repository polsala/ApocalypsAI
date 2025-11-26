"""
zen.py - deterministic daily Zen quote generator.
"""

import datetime
import sys
from typing import Optional

_QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is pure, joy follows like a shadow.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Be like water: adaptable and resilient.",
    "In the middle of difficulty lies opportunity.",
    "Patience is the companion of wisdom.",
    "A single moment can change everything."
]


def _index_for_date(date: datetime.date) -> int:
    """Deterministically map a date to an index in _QUOTES.

    The mapping uses the date's ordinal value, ensuring the same date always
    selects the same quote without any external state.
    """
    seed = date.toordinal()
    return seed % len(_QUOTES)


def get_zen_quote(date: Optional[datetime.date] = None) -> str:
    """Return the Zen quote for the given date (defaults to today)."""
    if date is None:
        date = datetime.date.today()
    idx = _index_for_date(date)
    return _QUOTES[idx]


def main() -> None:
    """CLI entry point.

    Optional argument: a date in ``YYYY-MM-DD`` format. If omitted, today's
    quote is printed.
    """
    if len(sys.argv) > 1:
        try:
            date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        date = None
    print(get_zen_quote(date))


if __name__ == "__main__":
    main()
