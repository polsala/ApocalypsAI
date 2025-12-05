import sys
import datetime
from typing import Tuple

# Mapping of time ranges (start_hour, end_hour) to emojis and descriptions
_TIME_RANGES: Tuple[Tuple[int, int, str, str], ...] = (
    (5, 12, "🌅", "Morning"),
    (12, 17, "🌞", "Afternoon"),
    (17, 21, "🌇", "Evening"),
    (21, 24, "🌙", "Night"),
    (0, 5, "🌙", "Night"),
)


def get_mood_emoji(now: datetime.datetime | None = None) -> str:
    """Return an emoji representing the time of day.

    Args:
        now: Optional datetime to evaluate. If ``None`` (default) the current
            UTC time is used. Supplying a value makes the function deterministic
            for testing.
    Returns:
        A single Unicode emoji string.
    """
    if now is None:
        now = datetime.datetime.utcnow()
    hour = now.hour
    for start, end, emoji, _ in _TIME_RANGES:
        if start <= hour < end:
            return emoji
    # Fallback – should never happen because ranges cover 0‑23
    return "❓"


def main() -> int:
    """CLI entry point that prints the mood emoji to stdout.

    Returns:
        Exit code (0 on success).
    """
    emoji = get_mood_emoji()
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
