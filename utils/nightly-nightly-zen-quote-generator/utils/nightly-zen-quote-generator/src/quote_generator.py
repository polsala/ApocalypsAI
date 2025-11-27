import argparse
import random
from typing import List

# A small collection of zen‑style quotes – completely offline.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
]


def get_quote(seed: int | None = None) -> str:
    """Return a quote.

    If *seed* is provided, the selection is deterministic using that seed.
    Otherwise a random quote is chosen.
    """
    if seed is not None:
        rng = random.Random(seed)
        return rng.choice(QUOTES)
    return random.choice(QUOTES)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for deterministic output.",
    )
    args = parser.parse_args()
    quote = get_quote(args.seed)
    print(quote)


if __name__ == "__main__":
    main()
