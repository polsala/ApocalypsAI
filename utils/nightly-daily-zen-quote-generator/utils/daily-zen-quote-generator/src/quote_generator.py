"""daily_zen_quote_generator

Provides a deterministic daily Zen quote based on the day of the year.
"""

from __future__ import annotations

import datetime
from typing import List

# A modest collection of Zen‑style sayings. Feel free to extend.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the stillness, you hear the truth.",
    "A single breath can change everything.",
    "The moon does not fight the night; it simply shines.",
    "Patience is the companion of wisdom.",
    "When you realize nothing is lacking, the whole world belongs to you.",
]


def get_daily_zen(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection is deterministic: ``day_of_year % len(_QUOTES)``.
    """
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    index = day_of_year % len(_QUOTES)
    return _QUOTES[index]


def _main() -> None:
    """CLI entry point – prints today's Zen quote to stdout."""
    print(get_daily_zen())


if __name__ == "__main__":
    _main()
