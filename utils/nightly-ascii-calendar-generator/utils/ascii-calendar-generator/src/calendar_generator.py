'''ASCII Calendar Generator utility.'''

import sys
import calendar
import datetime
from typing import Optional


def generate_calendar(month: int, year: int, highlight_today: bool = False) -> str:
    """
    Return an ASCII calendar for the given month and year.

    If ``highlight_today`` is True and the supplied month/year matches the
    current date, the current day is wrapped in ``*`` characters.
    """
    cal = calendar.TextCalendar(firstweekday=0)  # Monday as first day
    cal_str = cal.formatmonth(year, month)

    if highlight_today:
        today = datetime.date.today()
        if today.year == year and today.month == month:
            # The calendar module pads single‑digit days with a leading space.
            day_str = f"{today.day:2d}"
            highlighted = f"*{day_str}*"
            cal_str = cal_str.replace(day_str, highlighted)
    return cal_str


def _parse_args(args: Optional[list] = None) -> tuple[int, int, bool]:
    """Parse command‑line arguments.

    Expected usage: ``python -m src.calendar_generator <year> <month> [--highlight]``.
    """
    if args is None:
        args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit(
            "Usage: python -m src.calendar_generator <year> <month> [--highlight]"
        )
    year = int(args[0])
    month = int(args[1])
    highlight = "--highlight" in args
    return month, year, highlight


def main() -> None:
    month, year, highlight = _parse_args()
    print(generate_calendar(month, year, highlight))


if __name__ == "__main__":
    main()
