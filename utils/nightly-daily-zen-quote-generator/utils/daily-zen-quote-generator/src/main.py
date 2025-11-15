"""Daily Zen Quote Generator.

Provides a deterministic quote of the day based on the current date.
"""

from __future__ import annotations

import datetime
from typing import List

# Embedded quotes list; could also be loaded from a JSON file.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity.",
    "Do not seek to follow in the footsteps of the wise; seek what they sought.",
    "When the mind is still, the universe surrenders.",
]


def _load_quotes() -> List[str]:
    """Return the list of quotes.

    # Mock rationale:
    In a real implementation this could read from an external JSON file.
    For this utility we keep the list in‑code to stay self‑contained.
    """
    return _QUOTES


def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date.

    The quote is selected by computing the number of days since the Unix epoch,
    then taking that modulo the number of available quotes.
    """
    if date is None:
        date = datetime.date.today()
    days_since_epoch = (date - datetime.date(1970, 1, 1)).days
    quotes = _load_quotes()
    index = days_since_epoch % len(quotes)
    return quotes[index]


def main() -> None:
    """CLI entry point: print today's quote."""
    print(get_quote())


if __name__ == "__main__":
    main()
