import argparse
import random
from typing import List, Optional

# Mock rationale: static data ensures offline determinism and no external calls.
COMPLIMENTS = {
    "general": [
        "You are a ray of sunshine!",
        "Your smile lights up the room.",
        "You have a heart of gold."
    ],
    "work": [
        "Your productivity is inspiring.",
        "You turn challenges into opportunities.",
        "Your teamwork makes the dream work."
    ],
    "coding": [
        "Your code is poetry in motion.",
        "You debug like a detective on a case.",
        "Your algorithms are elegant and efficient."
    ]
}

def _flatten(categories: Optional[List[str]] = None) -> List[str]:
    """Return a flat list of compliments for the given categories.

    If *categories* is ``None`` or empty, all compliments are returned.
    """
    if not categories:
        # Return all compliments across all categories
        return [c for cat in COMPLIMENTS.values() for c in cat]
    # Validate categories and collect matching compliments
    result: List[str] = []
    for cat in categories:
        if cat not in COMPLIMENTS:
            raise ValueError(f"Unknown category: {cat!r}. Available: {list(COMPLIMENTS)}")
        result.extend(COMPLIMENTS[cat])
    return result

def get_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Parameters
    ----------
    category: Optional[str]
        One of ``"general"``, ``"work"`` or ``"coding"``. If omitted, any category is used.
    """
    candidates = _flatten([category] if category else None)
    return random.choice(candidates)

def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random compliment.")
    parser.add_argument(
        "--category",
        choices=list(COMPLIMENTS.keys()),
        help="Optional category to limit the compliment."
    )
    args = parser.parse_args()
    try:
        compliment = get_compliment(args.category)
        print(compliment)
    except ValueError as exc:
        parser.error(str(exc))

if __name__ == "__main__":
    main()
