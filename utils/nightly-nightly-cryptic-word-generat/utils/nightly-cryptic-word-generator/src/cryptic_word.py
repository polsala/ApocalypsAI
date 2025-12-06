"""
cryptic_word.py

Provides a simple utility to fetch a random cryptic word and its definition.
"""

import json
import random
from typing import Dict

# A small curated list of cryptic words.
_WORDS = [
    {"word": "obfuscate", "definition": "make obscure, unclear, or unintelligible"},
    {"word": "serendipity", "definition": "the occurrence of events by chance in a happy or beneficial way"},
    {"word": "ephemeral", "definition": "lasting for a very short time"},
    {"word": "limerence", "definition": "the state of being infatuated or obsessed with another person"},
    {"word": "petrichor", "definition": "a pleasant smell that frequently accompanies the first rain after a long period of warm, dry weather"},
]


def get_random_word() -> Dict[str, str]:
    """
    Return a random word and its definition from the curated list.

    Returns
    -------
    dict
        A dictionary with keys ``word`` and ``definition``.
    """
    return random.choice(_WORDS)


def main() -> None:
    """Print a random word as JSON to stdout."""
    word_info = get_random_word()
    print(json.dumps(word_info))


if __name__ == "__main__":
    main()
