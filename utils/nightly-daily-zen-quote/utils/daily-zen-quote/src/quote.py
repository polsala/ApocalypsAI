#!/usr/bin/env python3
"""
Daily Zen Quote utility

Prints a random Zen‑inspired quote. An optional integer seed makes the output deterministic.
"""

import argparse
import random
import sys
from typing import List, Optional

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path.",
]


def get_quote(seed: Optional[int] = None) -> str:
    """Return a quote.

    If *seed* is provided, the selection is deterministic using that seed.
    """
    rnd = random.Random(seed) if seed is not None else random
    return rnd.choice(_QUOTES)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote",
        description="Print a random Zen‑inspired quote.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional integer seed for deterministic output.",
    )
    args = parser.parse_args(argv)

    quote = get_quote(args.seed)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
