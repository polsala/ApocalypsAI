#!/usr/bin/env python3
"""Random Compliment Generator

Provides a function to fetch a random compliment, optionally filtered by category,
and a small CLI for direct usage.
"""

import argparse
import random
import sys
from typing import List, Optional

COMPLIMENTS = {
    "general": [
        "You are awesome!",
        "Your smile brightens the room.",
        "You have a great sense of humor."
    ],
    "work": [
        "Your productivity is impressive.",
        "You handle challenges like a pro.",
        "Your contributions make a difference."
    ],
    "coding": [
        "Your code is clean and elegant.",
        "You debug like a detective.",
        "Your algorithms are top‑notch."
    ]
}


def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category name (case‑insensitive). If omitted, a compliment
                  is chosen from all categories.
    Raises:
        ValueError: If a non‑existent category is supplied.
    """
    if category:
        pool = COMPLIMENTS.get(category.lower())
        if not pool:
            raise ValueError(f"Unknown category: {category}")
    else:
        # Flatten all compliments into a single list
        pool = [c for lst in COMPLIMENTS.values() for c in lst]
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random compliment.")
    parser.add_argument(
        "-c",
        "--category",
        help="Category of compliment (general, work, coding).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        print(get_compliment(args.category))
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
