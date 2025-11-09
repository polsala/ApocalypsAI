"""
random_compliment_generator

Provides a function to retrieve a random compliment.
"""

import random
import argparse
from typing import List

_COMPLIMENTS: List[str] = [
    "You're a coding wizard!",
    "Your mind is a treasure trove of ideas.",
    "You make the world brighter with your presence.",
    "Your curiosity fuels innovation.",
    "You have a knack for turning challenges into opportunities.",
    "Your smile is contagious.",
    "You bring clarity to complex problems.",
    "Your perseverance is inspiring.",
    "You have a brilliant sense of humor.",
    "Your kindness makes a difference."
]


def get_compliment(seed: int | None = None) -> str:
    """
    Return a random compliment.

    Args:
        seed: Optional integer seed for deterministic selection.

    Returns:
        A compliment string.
    """
    rng = random.Random(seed)
    return rng.choice(_COMPLIMENTS)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random compliment."
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional integer seed for deterministic output."
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    print(get_compliment(seed=args.seed))


if __name__ == "__main__":
    main()
