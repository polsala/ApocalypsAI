"""daily-zen-quote-generator
================================

Provides a single public function :func:`get_random_quote` that returns a random
Zen‑style quote from a hard‑coded list. When executed as a module it prints the
quote to stdout.
"""

import random
from typing import List

# A curated list of short Zen‑style sayings.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the still water, the moon reflects.",
    "A single breath can change a day.",
]


def get_random_quote() -> str:
    """Return a random quote from :data:`QUOTES`.

    The function is deliberately tiny so it can be imported without side‑effects.
    """
    return random.choice(QUOTES)


if __name__ == "__main__":
    # When run as a script, simply print a quote.
    print(get_random_quote())
