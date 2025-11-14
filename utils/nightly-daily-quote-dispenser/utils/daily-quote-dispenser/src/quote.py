import random
from typing import List

# A small curated list of inspirational quotes.
QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in collection.

    The function is deliberately simple to keep the utility self‑contained and
    free of external dependencies.
    """
    return random.choice(QUOTES)


if __name__ == "__main__":
    print(get_random_quote())
