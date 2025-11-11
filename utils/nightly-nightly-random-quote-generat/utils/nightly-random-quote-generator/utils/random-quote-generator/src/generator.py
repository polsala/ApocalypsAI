import argparse
import random
from typing import List, Optional

# A small curated list of inspirational quotes.
_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
]


def _filter_quotes(keyword: str) -> List[str]:
    """Return quotes that contain *keyword* (case‑insensitive)."""
    lowered = keyword.lower()
    return [q for q in _QUOTES if lowered in q.lower()]


def get_random_quote(keyword: Optional[str] = None) -> str:
    """Return a random quote.

    If *keyword* is provided, only quotes containing that keyword are considered.
    Raises ``ValueError`` when no quotes match the keyword.
    """
    pool = _QUOTES
    if keyword:
        pool = _filter_quotes(keyword)
        if not pool:
            raise ValueError(f"No quotes found containing keyword: {keyword!r}")
    return random.choice(pool)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--keyword",
        type=str,
        help="Only consider quotes containing this word (case‑insensitive).",
    )
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.keyword)
        print(quote)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    _cli()
