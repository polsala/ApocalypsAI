"""
emoji_clock.py

Utility to convert a time into clock‑face emojis.
"""

import argparse
import datetime
from typing import Tuple

# Mapping from hour (0‑23) to clock emoji (12‑hour face)
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


def _minute_to_emoji(minute: int) -> str:
    """
    Round minute down to the nearest 5‑minute block and return the corresponding clock emoji.
    """
    # 0‑4 -> 0, 5‑9 -> 5, etc.
    rounded = (minute // 5) * 5
    # Each 5‑minute block maps to the next hour emoji in the sequence.
    index = (rounded // 5) % 12
    # Use a temporary hour value (0‑11) to fetch the emoji.
    return _HOUR_EMOJI[index]


def time_to_emoji(hour: int, minute: int) -> str:
    """
    Convert hour and minute to a two‑emoji string: hour emoji + minute emoji.
    """
    hour_emoji = _HOUR_EMOJI[hour % 24]
    minute_emoji = _minute_to_emoji(minute)
    return f"{hour_emoji}{minute_emoji}"


def parse_time_string(time_str: str) -> Tuple[int, int]:
    """
    Parse a HH:MM string into hour and minute integers.
    """
    parts = time_str.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid time format: {time_str}")
    hour = int(parts[0])
    minute = int(parts[1])
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"Time out of range: {time_str}")
    return hour, minute


def main() -> None:
    parser = argparse.ArgumentParser(description="Print current time as emoji clock.")
    parser.add_argument(
        "--time",
        type=str,
        help="Optional HH:MM time. If omitted, uses current local time.",
    )
    args = parser.parse_args()

    if args.time:
        hour, minute = parse_time_string(args.time)
    else:
        now = datetime.datetime.now()
        hour, minute = now.hour, now.minute

    emoji = time_to_emoji(hour, minute)
    print(emoji)


if __name__ == "__main__":
    main()
