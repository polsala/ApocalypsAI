"""daily_motivation_quote – core implementation.

Provides functions to retrieve a random quote, a deterministic "quote of the day",
and a small CLI wrapper.
"""

import argparse
import datetime
import random
import sys
from typing import List, Optional

# ---------------------------------------------------------------------------
# Built‑in quote collection (whimsical but genuinely uplifting)
# ---------------------------------------------------------------------------
QUOTES: List[str] = [
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Dream big, work hard, stay humble.",
    "Every day is a second chance.",
    "Turn the pain into power.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Success doesn’t just find you. You have to go out and get it.",
    "Don’t stop when you’re tired. Stop when you’re done.",
]

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _apply_length_filter(quotes: List[str], max_length: Optional[int]) -> List[str]:
    """Return only quotes whose length is <= max_length.

    Args:
        quotes: List of candidate quotes.
        max_length: Maximum allowed character count (inclusive). ``None`` means no filter.
    """
    if max_length is None:
        return quotes
    return [q for q in quotes if len(q) <= max_length]


def get_random_quote(max_length: Optional[int] = None) -> str:
    """Return a random quote, optionally respecting a length constraint.

    The function uses ``random.choice`` which is mocked in the test suite for
    deterministic behaviour.
    """
    candidates = _apply_length_filter(QUOTES, max_length)
    if not candidates:
        raise ValueError("No quotes satisfy the length constraint.")
    return random.choice(candidates)


def get_quote_of_the_day(date: Optional[datetime.date] = None, max_length: Optional[int] = None) -> str:
    """Return a deterministic quote based on the supplied ``date``.

    The algorithm maps the day of year to an index in the (optionally filtered)
    quote list.  ``date`` defaults to ``datetime.date.today()``.
    """
    if date is None:
        date = datetime.date.today()
    candidates = _apply_length_filter(QUOTES, max_length)
    if not candidates:
        raise ValueError("No quotes satisfy the length constraint.")
    index = date.timetuple().tm_yday % len(candidates)
    return candidates[index]

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="daily-motivation-quote",
        description="Print a motivational quote.",
    )
    parser.add_argument(
        "--today",
        action="store_true",
        help="Show the deterministic quote of the day instead of a random one.",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        metavar="N",
        help="Maximum number of characters for the selected quote.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    args = _parse_args(argv)
    try:
        if args.today:
            quote = get_quote_of_the_day(max_length=args.max_length)
        else:
            quote = get_random_quote(max_length=args.max_length)
        print(quote)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
