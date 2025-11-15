"""emoji forecast utility

Provides a deterministic emoji based on the day of the week.
"""

from __future__ import annotations

import datetime
from typing import Optional

# Mapping from weekday (0=Monday) to emoji
_WEEKDAY_EMOJI = {
    0: "🌞",  # Monday
    1: "🌤️",  # Tuesday
    2: "🌧️",  # Wednesday
    3: "⛈️",  # Thursday
    4: "🌈",  # Friday
    5: "❄️",  # Saturday
    6: "🌙",  # Sunday
}


def get_emoji_forecast(date: Optional[datetime.date] = None) -> str:
    """Return the emoji forecast for *date*.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    weekday = date.weekday()  # Monday == 0
    return _WEEKDAY_EMOJI[weekday]


def _cli() -> None:
    """Simple CLI entry‑point that prints today's emoji forecast."""
    print(get_emoji_forecast())


if __name__ == "__main__":
    _cli()
