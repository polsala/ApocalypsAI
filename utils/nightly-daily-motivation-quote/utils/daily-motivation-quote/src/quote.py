"""daily_motivation_quote – random motivational quote utility.

Provides a simple CLI entry point and a programmatic function.
"""

import random
import sys
from pathlib import Path

# Built‑in collection of quotes
_QUOTES = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Dream big and dare to fail. – Norman Vaughan",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in list.

    The function is deliberately tiny so it can be imported without side effects.
    """
    return random.choice(_QUOTES)


def _cli() -> None:
    """CLI entry point used by `python -m daily_motivation_quote`.
    """
    quote = get_random_quote()
    print(quote)


if __name__ == "__main__":
    _cli()
