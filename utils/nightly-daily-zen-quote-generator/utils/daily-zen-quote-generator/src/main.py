#!/usr/bin/env python3
"""Daily Zen Quote Generator

Prints a deterministic quote based on the current UTC date.
"""

import sys
from datetime import datetime, date
from typing import List

# Mock rationale: a small, curated list of timeless quotes.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken."
]


def get_quote(target_date: date = None) -> str:
    """Return a deterministic quote for *target_date*.

    If *target_date* is ``None`` the current UTC date is used.
    The quote index is ``date.toordinal() % len(_QUOTES)``.
    """
    if target_date is None:
        target_date = datetime.utcnow().date()
    index = target_date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main(argv=None) -> int:
    """CLI entry point.

    Prints the quote of today to stdout.
    Returns an exit code compatible with the repository's agent contract.
    """
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] in ("-h", "--help"):
        print("Usage: python -m src.main")
        return 0
    quote = get_quote()
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
