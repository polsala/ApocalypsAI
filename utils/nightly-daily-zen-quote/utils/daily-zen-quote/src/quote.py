'''daily-zen-quote utility.

Provides a function to retrieve a random Zen quote, optionally seeded for
deterministic output, and a CLI entry point.
'''

from __future__ import annotations

import argparse
import random
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path.",
    "Silence is a source of great strength.",
    "Know the rules well, so you can break them.",
]


def get_quote(seed: int | None = None) -> str:
    """Return a random quote.

    Args:
        seed: Optional integer seed for deterministic selection.

    Returns:
        A quote string.
    """
    rng = random.Random(seed)
    return rng.choice(_QUOTES)


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote",
        description="Print a random Zen‑inspired quote."
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Integer seed for deterministic output."
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    quote = get_quote(args.seed)
    print(quote)


if __name__ == "__main__":
    main()
