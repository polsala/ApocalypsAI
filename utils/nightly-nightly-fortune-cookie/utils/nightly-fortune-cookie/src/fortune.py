"""
fortune.py - Simple fortune cookie generator.

Provides:
- get_fortune() -> str: returns a random fortune string.
- main(): prints a fortune to stdout.
"""

import random
from typing import List

_FORTUNES: List[str] = [
    "You will find great success in unexpected places.",
    "A fresh start will put you on your way.",
    "Patience is a virtue; good things come to those who wait.",
    "Adventure awaits you this week.",
    "Your hard work will soon pay off."
]

def get_fortune() -> str:
    """Return a random fortune from the built‑in list."""
    return random.choice(_FORTUNES)

def main() -> None:
    """CLI entry point: print a random fortune."""
    print(get_fortune())

if __name__ == "__main__":
    main()
