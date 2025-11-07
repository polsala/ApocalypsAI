#!/usr/bin/env python3
"""emoji-calendar utility

Prints a date as a whimsical emoji string.
"""

import argparse
import datetime
import sys
from typing import List

# ---------------------------------------------------------------------------
# Emoji mappings (deterministic, no external resources)
# ---------------------------------------------------------------------------
WEEKDAY_EMOJIS: List[str] = [
    "🌞",  # Monday
    "🌜",  # Tuesday
    "🌟",  # Wednesday
    "🌈",  # Thursday
    "🎉",  # Friday
    "🛌",  # Saturday
    "☕",   # Sunday
]

MONTH_EMOJIS: List[str] = [
    "❄️",   # January
    "❤️",   # February
    "🌱",   # March
    "🌧️",   # April
    "🌸",   # May
    "☀️",   # June
    "🏖️",   # July
    "🍉",   # August
    "📚",   # September
    "🎃",   # October
    "🦃",   # November
    "🎄",   # December
]

DIGIT_EMOJIS = {
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
}

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def number_to_emoji(n: int) -> str:
    """Convert an integer (1‑31) to a concatenated sequence of digit emojis.

    Example: 31 -> "3️⃣1️⃣"
    """
    return "".join(DIGIT_EMOJIS[d] for d in str(n))


def get_emoji_date(date: datetime.date) -> str:
    """Return the emoji representation for *date*.

    Format: "<weekday_emoji> <month_emoji> <day_number_emoji>"
    """
    weekday_emoji = WEEKDAY_EMOJIS[date.weekday()]
    month_emoji = MONTH_EMOJIS[date.month - 1]
    day_emoji = number_to_emoji(date.day)
    return f"{weekday_emoji} {month_emoji} {day_emoji}"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a date as emojis.")
    parser.add_argument(
        "--date",
        type=str,
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {args.date}. Expected YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target_date = datetime.date.today()

    emoji_str = get_emoji_date(target_date)
    print(emoji_str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
