import sys
import calendar
from datetime import datetime
from typing import Dict, List


def _mock_holiday_emoji(date_str: str) -> str:
    """Return a holiday emoji for a given ISO date string.

    This is a deterministic mock used both by the CLI and the test suite.
    # Mock rationale: provide a predictable set of holidays without external data.
    """
    mock_holidays = {
        "2025-01-01": "🎉",  # New Year's Day
        "2025-12-25": "🎄",  # Christmas
        "2025-11-28": "🦃",  # Thanksgiving (US, mocked date)
    }
    return mock_holidays.get(date_str, "")


def _emoji_for_day(year: int, month: int, day: int) -> str:
    """Select an emoji for a specific calendar day.

    Weekdays → 🌞, Weekends → 🌙, Mock holidays override.
    """
    date_str = f"{year:04d}-{month:02d}-{day:02d}"
    holiday = _mock_holiday_emoji(date_str)
    if holiday:
        return holiday
    weekday = datetime(year, month, day).weekday()  # Monday=0
    return "🌞" if weekday < 5 else "🌙"


def generate_month_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar with emojis.

    The layout mimics `calendar.month` but replaces each day number with its emoji.
    Empty slots are padded with two spaces for alignment.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday start
    weeks: List[List[str]] = []
    for week in cal.monthdayscalendar(year, month):
        week_repr: List[str] = []
        for day in week:
            if day == 0:
                week_repr.append("  ")
            else:
                week_repr.append(_emoji_for_day(year, month, day))
        weeks.append(week_repr)

    header = calendar.month_name[month] + f" {year}".rjust(20 - len(calendar.month_name[month]))
    weekdays_header = "Mo Tu We Th Fr Sa Su"
    lines = [header, weekdays_header]
    for week in weeks:
        line = " ".join(week)
        lines.append(line)
    return "\n".join(lines)


def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        try:
            year_month = argv[0]
            year, month = map(int, year_month.split("-"))
        except Exception:
            print("Usage: python -m src.emoji_calendar [YYYY-MM]", file=sys.stderr)
            sys.exit(1)
    else:
        today = datetime.today()
        year, month = today.year, today.month
    print(generate_month_calendar(year, month))


if __name__ == "__main__":
    main()
