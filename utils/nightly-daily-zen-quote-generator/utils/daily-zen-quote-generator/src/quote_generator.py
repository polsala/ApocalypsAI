"""
Daily Zen Quote Generator

Provides a deterministic quote based on the current date.
"""

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When the mind is still, the universe surrenders.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "Nature does not hurry, yet everything is accomplished.",
    "The only constant is change.",
    "Know yourself and you will win all battles.",
    "Be present, not perfect."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date.

    If *date* is None, uses today's date.
    """
    if date is None:
        date = datetime.date.today()
    # Day of year (1-366) modulo number of quotes
    index = (date.timetuple().tm_yday - 1) % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # Allow optional date argument for testing: YYYY-MM-DD
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(get_quote(custom_date))
    else:
        main()
