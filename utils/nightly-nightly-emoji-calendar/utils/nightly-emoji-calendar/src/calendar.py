#!/usr/bin/env python3
"""
emoji_calendar.py: Generate a markdown calendar with weekday emojis.
"""

import argparse
import calendar
import datetime
from typing import List

WEEKDAY_EMOJIS = {
    0: "🌞",  # Monday
    1: "🚀",  # Tuesday
    2: "🌱",  # Wednesday
    3: "🔥",  # Thursday
    4: "🎉",  # Friday
    5: "🛌",  # Saturday
    6: "☕",  # Sunday
}


def generate_emoji_calendar(year: int, month: int) -> str:
    """Return a markdown table representing the month with emojis.

    Args:
        year: Four‑digit year.
        month: Month number 1‑12.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday = 0
    weeks = cal.monthdayscalendar(year, month)

    header = "| Mon | Tue | Wed | Thu | Fri | Sat | Sun |\n"
    separator = "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
    rows = [header, separator]

    for week in weeks:
        cells: List[str] = []
        for i, day in enumerate(week):
            if day == 0:
                cells.append(" ")
            else:
                emoji = WEEKDAY_EMOJIS[i]
                cells.append(f"{emoji} {day}")
        rows.append("| " + " | ".join(cells) + " |\n")
    return "".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print an emoji calendar.")
    parser.add_argument("--year", type=int, help="Year (e.g., 2023)")
    parser.add_argument("--month", type=int, help="Month 1‑12")
    args = parser.parse_args()

    today = datetime.date.today()
    year = args.year or today.year
    month = args.month or today.month

    print(generate_emoji_calendar(year, month))


if __name__ == "__main__":
    main()
