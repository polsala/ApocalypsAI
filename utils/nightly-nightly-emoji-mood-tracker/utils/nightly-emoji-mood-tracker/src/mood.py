import sys
import random
from datetime import datetime
from typing import Optional

# Base emoji pools per time‑of‑day segment
_EMOJI_POOLS = {
    "morning": ["☀️", "🌅", "🥐", "😊"],
    "afternoon": ["😎", "🌞", "🍹", "😁"],
    "evening": ["🌇", "🌙", "🍷", "🙂"],
    "night": ["🌌", "🌃", "🛌", "😴"],
}

def _segment_for_hour(hour: int) -> str:
    """Return the time‑of‑day segment name for a given hour (0‑23)."""
    if 5 <= hour <= 11:
        return "morning"
    if 12 <= hour <= 17:
        return "afternoon"
    if 18 <= hour <= 21:
        return "evening"
    return "night"

def get_mood(dt: Optional[datetime] = None) -> str:
    """Return an emoji representing the mood for *dt*.

    If *dt* is ``None`` the current local time is used.
    The result is deterministic for a given calendar date because a
    ``random.Random`` instance is seeded with ``YYYYMMDD``.
    """
    now = dt or datetime.now()
    segment = _segment_for_hour(now.hour)
    pool = _EMOJI_POOLS[segment]

    # Deterministic seed based on the date (year, month, day)
    seed = int(now.strftime("%Y%m%d"))
    rng = random.Random(seed)
    return rng.choice(pool)

def _cli() -> None:
    """Simple CLI entry point – prints the emoji to stdout."""
    emoji = get_mood()
    print(emoji)

if __name__ == "__main__":
    _cli()
