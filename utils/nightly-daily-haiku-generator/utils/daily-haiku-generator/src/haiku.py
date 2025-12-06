'''Daily Haiku Generator utility.

Provides a function to generate a whimsical haiku based on a date.
''' 

import random
import datetime
from typing import Optional

# Word banks for haiku lines (5‑7‑5 syllable patterns)
FIVE_SYLLABLE_LINES = [
    "Morning dew glistens",
    "Silent moonlit night",
    "Leaves whisper softly",
    "Snowflakes kiss the earth",
    "Stars flicker above",
]

SEVEN_SYLLABLE_LINES = [
    "A breeze carries distant laughter",
    "Dreams drift on the river of time",
    "Shadows dance beneath the pine",
    "Petals fall like gentle rain",
    "Echoes linger in the canyon",
]


def _seed_for_date(date: datetime.date) -> int:
    """Create a deterministic seed from a date."""
    return date.toordinal()


def generate(date: Optional[datetime.date] = None) -> str:
    """Generate a haiku for the given date (or today if None).

    Returns:
        A three‑line string separated by newline characters.
    """
    if date is None:
        date = datetime.date.today()
    rnd = random.Random(_seed_for_date(date))
    line1 = rnd.choice(FIVE_SYLLABLE_LINES)
    line2 = rnd.choice(SEVEN_SYLLABLE_LINES)
    line3 = rnd.choice(FIVE_SYLLABLE_LINES)
    return f"{line1}\n{line2}\n{line3}"


if __name__ == "__main__":
    print(generate())
