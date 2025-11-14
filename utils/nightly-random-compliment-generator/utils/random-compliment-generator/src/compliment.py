"""random_compliment_generator – core logic

Provides a function to retrieve a random compliment, optionally filtered by category.
"""

import random
from typing import List, Optional, Dict

# Pre‑defined compliments grouped by category
_COMPLIMENTS: Dict[Optional[str], List[str]] = {
    None: [
        "You have a great sense of humor!",
        "Your curiosity is infectious.",
        "You make the world a better place.",
        "Your ideas are brilliant.",
        "You have a remarkable ability to stay calm under pressure."
    ],
    "creative": [
        "Your imagination knows no bounds.",
        "You turn ordinary moments into art.",
        "Your creativity inspires everyone around you."
    ],
    "technical": [
        "Your code is elegant and efficient.",
        "You solve complex problems with ease.",
        "Your debugging skills are legendary."
    ],
    "general": [
        "Your kindness is a gift to those around you.",
        "You have a wonderful way of making people feel heard.",
        "Your optimism lights up the room."
    ]
}


def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category to filter compliments. If the category is not
            recognized, the function falls back to the unfiltered list.

    Returns:
        A randomly selected compliment string.
    """
    # Normalize category to lower‑case for case‑insensitive matching
    cat_key = category.lower() if isinstance(category, str) else None
    compliments = _COMPLIMENTS.get(cat_key, _COMPLIMENTS[None])
    return random.choice(compliments)


def main() -> None:
    """CLI entry point.

    Parses optional ``--category`` argument and prints a random compliment.
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="random_compliment_generator",
        description="Print a random compliment, optionally filtered by category."
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Category of compliment (creative, technical, general)."
    )
    args = parser.parse_args()
    print(get_compliment(args.category))


if __name__ == "__main__":
    main()
