"""Zen Quote utility.

Provides a function to retrieve a random Zen‑inspired quote.
"""

import random
import sys
from pathlib import Path

_QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When the mind is still, the universe surrenders.",
    "Let go or be dragged.",
    "The obstacle is the path.",
    "Silence is a source of great strength.",
    "Know the rules well, so you can break them.",
    "The only constant is change.",
    "Be present, not perfect.",
    "A smooth sea never made a skilled sailor."
]


def get_quote() -> str:
    """Return a random Zen quote."""
    return random.choice(_QUOTES)


def main() -> None:
    """Print a random quote to stdout."""
    print(get_quote())


if __name__ == "__main__":
    main()
