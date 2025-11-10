"""
fortune.py - Simple Fortune Cookie Generator

Provides a function to retrieve a random fortune and a CLI entrypoint.
"""

import random
from typing import List

FORTUNES: List[str] = [
    "You will find great success in unexpected places.",
    "A fresh start will put you on the path to success.",
    "Adventure can be real happiness.",
    "A pleasant surprise is waiting for you.",
    "Now is the time to try something new.",
    "Your hard work will soon pay off.",
    "Believe in yourself and others will too.",
    "Good news will come to you by mail.",
    "A new perspective will change your life.",
    "Patience is a virtue; good things come to those who wait."
]


def get_fortune() -> str:
    """Return a random fortune from the list."""
    return random.choice(FORTUNES)


def main() -> None:
    """CLI entrypoint: print a random fortune."""
    fortune = get_fortune()
    print(fortune)


if __name__ == "__main__":
    # Allow running as script
    main()
