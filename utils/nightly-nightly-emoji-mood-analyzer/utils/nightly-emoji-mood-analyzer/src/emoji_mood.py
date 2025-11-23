"""emoji_mood.py

Simple sentiment‑to‑emoji mapper.

Provides:
- `analyze_sentiment(text: str) -> str` – returns an emoji.
- CLI entry‑point for quick usage.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import List

_POSITIVE_WORDS: List[str] = [
    "good",
    "great",
    "awesome",
    "fantastic",
    "happy",
    "love",
    "excellent",
    "nice",
    "wonderful",
    "amazing",
]

_NEGATIVE_WORDS: List[str] = [
    "bad",
    "terrible",
    "sad",
    "hate",
    "angry",
    "worst",
    "awful",
    "horrible",
    "poor",
    "disappoint",
]

_POSITIVE_EMOJI = "😊"
_NEGATIVE_EMOJI = "😞"
_NEUTRAL_EMOJI = "😐"


def _tokenize(text: str) -> List[str]:
    """Very naive tokenization – split on whitespace and strip punctuation."""
    import string

    translator = str.maketrans("", "", string.punctuation)
    return [word.translate(translator).lower() for word in text.split()]


def analyze_sentiment(text: str) -> str:
    """Return an emoji representing the sentiment of *text*.

    The algorithm counts occurrences of words from the positive and negative
    word‑lists. If positives > negatives → 😊, if negatives > positives → 😞,
    otherwise → 😐.
    """
    tokens = _tokenize(text)
    counts = Counter(tokens)

    pos_score = sum(counts[word] for word in _POSITIVE_WORDS)
    neg_score = sum(counts[word] for word in _NEGATIVE_WORDS)

    if pos_score > neg_score:
        return _POSITIVE_EMOJI
    if neg_score > pos_score:
        return _NEGATIVE_EMOJI
    return _NEUTRAL_EMOJI


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Return a sentiment emoji for a given piece of text."
    )
    parser.add_argument("text", nargs="+", help="Text to analyze (will be joined with spaces)")
    args = parser.parse_args()
    text = " ".join(args.text)
    emoji = analyze_sentiment(text)
    print(emoji)


if __name__ == "__main__":
    # When executed as a module: python -m utils/nightly-emoji-mood-analyzer/src/emoji_mood "..."
    _cli()
