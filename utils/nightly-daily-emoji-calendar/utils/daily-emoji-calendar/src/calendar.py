import argparse
import calendar
from typing import List


def generate_calendar(year: int, month: int) -> str:
    """Return a string representation of the month calendar.

    Weekdays are shown as right‑aligned two‑digit numbers.
    Saturday is replaced with the 🌞 emoji and Sunday with 🌜.
    Empty days (padding) are rendered as two spaces.
    """
    cal = calendar.Calendar(firstweekday=0)  # Monday = 0
    weeks: List[List[int]] = cal.monthdayscalendar(year, month)
    lines: List[str] = []
    for week in weeks:
        rendered: List[str] = []
        for idx, day in enumerate(week):
            if day == 0:
                rendered.append("  ")
            elif idx == 5:  # Saturday
                rendered.append("🌞")
            elif idx == 6:  # Sunday
                rendered.append("🌜")
            else:
                rendered.append(f"{day:2d}")
        lines.append(" ".join(rendered))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a month calendar with weekend emojis.")
    parser.add_argument("year", type=int, help="Year (e.g., 2023)")
    parser.add_argument("month", type=int, help="Month number (1‑12)")
    args = parser.parse_args()
    output = generate_calendar(args.year, args.month)
    print(output)


if __name__ == "__main__":
    main()
