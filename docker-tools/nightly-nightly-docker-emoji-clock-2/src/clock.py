#!/usr/bin/env python3
import sys
from datetime import datetime

def get_clock_emoji(dt: datetime) -> str:
    """Return the Unicode clock‑face emoji that best represents *dt*.

    The algorithm rounds to the nearest full hour or half hour:
    * minutes < 15  → full hour
    * 15 ≤ minutes < 45 → half hour
    * minutes ≥ 45 → next full hour
    """
    hour = dt.hour % 12
    minute = dt.minute
    # Determine rounding
    if minute >= 45:
        hour = (hour + 1) % 12
        half = False
    elif minute >= 15:
        half = True
    else:
        half = False
    # Map to emoji code points
    if hour == 0:
        hour = 12
    if half:
        # Half‑hour emojis start at U+1F55C (1:30)
        emoji_code = 0x1F55C + (hour - 1)
    else:
        # Full‑hour emojis start at U+1F550 (1:00)
        emoji_code = 0x1F550 + (hour - 1)
    return chr(emoji_code)

def main():
    now = datetime.utcnow()
    emoji = get_clock_emoji(now)
    print(emoji)

if __name__ == "__main__":
    main()
