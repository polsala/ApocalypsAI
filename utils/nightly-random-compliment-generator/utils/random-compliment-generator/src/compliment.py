import random
import sys
from pathlib import Path

# List of cheerful compliments
_COMPLIMENTS = [
    "You're a coding wizard!",
    "Your logic is as clear as crystal.",
    "You make bugs disappear like magic.",
    "Your code shines brighter than the sun.",
    "You turn coffee into code effortlessly.",
    "Your algorithms are pure poetry.",
    "You have the debugging instincts of a cat.",
    "Your pull requests are pure gold.",
]


def get_random_compliment() -> str:
    """Return a random compliment from the predefined list.

    The function is deliberately simple and deterministic when the random
    module is mocked, which makes it easy to test.
    """
    return random.choice(_COMPLIMENTS)


def _cli() -> None:
    """CLI entry point – prints a random compliment to stdout.
    """
    compliment = get_random_compliment()
    print(compliment)


if __name__ == "__main__":
    # Allow execution as a module: `python -m utils.random-compliment-generator.src.compliment`
    _cli()
