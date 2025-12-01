"""emoji_calendar.py

A tiny utility that prints a month calendar where each day is replaced by an emoji
representing the weekday.

Usage:
    python -m utils.nightly-emoji-calendar.src.emoji_calendar [--year YYYY] [--month MM]

If no arguments are supplied, the current month is used.
"""

from __future__ import annotations

import argparse
import calendar
import datetime
from typing import Dict

# Mapping of weekday (0=Monday) to emoji
WEEKDAY_EMOJI: Dict[int, str] = {
    0: "🌞",  # Monday
    1: "🌜",  # Tuesday
    2: "🌟",  # Wednesday
    3: "🌈",  # Thursday
    4: "🎉",  # Friday
    5: "🛌",  # Saturday
    6: "🍳",  # Sunday
}


def get_emoji_for_date(date: datetime.date) -> str:
    """Return the emoji for the given date based on its weekday.

    Args:
        date: A ``datetime.date`` instance.
    Returns:
        The emoji string.
    """
    return WEEKDAY_EMOJI[date.weekday()]


def build_month_grid(year: int, month: int) -> list[list[str | None]]:
    """Create a 2‑dimensional list representing the month.

    Each cell contains the emoji for that day or ``None`` for padding.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday as first column
    month_days = cal.itermonthdates(year, month)
    weeks: list[list[str | None]] = []
    week: list[str | None] = []
    for day in month_days:
        if day.month != month:
            week.append(None)
        else:
            week.append(get_emoji_for_date(day))
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        # Pad the last week to length 7
        while len(week) < 7:
            week.append(None)
        weeks.append(week)
    return weeks


def render_grid(weeks: list[list[str | None]]) -> str:
    """Render the emoji grid as a string.

    Empty cells are rendered as two spaces for alignment.
    """
    lines = []
    for week in weeks:
        line = " ".join(cell if cell is not None else "  " for cell in week)
        lines.append(line.rstrip())
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print an emoji calendar for a given month.")
    parser.add_argument("--year", type=int, help="Year (e.g., 2025)")
    parser.add_argument("--month", type=int, help="Month number 1‑12")
    args = parser.parse_args()

    today = datetime.date.today()
    year = args.year if args.year is not None else today.year
    month = args.month if args.month is not None else today.month

    weeks = build_month_grid(year, month)
    output = render_grid(weeks)
    print(output)


if __name__ == "__main__":
    main()
