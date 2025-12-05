"""Daily Zen Quote Generator.

Provides a function to retrieve a random Zen‑inspired quote and a CLI entry point.
"""

import random
from typing import List

QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is pure, joy follows like a shadow that never leaves.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present, and trust the future.",
    "Silence is a source of great strength.",
]

def get_random_quote() -> str:
    """Return a random quote from the built‑in collection."""
    return random.choice(QUOTES)

def main() -> None:
    """CLI entry point."""
    print(get_random_quote())

if __name__ == "__main__":
    main()
