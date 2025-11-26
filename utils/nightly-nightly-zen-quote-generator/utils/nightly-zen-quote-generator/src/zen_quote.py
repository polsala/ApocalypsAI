"""
zen_quote.py

Provides a small collection of Zen‑inspired quotes and a function to retrieve a random one.
"""

import random
import argparse
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Quote:
    text: str
    author: str

# Predefined list of quotes
_QUOTES: List[Quote] = [
    Quote(text="The journey of a thousand miles begins with one step.", author="Lao Tzu"),
    Quote(text="When the mind is still, the universe surrenders.", author="Unknown"),
    Quote(text="Simplicity is the ultimate sophistication.", author="Leonardo da Vinci"),
    Quote(text="Let go or be dragged.", author="Zen Proverb"),
    Quote(text="The obstacle is the path.", author="Zen Proverb"),
]

def get_random_quote(seed: Optional[int] = None) -> Quote:
    """
    Return a random Quote from the internal list.

    Args:
        seed: Optional integer to seed the random generator for reproducibility.

    Returns:
        A Quote instance.
    """
    if seed is not None:
        random.seed(seed)
    # Mock rationale: deterministic selection via random.choice; tests patch this.
    return random.choice(_QUOTES)

def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional integer seed for reproducible output.",
    )
    args = parser.parse_args()
    quote = get_random_quote(seed=args.seed)
    print(f'"{quote.text}" — {quote.author}')

if __name__ == "__main__":
    main()
