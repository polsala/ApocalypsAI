"""emoji_date_formatter/src/formatter.py

Utility to convert an ISO date (YYYY‑MM‑DD) into a whimsical emoji string.

Public API
----------
- ``format_date(date_str: str) -> str``: Returns the emoji representation.
- ``main()``: CLI entry point.
"""

from __future__ import annotations

import sys
from typing import Dict

# Mapping of digit characters to their emoji equivalents.
_DIGIT_EMOJI: Dict[str, str] = {
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

# Mapping of month numbers (01‑12) to seasonal emojis.
_MONTH_EMOJI: Dict[str, str] = {
    "01": "🌱",  # January – new growth
    "02": "❄️",  # February – winter
    "03": "🌸",  # March – spring bloom
    "04": "🌷",  # April – flowers
    "05": "🌼",  # May – sunshine
    "06": "☀️",  # June – summer
    "07": "🏖️",  # July – beach
    "08": "🌻",  # August – sunflowers
    "09": "🍂",  # September – fall
    "10": "🎃",  # October – Halloween
    "11": "🦃",  # November – turkey
    "12": "🎄",  # December – holidays
}


def _replace_digits(s: str) -> str:
    """Replace each character in *s* with its digit emoji.

    Non‑digit characters are left untouched (though the function is only
    called on strings that consist solely of digits).
    """
    return "".join(_DIGIT_EMOJI.get(ch, ch) for ch in s)


def format_date(date_str: str) -> str:
    """Convert ``YYYY‑MM‑DD`` into an emoji string.

    Example
    -------
    >>> format_date("2025-12-31")
    '🎄 2️⃣2️⃣❄️'
    """
    # Basic validation – keep it lightweight; raise ValueError on malformed input.
    if len(date_str) != 10 or date_str[4] != "-" or date_str[7] != "-":
        raise ValueError(
            f"Invalid date format: '{date_str}'. Expected 'YYYY-MM-DD'."
        )

    year, month, day = date_str.split("-")
    # Convert year and day digits to emojis.
    year_emoji = _replace_digits(year)
    day_emoji = _replace_digits(day)
    # Map month to its seasonal emoji; fallback to digit replacement.
    month_emoji = _MONTH_EMOJI.get(month, _replace_digits(month))
    # Join parts with a space for readability.
    return f"{month_emoji} {year_emoji}{day_emoji}"


def _cli() -> None:
    """Simple command‑line interface.

    Usage: ``python -m utils.emoji_date_formatter.src.formatter <date>``
    """
    if len(sys.argv) != 2:
        print("Usage: python -m utils.emoji_date_formatter.src.formatter <YYYY-MM-DD>")
        sys.exit(1)
    try:
        result = format_date(sys.argv[1])
        print(result)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
