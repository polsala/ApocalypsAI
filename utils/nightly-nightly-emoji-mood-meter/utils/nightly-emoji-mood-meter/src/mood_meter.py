"""Emoji Mood Meter utility.

Provides a simple function `get_mood` that returns an emoji representing the
typical mood for a given hour of the day.
"""

from __future__ import annotations

import datetime
from typing import Optional

# Mapping of hour ranges to emojis
_MOOD_MAP = {
    range(0, 6): "🌙",   # Late night
    range(6, 10): "🌅",  # Sunrise
    range(10, 13): "☕", # Coffee break
    range(13, 18): "💼", # Work hustle
    range(18, 21): "🌆", # Evening unwind
    range(21, 24): "🌙", # Nightfall
}


def _emoji_for_hour(hour: int) -> str:
    """Return the emoji for a specific hour."""
    for hour_range, emoji in _MOOD_MAP.items():
        if hour in hour_range:
            return emoji
    # Should never happen because ranges cover 0‑23
    raise ValueError(f"Hour {hour} is out of expected range 0‑23.")


def get_mood(hour: Optional[int] = None) -> str:
    """Return an emoji representing the mood for the given hour.

    If *hour* is ``None`` the current local hour is used.

    Args:
        hour: Optional hour in 24‑hour format (0‑23).

    Returns:
        A single‑character emoji string.

    Raises:
        ValueError: If *hour* is not in the range 0‑23.
    """
    if hour is None:
        hour = datetime.datetime.now().hour
    if not isinstance(hour, int) or not (0 <= hour <= 23):
        raise ValueError("hour must be an integer between 0 and 23 inclusive")
    return _emoji_for_hour(hour)
