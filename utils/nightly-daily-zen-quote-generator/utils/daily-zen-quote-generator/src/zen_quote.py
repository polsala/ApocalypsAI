"""zen_quote.py – deterministic daily Zen quote generator."""

from __future__ import annotations

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The obstacle is the path.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "Simplicity is the ultimate sophistication.",
    "The journey of a thousand miles begins with one step.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "The mind is everything. What you think you become.",
    "Do not seek to follow in the footsteps of the wise. Seek what they sought.",
    "The only true wisdom is in knowing you know nothing.",
    "When the mind is still, the universe surrenders."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date.

    If *date* is ``None`` the current local date is used.
    The quote is selected by ``date.toordinal() % len(_QUOTES)``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point – prints today’s quote to stdout."""
    quote = get_quote()
    print(f"🧘 Today’s Zen: “{quote}”")


if __name__ == "__main__":
    # When executed as a module: ``python -m zen_quote``
    main()
