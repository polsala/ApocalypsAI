"""daily_zen_quote_generator

Provides a deterministic Zen‑style quote for a given date.

The selection algorithm is simple: the date's ordinal value modulo the number of
available quotes determines the index.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from typing import List

# ---------------------------------------------------------------------------
# Quote database (feel free to extend)
# ---------------------------------------------------------------------------
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with a single step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "In the middle of difficulty lies opportunity.",
    "Know the rules well, so you can break them wisely.",
    "A smooth sea never made a skilled sailor.",
    "The only constant is change.",
]


def get_quote(target_date: date) -> str:
    """Return a deterministic quote for *target_date*.

    The algorithm uses ``target_date.toordinal()`` to compute an index into the
    ``_QUOTES`` list. This ensures the same date always maps to the same quote
    without any external state.
    """
    index = target_date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def parse_cli(argv: List[str] | None = None) -> date:
    """Parse command‑line arguments and return the requested date.

    If no date argument is supplied, ``date.today()`` is used.
    """
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote-generator",
        description="Print a deterministic Zen quote for a given date.",
    )
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY‑MM‑DD format (default: today)",
    )
    args = parser.parse_args(argv)
    if args.date:
        try:
            parsed = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            parser.error(f"Invalid date format: {args.date!r}. Expected YYYY-MM-DD.")
        return parsed
    return date.today()


def main(argv: List[str] | None = None) -> int:
    target = parse_cli(argv)
    quote = get_quote(target)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
