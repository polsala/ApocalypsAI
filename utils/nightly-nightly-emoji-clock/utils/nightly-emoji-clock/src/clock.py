"""nightly_emoji_clock – Convert times to clock‑face emojis.

Provides a small CLI and a library function:
    time_to_emoji(time_str: str) -> str

The function accepts a string in ``HH:MM`` (24‑hour) format, rounds the minutes
to the nearest half hour, and returns the matching Unicode clock emoji.
"""

import sys
from typing import Tuple

# Mapping of hour (1‑12) to full‑hour emoji
FULL_HOUR_EMOJI = {
    12: "\U0001F55B",  # 🕛
    1: "\U0001F550",   # 🕐
    2: "\U0001F551",   # 🕑
    3: "\U0001F552",   # 🕒
    4: "\U0001F553",   # 🕓
    5: "\U0001F554",   # 🕔
    6: "\U0001F555",   # 🕕
    7: "\U0001F556",   # 🕖
    8: "\U0001F557",   # 🕗
    9: "\U0001F558",   # 🕘
    10: "\U0001F559",  # 🕙
    11: "\U0001F55A",  # 🕚
}

# Mapping of hour (1‑12) to half‑hour emoji
HALF_HOUR_EMOJI = {
    12: "\U0001F55C",  # 🕜
    1: "\U0001F55D",   # 🕝
    2: "\U0001F55E",   # 🕞
    3: "\U0001F55F",   # 🕟
    4: "\U0001F560",   # 🕠
    5: "\U0001F561",   # 🕡
    6: "\U0001F562",   # 🕢
    7: "\U0001F563",   # 🕣
    8: "\U0001F564",   # 🕤
    9: "\U0001F565",   # 🕥
    10: "\U0001F566",  # 🕦
    11: "\U0001F567",  # 🕧
}


def _parse_time(time_str: str) -> Tuple[int, int]:
    """Parse ``HH:MM`` into hour and minute integers.

    Raises:
        ValueError: If the format is invalid or values are out of range.
    """
    if ":" not in time_str:
        raise ValueError(f"Invalid time format: '{time_str}'. Expected HH:MM.")
    hour_str, minute_str = time_str.split(":", 1)
    hour = int(hour_str)
    minute = int(minute_str)
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        raise ValueError(f"Hour or minute out of range in '{time_str}'.")
    return hour, minute


def _round_to_half_hour(minute: int) -> int:
    """Round minutes to the nearest half hour (0 or 30).

    Returns the rounded minute value (0 or 30).
    """
    return 0 if minute < 15 else (30 if minute < 45 else 0)


def time_to_emoji(time_str: str) -> str:
    """Convert a ``HH:MM`` time string to the nearest clock‑face emoji.

    The minutes are rounded to the nearest half hour. If rounding pushes the
    minutes to ``60``, the hour is incremented (wrapping around 24).
    """
    hour, minute = _parse_time(time_str)
    rounded_minute = _round_to_half_hour(minute)
    if rounded_minute == 0:
        # Full hour case
        display_hour = hour % 12 or 12
        return FULL_HOUR_EMOJI[display_hour]
    else:
        # Half hour case – increment hour for display if minute rolled over
        display_hour = (hour + 1) % 12 or 12
        return HALF_HOUR_EMOJI[display_hour]


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m nightly_emoji_clock.src.clock <HH:MM>")
        sys.exit(1)
    try:
        emoji = time_to_emoji(sys.argv[1])
        print(emoji)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
