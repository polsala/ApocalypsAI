"""emoji_clock.py
~~~~~~~~~~~~~~~~~~
Utility to map a 24‑hour time to the appropriate clock‑face emoji.

The Unicode clock emojis cover the 12‑hour clock with hour‑only and half‑hour variants:

- 🕛 U+1F55B – 12 o’clock
- 🕧 U+1F567 – 12:30
- 🕐 U+1F550 – 1 o’clock
- 🕜 U+1F55C – 1:30
- … up to 🕚 (11 o’clock) and 🕦 (11:30).

The function rounds minutes to the nearest half hour. Minutes >= 45 round up to the next hour,
minutes < 15 round down to the hour, and the rest round to the half hour.
"""

from __future__ import annotations

from typing import Tuple

# Mapping of hour (0‑23) to the base emoji for the hour (e.g., 0 → 🕛, 13 → 🕐)
_HOUR_EMOJI: Tuple[str, ...] = (
    "\U0001F55B",  # 12 o'clock (midnight)
    "\U0001F550",  # 1
    "\U0001F551",  # 2
    "\U0001F552",  # 3
    "\U0001F553",  # 4
    "\U0001F554",  # 5
    "\U0001F555",  # 6
    "\U0001F556",  # 7
    "\U0001F557",  # 8
    "\U0001F558",  # 9
    "\U0001F559",  # 10
    "\U0001F55A",  # 11
)

# Half‑hour emojis (12:30, 1:30, … 11:30)
_HALF_HOUR_EMOJI: Tuple[str, ...] = (
    "\U0001F567",  # 12:30
    "\U0001F55C",  # 1:30
    "\U0001F55D",  # 2:30
    "\U0001F55E",  # 3:30
    "\U0001F55F",  # 4:30
    "\U0001F560",  # 5:30
    "\U0001F561",  # 6:30
    "\U0001F562",  # 7:30
    "\U0001F563",  # 8:30
    "\U0001F564",  # 9:30
    "\U0001F565",  # 10:30
    "\U0001F566",  # 11:30
)


def _normalize_hour(hour: int) -> int:
    """Convert any integer hour to a 0‑23 range.

    Args:
        hour: Hour value, may be negative or >23.
    Returns:
        Normalized hour in the range 0‑23.
    """
    return hour % 24


def _round_to_nearest_half(minute: int) -> Tuple[bool, int]:
    """Round minutes to the nearest half hour.

    Returns a tuple ``(is_half, rounded_hour_increment)`` where ``is_half`` indicates
    whether the result should use the half‑hour emoji, and ``rounded_hour_increment``
    is 0 or 1 indicating if we need to advance the hour.
    """
    if minute < 15:
        return False, 0  # round down to the hour
    if minute < 45:
        return True, 0   # round to half hour
    return False, 1      # round up to next hour


def get_clock_emoji(hour: int, minute: int) -> str:
    """Return the clock‑face emoji representing the supplied time.

    The function is deterministic, offline and requires no external packages.

    Args:
        hour: Hour in 24‑hour format (0‑23). Values outside the range are wrapped.
        minute: Minute (0‑59). Values outside the range are wrapped modulo 60.
    Returns:
        A single Unicode clock emoji.
    """
    # Normalise inputs
    hour = _normalize_hour(hour)
    minute = minute % 60

    is_half, hour_inc = _round_to_nearest_half(minute)
    hour = (hour + hour_inc) % 24

    # Convert 24‑hour to 12‑hour index (0‑11) where 0 corresponds to 12.
    hour_12 = hour % 12

    if is_half:
        emoji = _HALF_HOUR_EMOJI[hour_12]
    else:
        emoji = _HOUR_EMOJI[hour_12]
    return emoji


if __name__ == "__main__":
    # Simple demo when run directly.
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m src.emoji_clock <hour> <minute>")
        sys.exit(1)
    h, m = map(int, sys.argv[1:])
    print(get_clock_emoji(h, m))
