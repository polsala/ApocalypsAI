import random
from typing import List, Tuple

# A small curated list of inspirational quotes.
_QUOTES: List[Tuple[str, str]] = [
    (
        "The only limit to our realization of tomorrow is our doubts of today.",
        "Franklin D. Roosevelt",
    ),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    (
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Zig Ziglar",
    ),
    (
        "Life is 10% what happens to us and 90% how we react to it.",
        "Charles R. Swindoll",
    ),
]


def get_random_quote() -> Tuple[str, str]:
    """Return a random (quote, author) tuple from the built‑in list."""
    return random.choice(_QUOTES)


def format_quote(quote: str, author: str) -> str:
    """Format a quote and its author for pretty console output."""
    return f'"{quote}"\n    — {author}'


def main() -> None:
    quote, author = get_random_quote()
    print(format_quote(quote, author))


if __name__ == "__main__":
    main()
