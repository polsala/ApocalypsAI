#!/usr/bin/env python3
"""
Simple sentiment‑to‑emoji analyzer.
"""

import sys
import re
from collections import Counter
from typing import List

POSITIVE_WORDS = {
    "love",
    "wonderful",
    "great",
    "fantastic",
    "happy",
    "excellent",
    "good",
    "awesome",
    "joy",
    "delight",
    "pleased",
    "amazing",
}

NEGATIVE_WORDS = {
    "hate",
    "terrible",
    "bad",
    "awful",
    "sad",
    "horrible",
    "worst",
    "angry",
    "disappointed",
    "pain",
    "depressed",
    "unhappy",
}

EMOJI_POSITIVE = "😊"
EMOJI_NEGATIVE = "😞"
EMOJI_NEUTRAL = "😐"


def tokenize(text: str) -> List[str]:
    """Return a list of lowercase words stripped of punctuation."""
    return re.findall(r"\b\w+\b", text.lower())


def analyze_sentiment(text: str) -> str:
    """Return an emoji representing the sentiment of *text*.

    The algorithm counts occurrences of words from the positive and negative
    word sets. If the positive count exceeds the negative count, a positive
    emoji is returned; if the negative count exceeds the positive count, a
    negative emoji is returned; otherwise a neutral emoji is returned.
    """
    words = tokenize(text)
    counts = Counter(words)
    pos = sum(counts[w] for w in POSITIVE_WORDS if w in counts)
    neg = sum(counts[w] for w in NEGATIVE_WORDS if w in counts)

    if pos > neg:
        return EMOJI_POSITIVE
    elif neg > pos:
        return EMOJI_NEGATIVE
    else:
        return EMOJI_NEUTRAL


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Prints the emoji to stdout. Returns exit code 0 on success, 2 if no
    arguments were supplied.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m src.analyzer \"Your text here\"")
        return 2
    text = " ".join(argv)
    print(analyze_sentiment(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
