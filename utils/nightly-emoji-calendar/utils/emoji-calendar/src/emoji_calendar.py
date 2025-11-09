import sys
import calendar


def generate_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar.

    Saturdays are replaced with the 🎉 emoji and Sundays with 🌞.
    Empty days are rendered as two spaces.
    """
    cal = calendar.monthcalendar(year, month)
    lines = []
    header = f"{calendar.month_name[month]} {year}"
    lines.append(header.center(20))
    lines.append("Mo Tu We Th Fr Sa Su")
    for week in cal:
        line_parts = []
        for i, day in enumerate(week):
            if day == 0:
                line_parts.append("  ")
            else:
                if i == 5:  # Saturday
                    line_parts.append("🎉")
                elif i == 6:  # Sunday
                    line_parts.append("🌞")
                else:
                    line_parts.append(f"{day:2d}")
        lines.append(" ".join(line_parts))
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m src.emoji_calendar <year> <month>")
        sys.exit(1)
    y, m = map(int, sys.argv[1:3])
    print(generate_calendar(y, m))
