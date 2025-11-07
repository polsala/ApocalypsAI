import sys
import calendar
from typing import Dict, Tuple

# Mapping of (month, day) -> emoji for a few common holidays
HOLIDAYS: Dict[Tuple[int, int], str] = {
    (1, 1): "🎉",   # New Year's Day
    (11, 28): "🦃",  # Thanksgiving (fixed date for demo purposes)
    (12, 25): "🎄",  # Christmas
}

WEEKEND_EMOJIS = {5: "🌞", 6: "🌜"}  # 5=Saturday, 6=Sunday (Monday=0)


def _day_repr(year: int, month: int, day: int, weekday: int) -> str:
    """Return the string representation for a given day.

    * Holiday → holiday emoji
    * Weekend → weekend emoji
    * Otherwise → right‑aligned day number
    """
    if (month, day) in HOLIDAYS:
        return HOLIDAYS[(month, day)]
    if weekday in WEEKEND_EMOJIS:
        return WEEKEND_EMOJIS[weekday]
    return f"{day:2d}"


def generate_month(year: int, month: int) -> str:
    """Generate an emoji‑enhanced calendar for *year*/*month*.

    Returns a multi‑line string ready for printing.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday
    header = "Mo Tu We Th Fr Sa Su"
    weeks = []
    for week in cal.monthdays2calendar(year, month):
        week_str = []
        for day, weekday in week:
            if day == 0:
                week_str.append("  ")
            else:
                week_str.append(_day_repr(year, month, day, weekday))
        weeks.append(" ".join(week_str))
    return "\n".join([header] + weeks)


def _cli() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m utils.emoji-calendar.src.main <year> <month>")
        sys.exit(1)
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
    except ValueError:
        print("Year and month must be integers.")
        sys.exit(1)
    if not (1 <= month <= 12):
        print("Month must be between 1 and 12.")
        sys.exit(1)
    print(generate_month(year, month))


if __name__ == "__main__":
    _cli()
