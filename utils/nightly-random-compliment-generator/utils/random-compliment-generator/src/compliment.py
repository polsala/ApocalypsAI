"""random-compliment-generator/src/compliment.py

Provides a simple function to return a random compliment and a tiny CLI entry‑point.
"""

import random
from typing import List

# A curated list of uplifting compliments.
_COMPLIMENTS: List[str] = [
    "Your curiosity is a superpower.",
    "You make complex problems look easy.",
    "Your code brings joy to the world.",
    "You have a brilliant mind.",
    "Your optimism is contagious.",
    "You turn challenges into opportunities.",
]


def get_compliment() -> str:
    """Return a random compliment from the internal list.

    The function is deliberately tiny to keep the utility lightweight.
    """
    return random.choice(_COMPLIMENTS)


def main() -> None:
    """CLI entry‑point that prints a random compliment to stdout."""
    print(get_compliment())


if __name__ == "__main__":
    main()
