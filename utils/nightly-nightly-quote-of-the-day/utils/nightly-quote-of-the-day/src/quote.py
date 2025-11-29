#!/usr/bin/env python3
"""
nightly-quote-of-the-day utility.

Provides a function to retrieve a random post‑apocalyptic quote and a CLI entrypoint.
"""

import random
import sys
from typing import List

_QUOTES: List[str] = [
    "The ashes whisper, 'Rise again.'",
    "When the sky fell, we learned to look up.",
    "Survival is a habit, not a moment.",
    "In the silence, hope shouts the loudest.",
    "Even ruins have stories to tell."
]

def get_random_quote() -> str:
    """Return a random quote from the internal list."""
    return random.choice(_QUOTES)

def main() -> None:
    """CLI entrypoint: print a random quote."""
    quote = get_random_quote()
    print(quote)

if __name__ == "__main__":
    # Allow optional seed for reproducibility when called as script
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
            random.seed(seed)
        except ValueError:
            pass
    main()
