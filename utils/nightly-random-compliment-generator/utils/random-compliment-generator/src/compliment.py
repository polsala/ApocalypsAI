"""Random Compliment Generator.

Provides a CLI that prints a random compliment, optionally filtered by category.
"""

import argparse
import random
import sys
from typing import List, Optional

# Hard‑coded compliments grouped by category
_COMPLIMENTS = {
    "general": [
        "You're a fantastic problem‑solver!",
        "Your curiosity is contagious.",
        "You make the world a brighter place."
    ],
    "creative": [
        "Your imagination paints the sky with new colors.",
        "Ideas flow from you like a river."
    ],
    "technical": [
        "Your code is poetry in motion.",
        "You debug with the precision of a surgeon."
    ],
}


def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category to filter compliments. If None or unknown,
                  all categories are considered.

    Returns:
        A single compliment string.
    """
    if category and category in _COMPLIMENTS:
        pool: List[str] = _COMPLIMENTS[category]
    else:
        # Flatten all compliments
        pool = [c for cat in _COMPLIMENTS.values() for c in cat]
    return random.choice(pool)


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random compliment."
    )
    parser.add_argument(
        "--category",
        choices=list(_COMPLIMENTS.keys()),
        help="Filter compliments by category."
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    compliment = get_compliment(args.category)
    print(compliment)
    return 0


if __name__ == "__main__":
    sys.exit(main())
