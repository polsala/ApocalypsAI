"""
nightly-motivation-quote-dispenser utility.

Provides a function to retrieve a random motivational quote and a CLI entry point.
"""

import random
import argparse
from typing import List

_QUOTES: List[str] = [
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Dream big and dare to fail.",
    "Stay hungry, stay foolish.",
    "Turn obstacles into opportunities."
]

def get_random_quote() -> str:
    """Return a random quote from the curated list."""
    return random.choice(_QUOTES)

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random motivational quote."
    )
    return parser.parse_args()

def main() -> None:
    """CLI entry point."""
    _ = _parse_args()  # args currently unused; placeholder for future flags
    print(get_random_quote())

if __name__ == "__main__":
    main()
