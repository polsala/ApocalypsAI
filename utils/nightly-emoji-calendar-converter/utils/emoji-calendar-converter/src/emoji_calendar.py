"""
emoji_calendar.py
Utility to convert dates to emoji strings and back.
"""

from datetime import datetime

# Mapping digits 0-9 to emojis (digit + variation selector)
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
}

# Emoji used to represent the dash separator
DASH_EMOJI = "➖"


def date_to_emoji(date_str: str) -> str:
    """Convert a date string in YYYY-MM-DD format to an emoji representation.

    Args:
        date_str: Date string like ``"2023-10-31"``.
    Returns:
        Emoji string, e.g. ``"2️⃣0️⃣2️⃣3️⃣➖1️⃣0️⃣➖3️⃣1️⃣"``.
    Raises:
        ValueError: If the input does not match the expected format.
    """
    # Validate format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_str}") from e

    return "".join(
        DIGIT_EMOJI[ch] if ch.isdigit() else DASH_EMOJI for ch in date_str
    )


def emoji_to_date(emoji_str: str) -> str:
    """Convert an emoji representation back to a YYYY-MM-DD string.

    Args:
        emoji_str: Emoji string produced by :func:`date_to_emoji`.
    Returns:
        Original date string.
    Raises:
        ValueError: If the emoji string contains unknown symbols.
    """
    # Reverse lookup tables
    rev_digit = {v: k for k, v in DIGIT_EMOJI.items()}
    rev_dash = {DASH_EMOJI: "-"}

    result_chars = []
    i = 0
    while i < len(emoji_str):
        # Try to match a two‑character digit emoji first
        two = emoji_str[i : i + 2]
        if two in rev_digit:
            result_chars.append(rev_digit[two])
            i += 2
        elif emoji_str[i] in rev_dash:
            result_chars.append(rev_dash[emoji_str[i]])
            i += 1
        else:
            raise ValueError(
                f"Unrecognized emoji segment at position {i}: {emoji_str[i:]}"
            )
    return "".join(result_chars)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m emoji_calendar <YYYY-MM-DD>")
        sys.exit(1)
    try:
        print(date_to_emoji(sys.argv[1]))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
