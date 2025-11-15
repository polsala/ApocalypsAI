'''Random Compliment Generator utility.

Provides a function to retrieve a random compliment, optionally filtered by category.
Can be used as a CLI.
'''

import argparse
import random
from typing import List, Optional

_COMPLIMENTS = {
    "general": [
        "You're a fantastic problem-solver!",
        "Your curiosity is contagious.",
        "You make the world a better place just by being you."
    ],
    "coding": [
        "Your code is poetry in motion.",
        "Debugging is your superpower.",
        "You turn bugs into features."
    ],
    "design": [
        "Your eye for design is impeccable.",
        "Every UI you touch becomes user-friendly."
    ]
}


def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category to filter compliments. If None or unknown,
                  compliments from all categories are considered.

    Returns:
        A randomly selected compliment string.
    """
    if category and category in _COMPLIMENTS:
        pool: List[str] = _COMPLIMENTS[category]
    else:
        # Flatten all compliments
        pool = [c for comps in _COMPLIMENTS.values() for c in comps]
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random compliment.")
    parser.add_argument(
        "--category",
        help="Filter compliments by category (e.g., general, coding, design).",
        choices=list(_COMPLIMENTS.keys())
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    print(get_compliment(args.category))


if __name__ == "__main__":
    main()
