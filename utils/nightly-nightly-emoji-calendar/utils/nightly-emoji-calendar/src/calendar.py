#!/usr/bin/env python3
"""
Emoji Calendar utility.

Prints a month calendar where each day is replaced by an emoji:
- Weekdays → 📅
- Weekends → 🌞
"""

import sys
import calendar
from datetime import datetime

WEEKDAY_EMOJI = "📅"
WEEKEND_EMOJI = "🌞"


def generate_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar with emojis.

    The layout mirrors ``calendar.Calendar`` with Monday as the first column.
    Empty cells (days belonging to adjacent months) are rendered as two spaces
    to keep column alignment.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday = 0
    weeks = cal.monthdayscalendar(year, month)
    lines = []
    header = "Mo Tu We Th Fr Sa Su"
    lines.append(header)
    for week in weeks:
        line_parts = []
        for day in week:
            if day == 0:
                line_parts.append("  ")
            else:
                weekday = datetime(year, month, day).weekday()
                emoji = WEEKEND_EMOJI if weekday >= 5 else WEEKDAY_EMOJI
                line_parts.append(emoji)
        lines.append(" ".join(line_parts))
    return "\n".join(lines)


def _main() -> None:
    now = datetime.now()
    year = now.year
    month = now.month
    if len(sys.argv) == 3:
        try:
            year = int(sys.argv[1])
            month = int(sys.argv[2])
        except ValueError:
            print("Usage: python calendar.py [year month]")
            sys.exit(1)
    print(generate_calendar(year, month))


if __name__ == "__main__":
    _main()
