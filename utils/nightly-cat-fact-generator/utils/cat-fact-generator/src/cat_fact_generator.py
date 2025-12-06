#!/usr/bin/env python3
"""
cat_fact_generator: Print a random cat fact.

Usage:
    python -m cat_fact_generator
"""

import random
import sys

FACTS = [
    "Cats have five toes on their front paws, but only four on the back.",
    "A group of cats is called a clowder.",
    "Cats can rotate their ears 180 degrees.",
    "A cat’s brain is 90% similar to a human’s.",
    "Cats have whiskers on the backs of their front legs."
]


def get_fact() -> str:
    """Return a random cat fact."""
    return random.choice(FACTS)


def main() -> None:
    """Print a random cat fact to stdout."""
    fact = get_fact()
    print(fact)


if __name__ == "__main__":
    sys.exit(main())
