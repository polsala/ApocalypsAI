'''quote_dispenser.py - Provide random cryptic apocalypse quotes.'''

import random
from typing import List

_QUOTES: List[str] = [
    "When the sky cracks, the earth whispers.",
    "Ashes to ash, dust to dust, code to code.",
    "The last backup fell silent.",
    "Even the servers sigh under the weight of silence.",
    "In the void, logs become legends."
]


def get_random_quote(seed: int | None = None) -> str:
    """Return a random quote from the built‑in list.

    Args:
        seed: Optional integer to seed the random generator for deterministic output.
    Returns:
        A cryptic quote string.
    """
    if seed is not None:
        random.seed(seed)  # deterministic for testing
    return random.choice(_QUOTES)


def main() -> None:
    """CLI entry point – prints a random quote."""
    print(get_random_quote())


if __name__ == "__main__":
    main()
