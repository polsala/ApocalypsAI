"""
emoji_clock.py - Map a datetime hour to a clock face emoji.

Provides:
    get_clock_emoji(dt: datetime) -> str
"""

from datetime import datetime

# Mapping of hour (0‑11) to clock face emojis (12‑hour clock)
_HOUR_TO_EMOJI = {
    0: "🕛",  # 12 o'clock
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
}


def get_clock_emoji(dt: datetime) -> str:
    """Return the clock face emoji representing the hour of the given datetime.

    Args:
        dt: A `datetime` instance (timezone‑aware or naive).

    Returns:
        A single Unicode clock face emoji.
    """
    hour = dt.hour % 12
    return _HOUR_TO_EMOJI[hour]
