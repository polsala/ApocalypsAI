import sys
from datetime import datetime
from typing import List

# Mapping hour (1‑12) to clock‑face emojis
_HOUR_EMOJIS = {
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

# Mapping minute (rounded to nearest 5) to minute‑hand emojis
_MINUTE_EMOJIS = {
    0: "🕛",
    5: "🕐",
    10: "🕑",
    15: "🕒",
    20: "🕓",
    25: "🕔",
    30: "🕕",
    35: "🕖",
    40: "🕗",
    45: "🕘",
    50: "🕙",
    55: "🕚",
}


def _round_minute(minute: int) -> int:
    """Round a minute value to the nearest multiple of 5.

    The result is always in the range 0‑55; 60 wraps to 0.
    """
    rounded = int(5 * round(minute / 5)) % 60
    return rounded


def time_to_emoji(dt: datetime) -> str:
    """Convert a :class:`datetime.datetime` to a pair of emojis.

    The first emoji represents the hour hand, the second the minute hand.
    Minutes are rounded to the nearest 5‑minute increment.
    """
    hour = dt.hour % 12 or 12  # Convert 0 → 12 for 12‑hour clock
    minute = _round_minute(dt.minute)
    hour_emoji = _HOUR_EMOJIS[hour]
    minute_emoji = _MINUTE_EMOJIS[minute]
    return f"{hour_emoji}{minute_emoji}"


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Expected argument format: ``HH:MM`` (24‑hour clock).
    Returns exit code ``0`` on success, ``1`` on invalid input, ``2`` on missing argument.
    """
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m emoji_clock HH:MM")
        return 2
    try:
        time_str = argv[0]
        dt = datetime.strptime(time_str, "%H:%M")
    except ValueError:
        print("Invalid time format. Expected HH:MM")
        return 1
    print(time_to_emoji(dt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
