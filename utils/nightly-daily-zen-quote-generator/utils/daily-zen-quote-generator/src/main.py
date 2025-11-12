'''Daily Zen Quote Generator CLI.'''

import argparse
import random
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path.",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in collection."""
    return random.choice(_QUOTES)


def get_multiple_quotes(count: int) -> List[str]:
    """Return a list of `count` random quotes (may contain duplicates)."""
    return [get_random_quote() for _ in range(count)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Print one or more random Zen quotes.")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of quotes to print (default: 1)",
    )
    args = parser.parse_args()
    quotes = get_multiple_quotes(args.count)
    for q in quotes:
        print(f"🧘 {q}")


if __name__ == "__main__":
    main()
