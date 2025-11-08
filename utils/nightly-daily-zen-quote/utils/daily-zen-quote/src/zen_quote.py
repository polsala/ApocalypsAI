"""daily-zen-quote utility

Provides a deterministic Zen quote based on the calendar date.
"""

from __future__ import annotations

import datetime
from typing import List

# A small curated list of Zen‑style quotes.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "Nature does not hurry, yet everything is accomplished.",
    "The only constant is change.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "A single act of kindness throws out roots in all directions.",
]


def get_zen_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection is deterministic: ``date.toordinal() % len(QUOTES)``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(QUOTES)
    return QUOTES[index]


def _cli() -> None:
    """Simple command‑line interface.

    Prints today's Zen quote to stdout.
    """
    print(get_zen_quote())


if __name__ == "__main__":
    _cli()
