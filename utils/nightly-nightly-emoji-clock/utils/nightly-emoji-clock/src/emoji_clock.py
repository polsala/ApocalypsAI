"""Emoji Clock utility.

Provides a function to convert a datetime hour into a clock‑face emoji.
"""

from __future__ import annotations

import datetime
import sys

# Mapping from hour (0‑23) to clock emoji (12‑hour face)
_HOUR_TO_EMOJI = {
    0: "🕛",  # 12 AM
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
    12: "🕛",  # 12 PM
    13: "🕐",
    14: "🕑",
    15: "🕒",
    16: "🕓",
    17: "🕔",
    18: "🕕",
    19: "🕖",
    20: "🕗",
    21: "🕘",
    22: "🕙",
    23: "🕚",
}


def get_emoji_time(dt: datetime.datetime | None = None) -> str:
    """Return the clock‑face emoji for the hour of *dt* (or now).

    Args:
        dt: Optional datetime; if omitted, uses ``datetime.datetime.now()``.

    Returns:
        A single Unicode emoji string.
    """
    if dt is None:
        dt = datetime.datetime.now()
    hour = dt.hour
    return _HOUR_TO_EMOJI[hour]


def main() -> None:
    """CLI entry point: print the current time as an emoji."""
    emoji = get_emoji_time()
    print(emoji)


if __name__ == "__main__":
    # Allow execution as a script
    sys.exit(main())
