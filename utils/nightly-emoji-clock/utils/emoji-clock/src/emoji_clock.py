import datetime
from typing import Optional

# Mapping of hour (0‑23) to clock face emojis. The emojis represent the hour on a 12‑hour clock.
_HOUR_EMOJI_MAP = {
    0: "🕛",  # 12 AM
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
    12: "🕛",  # 12 PM
    13: "🕐",
    14: "🕑",
    15: "🕒",
    16: "🕓",
    17: "🕔",
    18: "🕕",
    19: "🕖",
    20: "🕗",
    21: "🕘",
    22: "🕙",
    23: "🕚",
}


def get_emoji_time(now: Optional[datetime.datetime] = None) -> str:
    """Return the clock‑face emoji representing the current hour.

    Args:
        now: Optional datetime to use instead of ``datetime.datetime.now()``.
            Supplying a value is useful for testing.
    Returns:
        A single emoji string.
    """
    if now is None:
        now = datetime.datetime.now()
    hour = now.hour
    return _HOUR_EMOJI_MAP[hour]


def main() -> None:
    """CLI entry point – prints the emoji for the current hour."""
    print(get_emoji_time())


if __name__ == "__main__":
    main()
