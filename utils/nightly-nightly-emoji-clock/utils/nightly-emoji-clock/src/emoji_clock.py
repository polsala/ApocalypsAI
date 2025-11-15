"""Emoji Clock utility.

Provides a function to render a datetime as a string of emoji digits.
"""

from datetime import datetime
from typing import Optional

# Mapping of digit characters to corresponding emoji numbers
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


def _to_emoji(num: int) -> str:
    """Convert a two‑digit integer to its emoji representation."""
    return "".join(_DIGIT_EMOJI[d] for d in f"{num:02d}")


def get_emoji_time(dt: Optional[datetime] = None) -> str:
    """Return the time (HH:MM) as emoji digits.

    If *dt* is None, the current local time is used.
    """
    if dt is None:
        dt = datetime.now()
    hour_emoji = _to_emoji(dt.hour)
    minute_emoji = _to_emoji(dt.minute)
    return f"{hour_emoji}:{minute_emoji}"


def main() -> None:
    """CLI entry point."""
    print(get_emoji_time())


if __name__ == "__main__":
    main()
