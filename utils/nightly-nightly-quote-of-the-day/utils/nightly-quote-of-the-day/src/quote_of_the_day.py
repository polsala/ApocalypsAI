import argparse
import random
from typing import List

# ---------------------------------------------------------------------------
# Quote data – a small curated list of inspirational sayings.
# ---------------------------------------------------------------------------
_QUOTES: List[str] = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Life is what happens when you're busy making other plans. – John Lennon",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Stay hungry, stay foolish. – Steve Jobs",
    "In the middle of difficulty lies opportunity. – Albert Einstein",
]


def get_random_quote(rng: random.Random = random) -> str:
    """Return a random quote from the bundled list.

    The *rng* argument allows callers (and tests) to inject a deterministic
    random source. By default it uses the global ``random`` module.
    """
    # ``random.choice`` is used for brevity; it can be mocked in tests.
    return rng.choice(_QUOTES)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a random inspirational quote to stdout."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for reproducible output.",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed) if args.seed is not None else random
    print(get_random_quote(rng))


if __name__ == "__main__":
    main()
