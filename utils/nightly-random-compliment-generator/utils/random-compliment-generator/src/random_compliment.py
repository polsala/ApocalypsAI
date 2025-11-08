"""random_compliment
~~~~~~~~~~~~~~~~~~~

Provides a simple function to return a random compliment from a curated list.
The module can be executed as a script to print the compliment to stdout.
"""

import random
from typing import List

# A modest list of uplifting compliments.
_COMPLIMENTS: List[str] = [
    "You are a coding wizard!",
    "Your logic is as clear as crystal.",
    "You make bugs disappear like magic.",
    "Your creativity shines brighter than a supernova.",
    "Every line you write is a masterpiece.",
]


def get_compliment() -> str:
    """Return a random compliment.

    The function is deliberately tiny to keep the utility lightweight.
    """
    return random.choice(_COMPLIMENTS)


def _main() -> None:
    """CLI entry point – prints a random compliment to stdout."""
    print(get_compliment())


if __name__ == "__main__":
    _main()
