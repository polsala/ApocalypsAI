import calendar
import datetime
from typing import List, Optional

# Emoji constants
WEEKDAY_EMOJI = "🟦"
WEEKEND_EMOJI = "🟧"
HOLIDAY_EMOJI = "🎉"


def _is_holiday(day: datetime.date, holidays: Optional[List[datetime.date]]) -> bool:
    """Return True if *day* is in the *holidays* list.

    # Mock rationale: simple containment check – no external look‑ups.
    """
    if not holidays:
        return False
    return day in holidays


def generate_calendar(year: int, month: int, holidays: Optional[List[datetime.date]] = None) -> str:
    """Generate a month calendar where each day is suffixed with an emoji.

    Parameters
    ----------
    year: int
        Four‑digit year.
    month: int
        Month number (1‑12).
    holidays: list[datetime.date] | None
        Optional list of dates that should be marked as holidays.

    Returns
    -------
    str
        Multiline string representing the calendar.
    """
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    weeks = cal.monthdayscalendar(year, month)
    lines = []
    header = "Mo Tu We Th Fr Sa Su"
    lines.append(header)
    for week in weeks:
        line_parts = []
        for day in week:
            if day == 0:
                # Day outside the month
                line_parts.append("   ")
                continue
            day_date = datetime.date(year, month, day)
            weekday = day_date.weekday()  # Monday=0, Sunday=6
            if _is_holiday(day_date, holidays):
                emoji = HOLIDAY_EMOJI
            elif weekday >= 5:  # Saturday or Sunday
                emoji = WEEKEND_EMOJI
            else:
                emoji = WEEKDAY_EMOJI
            line_parts.append(f"{day:2d}{emoji}")
        lines.append(" ".join(line_parts))
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Print an emoji‑decorated month calendar.")
    parser.add_argument("--year", type=int, required=True, help="Year (e.g., 2023)")
    parser.add_argument("--month", type=int, required=True, help="Month number (1‑12)")
    parser.add_argument(
        "--holidays",
        type=str,
        default="",
        help="Comma‑separated list of holiday dates in YYYY‑MM‑DD format",
    )
    args = parser.parse_args()
    holiday_dates = []
    if args.holidays:
        for part in args.holidays.split(","):
            try:
                y, m, d = map(int, part.split("-"))
                holiday_dates.append(datetime.date(y, m, d))
            except ValueError:
                raise SystemExit(f"Invalid holiday format: {part}")
    print(generate_calendar(args.year, args.month, holiday_dates))
