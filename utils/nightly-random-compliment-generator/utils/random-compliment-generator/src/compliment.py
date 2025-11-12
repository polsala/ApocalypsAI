import argparse
import random
from typing import List, Optional

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_COMPLIMENTS: dict[str, List[str]] = {
    "general": [
        "You are a ray of sunshine!",
        "Your smile brightens everyone's day.",
        "You have a heart of gold.",
    ],
    "code": [
        "Your code is poetry in motion.",
        "You turn bugs into features effortlessly.",
        "Your algorithms are pure elegance.",
    ],
    "life": [
        "You make the world a better place just by being you.",
        "Your curiosity inspires everyone around you.",
        "You have the courage to chase your dreams.",
    ],
}

_DEFAULT_CATEGORY = "general"

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category name. If omitted or unknown, falls back to the
            default *general* category.
    Returns:
        A randomly selected compliment string.
    """
    cat = category if category in _COMPLIMENTS else _DEFAULT_CATEGORY
    compliments = _COMPLIMENTS[cat]
    # Using random.choice makes the function easy to mock in tests.
    return random.choice(compliments)

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random compliment to stdout."
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Compliment category (general, code, life).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    compliment = get_compliment(args.category)
    print(compliment)


if __name__ == "__main__":
    main()
