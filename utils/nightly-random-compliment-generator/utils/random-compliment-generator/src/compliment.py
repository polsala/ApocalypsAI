#!/usr/bin/env python3
"""
random_compliment_generator

Provides a function to fetch a random compliment, optionally filtered by category.
"""

import argparse
import random
from typing import List, Optional

# Mock rationale: predefined compliment pools for offline operation
_COMPLIMENTS = {
    "general": [
        "You're a fantastic person!",
        "Your smile lights up the room.",
        "You have a great sense of humor."
    ],
    "work": [
        "Your work ethic is inspiring.",
        "You solve problems like a pro.",
        "Your ideas are always on point."
    ],
    "creative": [
        "Your creativity knows no bounds.",
        "You have an eye for beautiful design.",
        "Your imagination is a gift."
    ]
}


def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category to limit compliments. If ``None`` or unknown,
                  compliments from all categories are considered.

    Returns:
        A randomly selected compliment string.
    """
    if category and category in _COMPLIMENTS:
        pool: List[str] = _COMPLIMENTS[category]
    else:
        # Flatten all compliments across categories
        pool = [c for lst in _COMPLIMENTS.values() for c in lst]
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random compliment.")
    parser.add_argument(
        "-c",
        "--category",
        choices=list(_COMPLIMENTS.keys()),
        help="Category of compliment (default: any)."
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    print(get_compliment(args.category))


if __name__ == "__main__":
    main()
