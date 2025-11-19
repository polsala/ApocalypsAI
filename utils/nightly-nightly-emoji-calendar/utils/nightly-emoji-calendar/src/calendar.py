import sys
import calendar
from typing import List

# Mapping of weekday index (Monday=0) to emoji
WEEKDAY_EMOJIS: List[str] = ["🌞", "🌜", "🌟", "🌈", "🍀", "🎉", "🌙"]


def generate_emoji_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar with emojis.

    Each day is rendered as "<day><emoji>" where the emoji corresponds to the
    weekday of that day. Empty cells are omitted.
    """
    cal = calendar.monthcalendar(year, month)  # weeks start on Monday
    lines: List[str] = []
    for week in cal:
        cells: List[str] = []
        for idx, day in enumerate(week):
            if day == 0:
                cells.append("")
            else:
                cells.append(f"{day}{WEEKDAY_EMOJIS[idx]}")
        # Join cells with a single space; empty strings produce leading spaces
        line = " ".join(cells).rstrip()
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m utils.nightly-emoji-calendar.src.calendar <year> <month>")
        sys.exit(1)
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    print(generate_emoji_calendar(year, month))


if __name__ == "__main__":
    main()
