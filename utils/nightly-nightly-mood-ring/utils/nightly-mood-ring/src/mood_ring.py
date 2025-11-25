import datetime
import sys

# Mapping of hour ranges to mood emojis
_MOOD_RANGES = [
    (range(0, 4), "🌑"),   # Midnight
    (range(4, 8), "🌅"),   # Dawn
    (range(8, 12), "☀️"),  # Morning
    (range(12, 16), "😎"), # Noon
    (range(16, 20), "🌆"), # Evening
    (range(20, 24), "🌙"), # Night
]


def _emoji_for_hour(hour: int) -> str:
    """Return the emoji that matches *hour*.

    The function iterates over the predefined ranges and returns the first match.
    """
    for hour_range, emoji in _MOOD_RANGES:
        if hour in hour_range:
            return emoji
    # Fallback (should never happen)
    return "❓"


def get_mood(dt: datetime.datetime | None = None) -> str:
    """Return a mood emoji for the given datetime.

    If *dt* is ``None`` the current local time is used.
    """
    if dt is None:
        dt = datetime.datetime.now()
    return _emoji_for_hour(dt.hour)


def main() -> None:
    """CLI entry‑point that prints the current mood emoji to stdout."""
    emoji = get_mood()
    print(emoji)


if __name__ == "__main__":
    # Allow execution as a script: ``python mood_ring.py``
    main()
