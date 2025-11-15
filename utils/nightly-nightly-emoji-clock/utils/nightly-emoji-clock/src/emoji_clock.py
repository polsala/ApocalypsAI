"""
Emoji Clock utility.

Provides a function to convert a datetime into an emoji representation.
"""

from datetime import datetime
import sys

DIGIT_EMOJI = {
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
    ":": "⏰",
}

def get_emoji_time(dt: datetime) -> str:
    """
    Convert a datetime object to an emoji string.
    Example: 13:45 -> "1️⃣3️⃣⏰4️⃣5️⃣"
    """
    time_str = dt.strftime("%H:%M")
    return "".join(DIGIT_EMOJI.get(ch, ch) for ch in time_str)

def main() -> None:
    """Print the current time as emojis."""
    now = datetime.now()
    print(get_emoji_time(now))

if __name__ == "__main__":
    main()
