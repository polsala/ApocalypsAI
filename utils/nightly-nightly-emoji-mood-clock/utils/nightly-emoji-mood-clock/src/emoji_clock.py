"""emoji_clock.py

Utility that maps an hour of the day (0‑23) to a mood‑representing emoji.

Provides:
- `get_emoji_for_hour(hour: int) -> str`
- CLI entry point that prints the emoji for the current local hour.
"""

from __future__ import annotations
import argparse
import datetime
import sys
from typing import Dict, Tuple

# Mapping of hour ranges (inclusive) to emojis.
# Each tuple is (start_hour, end_hour, emoji).
_EMOJI_RANGES: Tuple[Tuple[int, int, str], ...] = (
    (0, 5, "🌙"),   # Night
    (6, 8, "🌅"),   # Sunrise
    (9, 11, "🌤️"), # Morning
    (12, 13, "☀️"), # Midday
    (14, 17, "🌞"), # Afternoon
    (18, 19, "🌇"), # Sunset
    (20, 23, "🌌"), # Late night
)

def get_emoji_for_hour(hour: int) -> str:
    """Return the emoji that corresponds to *hour*.

    Args:
        hour: Integer hour in 24‑hour format (0‑23).

    Returns:
        A single emoji string.

    Raises:
        ValueError: If *hour* is outside the 0‑23 range.
    """
    if not (0 <= hour <= 23):
        raise ValueError(f"Hour must be between 0 and 23 inclusive, got {hour}")
    for start, end, emoji in _EMOJI_RANGES:
        if start <= hour <= end:
            return emoji
    # Fallback – should never happen because ranges cover all hours.
    return "❓"

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print an emoji representing the current hour.")
    parser.add_argument(
        "--hour",
        type=int,
        help="Specify an hour (0‑23) instead of using the current local time.",
    )
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        hour = args.hour if args.hour is not None else datetime.datetime.now().hour
        emoji = get_emoji_for_hour(hour)
        print(emoji)
        return 0
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
