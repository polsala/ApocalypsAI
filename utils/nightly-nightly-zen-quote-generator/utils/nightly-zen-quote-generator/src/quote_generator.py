"""zen_quote_generator

Provides a simple API to retrieve a random Zen‑style quote.

The module is deliberately lightweight – only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Quote:
    text: str
    author: str


_QUOTE_BANK: List[Quote] = [
    Quote(text="The journey of a thousand miles begins with one step.", author="Lao Tzu"),
    Quote(text="When the mind is still, the universe surrenders.", author="Zen Proverb"),
    Quote(text="Simplicity is the ultimate sophistication.", author="Leonardo da Vinci"),
    Quote(text="Let go or be dragged.", author="Zen Saying"),
    Quote(text="The obstacle is the path.", author="Zen Proverb"),
]


def get_random_quote(seed: Optional[int] = None) -> Quote:
    """Return a random quote from the internal bank.

    Args:
        seed: Optional integer to seed ``random`` for deterministic output.
    Returns:
        A :class:`Quote` instance.
    """
    if seed is not None:
        random.seed(seed)
    # ``random.choice`` is used for clarity; tests mock it for determinism.
    return random.choice(_QUOTE_BANK)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional seed for reproducible output.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    quote = get_random_quote(seed=args.seed)
    print(f"\"{quote.text}\" — {quote.author}")


if __name__ == "__main__":
    # When executed as a module: ``python -m nightly_zen_quote_generator``
    main()
