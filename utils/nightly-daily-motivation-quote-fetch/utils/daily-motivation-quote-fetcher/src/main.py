"""Daily Motivation Quote Fetcher.

Provides a function to retrieve a random motivational quote.
Can be executed as a script to print a quote to stdout.
"""

import random
from typing import List

_QUOTES: List[str] = [
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Dream big and dare to fail.",
    "Stay hungry, stay foolish.",
    "Your limitation—it's only your imagination."
]

def get_random_quote() -> str:
    """Return a random quote from the built‑in list."""
    return random.choice(_QUOTES)

def main() -> None:
    """Print a random quote to stdout."""
    print(get_random_quote())

if __name__ == "__main__":
    main()
