"""emoji_clock.py

Utility to convert an ISO‑8601 timestamp into a string containing:

* a clock emoji representing the hour (🕐‑🕛)
* a 12‑hour formatted time with minutes
* a relative phrase (e.g. "in 3 hours", "2 days ago")

All logic lives in the standard library – no third‑party packages required.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from typing import Tuple

# Mapping of hour (1‑12) to clock emoji. Index 0 is a placeholder for hour 12.
_CLOCK_EMOJIS = [
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


def _hour_to_emoji(hour: int) -> str:
    """Return the clock emoji for a given hour in 24‑hour format.

    The clock emojis cycle every 12 hours, with 0 → 12.
    """
    hour_12 = hour % 12
    # hour % 12 yields 0 for 12, 0‑11 for others. Emoji list uses index 0 for 12.
    return _CLOCK_EMOJIS[hour_12]


def _human_delta(delta: timedelta) -> str:
    """Convert a ``timedelta`` into a short human‑readable phrase.

    * Future: "in X"
    * Past: "X ago"
    The largest non‑zero unit (days, hours, minutes, seconds) is used.
    """
    total_seconds = int(delta.total_seconds())
    future = total_seconds > 0
    seconds = abs(total_seconds)

    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)

    if days:
        qty, unit = days, "day"
    elif hours:
        qty, unit = hours, "hour"
    elif minutes:
        qty, unit = minutes, "minute"
    else:
        qty, unit = secs, "second"

    if qty != 1:
        unit += "s"
    phrase = f"{qty} {unit}"
    return f"in {phrase}" if future else f"{phrase} ago"


def _format_time(dt: datetime) -> str:
    """Return a string like ``🕒 3:30 PM`` for a ``datetime`` object.
    """
    hour = dt.hour
    minute = dt.minute
    emoji = _hour_to_emoji(hour)
    # 12‑hour clock with AM/PM
    hour_12 = hour % 12
    hour_12 = 12 if hour_12 == 0 else hour_12
    am_pm = "AM" if hour < 12 else "PM"
    return f"{emoji} {hour_12}:{minute:02d} {am_pm}"


def format_time(timestamp: str, tz: str = "UTC") -> str:
    """Public API.

    Parameters
    ----------
    timestamp: str
        ISO‑8601 timestamp (e.g. ``2025-01-01T15:30:00+00:00``).
    tz: str, optional
        IANA time‑zone name for *now* and for the output. Defaults to ``UTC``.

    Returns
    -------
    str
        Human‑readable string with emoji and relative phrase.
    """
    # Parse the incoming timestamp; ``fromisoformat`` handles offsets.
    target = datetime.fromisoformat(timestamp)
    if target.tzinfo is None:
        # Assume UTC if no offset supplied.
        target = target.replace(tzinfo=timezone.utc)

    # Resolve the requested zone for "now".
    zone = ZoneInfo(tz)
    now = datetime.now(zone)

    # Convert target to the same zone for proper delta calculation.
    target = target.astimezone(zone)

    delta = target - now
    relative = _human_delta(delta)
    formatted = _format_time(target)
    return f"{formatted} ({relative})"


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_clock <ISO‑8601 timestamp>")
        sys.exit(1)
    ts = sys.argv[1]
    print(format_time(ts))


if __name__ == "__main__":
    _cli()
