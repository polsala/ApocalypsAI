"""nightly-emoji-calendar

Render a month calendar where each day is replaced by an emoji:
- 📚 Monday‑Friday (workdays)
- 🌞 Saturday
- 🌛 Sunday

The module provides a `render_calendar(year, month)` function returning a multi‑line string.
It also offers a tiny CLI for quick ad‑hoc usage.
"""

from __future__ import annotations

import argparse
import calendar
from datetime import datetime
from typing import List

# Emoji mapping for weekdays (0=Monday … 6=Sunday)
_EMOJI_MAP = {
    0: "📚",  # Monday
    1: "📚",  # Tuesday
    2: "📚",  # Wednesday
    3: "📚",  # Thursday
    4: "📚",  # Friday
    5: "🌞",  # Saturday
    6: "🌛",  # Sunday
}


def _week_to_emoji(week: List[int]) -> str:
    """Convert a list of 7 ints (as returned by ``calendar.monthcalendar``) to a
    space‑separated string of emojis. ``0`` entries (padding) become two spaces.
    """
    tokens: List[str] = []
    for day, weekday in zip(week, range(7)):
        if day == 0:
            tokens.append("  ")  # placeholder for empty cells
        else:
            tokens.append(_EMOJI_MAP[weekday])
    # Join with a single space for readability
    return " ".join(tokens)


def render_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar using emojis.

    Parameters
    ----------
    year: int
        Four‑digit year.
    month: int
        Month number (1‑12).
    """
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    weeks = cal.monthdayscalendar(year, month)
    rendered_weeks = [_week_to_emoji(week) for week in weeks]
    return "\n".join(rendered_weeks)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an emoji calendar for a given month.")
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Year (default: current year)",
    )
    parser.add_argument(
        "--month",
        type=int,
        default=datetime.now().month,
        help="Month 1‑12 (default: current month)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output = render_calendar(args.year, args.month)
    print(output)


if __name__ == "__main__":
    main()
