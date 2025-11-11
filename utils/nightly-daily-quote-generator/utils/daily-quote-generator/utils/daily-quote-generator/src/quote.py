import random
from typing import List, Optional

_QUOTE_BANK = {
    "motivation": [
        "The only limit is your mind.",
        "Dream big, act bigger."
    ],
    "humor": [
        "I’m not lazy, I’m on energy‑saving mode.",
        "Why don’t scientists trust atoms? Because they make up everything."
    ],
    "general": [
        "Life is what happens when you’re busy making other plans."
    ]
}


def get_random_quote(category: Optional[str] = None) -> str:
    """Return a random quote.

    Args:
        category: Optional category to filter quotes. If ``None`` or an unknown
            category is supplied, the function selects from the full collection.

    Returns:
        A quote string.
    """
    if category and category in _QUOTE_BANK:
        pool: List[str] = _QUOTE_BANK[category]
    else:
        # Flatten all quotes into a single list
        pool = [q for quotes in _QUOTE_BANK.values() for q in quotes]
    return random.choice(pool)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Print a random quote.")
    parser.add_argument("category", nargs="?", default=None, help="Quote category")
    args = parser.parse_args()
    print(get_random_quote(args.category))
