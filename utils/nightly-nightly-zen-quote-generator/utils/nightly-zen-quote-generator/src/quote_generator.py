"""quote_generator.py

Provides a simple function to fetch a random Zen quote and a tiny CLI wrapper.
"""

import random
import sys
from pathlib import Path

# A modest collection of Zen‑style sayings – completely offline.
_QUOTES = [
    "The obstacle is the path.",
    "When the mind is still, the universe surrenders.",
    "Sitting quietly, doing nothing, spring comes, and the grass grows by itself.",
    "The journey of a thousand miles begins with one step.",
    "Let go or be dragged.",
]


def get_random_quote() -> str:
    """Return a random quote from the internal list.

    The function is deliberately tiny and has no external dependencies.
    """
    return random.choice(_QUOTES)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Prints a random quote to stdout and returns exit code ``0``.
    """
    if argv is None:
        argv = sys.argv[1:]
    # No arguments are required; we ignore any that are passed.
    quote = get_random_quote()
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
