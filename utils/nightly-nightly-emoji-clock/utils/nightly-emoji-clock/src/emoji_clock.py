import datetime
from typing import Optional

# Mapping of hour (0‑23) to clock‑face emojis. The list repeats for 12‑hour cycles.
_CLOCK_EMOJIS = [
    "🕛",  # 0 / 12 AM
    "🕐",  # 1 AM
    "🕑",  # 2 AM
    "🕒",  # 3 AM
    "🕓",  # 4 AM
    "🕔",  # 5 AM
    "🕕",  # 6 AM
    "🕖",  # 7 AM
    "🕗",  # 8 AM
    "🕘",  # 9 AM
    "🕙",  # 10 AM
    "🕚",  # 11 AM
    "🕛",  # 12 PM (no separate emoji, reuse midnight)
    "🕐",  # 1 PM
    "🕑",  # 2 PM
    "🕒",  # 3 PM
    "🕓",  # 4 PM
    "🕔",  # 5 PM
    "🕕",  # 6 PM
    "🕖",  # 7 PM
    "🕗",  # 8 PM
    "🕘",  # 9 PM
    "🕙",  # 10 PM
    "🕚",  # 11 PM
]


def _hour_to_emoji(hour: int) -> str:
    """Return the clock‑face emoji for a given hour (0‑23)."""
    return _CLOCK_EMOJIS[hour % 24]


def get_emoji_time(now: Optional[datetime.datetime] = None) -> str:
    """Return a string like "🕒 07" representing the current time.

    Args:
        now: Optional datetime to use instead of ``datetime.datetime.now()``.
             Supplying a value makes the function deterministic for testing.
    Returns:
        A string with the hour emoji followed by the minute (zero‑padded).
    """
    if now is None:
        now = datetime.datetime.now()
    hour_emoji = _hour_to_emoji(now.hour)
    minute_str = f"{now.minute:02d}"
    return f"{hour_emoji} {minute_str}"


if __name__ == "__main__":
    print(get_emoji_time())
