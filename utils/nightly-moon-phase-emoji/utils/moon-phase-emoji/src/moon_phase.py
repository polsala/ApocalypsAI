"""moon_phase.py

Utility to compute the moon phase for a given Gregorian date and return a corresponding emoji.

Algorithm based on John Conway's method (simplified for clarity). The result is one of eight phases:

0 – New Moon 🌑
1 – Waxing Crescent 🌒
2 – First Quarter 🌓
3 – Waxing Gibbous 🌔
4 – Full Moon 🌕
5 – Waning Gibbous 🌖
6 – Last Quarter 🌗
7 – Waning Crescent 🌘
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from typing import Tuple

# Mapping of phase index to emoji
_PHASE_EMOJIS: Tuple[str, ...] = (
    "🌑",  # New Moon
    "🌒",  # Waxing Crescent
    "🌓",  # First Quarter
    "🌔",  # Waxing Gibbous
    "🌕",  # Full Moon
    "🌖",  # Waning Gibbous
    "🌗",  # Last Quarter
    "🌘",  # Waning Crescent
)


def _conway_algorithm(d: date) -> int:
    """Return an integer 0‑7 representing the moon phase.

    The algorithm works entirely offline and is deterministic.
    Reference: https://en.wikipedia.org/wiki/Date_of_Easter#Anonymous_Gregorian_algorithm
    """
    year = d.year
    month = d.month
    day = d.day

    if month < 3:
        year -= 1
        month += 12
    month += 1  # March = 4, April = 5, …
    c = 365.25 * year
    e = 30.6 * month
    jd = int(c) + int(e) + day - 694039.09  # Julian date relative to known new moon
    jd /= 29.5305882  # Moon cycle
    phase = int(jd) % 8
    return phase


def get_moon_phase_emoji(d: date) -> str:
    """Return the moon‑phase emoji for *d*.

    Parameters
    ----------
    d: datetime.date
        The date for which to compute the moon phase.
    """
    phase_index = _conway_algorithm(d)
    return _PHASE_EMOJIS[phase_index]


def _parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print the moon‑phase emoji for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date in ISO format (YYYY‑MM‑DD). If omitted, uses today.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_cli_args(argv)
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"Invalid date format: {args.date}. Expected YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target_date = date.today()
    emoji = get_moon_phase_emoji(target_date)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
