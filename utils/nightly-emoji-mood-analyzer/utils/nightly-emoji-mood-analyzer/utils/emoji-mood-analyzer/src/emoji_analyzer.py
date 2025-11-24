'''
emoji_analyzer.py

Provides a simple function to analyze the mood of a text and return an emoji.
'''

from __future__ import annotations
import re
from typing import List

POSITIVE_WORDS: List[str] = [
    "love",
    "great",
    "happy",
    "joy",
    "awesome",
    "fantastic",
    "good",
    "wonderful",
    "excellent",
    "sunny",
]

NEGATIVE_WORDS: List[str] = [
    "hate",
    "terrible",
    "sad",
    "bad",
    "awful",
    "horrible",
    "depressing",
    "rainy",
    "worst",
]


def _tokenize(text: str) -> List[str]:
    """Return a list of lowercase words from the input text."""
    return re.findall(r"\b\w+\b", text.lower())


def analyze_mood(text: str) -> str:
    """
    Analyze the mood of the given text and return an emoji.

    - Positive → 😊
    - Negative → 😞
    - Neutral → 😐
    """
    tokens = _tokenize(text)
    pos_hits = sum(token in POSITIVE_WORDS for token in tokens)
    neg_hits = sum(token in NEGATIVE_WORDS for token in tokens)

    if pos_hits > neg_hits:
        return "😊"
    elif neg_hits > pos_hits:
        return "😞"
    else:
        return "😐"


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.emoji_analyzer \"Your text here\"")
        sys.exit(1)
    print(analyze_mood(sys.argv[1]))
