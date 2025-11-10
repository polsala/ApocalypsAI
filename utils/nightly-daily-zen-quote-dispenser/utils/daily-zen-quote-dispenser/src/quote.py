"""Daily Zen Quote Dispenser.

Provides `get_zen_quote` to retrieve a random Zen‑inspired quote.
"""

import random
from typing import List, Optional

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the illusion of control.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Know the rules well, so you can break them.",
    "Nature does not hurry, yet everything is accomplished.",
    "To understand everything is to forgive everything.",
    "The only constant is change."
]


def get_zen_quote(max_length: Optional[int] = None) -> str:
    """Return a random Zen quote.

    Args:
        max_length: If provided, only quotes with length <= max_length are considered.

    Returns:
        A randomly selected quote string.

    Raises:
        ValueError: If no quotes satisfy the length constraint.
    """
    candidates = _QUOTES
    if max_length is not None:
        candidates = [q for q in _QUOTES if len(q) <= max_length]
        if not candidates:
            raise ValueError("No quotes fit the given max_length.")
    return random.choice(candidates)


if __name__ == "__main__":
    print(get_zen_quote())
