import argparse
import random
from typing import List

# A curated list of Zen‑inspired sayings.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the stillness, you hear the answer.",
    "A single breath can change a lifetime.",
    "The moon does not fight the night; it simply shines.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "The bamboo that bends is stronger than the oak that resists."
]


def get_quote(seed: int | None = None) -> str:
    """Return a quote.

    If *seed* is provided, the selection is deterministic using a local
    ``random.Random`` instance.  Otherwise the global random state is used.
    """
    rng = random.Random(seed) if seed is not None else random
    # ``choice`` works on any sequence; ``rng`` mimics the ``random`` module.
    return rng.choice(QUOTES)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a Zen‑style quote."
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional integer seed for reproducible output."
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    print(get_quote(seed=args.seed))


if __name__ == "__main__":
    main()
