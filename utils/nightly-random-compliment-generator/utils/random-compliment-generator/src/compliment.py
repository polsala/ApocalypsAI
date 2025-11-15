"""
random_compliment_generator

Provides a function to fetch a random compliment and a CLI entry point.
"""

import argparse
import random
from typing import List

_COMPLIMENTS: List[str] = [
    "You're a coding wizard!",
    "Your logic is impeccable.",
    "You make bugs disappear like magic.",
    "Your code shines brighter than the sun.",
    "You turn coffee into code effortlessly.",
]

def get_compliment(seed: int | None = None) -> str:
    """
    Return a random compliment.

    Args:
        seed: Optional integer seed for deterministic output.

    Returns:
        A compliment string.
    """
    if seed is not None:
        random.seed(seed)
    # Mock rationale: deterministic choice via mocked random.choice in tests
    return random.choice(_COMPLIMENTS)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a random compliment."
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional integer seed for reproducible output.",
    )
    args = parser.parse_args()
    print(get_compliment(seed=args.seed))

if __name__ == "__main__":
    main()
