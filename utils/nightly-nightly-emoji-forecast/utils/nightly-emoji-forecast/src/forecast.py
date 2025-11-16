#!/usr/bin/env python3
"""
emoji forecast utility
"""

from __future__ import annotations
import datetime
import sys

# Base emojis for weekdays Monday=0 ... Sunday=6
_WEEKDAY_EMOJIS = ["🌞", "🌜", "⭐", "⚡", "☔", "❄️", "🌈"]

# Month modifiers (index 1-12). Empty string for month 0 placeholder.
_MONTH_MODIFIERS = [
    "",  # placeholder for month 0
    "🌱", "🌸", "🌼", "🌻", "🌺", "🌹",
    "🍂", "🍁", "🍄", "🌰", "🥥", "❄️"
]

def get_daily_emoji(target_date: datetime.date) -> str:
    """Return a deterministic emoji for the given date.

    The algorithm:
    1. Pick a base emoji from the weekday list.
    2. Append a month modifier (if any) to create a combined string.
    3. If the combined string is longer than one emoji, return the base emoji
       (keeps output to a single glyph for terminal friendliness).

    Args:
        target_date: date for which to generate the emoji.

    Returns:
        A single emoji string.
    """
    base = _WEEKDAY_EMOJIS[target_date.weekday()]
    modifier = _MONTH_MODIFIERS[target_date.month]
    # Simple deterministic combination: if modifier exists, concatenate and take first char
    combined = base + modifier
    # Return first grapheme (emoji)
    return combined[0]

def _cli():
    today = datetime.date.today()
    emoji = get_daily_emoji(today)
    print(emoji)

if __name__ == "__main__":
    _cli()
