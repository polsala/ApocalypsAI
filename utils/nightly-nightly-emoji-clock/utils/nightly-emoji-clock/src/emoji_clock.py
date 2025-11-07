import datetime
import sys
from typing import Tuple

# Mapping of hour (0‑23) to clock face emojis (12‑hour cycle)
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

# Half‑hour indicator (adds a small dot to the right of the clock)
_HALF_HOUR_EMOJI = "⏺"


def _round_minutes(minute: int) -> int:
    """Round minutes to the nearest 0 or 30.

    Returns 0 if the minute is <15, 30 if between 15‑44, otherwise 0 of the next hour.
    """
    if minute < 15:
        return 0
    if minute < 45:
        return 30
    # round up to next hour (handled by caller)
    return 60


def _hour_minute_from_datetime(dt: datetime.datetime) -> Tuple[int, int]:
    """Extract hour and minute, applying rounding logic.

    If minutes round up to 60, hour is incremented (mod 24) and minutes become 0.
    """
    hour = dt.hour
    minute = dt.minute
    rounded = _round_minutes(minute)
    if rounded == 60:
        hour = (hour + 1) % 24
        minute = 0
    else:
        minute = rounded
    return hour, minute


def get_emoji_time(dt: datetime.datetime) -> str:
    """Return a string representing *dt* as clock‑face emojis.

    Example: 13:45 → "🕐⏺" (1 PM with half‑hour indicator).
    """
    hour, minute = _hour_minute_from_datetime(dt)
    emoji = _HOUR_EMOJI[hour]
    if minute == 30:
        emoji += _HALF_HOUR_EMOJI
    return emoji


def _cli() -> None:
    now = datetime.datetime.now()
    print(get_emoji_time(now))


if __name__ == "__main__":
    _cli()
