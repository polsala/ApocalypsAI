from datetime import datetime
from typing import Dict

_DIGIT_EMOJI = {
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

_MONTH_EMOJI: Dict[int, str] = {
    1: "🎉",   # January
    2: "❤️",   # February
    3: "🍀",   # March
    4: "🌷",   # April
    5: "🌼",   # May
    6: "🌞",   # June
    7: "🎆",   # July
    8: "🏖️",  # August
    9: "🍂",   # September
    10: "🎃",  # October
    11: "🍁",  # November
    12: "🎄",  # December
}


def _digits_to_emoji(s: str) -> str:
    """Convert each digit in *s* to its keycap emoji."""
    return "".join(_DIGIT_EMOJI[d] for d in s)


def date_to_emoji(date_str: str) -> str:
    """
    Convert an ISO‑format date (YYYY‑MM‑DD) to an emoji representation.

    Example
    -------
    >>> date_to_emoji("2023-10-31")
    '2️⃣0️⃣2️⃣3️⃣ 🎃 3️⃣1️⃣'
    """
    # Mock rationale: parsing is deterministic, no external calls.
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    year_emoji = _digits_to_emoji(str(dt.year))
    month_emoji = _MONTH_EMOJI[dt.month]
    day_emoji = _digits_to_emoji(f"{dt.day:02d}")
    return f"{year_emoji} {month_emoji} {day_emoji}"
