import random
import sys
from typing import List

# List of whimsical compliments
COMPLIMENTS: List[str] = [
    "You have the coding prowess of a caffeinated squirrel!",
    "Your debugging skills could tame a wild dragon.",
    "Your code is so clean, even the compiler smiles.",
    "You make algorithms look like poetry.",
    "Your commits are the highlight of the repo's history.",
]


def get_compliment() -> str:
    """Return a random compliment from the predefined list."""
    return random.choice(COMPLIMENTS)


def main() -> None:
    """CLI entry point – prints a random compliment to stdout."""
    compliment = get_compliment()
    print(compliment)


if __name__ == "__main__":
    # When executed as a script, behave like a CLI tool.
    main()
