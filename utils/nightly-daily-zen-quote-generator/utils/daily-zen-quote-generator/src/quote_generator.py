"""
Daily Zen Quote Generator

Selects a deterministic quote based on the day of the year.
"""

from __future__ import annotations
import datetime
from typing import List

# A short list of Zen‑like quotes; repeats if the year has more days than quotes.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the illusion of control.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Be present, not perfect.",
    "All things are temporary; cherish the now.",
    "Nature does not hurry, yet everything is accomplished.",
    "Peace comes from within; do not seek it elsewhere.",
    # Additional quotes can be added here.
]


def _select_quote(day_of_year: int) -> str:
    """Select a quote based on ``day_of_year`` (1‑366)."""
    index = (day_of_year - 1) % len(_QUOTES)
    return _QUOTES[index]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date, or today if ``None``.

    Args:
        date: Optional ``datetime.date``; defaults to today.

    Returns:
        A string containing the selected quote.
    """
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    return _select_quote(day_of_year)


if __name__ == "__main__":
    print(get_quote())
