"""random_compliment_generator – core implementation

Provides a function to fetch a random compliment, optionally filtered by a
category, and a tiny CLI wrapper.
"""

import argparse
import random
from typing import List, Optional

# Mock rationale: static data ensures offline operation and deterministic tests.
_COMPLIMENTS = {
    "work": [
        "Your code is a masterpiece of elegance.",
        "You turn bugs into features with style.",
        "Your pull requests are a joy to review."
    ],
    "friendship": [
        "Your friendship is a warm blanket on a cold day.",
        "You have a heart of gold and a laugh that lights up rooms.",
        "Being around you makes everything better."
    ],
    "self": [
        "You are capable of amazing things.",
        "Your curiosity fuels your growth.",
        "You have a brilliant mind and a kind soul."
    ],
    "general": [
        "You make the world a brighter place.",
        "Your presence is a gift to everyone around you.",
        "You inspire others just by being yourself."
    ]
}


def _flatten(comps: dict) -> List[str]:
    """Flatten all compliments into a single list (used for no‑category case)."""
    return [c for lst in comps.values() for c in lst]


def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category name. If omitted or unknown, a random
                  compliment from any category is returned.
    Returns:
        A string containing the compliment.
    """
    if category and category in _COMPLIMENTS:
        pool = _COMPLIMENTS[category]
    else:
        pool = _flatten(_COMPLIMENTS)
    # Random choice – deterministic in tests via mocking.
    return random.choice(pool)


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random compliment.")
    parser.add_argument(
        "--category",
        type=str,
        help="Optional category (work, friendship, self)."
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    compliment = get_compliment(category=args.category)
    print(compliment)


if __name__ == "__main__":
    main()
