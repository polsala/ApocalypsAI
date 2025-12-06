"""random_quote_generator – provide a random whimsical quote.

The module exposes a single public function `get_random_quote()` which selects a quote
from a hard‑coded list using `random.choice`. The CLI entry point prints the quote to
stdout.
"""

import random
from typing import List

# A curated list of whimsical quotes – feel free to extend.
_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I intend to live forever. So far, so good.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why do we park on a driveway and drive on a parkway?",
    "I’m not arguing, I’m just explaining why I’m right.",
]


def get_random_quote() -> str:
    """Return a random quote from the internal list.

    The function is deliberately simple to keep the utility self‑contained.
    """
    return random.choice(_QUOTES)


def _main() -> None:
    """CLI entry point – prints a random quote to stdout."""
    print(get_random_quote())


if __name__ == "__main__":
    _main()
