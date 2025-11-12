"""Random Compliment Generator utility.

Provides a function to retrieve a random compliment from a predefined list.
"""

import random
from typing import List

_COMPLIMENTS: List[str] = [
    "You're a coding wizard!",
    "Your ideas sparkle like stars.",
    "You make the world brighter.",
    "Your curiosity is contagious.",
    "You have a brilliant mind.",
    "Your smile could power a server farm.",
    "You turn bugs into features.",
    "Your logic is flawless.",
    "You bring joy to the terminal.",
    "Your code is poetry."
]

def get_compliment(seed: int | None = None) -> str:
    """Return a random compliment.

    Args:
        seed: Optional integer seed for deterministic output.

    Returns:
        A compliment string.
    """
    if seed is not None:
        random.seed(seed)
    # Mock rationale: using random.choice for simplicity and testability.
    return random.choice(_COMPLIMENTS)

def main() -> None:
    """CLI entry point."""
    print(get_compliment())

if __name__ == "__main__":
    main()
