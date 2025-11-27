import argparse
import random
import sys
from typing import List

# A small curated list of motivational quotes.
_QUOTES: List[str] = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "Dream big and dare to fail. – Norman Vaughan",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. – Zig Ziglar",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in list.

    The function is deliberately simple to keep the utility lightweight.
    """
    return random.choice(_QUOTES)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a random motivational quote to stdout."
    )
    # No additional arguments needed; placeholder for future extensions.
    parser.parse_args()
    quote = get_random_quote()
    print(quote)


if __name__ == "__main__":
    # When executed as a module (`python -m src.quote_fetcher`) we invoke main.
    main()
