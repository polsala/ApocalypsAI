import argparse
import calendar
import datetime
from typing import List


def _parse_holidays(holidays_str: str) -> List[datetime.date]:
    """Parse a comma‑separated list of YYYY‑MM‑DD strings into date objects.
    # Mock rationale: simple split and datetime conversion, no external calls.
    """
    if not holidays_str:
        return []
    dates = []
    for part in holidays_str.split(','):
        part = part.strip()
        if part:
            try:
                dates.append(datetime.datetime.strptime(part, "%Y-%m-%d").date())
            except ValueError:
                raise argparse.ArgumentTypeError(f"Invalid holiday date: {part}")
    return dates


def generate_calendar(year: int, month: int, holidays: List[datetime.date] = None) -> str:
    """Return a string representation of the month calendar with emojis.
    Weekends are decorated: Saturday → 🌞, Sunday → 🌜.
    Holidays (if any) are marked with 🎉 before the day number.
    """
    holidays = holidays or []
    cal = calendar.Calendar(firstweekday=0)  # Monday=0
    month_name = calendar.month_name[month]
    header = f"      📅 {month_name} {year}\n"
    week_header = "Mo Tu We Th Fr Sa Su\n"
    lines = [header, week_header]
    for week in cal.monthdayscalendar(year, month):
        line_parts = []
        for i, day in enumerate(week):
            if day == 0:
                line_parts.append("  ")
                continue
            day_date = datetime.date(year, month, day)
            emoji = ""
            if day_date in holidays:
                emoji = "🎉"
            elif i == 5:  # Saturday (0=Mon)
                emoji = "🌞"
            elif i == 6:  # Sunday
                emoji = "🌜"
            # Pad day number to width 2
            day_str = f"{day:2d}"
            line_parts.append(f"{emoji}{day_str}" if emoji else f" {day_str}")
        lines.append(" ".join(line_parts).rstrip())
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print the current month calendar with emojis.")
    parser.add_argument(
        "--holidays",
        type=str,
        default="",
        help="Comma‑separated list of holiday dates (YYYY-MM-DD)."
    )
    args = parser.parse_args()
    today = datetime.date.today()
    holidays = _parse_holidays(args.holidays)
    calendar_str = generate_calendar(today.year, today.month, holidays)
    print(calendar_str)


if __name__ == "__main__":
    main()
