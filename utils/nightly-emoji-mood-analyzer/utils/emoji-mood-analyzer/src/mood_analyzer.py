#!/usr/bin/env python3
"""
Emoji Mood Analyzer

Provides `analyze_mood(text: str) -> str` which returns an emoji
representing the sentiment of the given text.
"""

from __future__ import annotations
import sys
import re
from collections import Counter
from typing import List

POSITIVE_WORDS = {
    "love",
    "happy",
    "joy",
    "awesome",
    "great",
    "fantastic",
    "good",
    "wonderful",
    "excellent",
    "amazing",
    "delight",
    "pleased",
    "smile",
    "sunny",
    "bright",
}

NEGATIVE_WORDS = {
    "hate",
    "sad",
    "bad",
    "terrible",
    "awful",
    "worst",
    "pain",
    "angry",
    "depressed",
    "gloomy",
    "rainy",
    "dark",
    "sick",
    "fail",
    "failure",
}

EMOJI_MAP = {
    "positive": "😊",
    "negative": "😞",
    "neutral": "😐",
}


def tokenize(text: str) -> List[str]:
    """Return a list of lowercase words stripped of punctuation."""
    return re.findall(r"\b\w+\b", text.lower())


def analyze_mood(text: str) -> str:
    """
    Analyze the sentiment of *text* and return an emoji.

    Simple heuristic:
    - Count occurrences of known positive and negative words.
    - If positives > negatives → positive emoji.
    - If negatives > positives → negative emoji.
    - Otherwise neutral.
    """
    words = tokenize(text)
    counts = Counter(words)

    pos = sum(counts[w] for w in POSITIVE_WORDS if w in counts)
    neg = sum(counts[w] for w in NEGATIVE_WORDS if w in counts)

    if pos > neg:
        return EMOJI_MAP["positive"]
    elif neg > pos:
        return EMOJI_MAP["negative"]
    else:
        return EMOJI_MAP["neutral"]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python -m mood_analyzer \"Your text here\"")
        return 2

    text = " ".join(argv)
    emoji = analyze_mood(text)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
