"""emoji_calendar.py

A tiny, dependency‑free utility that maps dates to whimsical emojis and can render a month‑view calendar using those emojis.

Public API:
    - get_emoji_for_date(date_obj: datetime.date) -> str
    - month_calendar(year: int, month: int) -> List[List[Tuple[int, str]]]

CLI usage:
    python -m utils.nightly_emoji_calendar.src.emoji_calendar <YYYY-MM-DD>
    python -m utils.nightly_emoji_calendar.src.emoji_calendar --month <YEAR> <MONTH>
"""

from __future__ import annotations

import argparse
import calendar
import datetime
from typing import List, Tuple

# Mapping of weekday (0=Monday) to emoji
WEEKDAY_EMOJI = {
    0: "🌞",  # Monday – sunrise
    1: "🚀",  # Tuesday – launch day
    2: "🐪",  # Wednesday – hump day
    3: "🦉",  # Thursday – wise owl
    4: "🎉",  # Friday – party
    5: "🏖️",  # Saturday – beach
    6: "🛌",  # Sunday – rest
}

# Optional special‑date overrides (e.g., holidays). Extend as desired.
SPECIAL_DATE_EMOJI = {
    (12, 25): "🎄",  # Christmas
    (1, 1): "🥂",   # New Year's Day
}


def get_emoji_for_date(date_obj: datetime.date) -> str:
    """Return an emoji for *date_obj*.

    The function first checks *SPECIAL_DATE_EMOJI* (month, day) overrides.
    If none match, it falls back to the weekday mapping.
    """
    # Check special dates
    special = SPECIAL_DATE_EMOJI.get((date_obj.month, date_obj.day))
    if special:
        return special
    # Default to weekday emoji
    return WEEKDAY_EMOJI[date_obj.weekday()]


def month_calendar(year: int, month: int) -> List[List[Tuple[int, str]]]:
    """Return a calendar for *year*/*month* where each day is a tuple ``(day, emoji)``.

    Empty slots (padding days) are represented as ``(0, "")``.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday as first day
    weeks: List[List[Tuple[int, str]]] = []
    for week in cal.monthdayscalendar(year, month):
        week_repr: List[Tuple[int, str]] = []
        for day in week:
            if day == 0:
                week_repr.append((0, ""))
            else:
                date_obj = datetime.date(year, month, day)
                week_repr.append((day, get_emoji_for_date(date_obj)))
        weeks.append(week_repr)
    return weeks


def _print_month(year: int, month: int) -> None:
    """Pretty‑print the emoji calendar for *year*/*month* to stdout."""
    weeks = month_calendar(year, month)
    header = calendar.month_name[month] + f" {year}".rjust(20 - len(calendar.month_name[month]))
    print(header)
    print("Mo Tu We Th Fr Sa Su")
    for week in weeks:
        line = []
        for day, emoji in week:
            if day == 0:
                line.append("  ")
            else:
                # Show day number followed by emoji (emoji may be multi‑char, keep spacing simple)
                line.append(f"{day:2d}{emoji}")
        print(" ".join(line))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emoji Calendar utility")
    parser.add_argument("date", nargs="?", help="Date in YYYY-MM-DD format (defaults to today)")
    parser.add_argument(
        "--month",
        nargs=2,
        metavar=("YEAR", "MONTH"),
        type=int,
        help="Render an entire month calendar (year month)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.month:
        year, month = args.month
        _print_month(year, month)
        return
    # Single date mode
    if args.date:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        date_obj = datetime.date.today()
    emoji = get_emoji_for_date(date_obj)
    print(f"{date_obj.isoformat()} → {emoji}")


if __name__ == "__main__":
    main()
