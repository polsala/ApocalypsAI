"""Emoji Clock utility.

Provides `time_to_emoji` to map a HH:MM string to the nearest clock face emoji.
"""

from __future__ import annotations


def _hour_to_emoji(hour: int) -> str:
    """Return the hour‑only clock emoji for given hour (0‑23)."""
    hour12 = hour % 12
    emojis = [
        "🕛",  # 12
        "🕐",  # 1
        "🕑",  # 2
        "🕒",  # 3
        "🕓",  # 4
        "🕔",  # 5
        "🕕",  # 6
        "🕖",  # 7
        "🕗",  # 8
        "🕘",  # 9
        "🕙",  # 10
        "🕚",  # 11
    ]
    return emojis[hour12]


def _half_to_emoji(hour: int) -> str:
    """Return the half‑hour clock emoji for given hour (0‑23)."""
    hour12 = hour % 12
    emojis = [
        "🕜",  # 12:30
        "🕝",  # 1:30
        "🕞",  # 2:30
        "🕟",  # 3:30
        "🕠",  # 4:30
        "🕡",  # 5:30
        "🕢",  # 6:30
        "🕣",  # 7:30
        "🕤",  # 8:30
        "🕥",  # 9:30
        "🕦",  # 10:30
        "🕧",  # 11:30
    ]
    return emojis[hour12]


def time_to_emoji(time_str: str) -> str:
    """Convert `HH:MM` (24‑hour) to the nearest clock face emoji.

    Rounds to the nearest half hour. If exactly halfway, rounds up.
    """
    try:
        hour_part, minute_part = time_str.split(":")
        hour = int(hour_part)
        minute = int(minute_part)
    except Exception as exc:
        raise ValueError(f"Invalid time format '{time_str}'. Expected HH:MM.") from exc

    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"Hour or minute out of range in '{time_str}'.")

    total_minutes = hour * 60 + minute
    # Round to nearest 30 minutes; ties go up
    rounded = ((total_minutes + 15) // 30) * 30
    rounded %= 24 * 60  # wrap around midnight

    rounded_hour = rounded // 60
    rounded_minute = rounded % 60

    if rounded_minute == 0:
        return _hour_to_emoji(rounded_hour)
    else:
        return _half_to_emoji(rounded_hour)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-emoji-clock.src.emoji_clock <HH:MM>")
        sys.exit(1)

    print(time_to_emoji(sys.argv[1]))
