'''"""Daily Zen Quote Dispenser.

Provides `get_zen_quote` to retrieve a random Zen quote.
When run as a script, prints a quote to stdout.
"""

import random
import argparse
from typing import List, Optional

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When the mind is still, the universe surrenders.",
    "Let go or be dragged.",
    "Silence is a source of great strength."
]

def get_zen_quote(max_length: Optional[int] = None) -> str:
    """Return a random Zen quote.

    If `max_length` is provided, only quotes with length <= max_length are considered.
    Raises ValueError if no quotes satisfy the length constraint.
    """
    candidates = _QUOTES
    if max_length is not None:
        candidates = [q for q in _QUOTES if len(q) <= max_length]
        if not candidates:
            raise ValueError("No quotes fit the length constraint")
    return random.choice(candidates)

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum character length of the quote."
    )
    return parser.parse_args()

def main() -> None:
    args = _parse_args()
    try:
        quote = get_zen_quote(max_length=args.max_length)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(quote)

if __name__ == "__main__":
    main()
'''
