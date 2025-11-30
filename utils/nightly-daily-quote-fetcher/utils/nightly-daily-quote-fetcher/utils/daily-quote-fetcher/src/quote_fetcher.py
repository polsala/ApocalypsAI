"""Daily Quote Fetcher utility.

Provides a function to retrieve a random inspirational quote from a static list.
"""

import random
from typing import List

QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in list."""
    return random.choice(QUOTES)


def main() -> None:
    """CLI entry point: print a random quote."""
    print(get_random_quote())


if __name__ == "__main__":
    main()
