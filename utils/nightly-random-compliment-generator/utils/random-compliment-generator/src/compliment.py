import argparse
import random
from typing import List, Optional

_COMPLIMENTS: List[str] = [
    "You're a coding wizard!",
    "Your logic is as clear as crystal.",
    "You make bugs disappear like magic.",
    "Your code shines brighter than the sun.",
    "You turn coffee into code effortlessly.",
    "Your algorithms are poetry in motion.",
    "You debug like a detective on a case.",
    "Your commits are always a masterpiece.",
    "You bring joy to the repository.",
    "Your pull requests are pure gold.",
]


def get_compliment(seed: Optional[int] = None) -> str:
    """Return a random compliment.

    If *seed* is provided, the random generator is seeded for deterministic output.
    """
    if seed is not None:
        random.seed(seed)
    return random.choice(_COMPLIMENTS)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random compliment to stdout."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for reproducible output.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    compliment = get_compliment(seed=args.seed)
    print(compliment)


if __name__ == "__main__":
    main()
