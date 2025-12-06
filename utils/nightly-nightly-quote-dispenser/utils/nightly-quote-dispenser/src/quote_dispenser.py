import random
import sys
from typing import List

# A curated list of motivational quotes – completely offline.
QUOTES: List[str] = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Dream big and dare to fail. – Norman Vaughan",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. – Zig Ziglar",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in list.

    The function is deliberately tiny to keep the utility self‑contained.
    """
    return random.choice(QUOTES)


def main() -> None:
    """CLI entry point – prints a random quote to stdout.

    Exits with status 0 on success.
    """
    quote = get_random_quote()
    print(quote)
    sys.exit(0)


if __name__ == "__main__":
    main()
