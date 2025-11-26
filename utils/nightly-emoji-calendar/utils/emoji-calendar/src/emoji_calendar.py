"""
emoji-calendar utility.

Provides a function to render a month calendar with weekday‑specific emojis.
"""

import sys
import calendar
from datetime import datetime
from typing import List

# Mapping Monday=0 … Sunday=6 (whimsical cycle)
_WEEKDAY_EMOJIS = ["🌞", "🌜", "🌛", "🌞", "🌜", "🌛", "🌞"]


def get_weekday_emoji(weekday: int) -> str:
    """Return the emoji for a given weekday (0=Monday)."""
    return _WEEKDAY_EMOJIS[weekday % 7]


def _format_day(day: int, weekday: int) -> str:
    """Format a single day number with its emoji, or blanks for padding."""
    if day == 0:
        return "   "
    return f"{get_weekday_emoji(weekday)}{day:2d}"


def render_month(year: int, month: int) -> str:
    """Render a month calendar where each day is prefixed by its weekday emoji.

    Returns a multi‑line string.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday as first day
    month_name = calendar.month_name[month]
    header = f"{month_name} {year}"
    weekday_header = "Mo Tu We Th Fr Sa Su"
    lines: List[str] = [header, weekday_header]

    for week in cal.monthdays2calendar(year, month):
        # week is a list of (day, weekday) tuples
        formatted = [_format_day(day, wd) for day, wd in week]
        lines.append(" ".join(formatted))
    return "\n".join(lines)


def _run_cli() -> None:
    """CLI entry point: prints the current month."""
    now = datetime.now()
    print(render_month(now.year, now.month))


if __name__ == "__main__":
    _run_cli()
