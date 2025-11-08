"""emoji_date.py

Utility to transform an ISO date (YYYY‑MM‑DD) into a whimsical emoji string.

Public API:
    format_date(date_str: str) -> str
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Dict

# Mapping of digit characters to their keycap emoji equivalents
DIGIT_EMOJI_MAP: Dict[str, str] = {
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

# Mapping of month numbers (01‑12) to seasonal plant emojis
MONTH_EMOJI_MAP: Dict[str, str] = {
    "01": "🌸",
    "02": "🌼",
    "03": "🌻",
    "04": "🌹",
    "05": "🌷",
    "06": "🌺",
    "07": "🌱",
    "08": "🌲",
    "09": "🌳",
    "10": "🌴",
    "11": "🌵",
    "12": "🌾",
}


def _replace_digits(s: str) -> str:
    """Replace each digit in *s* with its keycap emoji.

    Args:
        s: Input string containing digits.
    Returns:
        String with digits replaced.
    """
    return "".join(DIGIT_EMOJI_MAP.get(ch, ch) for ch in s)


def format_date(date_str: str) -> str:
    """Convert an ISO date (YYYY‑MM‑DD) to an emoji representation.

    The function validates the input using ``datetime.strptime`` to ensure the
    date is real (e.g., rejects ``2023-02-30``). It then replaces the month part
    with a plant emoji and each remaining digit with its keycap emoji.

    Args:
        date_str: Date string in ``YYYY-MM-DD`` format.
    Returns:
        Emoji‑rich string.
    Raises:
        ValueError: If *date_str* is not a valid ISO date.
    """
    # Validate and split the date
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"Invalid ISO date '{date_str}': {exc}") from None

    year = f"{dt.year:04d}"
    month = f"{dt.month:02d}"
    day = f"{dt.day:02d}"

    # Replace month with its emoji
    month_emoji = MONTH_EMOJI_MAP[month]

    # Replace digits in year and day
    year_emoji = _replace_digits(year)
    day_emoji = _replace_digits(day)

    # Assemble final string: <year_emoji><month_emoji>-<day_emoji>
    return f"{year_emoji}{month_emoji}-{day_emoji}"


def _cli() -> None:
    """Simple command‑line interface.

    Usage:
        python -m utils.emoji-date-formatter.src.emoji_date <date>
    """
    if len(sys.argv) != 2:
        print("Usage: python -m utils.emoji-date-formatter.src.emoji_date <YYYY-MM-DD>")
        sys.exit(1)
    input_date = sys.argv[1]
    try:
        print(format_date(input_date))
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
