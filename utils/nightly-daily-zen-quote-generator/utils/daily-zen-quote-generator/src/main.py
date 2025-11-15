"""
Daily Zen Quote Generator

Provides a deterministic quote of the day from a static list.
"""

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "🌿 “The only true wisdom is in knowing you know nothing.” – Socrates",
    "🌱 “Be yourself; everyone else is already taken.” – Oscar Wilde",
    "🍃 “In the middle of difficulty lies opportunity.” – Albert Einstein",
    "🌸 “The journey of a thousand miles begins with one step.” – Lao Tzu",
    "🌼 “What we think, we become.” – Buddha",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for the given date.

    If *date* is ``None``, uses today's date.
    The selection is deterministic: ``(ordinal % len(_QUOTES))``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point: print today's quote."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    main()
