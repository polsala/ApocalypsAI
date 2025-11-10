"""Daily Zen Quote Generator.

Selects a random Zen‑inspired quote from a built‑in list and prints it.
"""

import random

_QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path.",
]

def get_random_quote() -> str:
    """Return a random quote from the built‑in list."""
    return random.choice(_QUOTES)

def main() -> None:
    """Entry point for the CLI."""
    print(get_random_quote())

if __name__ == "__main__":
    main()
