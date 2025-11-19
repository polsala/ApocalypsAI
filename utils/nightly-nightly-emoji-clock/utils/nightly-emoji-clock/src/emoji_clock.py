"""
emoji_clock utility

Provides a function to represent the current (or supplied) time using emojis.
"""

import datetime
from typing import Optional

# Mapping of hour (1‑12) to the corresponding clock‑face emoji.
_CLOCK_EMOJIS = {
    1: "🕐",
    2: "🕑",
    3: "🕒",
    4: "🕓",
    5: "🕔",
    6: "🕕",
    7: "🕖",
    8: "🕗",
    9: "🕘",
    10: "🕙",
    11: "🕚",
    12: "🕛",
}

# Mapping of decimal digit characters to their emoji equivalents.
_DIGIT_EMOJIS = {
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


def _hour_to_emoji(hour: int) -> str:
    """Convert a 24‑hour integer to the appropriate clock‑face emoji.

    Args:
        hour: Hour in 0‑23 range.
    Returns:
        A single clock‑face emoji string.
    """
    hour12 = hour % 12
    hour12 = 12 if hour12 == 0 else hour12
    return _CLOCK_EMOJIS[hour12]


def _minutes_to_emoji(minute: int) -> str:
    """Convert a minute value (0‑59) to two digit emojis.

    Args:
        minute: Minute component.
    Returns:
        Two concatenated digit emojis representing the minute.
    """
    tens, ones = divmod(minute, 10)
    return _DIGIT_EMOJIS[str(tens)] + _DIGIT_EMOJIS[str(ones)]


def get_emoji_time(dt: Optional[datetime.datetime] = None) -> str:
    """Return the time formatted as emojis.

    If *dt* is ``None`` the current local time is used.
    """
    now = dt or datetime.datetime.now()
    hour_emoji = _hour_to_emoji(now.hour)
    minute_emoji = _minutes_to_emoji(now.minute)
    return f"{hour_emoji} {minute_emoji}"


def main() -> None:
    """CLI entry‑point that prints the emoji time to stdout."""
    print(get_emoji_time())


if __name__ == "__main__":
    main()
