"""daily_zen_quote_generator – deterministic quote‑of‑the‑day utility.

Provides a single public function ``get_quote`` and a tiny CLI entry‑point.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# ---------------------------------------------------------------------------
# Built‑in quote pool – feel free to extend.
# ---------------------------------------------------------------------------
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When the mind is still, the whole universe surrenders.",
    "Let go of what you cannot change.",
    "Silence is a source of great strength.",
    "Be present; the now is all we ever have.",
    "Patience is the companion of wisdom.",
    "A calm mind brings inner power.",
    "Nature does not hurry, yet everything is accomplished.",
    "Kindness is a language the deaf can hear and the blind can see.",
]


def _index_for_date(date: datetime.date) -> int:
    """Return a stable index into ``_QUOTES`` for *date*.

    The algorithm combines the year and the day‑of‑year into a single integer
    and then takes the modulo with the number of quotes. This yields a repeatable
    mapping that changes once per day.
    """
    # ``date.timetuple().tm_yday`` gives 1‑based day of year.
    day_of_year = date.timetuple().tm_yday
    # Combine year and day to spread the distribution across years.
    combined = date.year * 366 + day_of_year  # 366 to avoid collisions on leap years.
    return combined % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date* (defaults to ``datetime.date.today()``).

    The function is pure and deterministic, making it trivial to test.
    """
    if date is None:
        date = datetime.date.today()
    idx = _index_for_date(date)
    return _QUOTES[idx]


def _cli() -> None:
    """Simple command‑line interface.

    Prints the quote for today. If a date string ``YYYY‑MM‑DD`` is supplied as
    the first argument, the quote for that date is printed instead (useful for
    debugging).
    """
    if len(sys.argv) > 1:
        try:
            date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        date = None
    print(get_quote(date))


if __name__ == "__main__":
    _cli()
