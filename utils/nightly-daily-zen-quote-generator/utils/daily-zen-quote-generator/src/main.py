"""
Daily Zen Quote Generator

Provides a deterministic quote of the day based on the current date.
"""

import argparse
import datetime
from typing import List, Tuple

# A small curated list of Zen quotes.
_QUOTES: List[Tuple[str, str]] = [
    ("The journey of a thousand miles begins with one step.", "Lao Tzu"),
    ("When the mind is still, the universe surrenders.", "Unknown"),
    ("Simplicity is the ultimate sophistication.", "Leonardo da Vinci"),
    ("Let go or be dragged.", "Zen Proverb"),
    ("The obstacle is the path.", "Zen Proverb"),
    ("Do not seek the truth, simply stop believing.", "Anonymous"),
]


def _select_quote_for_date(target_date: datetime.date) -> Tuple[str, str]:
    """Select a quote deterministically based on the given date.

    The index is computed as the number of days since the Unix epoch modulo the
    number of available quotes.
    """
    epoch = datetime.date(1970, 1, 1)
    days = (target_date - epoch).days
    index = days % len(_QUOTES)
    return _QUOTES[index]


def get_quote_of_the_day(date: datetime.date | None = None) -> Tuple[str, str]:
    """Return the quote of the day.

    Args:
        date: Optional date to use instead of today (useful for testing).

    Returns:
        A tuple ``(quote, author)``.
    """
    if date is None:
        date = datetime.date.today()
    return _select_quote_for_date(date)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a deterministic Zen quote for today."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Override the date (YYYY-MM-DD) for testing.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    quote, author = get_quote_of_the_day(args.date)
    print(f'"{quote}" — {author}')


if __name__ == "__main__":
    main()
