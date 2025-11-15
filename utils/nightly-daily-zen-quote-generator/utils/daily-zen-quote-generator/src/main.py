"""
Daily Zen Quote Generator

Provides a deterministic "quote of the day" from a built‑in list.
"""

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "Know the rules well, so you can break them.",
    "The only constant is change.",
]


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point that prints today's quote."""
    quote = get_quote_of_the_day()
    print(quote)


if __name__ == "__main__":
    # Optional date argument for manual testing: ``YYYY-MM-DD``
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(get_quote_of_the_day(custom_date))
    else:
        main()
