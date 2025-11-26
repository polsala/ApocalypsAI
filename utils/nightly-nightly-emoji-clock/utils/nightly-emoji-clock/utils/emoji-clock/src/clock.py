"""
emoji_clock utility
Provides a function to render the current time as a clock‑face emoji.
"""

from datetime import datetime
from typing import Optional

_HOUR_EMOJI = {
    0: "🕛",
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


def _hour_to_12h(hour: int) -> int:
    """Convert a 24‑hour value to the 12‑hour clock face used by the emojis."""
    return hour % 12


def get_emoji_clock(dt: Optional[datetime] = None) -> str:
    """Return a string with a clock‑face emoji representing the hour and the minute.

    Parameters
    ----------
    dt: datetime, optional
        The datetime to represent. If omitted, uses ``datetime.now()``.

    Returns
    -------
    str
        Example: ``🕒 07m`` for 14:07.
    """
    if dt is None:
        dt = datetime.now()
    hour_12 = _hour_to_12h(dt.hour)
    hour_emoji = _HOUR_EMOJI[hour_12]
    return f"{hour_emoji} {dt.minute:02d}m"


if __name__ == "__main__":
    print(get_emoji_clock())
