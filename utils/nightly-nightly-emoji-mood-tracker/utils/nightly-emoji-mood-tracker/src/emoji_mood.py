import sys
import datetime
from typing import Dict

# Fixed mapping from weekday (0=Monday) to an emoji representing the day's mood.
WEEKDAY_EMOJI_MAP: Dict[int, str] = {
    0: "☕",  # Monday – coffee needed
    1: "🚀",  # Tuesday – launch day
    2: "🌱",  # Wednesday – mid‑week growth
    3: "🎯",  # Thursday – target in sight
    4: "🍻",  # Friday – weekend vibes
    5: "🏖️",  # Saturday – relax
    6: "🎄",  # Sunday – cozy
}


def get_mood(date: datetime.date) -> str:
    """Return the emoji mood for *date*.

    The function is pure and deterministic – no external I/O.
    """
    weekday = date.weekday()
    return WEEKDAY_EMOJI_MAP[weekday]


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_mood <YYYY-MM-DD>")
        sys.exit(1)
    try:
        input_date = datetime.date.fromisoformat(sys.argv[1])
    except ValueError:
        print("Invalid date format. Expected YYYY-MM-DD.")
        sys.exit(1)
    print(get_mood(input_date))


if __name__ == "__main__":
    _cli()
