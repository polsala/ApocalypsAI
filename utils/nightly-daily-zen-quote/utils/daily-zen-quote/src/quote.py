"""daily_zen_quote – deterministic daily Zen quote provider.

This module contains a small list of Zen‑style quotes and a helper function
`get_daily_quote` that returns a quote based on the supplied date (or today).
"""

from __future__ import annotations

import datetime
from typing import List

# A curated list of short Zen‑style sayings.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go of the past, embrace the present.",
    "A single breath can calm a storm.",
    "Nature does not hurry, yet everything is accomplished.",
    "The bamboo that bends is stronger than the oak that resists.",
    "Empty your cup so it may be filled anew.",
    "In the stillness, truth reveals itself.",
    "A river cuts through rock not by force, but by persistence.",
    "The moon does not fight the night; it simply shines.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "The sound of one hand clapping is the echo of awareness.",
    "Patience is the companion of wisdom.",
    "A candle loses nothing by lighting another.",
    "The mind is a garden; tend it with care.",
    "Even the smallest pebble creates ripples.",
    "To know the road ahead, walk it.",
    "The wind does not ask permission to move.",
    "Simplicity is the ultimate sophistication.",
    "When you are present, the world is present.",
    "A single seed holds a forest within.",
    "The mountain does not envy the valley.",
    "Listen to the silence between notes.",
    "A smile is the universal welcome.",
    "The deepest water is still.",
    "Every ending is a new beginning.",
    "Let your actions be your poetry.",
    "The sun rises for no one in particular; it simply rises.",
]


def _day_of_year(target_date: datetime.date) -> int:
    """Return the day of year (1‑366) for *target_date*.

    This helper exists to make the logic testable and isolated.
    """
    return target_date.timetuple().tm_yday


def get_daily_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The quote is selected by computing ``day_of_year % len(_QUOTES)``.
    """
    if date is None:
        date = datetime.date.today()
    index = (_day_of_year(date) - 1) % len(_QUOTES)  # -1 because day 1 should map to index 0
    return _QUOTES[index]


def _cli() -> None:
    """Simple command‑line interface that prints today's quote."""
    print(get_daily_quote())


if __name__ == "__main__":
    _cli()
