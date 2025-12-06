"""emoji_clock.py

Utility to convert a given hour and minute into the nearest clock‑face emoji.

Supported emojis:
- Full hour faces: 🕐 (1:00) … 🕛 (12:00)
- Half‑hour faces: 🕜 (1:30) … 🕧 (12:30)

The mapping follows the Unicode clock face set.
"""

import argparse
import sys
from typing import Tuple

# Mapping of hour (1‑12) to full‑hour emoji
FULL_HOUR_EMOJI = {
    1: "\U0001F550",
    2: "\U0001F551",
    3: "\U0001F552",
    4: "\U0001F553",
    5: "\U0001F554",
    6: "\U0001F555",
    7: "\U0001F556",
    8: "\U0001F557",
    9: "\U0001F558",
    10: "\U0001F559",
    11: "\U0001F55A",
    12: "\U0001F55B",
}

# Mapping of hour (1‑12) to half‑hour emoji
HALF_HOUR_EMOJI = {
    1: "\U0001F55C",
    2: "\U0001F55D",
    3: "\U0001F55E",
    4: "\U0001F55F",
    5: "\U0001F560",
    6: "\U0001F561",
    7: "\U0001F562",
    8: "\U0001F563",
    9: "\U0001F564",
    10: "\U0001F565",
    11: "\U0001F566",
    12: "\U0001F567",
}


def _normalize_hour(hour: int) -> int:
    """Convert any hour integer to 12‑hour clock representation (1‑12)."""
    hour_mod = hour % 12
    return 12 if hour_mod == 0 else hour_mod


def _round_to_nearest(hour: int, minute: int) -> Tuple[int, bool]:
    """Round minutes to the nearest hour or half‑hour.

    Returns a tuple ``(hour, is_half)`` where ``is_half`` indicates whether the
    result should use the half‑hour emoji.
    """
    if minute < 15:
        # Closer to the hour
        return hour, False
    elif minute < 45:
        # Closer to half‑hour
        return hour, True
    else:
        # Closer to next hour
        return (hour + 1) % 24, False


def time_to_emoji(hour: int, minute: int) -> str:
    """Return the clock‑face emoji that best represents ``hour``:`minute`.

    Parameters
    ----------
    hour: int
        Hour in 24‑hour format (0‑23).
    minute: int
        Minute (0‑59).
    """
    if not (0 <= hour <= 23):
        raise ValueError("hour must be in 0..23")
    if not (0 <= minute <= 59):
        raise ValueError("minute must be in 0..59")

    rounded_hour, is_half = _round_to_nearest(hour, minute)
    normalized = _normalize_hour(rounded_hour)
    if is_half:
        return HALF_HOUR_EMOJI[normalized]
    else:
        return FULL_HOUR_EMOJI[normalized]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a time to the nearest clock‑face emoji.")
    parser.add_argument("--hour", type=int, required=True, help="Hour in 24‑hour format (0‑23)")
    parser.add_argument("--minute", type=int, required=True, help="Minute (0‑59)")
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    try:
        emoji = time_to_emoji(args.hour, args.minute)
        print(emoji)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
