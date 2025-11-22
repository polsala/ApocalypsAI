import datetime
from typing import List

# List of emojis representing a whimsical mood progression throughout the year.
_EMOJI_CYCLE: List[str] = [
    "🌅",  # Dawn – hopeful
    "😊",  # Light‑hearted
    "😎",  # Confident
    "🤔",  # Pensive
    "🤗",  # Warm
    "😴",  # Lazy
    "😐",  # Neutral
    "🙃",  # Playful
    "🤩",  # Excited
    "🥳",  # Celebratory
    "🌙",  # Calm night
    "💤",  # Sleepy
]


def _day_of_year(date: datetime.date) -> int:
    """Return the day of the year (1‑based). Handles leap years correctly."""
    return date.timetuple().tm_yday


def get_mood_emoji(date: datetime.date) -> str:
    """Return an emoji representing the *mood* for the given ``date``.

    The algorithm is deterministic:

    1. Compute the day of the year.
    2. Modulo the day by the length of ``_EMOJI_CYCLE``.
    3. Return the emoji at that index.

    Parameters
    ----------
    date: datetime.date
        The date for which to compute the mood.

    Returns
    -------
    str
        A single Unicode emoji.
    """
    day_index = (_day_of_year(date) - 1) % len(_EMOJI_CYCLE)
    return _EMOJI_CYCLE[day_index]


def _cli() -> None:
    """Simple command‑line interface that prints today's emoji."""
    today = datetime.date.today()
    print(get_mood_emoji(today))


if __name__ == "__main__":
    _cli()
