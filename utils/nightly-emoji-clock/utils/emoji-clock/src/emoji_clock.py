"""Emoji Clock utility.

Provides a function to map an hour (0‑23) to its corresponding clock face emoji.
"""

from __future__ import annotations
import sys


def get_clock_emoji(hour: int) -> str:
    """Return the clock face emoji for the given hour.

    Args:
        hour: Hour in 24‑hour format (0‑23). Values outside this range are wrapped modulo 12.

    Returns:
        A single Unicode clock face emoji.

    Raises:
        TypeError: If ``hour`` is not an integer.
    """
    if not isinstance(hour, int):
        raise TypeError("hour must be an integer")
    hour_mod = hour % 12
    mapping = {
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
    }
    return mapping[hour_mod]


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.emoji_clock <hour>")
        sys.exit(1)
    try:
        hour = int(sys.argv[1])
    except ValueError:
        print("Hour must be an integer")
        sys.exit(1)
    print(get_clock_emoji(hour))


if __name__ == "__main__":
    _cli()
