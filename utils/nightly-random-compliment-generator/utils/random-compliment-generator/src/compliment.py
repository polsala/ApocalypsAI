"""
random_compliment_generator

Provides a function to retrieve a random compliment.
"""

import random
import sys
from typing import List

_COMPLIMENTS: List[str] = [
    "You're doing great!",
    "Your code is sparkling clean.",
    "You have a fantastic sense of humor.",
    "Your problem‑solving skills are impressive.",
    "You make the world a better place.",
]

def get_compliment() -> str:
    """
    Return a random compliment from the predefined list.
    """
    return random.choice(_COMPLIMENTS)

def main() -> None:
    """
    CLI entry point: prints a random compliment to stdout.
    """
    print(get_compliment())

if __name__ == "__main__":
    # Allow running as a script: `python src/compliment.py`
    main()
