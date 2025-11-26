'''
Nightly Emoji Calendar utility.

Prints a calendar for a given month where each day is replaced by an emoji:
- 🌞 for weekends (Saturday, Sunday)
- 🌜 for weekdays (Monday‑Friday)

Run as a module:
    python -m src.calendar <year> <month>
'''

import argparse
import calendar
import sys
from typing import List

WEEKDAY_EMOJI = "🌜"
WEEKEND_EMOJI = "🌞"


def get_emoji_for_weekday(weekday: int) -> str:
    """
    Return the appropriate emoji for a given weekday.
    weekday: 0=Monday ... 6=Sunday
    """
    if weekday >= 5:  # Saturday (5) or Sunday (6)
        return WEEKEND_EMOJI
    return WEEKDAY_EMOJI


def generate_emoji_calendar(year: int, month: int) -> List[List[str]]:
    """
    Generate a calendar for the given month where each day is an emoji.
    Empty days are represented by an empty string.
    Returns a list of weeks, each week is a list of 7 strings.
    """
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    month_days = cal.monthdayscalendar(year, month)
    emoji_calendar: List[List[str]] = []
    for week in month_days:
        emoji_week = []
        for i, day in enumerate(week):
            if day == 0:
                emoji_week.append("")
            else:
                emoji_week.append(get_emoji_for_weekday(i))
        emoji_calendar.append(emoji_week)
    return emoji_calendar


def format_emoji_calendar(emoji_calendar: List[List[str]]) -> str:
    """
    Convert the emoji calendar into a pretty‑printed string.
    """
    lines = []
    header = "Mon Tue Wed Thu Fri Sat Sun"
    lines.append(header)
    for week in emoji_calendar:
        line = " ".join(day if day else "  " for day in week)
        lines.append(line)
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print an emoji calendar for a given month.")
    parser.add_argument("year", type=int, help="Year (e.g., 2023)")
    parser.add_argument("month", type=int, help="Month number (1‑12)")
    args = parser.parse_args(argv)

    try:
        emoji_cal = generate_emoji_calendar(args.year, args.month)
    except calendar.IllegalMonthError:
        print(f"Invalid month: {args.month}", file=sys.stderr)
        return 1

    print(f"{args.year}-{args.month:02d}")
    print(format_emoji_calendar(emoji_cal))
    return 0


if __name__ == "__main__":
    sys.exit(main())
