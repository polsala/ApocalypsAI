"""Daily Zen Quote Generator.

Provides a function to retrieve a random Zen quote from a built‑in list.
Can be used as a CLI script: `python -m daily_zen_quote_generator` prints a quote.
"""

import random
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path."
]


def get_zen_quote() -> str:
    """Return a random Zen quote."""
    return random.choice(_QUOTES)


if __name__ == "__main__":
    print(get_zen_quote())
