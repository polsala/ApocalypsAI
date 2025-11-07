"""emoji-calendar utility

Provides a single public function ``date_to_emoji`` that converts a date string
(`YYYY-MM-DD`) into a fun emoji representation.

The module is deliberately dependency‑free and works with Python 3.11+.
"""

import sys
from datetime import datetime
from typing import Dict

# Mapping of month number to a representative emoji
_MONTH_EMOJI: Dict[int, str] = {
    1: "❄️",   # January – snowflake
    2: "❤️",   # February – heart (Valentine)
    3: "🌱",   # March – sprout
    4: "🌸",   # April – cherry blossom
    5: "🌼",   # May – flower
    6: "☀️",   # June – sun
    7: "🏖️",  # July – beach
    8: "🍉",   # August – watermelon
    9: "🍂",   # September – fallen leaves
    10: "🎃",  # October – pumpkin
    11: "🦃",  # November – turkey
    12: "🎄",  # December – Christmas tree
}

# Mapping of digit to its emoji representation
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

def _day_to_emoji(day: int) -> str:
    """Convert a day number (1‑31) into a concatenated digit‑emoji string.

    Example: 31 -> "3️⃣1️⃣"
    """
    if not (1 <= day <= 31):
        raise ValueError("Day must be in 1..31")
    return "".join(_DIGIT_EMOJI[d] for d in f"{day:02d}")


def date_to_emoji(date_str: str) -> str:
    """Convert a ``YYYY-MM-DD`` date string to an emoji representation.

    The year component is ignored. The result is ``<month_emoji><day_emoji>``.

    Parameters
    ----------
    date_str: str
        Date in ISO format, e.g. ``"2023-10-31"``.

    Returns
    -------
    str
        Emoji string.

    Raises
    ------
    ValueError
        If the input is not a valid date or is out of the supported range.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception as exc:
        raise ValueError(f"Invalid date format: {date_str!r}") from exc

    month_emoji = _MONTH_EMOJI.get(dt.month)
    if month_emoji is None:
        raise ValueError(f"Unsupported month: {dt.month}")

    day_emoji = _day_to_emoji(dt.day)
    return f"{month_emoji}{day_emoji}"


def _cli() -> None:
    """Simple command‑line interface.

    Usage: ``python -m src.main <date>``
    """
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <YYYY-MM-DD>")
        sys.exit(1)
    try:
        print(date_to_emoji(sys.argv[1]))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
