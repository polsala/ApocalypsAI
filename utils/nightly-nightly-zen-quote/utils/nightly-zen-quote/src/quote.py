"""quote.py

Utility to fetch a random Zen‑style quote.

Provides:
- `get_random_zen_quote(seed: int | None = None) -> str`
- CLI entry point (`python -m src.quote`)
"""

import argparse
import random
from typing import List

# A small curated list of Zen‑inspired sayings.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the stillness, you hear the sound of your own heart.",
]


def get_random_zen_quote(seed: int | None = None) -> str:
    """Return a random Zen quote.

    If *seed* is provided, the selection is deterministic.
    """
    rng = random.Random(seed) if seed is not None else random
    return rng.choice(_QUOTES)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for deterministic output.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    quote = get_random_zen_quote(seed=args.seed)
    print(quote)


if __name__ == "__main__":
    # When executed as a module (`python -m src.quote`), run the CLI.
    main()
