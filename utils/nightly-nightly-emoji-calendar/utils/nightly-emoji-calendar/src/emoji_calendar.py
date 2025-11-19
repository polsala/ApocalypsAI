"""
Emoji Calendar utility.
"""

from __future__ import annotations
import calendar
from typing import List

WEEKDAY_EMOJIS = {
    0: "🌞",  # Monday
    1: "🚀",  # Tuesday
    2: "📚",  # Wednesday
    3: "🍕",  # Thursday
    4: "🎉",  # Friday
    5: "🛌",  # Saturday
    6: "☕",  # Sunday
}


def generate_calendar(year: int, month: int) -> List[List[str]]:
    """
    Return a month calendar where each day is replaced by its weekday emoji.
    Empty days are represented by an empty string.
    """
    cal = calendar.monthcalendar(year, month)
    emoji_cal: List[List[str]] = []
    for week in cal:
        emoji_week = [
            WEEKDAY_EMOJIS[day_idx] if day != 0 else ""
            for day_idx, day in enumerate(week)
        ]
        emoji_cal.append(emoji_week)
    return emoji_cal


def format_calendar(emoji_cal: List[List[str]]) -> str:
    """
    Convert the emoji calendar into a pretty multiline string.
    """
    lines = []
    header = " ".join(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])
    lines.append(header)
    for week in emoji_cal:
        line = " ".join(day if day else "  " for day in week)
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Print an emoji calendar for a given month.")
    parser.add_argument("year", type=int, help="Year (e.g., 2023)")
    parser.add_argument("month", type=int, help="Month number 1-12")
    args = parser.parse_args()
    emoji_cal = generate_calendar(args.year, args.month)
    print(format_calendar(emoji_cal))


if __name__ == "__main__":
    main()
