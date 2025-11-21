import random
import sys
from typing import List

# A curated list of Zen‑inspired sayings.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "Let go of the rope and the knot will untie itself.",
    "A single breath can calm a storm within.",
]

def get_random_quote() -> str:
    """Return a random quote from the built‑in list.

    The function is deliberately tiny so it can be easily mocked in tests.
    """
    return random.choice(QUOTES)

def main() -> None:
    """CLI entry point – prints a random quote to stdout."""
    quote = get_random_quote()
    print(quote)

if __name__ == "__main__":
    # When executed as a script, behave like a CLI tool.
    main()
