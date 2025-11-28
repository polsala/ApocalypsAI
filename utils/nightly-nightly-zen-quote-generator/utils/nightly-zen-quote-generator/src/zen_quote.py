"""Zen Quote Generator utility.

Provides a function to retrieve a random Zen‑inspired quote.
"""

import random
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "In the middle of difficulty lies opportunity.",
    "Let go or be dragged."
]

def get_random_quote() -> str:
    """Return a random Zen quote.

    Returns:
        str: A randomly selected quote from the internal list.
    """
    return random.choice(_QUOTES)

def main() -> None:
    """CLI entry point that prints a random quote to stdout."""
    print(get_random_quote())

if __name__ == "__main__":
    main()
