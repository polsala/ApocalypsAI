"""Emoji Calendar utility.

Provides a function to map a date to a whimsical emoji.
"""

from __future__ import annotations

import datetime
from typing import Dict

# Mapping of weekday (0=Monday) to emoji
WEEKDAY_EMOJIS: Dict[int, str] = {
    0: "📅",  # Monday
    1: "🗓️",  # Tuesday
    2: "📆",  # Wednesday
    3: "🗒️",  # Thursday
    4: "📖",  # Friday
    5: "🛌",  # Saturday
    6: "☀️",  # Sunday
}

# Simple holiday mapping (month, day) -> emoji
HOLIDAY_EMOJIS: Dict[tuple[int, int], str] = {
    (1, 1): "🎉",   # New Year's Day
    (12, 25): "🎄", # Christmas
    (7, 4): "🧨",   # Independence Day (US)
    (10, 31): "🎃", # Halloween
}


def get_emoji_for_date(dt: datetime.date) -> str:
    """Return an emoji representing the given date.

    - If the date matches a known holiday, the holiday emoji is returned.
    - Otherwise the weekday emoji is returned.
    """
    # Holiday check
    holiday_key = (dt.month, dt.day)
    if holiday_key in HOLIDAY_EMOJIS:
        return HOLIDAY_EMOJIS[holiday_key]

    # Weekday fallback
    return WEEKDAY_EMOJIS[dt.weekday()]


def main() -> None:
    """CLI entry point.

    Expects a single argument in ISO format (YYYY-MM-DD). If omitted,
    uses today's date.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Print an emoji for a date.")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in ISO format (YYYY-MM-DD). Defaults to today.",
    )
    args = parser.parse_args()

    if args.date:
        try:
            target_date = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        target_date = datetime.date.today()

    emoji = get_emoji_for_date(target_date)
    print(emoji)


if __name__ == "__main__":
    main()
