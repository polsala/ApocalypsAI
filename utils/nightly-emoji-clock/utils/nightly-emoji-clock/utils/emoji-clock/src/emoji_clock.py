#!/usr/bin/env python3
"""
Emoji Clock Utility

Provides a function to convert a 24‑hour time into the closest
Unicode clock face emoji.
"""

from __future__ import annotations


def time_to_emoji(hour: int, minute: int) -> str:
    """Convert hour and minute to the nearest clock face emoji.

    The Unicode set contains emojis for each hour (🕐‑🕛) and each half‑hour
    (🕜‑🕧).  The function rounds the minute to the nearest half hour
    (0‑29 → hour, 30‑59 → hour+0.5) and then selects the appropriate emoji.

    Args:
        hour: Hour in 24‑hour format (0‑23).
        minute: Minute (0‑59).

    Returns:
        A single Unicode clock face emoji.

    Raises:
        ValueError: If hour or minute are out of range.
    """
    if not (0 <= hour <= 23):
        raise ValueError("hour must be between 0 and 23")
    if not (0 <= minute <= 59):
        raise ValueError("minute must be between 0 and 59")

    # Convert to 12‑hour clock for emoji mapping
    hour_12 = hour % 12 or 12

    # Determine if we need the half‑hour variant
    half = minute >= 30

    # Emoji code points: base hour emojis start at U+1F550 (🕐) for 1 o’clock.
    # Half‑hour emojis start at U+1F55C (🕜) for 1:30.
    if half:
        base = 0x1F55C  # 🕜 (1:30)
        offset = (hour_12 - 1) % 12
        return chr(base + offset)
    else:
        base = 0x1F550  # 🕐 (1 o’clock)
        offset = (hour_12 - 1) % 12
        return chr(base + offset)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Convert a time to a clock emoji.")
    parser.add_argument("time", help="Time in HH:MM (24‑hour) format")
    args = parser.parse_args()
    try:
        hour_str, minute_str = args.time.split(":")
        hour = int(hour_str)
        minute = int(minute_str)
        emoji = time_to_emoji(hour, minute)
        print(emoji)
    except Exception as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
