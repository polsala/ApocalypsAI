"""Emoji Clock utility.

Provides a function to map a datetime to a clock face emoji.
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping

# Mapping of hour (1-12) to clock face emoji.
_HOUR_TO_EMOJI: Mapping[int, str] = {
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


def get_clock_emoji(dt: datetime) -> str:
    """Return the clock face emoji representing the hour of *dt*.

    The hour is taken modulo 12, with 0 mapped to 12 (midnight/noon).

    Args:
        dt: A datetime instance.

    Returns:
        A single Unicode clock face emoji.
    """
    hour = dt.hour % 12
    hour = 12 if hour == 0 else hour
    return _HOUR_TO_EMOJI[hour]


def _cli() -> None:
    """CLI entry point: print the emoji for the current local time."""
    now = datetime.now()
    print(get_clock_emoji(now))


if __name__ == "__main__":
    _cli()
