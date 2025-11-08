"""
Daily Motivation Generator

Provides a simple API to fetch a random motivational quote.
"""

import random
from typing import Optional

_QUOTES = [
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("You miss 100% of the shots you don’t take.", "Wayne Gretzky"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
]


def get_motivation(category: Optional[str] = None) -> str:
    """Return a random motivational quote.

    Parameters
    ----------
    category: Optional[str]
        Currently unused; placeholder for future categorization.

    Returns
    -------
    str
        Quote formatted as "Quote — Author".
    """
    # In this simple implementation, category is ignored.
    quote, author = random.choice(_QUOTES)
    return f"{quote} — {author}"


if __name__ == "__main__":
    # CLI entry point: print a quote to stdout.
    print(get_motivation())
