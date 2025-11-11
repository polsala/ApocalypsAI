import argparse
import random
from typing import List

# A small collection of Zen‑style sayings
_QUOTES: List[str] = [
    "The obstacle is the path.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "Sitting quietly, doing nothing, spring comes, and the grass grows by itself.",
    "The journey of a thousand miles begins with one step.",
    "Let go or be dragged.",
    "When the mind is still, the universe surrenders.",
]

def get_random_quote() -> str:
    """Return a random quote from the built‑in list.

    The function is deliberately pure apart from the random choice, making it easy to mock in tests.
    """
    return random.choice(_QUOTES)

def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional seed for deterministic output (useful for testing).",
    )
    args = parser.parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    print(f"\"{get_random_quote()}\"")

if __name__ == "__main__":
    main()
