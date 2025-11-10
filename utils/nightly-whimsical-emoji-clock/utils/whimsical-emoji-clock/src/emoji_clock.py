"""emoji_clock.py

Utility that maps a 24‑hour time string to an emoji representing the time of day.

Provides:
- ``get_emoji_for_time(time_str: str) -> str`` – core function.
- CLI entry point ``python -m emoji_clock <HH:MM>``.
"""

import argparse
import sys
from datetime import datetime
from typing import Tuple

# Mapping of hour ranges to emojis
_TIME_EMOJI_MAP: Tuple[Tuple[int, int, str], ...] = (
    (0, 5, "🌙"),   # Night
    (6, 11, "🌅"),  # Sunrise
    (12, 17, "☀️"), # Day
    (18, 23, "🌇"), # Sunset
)


def _parse_time(time_str: str) -> datetime:
    """Parse ``HH:MM`` into a ``datetime`` object (date part ignored).

    Raises:
        ValueError: If the format is invalid.
    """
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError as exc:
        raise ValueError(f"Time '{time_str}' must be in HH:MM 24‑hour format") from exc


def get_emoji_for_time(time_str: str) -> str:
    """Return the emoji that corresponds to the supplied ``time_str``.

    The function is deterministic and does **not** perform any I/O.
    """
    dt = _parse_time(time_str)
    hour = dt.hour
    for start, end, emoji in _TIME_EMOJI_MAP:
        if start <= hour <= end:
            return emoji
    # Fallback – should never happen because the ranges cover 0‑23
    return "❓"


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Convert a 24‑hour time to a mood emoji.")
    parser.add_argument("time", help="Time in HH:MM 24‑hour format (e.g., 14:30)")
    args = parser.parse_args()
    try:
        emoji = get_emoji_for_time(args.time)
        print(emoji)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
