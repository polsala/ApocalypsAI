import sys
import calendar
from typing import Dict, Tuple

# Simple holiday mapping: (month, day) -> emoji
HOLIDAYS: Dict[Tuple[int, int], str] = {
    (1, 1): "🎉",   # New Year's Day
    (12, 25): "🎄", # Christmas
}

WEEKEND_EMOJIS = {
    5: "🛸",  # Saturday
    6: "☀️",  # Sunday
}

def _format_day(day: int, weekday: int, month: int) -> str:
    """Return a string representation of a calendar day with emojis.

    * ``day`` – numeric day of month (0 for padding)
    * ``weekday`` – 0=Mon … 6=Sun
    * ``month`` – month number (used for holiday lookup)
    """
    if day == 0:
        return "  "
    base = f"{day:2d}"
    # Holiday takes precedence over weekend emoji
    if (month, day) in HOLIDAYS:
        return f"{base}{HOLIDAYS[(month, day)]}"
    if weekday in WEEKEND_EMOJIS:
        return f"{base}{WEEKEND_EMOJIS[weekday]}"
    return base

def generate_calendar(year: int, month: int) -> str:
    """Generate a month calendar string with emojis.

    The layout mirrors ``calendar.monthcalendar`` where weeks start on Monday.
    Each day is padded to two characters; emojis are appended directly after the number.
    """
    cal = calendar.monthcalendar(year, month)
    lines = []
    for week in cal:
        formatted = [
            _format_day(day, weekday, month)
            for weekday, day in enumerate(week)
        ]
        lines.append(" ".join(formatted))
    return "\n".join(lines)

def _cli() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m utils.emoji-calendar.src.emoji_calendar <year> <month>")
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
    print(generate_calendar(year, month))

if __name__ == "__main__":
    _cli()
