#!/usr/bin/env python3
"""
emoji-mood-analyzer

Provides a simple function `analyze_mood(text: str) -> str` that returns an emoji
representing the mood of the given text based on keyword heuristics.
"""

import sys
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
    "sunny",
    "delight",
    "pleased",
    "smile",
    "laugh",
}

NEGATIVE_WORDS = {
    "hate",
    "sad",
    "angry",
    "bad",
    "terrible",
    "awful",
    "depressed",
    "gloom",
    "pain",
    "cry",
    "upset",
    "worst",
    "rainy",
    "storm",
}

NEUTRAL_WORDS = {
    "okay",
    "fine",
    "average",
    "meh",
    "neutral",
    "so‑so",
}

EMOJI_MAP = {
    "positive": "😊",
    "negative": "😞",
    "neutral": "😐",
    "unknown": "🤔",
}


def _tokenize(text: str) -> List[str]:
    """Very simple tokenizer: lower‑case and split on whitespace and punctuation."""
    import re

    return re.findall(r"\b\w+\b", text.lower())


def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The algorithm counts occurrences of positive and negative keywords.
    If positives outnumber negatives → positive emoji, vice‑versa for negative.
    Equal non‑zero counts → neutral emoji. If no keywords but a neutral word is present → neutral.
    Otherwise → unknown.
    """
    tokens = _tokenize(text)
    if not tokens:
        return EMOJI_MAP["unknown"]

    pos = sum(tok in POSITIVE_WORDS for tok in tokens)
    neg = sum(tok in NEGATIVE_WORDS for tok in tokens)

    if pos > neg:
        return EMOJI_MAP["positive"]
    if neg > pos:
        return EMOJI_MAP["negative"]
    if pos == neg and pos > 0:
        return EMOJI_MAP["neutral"]
    if any(tok in NEUTRAL_WORDS for tok in tokens):
        return EMOJI_MAP["neutral"]
    return EMOJI_MAP["unknown"]


def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m utils.emoji-mood-analyzer.src.analyzer \"<text>\"")
        sys.exit(1)
    text = sys.argv[1]
    print(analyze_mood(text))

if __name__ == "__main__":
    _cli()
