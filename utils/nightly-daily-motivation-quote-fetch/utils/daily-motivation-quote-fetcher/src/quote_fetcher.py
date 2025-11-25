"""Quote Fetcher utility.

Provides a function to retrieve a random motivational quote and a CLI entry point.
"""

import random
import sys
from typing import List

_QUOTES: List[str] = [
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Dream big and dare to fail.",
    "Stay hungry, stay foolish.",
    "What you get by achieving your goals is not as important as what you become by achieving your goals."
]

def get_random_quote() -> str:
    """Return a random quote from the internal list."""
    return random.choice(_QUOTES)

def main() -> None:
    """CLI entry point: print a random quote to stdout."""
    quote = get_random_quote()
    print(quote)

if __name__ == "__main__":
    # When executed as a script, behave like a CLI.
    main()
