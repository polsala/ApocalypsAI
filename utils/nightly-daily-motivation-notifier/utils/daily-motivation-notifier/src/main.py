#!/usr/bin/env python3
"""
Daily Motivation Notifier

Prints a random motivational quote to stdout.
"""

import random
import sys
from typing import List

_QUOTES: List[str] = [
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "Dream big and dare to fail.",
    "Stay hungry, stay foolish.",
    "Your limitation—it's only your imagination."
]

def get_random_quote() -> str:
    """Return a random quote from the internal list."""
    return random.choice(_QUOTES)

def main() -> None:
    """Entry point for the CLI."""
    quote = get_random_quote()
    print(quote)

if __name__ == "__main__":
    sys.exit(main())
