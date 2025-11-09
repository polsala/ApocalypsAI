"""
Daily Zen Quote – offline random Zen quote generator.

Provides:
- `get_random_quote()` – returns a random quote string.
- CLI entry point when run as a module.
"""

import random
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path.",
    "Silence is a source of great strength.",
]


def get_random_quote() -> str:
    """Return a random Zen quote from the internal collection."""
    return random.choice(_QUOTES)


def _main() -> None:
    """CLI entry point."""
    quote = get_random_quote()
    print(quote)


if __name__ == "__main__":
    _main()
