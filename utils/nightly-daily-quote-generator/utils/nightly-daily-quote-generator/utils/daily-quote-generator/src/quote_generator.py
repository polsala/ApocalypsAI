import argparse
import random
from typing import List, Tuple

# Mock rationale: static quote database ensures offline operation and deterministic tests.
QUOTES: dict[str, List[Tuple[str, str]]] = {
    "wisdom": [
        ("The only true wisdom is in knowing you know nothing.", "Socrates"),
        ("Know thyself.", "Ancient Greek Proverb"),
    ],
    "humor": [
        ("I can resist everything except temptation.", "Oscar Wilde"),
        ("I'm not arguing, I'm just explaining why I'm right.", "Anonymous"),
    ],
    "motivation": [
        ("The future depends on what you do today.", "Mahatma Gandhi"),
        ("Dream big and dare to fail.", "Norman Vaughan"),
    ],
}


def get_random_quote(category: str | None = None) -> Tuple[str, str]:
    """Return a random (quote, author) tuple.

    Args:
        category: Optional category to filter quotes. If ``None`` all categories are considered.
    Returns:
        A tuple containing the quote text and the author.
    Raises:
        ValueError: If a non‑existent category is supplied.
    """
    if category:
        if category not in QUOTES:
            raise ValueError(f"Unknown category '{category}'. Available: {', '.join(QUOTES)}")
        pool = QUOTES[category]
    else:
        # Flatten all quotes across categories
        pool = [q for quotes in QUOTES.values() for q in quotes]
    return random.choice(pool)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--category",
        type=str,
        help="Quote category (wisdom, humor, motivation).",
    )
    args = parser.parse_args()
    try:
        quote, author = get_random_quote(args.category)
        print(f'"{quote}" — {author}')
    except ValueError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
