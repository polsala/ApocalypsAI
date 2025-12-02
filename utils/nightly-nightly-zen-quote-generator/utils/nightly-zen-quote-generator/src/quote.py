import random
import sys
from typing import List

# Curated list of zen quotes
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present.",
    "Silence is a source of great strength.",
]


def get_random_quote() -> str:
    """Return a random quote from the curated list.

    The function is deliberately simple to keep the utility lightweight.
    """
    # Using random.choice for brevity; tests will mock this for determinism.
    return random.choice(_QUOTES)


def main() -> None:
    """CLI entry point that prints a random quote to stdout."""
    quote = get_random_quote()
    print(quote)


if __name__ == "__main__":
    # Allow execution via `python src/quote.py`
    main()
