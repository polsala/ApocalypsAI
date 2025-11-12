#!/usr/bin/env python3
"""
Silly Commit Message Generator

Run as a script to print a random commit message.
"""

import random
import sys
from typing import List

# Word lists
ADJECTIVES = [
    "fluffy",
    "mysterious",
    "glorious",
    "awkward",
    "zany",
    "epic",
    "cryptic",
]

NOUNS = [
    "unicorn",
    "algorithm",
    "banana",
    "nebula",
    "pancake",
    "robot",
    "tornado",
]

VERBS = [
    "refactor",
    "optimize",
    "debug",
    "document",
    "polish",
    "rebase",
    "merge",
]

TEMPLATES = [
    "{verb} the {adjective} {noun}",
    "Add {adjective} {noun} support",
    "Fix {adjective} {noun} bug",
    "Improve {noun} handling",
    "Remove obsolete {adjective} {noun}",
]


def generate_message() -> str:
    """Generate a whimsical commit message."""
    template = random.choice(TEMPLATES)
    mapping = {
        "adjective": random.choice(ADJECTIVES),
        "noun": random.choice(NOUNS),
        "verb": random.choice(VERBS),
    }
    return template.format(**mapping)


def main() -> None:
    """CLI entry point."""
    seed = None
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            pass
    if seed is not None:
        random.seed(seed)
    print(generate_message())


if __name__ == "__main__":
    main()
