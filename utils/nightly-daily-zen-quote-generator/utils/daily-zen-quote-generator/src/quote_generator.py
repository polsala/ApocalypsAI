"""daily_zen_quote_generator

Provides a CLI that prints a deterministic Zen quote for the current day.

The module can also be imported and used programmatically via `get_quote(date: datetime.date) -> str`.
"""

import datetime
import json
import sys
from pathlib import Path
from typing import List

# Embedded list of quotes – kept small for the example.
_QUOTES_JSON = """
[
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "Nature does not hurry, yet everything is accomplished.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "A single moment can change a lifetime.",
    "The only constant is change.",
    "Know the road, but walk the path."
]
"""

_QUOTES: List[str] = json.loads(_QUOTES_JSON)


def _seed_from_date(date: datetime.date) -> int:
    """Create a deterministic integer seed from a date.

    The formula combines year, month, and day into a single integer.
    """
    return date.year * 10000 + date.month * 100 + date.day


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_from_date(date)
    index = seed % len(_QUOTES)
    return _QUOTES[index]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Prints the quote for today. Returns exit code ``0`` on success.
    """
    if argv is None:
        argv = sys.argv[1:]
    # No arguments are expected; ignore any extras for simplicity.
    quote = get_quote()
    print(f"🧘  \"{quote}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
