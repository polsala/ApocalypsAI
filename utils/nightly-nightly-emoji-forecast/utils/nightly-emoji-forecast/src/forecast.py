'''
emoji forecast utility
'''

import datetime
import random
from typing import Optional

EMOJIS = ["☀️", "🌤️", "🌧️", "⛈️", "❄️", "🌈", "🌪️", "🌫️", "🌙", "⭐️"]


def _seed_random(date: datetime.date) -> None:
    """Seed random with a reproducible value derived from the date."""
    seed_str = date.isoformat()
    random.seed(seed_str)


def get_forecast(date: Optional[datetime.date] = None) -> str:
    """
    Return a deterministic emoji forecast for the given date.
    If no date is provided, uses today's date.
    """
    if date is None:
        date = datetime.date.today()
    _seed_random(date)
    return random.choice(EMOJIS)


def main() -> None:
    """CLI entry point."""
    print(get_forecast())


if __name__ == "__main__":
    main()
