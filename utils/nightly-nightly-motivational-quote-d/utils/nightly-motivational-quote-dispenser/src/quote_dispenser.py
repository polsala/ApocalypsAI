import argparse
import random
from typing import List

# Built‑in list of motivational quotes
_QUOTES: List[str] = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Dream big and dare to fail. – Norman Vaughan",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. – Zig Ziglar",
]


def get_random_quote(rng: random.Random = random) -> str:
    """Return a random quote from the built‑in list.

    The `rng` parameter is injectable for testing purposes.
    """
    return rng.choice(_QUOTES)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random motivational quote to stdout."
    )
    # No additional arguments needed; placeholder for future extensions
    return parser.parse_args()


def main() -> None:
    args = _parse_args()  # noqa: F841 – currently unused
    quote = get_random_quote()
    print(f"\"{quote}\"")


if __name__ == "__main__":
    main()
