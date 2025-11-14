"""Emoji Clock utility.

Provides a function to represent the current (or given) time with a clock‑face emoji.
"""

import datetime
from typing import Optional

# Mapping of hour (1‑12) to clock face emojis
_HOUR_EMOJI = {
    1: "🕐",
    2: "🕑",
    3: "🕒",
    4: "🕓",
    5: "🕔",
    6: "🕕",
    7: "🕖",
    8: "🕗",
    9: "🕘",
    10: "🕙",
    11: "🕚",
    12: "🕛",
}

# Mapping of hour (1‑12) to half‑hour clock face emojis
_HALF_EMOJI = {
    1: "🕜",
    2: "🕝",
    3: "🕞",
    4: "🕟",
    5: "🕠",
    6: "🕡",
    7: "🕢",
    8: "🕣",
    9: "🕤",
    10: "🕥",
    11: "🕦",
    12: "🕧",
}


def _hour_12(dt: datetime.datetime) -> int:
    """Convert 24‑hour clock to 12‑hour representation (1‑12)."""
    hour = dt.hour % 12
    return 12 if hour == 0 else hour


def get_emoji_time(dt: Optional[datetime.datetime] = None) -> str:
    """Return a string with a clock emoji and HH:MM time.

    Args:
        dt: Optional datetime; if omitted, uses ``datetime.datetime.now()``.

    Returns:
        A string like ``🕑 14:05``.
    """
    if dt is None:
        dt = datetime.datetime.now()
    hour = _hour_12(dt)
    emoji = _HOUR_EMOJI[hour] if dt.minute < 30 else _HALF_EMOJI[hour]
    return f"{emoji} {dt:%H:%M}"


if __name__ == "__main__":
    print(get_emoji_time())
