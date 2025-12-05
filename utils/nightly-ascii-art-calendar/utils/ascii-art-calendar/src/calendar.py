"""
ascii-art-calendar utility.

Provides `render_calendar(year: int, month: int) -> str` which returns a string
representation of the month calendar with weekend emojis.
"""

import sys
import calendar
from typing import List


def _day_str(day: int, weekday: int) -> str:
    """Return day string with emoji for weekends.

    Empty days (0) are rendered as three spaces.
    Saturdays get a ☀, Sundays get a 🌙.
    """
    if day == 0:
        return "   "
    if weekday == calendar.SATURDAY:
        return f"{day:2}☀"
    if weekday == calendar.SUNDAY:
        return f"{day:2}🌙"
    return f"{day:3}"


def render_calendar(year: int, month: int) -> str:
    """Render calendar for given year/month with whimsical weekend icons.

    The calendar starts on Monday to keep alignment simple.
    """
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    weeks = cal.monthdays2calendar(year, month)  # [(day, weekday), ...]
    header = f"{calendar.month_name[month]} {year}".center(20)
    week_header = "Mo Tu We Th Fr Sa Su"
    lines = [header, week_header]
    for week in weeks:
        line = " ".join(_day_str(day, wd) for day, wd in week)
        lines.append(line)
    return "\n".join(lines)


def main(argv: List[str] = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m src.calendar <year> <month>", file=sys.stderr)
        return 1
    try:
        year = int(argv[0])
        month = int(argv[1])
        if not (1 <= month <= 12):
            raise ValueError
    except ValueError:
        print("Year and month must be integers, month 1-12.", file=sys.stderr)
        return 1
    print(render_calendar(year, month))
    return 0


if __name__ == "__main__":
    sys.exit(main())
