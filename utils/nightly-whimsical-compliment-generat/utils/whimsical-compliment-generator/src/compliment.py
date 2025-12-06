"""Whimsical Compliment Generator.

Provides a function to generate a random compliment.
"""

import random
from typing import List

_COMPLIMENTS: List[str] = [
    "you are a dazzling comet of curiosity!",
    "your smile could power a small city!",
    "you have the wisdom of a thousand owls!",
    "your ideas sparkle like fireworks!",
    "you are a master of delightful chaos!",
]

def get_compliment(name: str = "Friend") -> str:
    """Return a random whimsical compliment addressed to *name*.

    Args:
        name: The name to address in the compliment.

    Returns:
        A string containing the name and a random compliment.
    """
    compliment = random.choice(_COMPLIMENTS)
    return f"{name}, {compliment}"

def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate a whimsical compliment.")
    parser.add_argument("name", nargs="?", default="Friend", help="Name to address")
    args = parser.parse_args()
    print(get_compliment(args.name))

if __name__ == "__main__":
    main()
