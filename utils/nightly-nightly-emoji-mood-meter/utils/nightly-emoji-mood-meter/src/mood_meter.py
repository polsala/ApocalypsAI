#!/usr/bin/env python3
"""
emoji mood meter utility
"""

import sys
from typing import List

POSITIVE_WORDS = {
    "love",
    "happy",
    "joy",
    "great",
    "good",
    "awesome",
    "fantastic",
    "excellent",
    "wonderful",
    "pleased",
}

NEGATIVE_WORDS = {
    "hate",
    "sad",
    "bad",
    "terrible",
    "awful",
    "horrible",
    "depressed",
    "angry",
    "upset",
    "disappointed",
}


def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood of the given text.

    The algorithm is deliberately simple: it tokenises the input, strips punctuation,
    lower‑cases the words, and counts how many belong to the positive and negative sets.
    """
    words = [w.strip(".,!?:;\"'").lower() for w in text.split()]
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    if pos > neg:
        return "😊"
    elif neg > pos:
        return "😞"
    else:
        return "😐"


def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m src.mood_meter \"Your text here\"")
        return 2
    text = " ".join(argv)
    print(analyze_mood(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
