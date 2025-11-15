"""daily_zen_quote – deterministic quote‑of‑the‑day CLI.

The module contains a small collection of Zen‑style quotes. The function
`quote_of_the_day(date: datetime.date) -> str` returns the quote for the
provided date. When executed as a script it prints the quote for ``datetime.date.today()``.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path

# A modest list of 30 quotes – enough to cover a full year with repetition.
_QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go, and be free.",
    "In the stillness, you hear the truth.",
    "A single breath can change everything.",
    "Nature does not hurry, yet everything is accomplished.",
    "The river flows, but never forgets its source.",
    "When you accept what is, you become the master of your destiny.",
    "The empty cup is ready to be filled.",
    "Patience is the companion of wisdom.",
    "A calm mind sees the whole picture.",
    "The moon does not fight the night; it simply shines.",
    "Every ending is a new beginning.",
    "Listen to the wind; it carries stories.",
    "The seed knows the tree it will become.",
    "Simplicity is the ultimate sophistication.",
    "When you smile at the world, the world smiles back.",
    "A stone dropped in water creates ripples that reach far.",
    "The present moment is a gift; that's why we call it now.",
    "Even the tallest mountain was once a grain of sand.",
    "Kindness is the language the deaf can hear and the blind can see.",
    "The fire that burns within is brighter than any external flame.",
    "To know the path, walk it.",
    "A river never forgets its source, even when it reaches the sea.",
    "The wind does not ask permission to move.",
    "When you let go of the rope, you discover you were never tied.",
    "The night is darkest before the sunrise, but the stars are always there.",
    "Peace is not the absence of noise, but the presence of harmony.",
]


def quote_of_the_day(date: datetime.date) -> str:
    """Return a deterministic quote for *date*.

    The algorithm is simple: compute the day‑of‑year (1‑365/366) and take the
    modulo of the number of quotes. This yields a repeatable mapping without
    any randomness or external resources.
    """
    day_of_year = date.timetuple().tm_yday  # 1‑366
    index = (day_of_year - 1) % len(_QUOTES)
    return _QUOTES[index]


def _main() -> None:
    today = datetime.date.today()
    quote = quote_of_the_day(today)
    print(quote)


if __name__ == "__main__":
    _main()
