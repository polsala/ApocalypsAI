import argparse
import random
from typing import List, Optional, Dict

# Mock rationale: static data ensures offline determinism
QUOTES: List[Dict[str, str]] = [
    {"text": "The early bird gets the worm, but the second mouse gets the cheese.", "category": "humor"},
    {"text": "Dreams are the seedlings of reality.", "category": "inspiration"},
    {"text": "When life gives you lemons, make lemonade. Then find someone whose life gave them vodka, and have a party.", "category": "humor"},
    {"text": "The only limit to our realization of tomorrow is our doubts of today.", "category": "inspiration"},
    {"text": "If at first you don’t succeed, skydiving is not for you.", "category": "humor"},
]

def get_random_quote(category: Optional[str] = None) -> str:
    """Return a random quote.

    Args:
        category: Optional filter to only consider quotes of this category.
    Returns:
        A quote string.
    Raises:
        ValueError: If no quotes match the requested category.
    """
    filtered = [q["text"] for q in QUOTES if (category is None or q["category"] == category)]
    if not filtered:
        raise ValueError(f"No quotes found for category '{category}'.")
    # Mock rationale: using random.choice keeps the function simple and testable via mocking.
    return random.choice(filtered)

def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random whimsical quote.")
    parser.add_argument(
        "--category",
        type=str,
        help="Filter quotes by category (e.g., 'humor' or 'inspiration').",
    )
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.category)
        print(quote)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
