import random
import sys
from pathlib import Path

# A curated list of Zen‑style quotes.
_QUOTES = [
    "The obstacle is the path.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "Sitting quietly, doing nothing, spring comes, and the grass grows by itself.",
    "The journey of a thousand miles begins with one step.",
    "Let go or be dragged.",
]


def get_random_quote() -> str:
    """Return a random quote from the internal list.

    The function is deliberately simple to keep the utility lightweight.
    """
    return random.choice(_QUOTES)


def main() -> None:
    """Entry point for the CLI.

    Prints a random quote to stdout. Returns exit code 0.
    """
    quote = get_random_quote()
    print(quote)


if __name__ == "__main__":
    # Allow execution via `python -m nightly_zen_quote_dispenser`
    # Resolve the module path relative to this file.
    # This block is kept minimal to avoid side‑effects during import.
    main()
