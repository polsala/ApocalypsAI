import random
from typing import List

# A curated list of motivational quotes. Feel free to extend.
_QUOTES: List[str] = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Dream big and dare to fail. – Norman Vaughan",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. – Zig Ziglar",
]


def get_random_quote() -> str:
    """Return a random quote from the internal list.

    The function is deliberately simple and offline – no network calls are made.
    """
    # Using random.choice makes the function easy to mock in tests.
    return random.choice(_QUOTES)


if __name__ == "__main__":
    # Simple CLI for manual testing
    print(get_random_quote())
