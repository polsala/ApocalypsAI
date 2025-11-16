#!/usr/bin/env python3
"""
emoji-calendar: Print a month calendar with weekday emojis.
"""

import argparse
import calendar
import datetime
from typing import List

# Mapping Monday=0 … Sunday=6 to emojis
WEEKDAY_EMOJI = {
    0: "🌞",  # Monday
    1: "🚀",  # Tuesday
    2: "🌱",  # Wednesday
    3: "📚",  # Thursday
    4: "🎉",  # Friday
    5: "🛌",  # Saturday
    6: "☕",  # Sunday
}


def day_with_emoji(year: int, month: int, day: int) -> str:
    """Return a string like ' 1🌱' for the given day.

    Args:
        year: Four‑digit year.
        month: Month number (1‑12).
        day: Day of month.
    """
    weekday = datetime.date(year, month, day).weekday()
    emoji = WEEKDAY_EMOJI[weekday]
    return f"{day:2d}{emoji}"


def generate_calendar(year: int, month: int) -> str:
    """Return a multiline string of the month calendar with emojis.

    The layout mimics the classic `cal` output but appends an emoji to each
    day number. Empty slots are padded with three spaces.
    """
    cal = calendar.monthcalendar(year, month)
    lines: List[str] = []
    header = f"{calendar.month_name[month]} {year}"
    lines.append(header.center(20))
    lines.append("Mo Tu We Th Fr Sa Su")
    for week in cal:
        week_str: List[str] = []
        for day in week:
            if day == 0:
                week_str.append("   ")
            else:
                week_str.append(day_with_emoji(year, month, day))
        lines.append(" ".join(week_str))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a month calendar with emojis.")
    parser.add_argument("month", type=int, help="Month as number (1‑12)")
    parser.add_argument("year", type=int, help="Year as four‑digit number")
    args = parser.parse_args()
    print(generate_calendar(args.year, args.month))


if __name__ == "__main__":
    main()
