import argparse
import random
from typing import Callable, List

# A curated list of Zen‑style quotes.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present.",
    "Silence is a source of great strength.",
]


def get_zen_quote(random_func: Callable[[List[str]], str] = random.choice) -> str:
    """Return a random Zen quote.

    The `random_func` parameter is injectable for testing purposes.
    """
    return random_func(QUOTES)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote-dispenser",
        description="Print a random Zen‑style quote to stdout.",
    )
    args = parser.parse_args()
    # No CLI options needed; just print a quote.
    print(get_zen_quote())


if __name__ == "__main__":
    _cli()
