"""
Emoji Calendar utility.
"""

import sys
import calendar
from typing import List

WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
SAT_EMOJI = "🌞"
SUN_EMOJI = "🌜"


def _format_day(day: int, weekday: int) -> str:
    if day == 0:
        return "  "
    if weekday == 5:
        return SAT_EMOJI
    if weekday == 6:
        return SUN_EMOJI
    return f"{day:2d}"


def render_month(year: int, month: int) -> str:
    """Return a string representation of the month with weekend emojis."""
    cal = calendar.monthcalendar(year, month)
    lines: List[str] = [" ".join(WEEKDAYS)]
    for week in cal:
        formatted = [_format_day(day, idx) for idx, day in enumerate(week)]
        lines.append(" ".join(formatted).rstrip())
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m nightly_emoji_calendar.src.calendar <year> <month>")
        return 1
    year, month = map(int, argv)
    print(render_month(year, month))
    return 0


if __name__ == "__main__":
    sys.exit(main())
