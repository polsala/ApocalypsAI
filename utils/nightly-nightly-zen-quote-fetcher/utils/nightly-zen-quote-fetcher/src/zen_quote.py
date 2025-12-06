"""
zen_quote.py

Provides a function to retrieve a random Zen‑inspired quote.
Can be executed as a module to print a quote to stdout.
"""

import random
from typing import List, Optional

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path."
]

def get_random_quote(random_state: Optional[random.Random] = None) -> str:
    """
    Return a random quote from the internal list.

    Args:
        random_state: Optional `random.Random` instance for deterministic selection.
    Returns:
        A quote string.
    """
    rng = random_state or random
    return rng.choice(_QUOTES)

def main() -> None:
    """Print a random Zen quote to stdout."""
    print(get_random_quote())

if __name__ == "__main__":
    main()
