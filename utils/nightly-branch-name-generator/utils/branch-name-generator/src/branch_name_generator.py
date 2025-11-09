"""
branch_name_generator

Provides a function to generate a random, git‑friendly branch name composed of
adjective‑noun pairs separated by hyphens.

The generator is deterministic when the random seed is set, which aids testing.
"""

import random
from typing import List

_ADJECTIVES: List[str] = [
    "sparkling",
    "mystic",
    "silent",
    "brave",
    "fuzzy",
    "ancient",
    "luminous",
    "swift",
    "crimson",
    "golden",
    "whispering",
    "stormy",
]

_NOUNS: List[str] = [
    "unicorn",
    "dragon",
    "phoenix",
    "tiger",
    "river",
    "mountain",
    "forest",
    "galaxy",
    "comet",
    "nebula",
    "canyon",
    "breeze",
]


def generate_branch_name(num_words: int = 2) -> str:
    """
    Generate a branch name consisting of `num_words` random words.
    For `num_words == 2`, the format is ``adjective-noun``.
    For larger values, words are concatenated with hyphens.

    The function ensures the result is <= 50 characters; if longer,
    it truncates excess words.

    Parameters
    ----------
    num_words: int
        Number of words to include (default 2).

    Returns
    -------
    str
        A hyphen‑separated branch name.
    """
    if num_words < 1:
        raise ValueError("num_words must be >= 1")
    words: List[str] = []
    for i in range(num_words):
        if i % 2 == 0:
            words.append(random.choice(_ADJECTIVES))
        else:
            words.append(random.choice(_NOUNS))
    name = "-".join(words)
    # Ensure length constraint
    if len(name) > 50:
        # Trim from the end until within limit
        while len(name) > 50 and words:
            words.pop()
            name = "-".join(words)
    return name


def main() -> None:
    """CLI entry point: prints a generated branch name."""
    print(generate_branch_name())


if __name__ == "__main__":
    main()
