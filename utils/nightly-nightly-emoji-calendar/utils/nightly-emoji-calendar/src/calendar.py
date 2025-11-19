"""
Emoji Calendar utility.

Provides `render_month(year, month)` which returns a string representation
of the month calendar with Saturdays replaced by 🌞 and Sundays by 🌜.
"""

import calendar
from typing import List


def _replace_weekends(week: List[int]) -> List[str]:
    """Replace weekend day numbers with emojis, keep zeros as empty strings.

    Parameters
    ----------
    week : List[int]
        A list of 7 integers representing a week as returned by
        ``calendar.monthdayscalendar`` where ``0`` denotes a day outside the
        month.
    """
    result: List[str] = []
    for i, day in enumerate(week):
        if day == 0:
            result.append("  ")
        elif i == 5:  # Saturday (0=Mon)
            result.append("🌞")
        elif i == 6:  # Sunday
            result.append("🌜")
        else:
            result.append(f"{day:2d}")
    return result


def render_month(year: int, month: int) -> str:
    """Return a formatted month calendar string with weekend emojis.

    Parameters
    ----------
    year : int
        Four‑digit year.
    month : int
        Month number 1‑12.

    Returns
    -------
    str
        Multiline string of the calendar.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday as first day
    month_name = calendar.month_name[month]
    header = f"{month_name} {year}".center(20).rstrip()
    week_header = "Mo Tu We Th Fr Sa Su"
    lines = [header, week_header]

    for week in cal.monthdayscalendar(year, month):
        replaced = _replace_weekends(week)
        line = " ".join(replaced).rstrip()
        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m utils.nightly-emoji-calendar.src.calendar <year> <month>")
        sys.exit(1)
    y, m = map(int, sys.argv[1:3])
    print(render_month(y, m))
