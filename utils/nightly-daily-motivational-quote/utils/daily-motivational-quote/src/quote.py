"""Daily Motivational Quote utility.

Provides a function to retrieve a random quote and a CLI entry point.
"""

import random
import sys
from typing import List, Tuple

_QUOTES: List[Tuple[str, str]] = [
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("You miss 100% of the shots you don’t take.", "Wayne Gretzky"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
]


def get_random_quote() -> Tuple[str, str]:
    """Return a random (quote, author) tuple."""
    return random.choice(_QUOTES)


def format_quote(quote: str, author: str) -> str:
    """Format the quote for display."""
    return f'"{quote}" – {author}'


def main() -> None:
    """CLI entry point: print a random motivational quote."""
    quote, author = get_random_quote()
    print(format_quote(quote, author))


if __name__ == "__main__":
    # Allow running as a script
    main()
