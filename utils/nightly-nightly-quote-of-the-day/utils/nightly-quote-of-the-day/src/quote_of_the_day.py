"""Quote of the Day utility.

Provides a deterministic quote based on the current date.
"""

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade… then find someone whose life gave them vodka.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "To err is human; to really mess things up you need a computer.",
    "Keep calm and debug on.",
    "Life is short. Smile while you still have teeth.",
    "In a world full of copies, be an original… or at least a good replica.",
    "The future is bright… if you wear sunglasses."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return a quote for the given date.

    If *date* is None, uses today's date.
    The selection is deterministic: the ISO calendar day is hashed to an index.
    """
    if date is None:
        date = datetime.date.today()
    # Use the day number (YYYYMMDD) as a simple deterministic hash.
    day_number = int(date.strftime("%Y%m%d"))
    index = day_number % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    main()
