"""Daily Zen Quote Generator.

Provides a function to retrieve a random Zen‑inspired quote,
optionally filtered by a keyword.
"""

import argparse
import random
from typing import List, Optional

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Peace comes from within. Do not seek it without.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the beginner's mind there are many possibilities.",
    "To know the road ahead, ask those who have traveled it.",
]


def get_random_quote(keyword: Optional[str] = None) -> str:
    """Return a random quote, optionally containing *keyword* (case‑insensitive).

    Args:
        keyword: If provided, only quotes containing the keyword are considered.
                 If no quotes match, a ValueError is raised.

    Returns:
        A randomly selected quote string.
    """
    if keyword:
        filtered = [q for q in _QUOTES if keyword.lower() in q.lower()]
        if not filtered:
            raise ValueError(f"No quotes found containing keyword: {keyword!r}")
        pool = filtered
    else:
        pool = _QUOTES
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random Zen‑inspired quote."
    )
    parser.add_argument(
        "--keyword",
        "-k",
        type=str,
        help="Filter quotes containing this keyword (case‑insensitive).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_random_quote(args.keyword)
    except ValueError as exc:
        print(exc)
        return
    print(quote)


if __name__ == "__main__":
    main()
