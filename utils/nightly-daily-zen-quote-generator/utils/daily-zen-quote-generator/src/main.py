"""
Daily Zen Quote Generator

Provides a deterministic daily Zen quote based on the current date.
"""

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the stillness, you hear the truth.",
    "A single moment can change a lifetime.",
]


def get_quote(target_date: datetime.date | None = None) -> str:
    """Return a quote deterministically based on the given date.

    If ``target_date`` is ``None``, uses today's date.
    The quote is selected by computing ``day_of_year % len(_QUOTES)``.
    """
    if target_date is None:
        target_date = datetime.date.today()
    # ``timetuple().tm_yday`` is 1‑based; subtract 1 for 0‑based indexing
    index = (target_date.timetuple().tm_yday - 1) % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """Print today's Zen quote to stdout."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # Optional CLI date argument for manual testing: YYYY-MM-DD
    if len(sys.argv) > 1:
        try:
            dt = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format, use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        print(get_quote(dt))
    else:
        main()
