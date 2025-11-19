"""
emoji_mood_tracker

Provides a simple function to map the hour of day to a mood emoji.
"""

import sys
from datetime import datetime


def get_mood_emoji(hour: int) -> str:
    """
    Return an emoji representing the typical mood for a given hour (0‑23).

    Ranges:
    - 0‑5   : 🌙 (late night)
    - 6‑9   : 🌅 (sunrise)
    - 10‑13 : ☀️ (midday)
    - 14‑17 : 🌤️ (afternoon)
    - 18‑20 : 🌇 (sunset)
    - 21‑23 : 🌙 (evening)

    Args:
        hour: Hour in 24‑hour format.

    Returns:
        A string containing a single emoji.
    """
    if not (0 <= hour <= 23):
        raise ValueError("hour must be in 0..23")
    if 0 <= hour <= 5:
        return "🌙"
    if 6 <= hour <= 9:
        return "🌅"
    if 10 <= hour <= 13:
        return "☀️"
    if 14 <= hour <= 17:
        return "🌤️"
    if 18 <= hour <= 20:
        return "🌇"
    return "🌙"


def main() -> None:
    """CLI entry point: prints current mood emoji."""
    now = datetime.now()
    emoji = get_mood_emoji(now.hour)
    print(f"{emoji}")


if __name__ == "__main__":
    # Allow running as a module: python -m mood_tracker
    main()
