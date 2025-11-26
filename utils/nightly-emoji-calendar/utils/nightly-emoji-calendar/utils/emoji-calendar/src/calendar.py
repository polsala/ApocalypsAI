"""
emoji_calendar: generate a month calendar with emojis for weekdays.
"""

import sys
import calendar
from typing import List

WEEKDAY_EMOJIS = {
    0: "🌞",  # Monday
    1: "🚀",  # Tuesday
    2: "🌱",  # Wednesday
    3: "📚",  # Thursday
    4: "🎉",  # Friday
    5: "🛌",  # Saturday
    6: "☕",  # Sunday
}


def generate_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar with emojis.

    The layout mirrors ``calendar.monthcalendar`` but replaces the weekday
    header with emojis. Days that belong to adjacent months are rendered as
    blanks.
    """
    # ``calendar.Calendar`` uses Monday=0 when ``firstweekday`` is 0.
    cal = calendar.Calendar(firstweekday=0)
    month_name = calendar.month_name[month]
    header = f"{month_name} {year}".center(20)
    # Emoji header for Monday‑Sunday order.
    weekday_header = " ".join(WEEKDAY_EMOJIS[i] for i in range(7))
    lines = [header, weekday_header]
    for week in cal.monthdayscalendar(year, month):
        line = " ".join(f"{day:2}" if day != 0 else "  " for day in week)
        lines.append(line)
    return "\n".join(lines)


def main(argv: List[str] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m emoji_calendar <year> <month>")
        return 1
    try:
        year = int(argv[0])
        month = int(argv[1])
        if not (1 <= month <= 12):
            raise ValueError
    except ValueError:
        print("Year and month must be integers, month between 1 and 12.")
        return 1
    print(generate_calendar(year, month))
    return 0


if __name__ == "__main__":
    sys.exit(main())
