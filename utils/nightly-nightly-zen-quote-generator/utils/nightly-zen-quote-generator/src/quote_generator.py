import argparse
import random
import sys
from typing import List

# A curated list of short zen‑style sayings.
QUOTES: List[str] = [
    "The obstacle is the path.",
    "When the mind is still, the universe surrenders.",
    "A single step is enough to begin the journey.",
    "Silence is the language of the soul.",
    "Let go, and the river will carry you.",
    "The moon does not fight the night; it simply shines.",
    "In the garden of the mind, weeds are thoughts; prune them.",
    "Even a stone can become a stepping stone.",
    "Patience is the companion of wisdom.",
    "The wind whispers what the heart already knows."
]


def get_random_quote(seed: int | None = None) -> str:
    """Return a random quote.

    If *seed* is provided, the selection is deterministic – useful for testing.
    """
    rng = random.Random(seed)
    return rng.choice(QUOTES)


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for deterministic output."
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    quote = get_random_quote(seed=args.seed)
    print(quote)


if __name__ == "__main__":
    # When executed as a module (`python -m quote_generator`) we forward sys.argv[1:]
    main()
