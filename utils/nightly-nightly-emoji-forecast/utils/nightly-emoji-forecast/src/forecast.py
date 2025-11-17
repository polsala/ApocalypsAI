import datetime
import random
from typing import Optional

EMOJI_POOL = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado (just for fun)
    "🌈",  # rainbow
    "🌙",  # night
    "💥",  # explosive surprise
]


def _seed_for_date(date: datetime.date) -> int:
    """Create a deterministic integer seed from a date.

    The ISO format string is hashed to an int; this is stable across Python versions.
    """
    # Mock rationale: using a simple deterministic hash ensures reproducibility without external libs.
    return int(date.strftime("%Y%m%d"))


def get_emoji_forecast(date: Optional[datetime.date] = None) -> str:
    """Return an emoji representing today's (or the supplied) forecast.

    Args:
        date: Optional specific date; defaults to ``datetime.date.today()``.
    Returns:
        A single emoji string.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_for_date(date)
    rng = random.Random(seed)
    return rng.choice(EMOJI_POOL)


def main() -> None:
    """CLI entry point – prints the emoji forecast for today."""
    emoji = get_emoji_forecast()
    print(emoji)


if __name__ == "__main__":
    main()
